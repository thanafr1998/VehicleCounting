'''
VCS entry point.
'''

# pylint: disable=wrong-import-position

import sys
import time
import cv2

from dotenv import load_dotenv
load_dotenv()

import settings
from util.logger import init_logger
from util.image import take_screenshot
from util.logger import get_logger
from util.debugger import mouse_callback
from ObjectCounter import ObjectCounter

init_logger()
logger = get_logger()

def write_result(array, name):
    '''
    Write result to read in app.
    '''
    file_result = open("./processing/"+name +".result","w")
    file_result.writelines(array)

def read_check(name):
    '''
    Check if the video should end or not
    '''
    file_check = open("./processing/"+name + ".check","r")
    return file_check.readline()

def write_check(name, end):
    '''
    Write .check
    '''
    file_check = open("./processing/"+name +".check","w")
    file_check.write("False," + end)

def run():
    '''
    Initialize object counter class and run counting loop.
    '''
    video = settings.VIDEO
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        logger.error('Invalid video source %s', video, extra={
            'meta': {'label': 'INVALID_VIDEO_SOURCE'},
        })
        sys.exit()
    ret, frame = cap.read()
    f_height, f_width, _ = frame.shape
    detection_interval = settings.DI
    mcdf = settings.MCDF
    mctf = settings.MCTF
    detector = settings.DETECTOR
    tracker = settings.TRACKER
    use_droi = settings.USE_DROI
    # create detection region of interest polygon
    droi = settings.DROI \
            if use_droi \
            else [(0, 0), (f_width, 0), (f_width, f_height), (0, f_height)]
    show_droi = settings.SHOW_DROI
    counting_lines = settings.COUNTING_LINES
    show_counts = settings.SHOW_COUNTS
    hud_color = settings.HUD_COLOR

    object_counter = ObjectCounter(frame, detector, tracker, droi, show_droi, mcdf, mctf,
                                   detection_interval, counting_lines, show_counts, hud_color)

    record = settings.RECORD
    if record:
        # initialize video object to record counting
        output_video = cv2.VideoWriter(settings.OUTPUT_VIDEO_PATH, \
                                        cv2.VideoWriter_fourcc(*'MJPG'), \
                                        30, \
                                        (f_width, f_height))

    logger.info('Processing started.', extra={
        'meta': {
            'label': 'START_PROCESS',
            'counter_config': {
                'di': detection_interval,
                'mcdf': mcdf,
                'mctf': mctf,
                'detector': detector,
                'tracker': tracker,
                'use_droi': use_droi,
                'droi': droi,
                'counting_lines': counting_lines
            },
        },
    })

    headless = settings.HEADLESS
    if not headless:
        # capture mouse events in the debug window
        cv2.namedWindow('Debug')
        cv2.setMouseCallback('Debug', mouse_callback, {'frame_width': f_width, 'frame_height': f_height})

    is_paused = False
    output_frame = None
    restart = False
    time_start = time.time()
    old_time = 0

    try:
        # main loop
        while cap.get(cv2.CAP_PROP_POS_FRAMES) + 1 < cap.get(cv2.CAP_PROP_FRAME_COUNT):
            k = cv2.waitKey(1) & 0xFF
            if k == ord('p'): # pause/play loop if 'p' key is pressed
                is_paused = False if is_paused else True
                logger.info('Loop paused/played.', extra={'meta': {'label': 'PAUSE_PLAY_LOOP', 'is_paused': is_paused}})
            if k == ord('s') and output_frame is not None: # save frame if 's' key is pressed
                take_screenshot(output_frame)
            if k == ord('q'): # end video loop if 'q' key is pressed
                logger.info('Loop stopped.', extra={'meta': {'label': 'STOP_LOOP'}})
                break
            if k == ord('r'): # restart video loop if 'r' is pressed
                logger.info('Restart video.')
                restart = True
                break

            if is_paused:
                time.sleep(0.5)
                continue

            videoName = video.split('/')
            if(old_time == 0):
                write_check(videoName[-1][0:-4], 'False')
            p, q =read_check(videoName[-1][0:-4]).split(',')
            if p == "True":
                time.sleep(0.5)
                continue
            if q == "True":
                logger.info('Loop stopped.', extra={'meta': {'label': 'STOP_LOOP'}})
                break

            _timer = cv2.getTickCount() # set timer to calculate processing frame rate

            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_now = round(cap.get(cv2.CAP_PROP_POS_FRAMES))
            time_now = frame_now/fps

            if(old_time != time_now):
                old_time = time_now
                if(old_time <= 900):
                    array = [str(old_time)]
                for line, objects in object_counter.counts.items():
                    for label, count in objects.items():
                        array.append(':' + str(label) + ',' + str(count))
                write_result(array, videoName[-1][0:-4])

            if ret:
                object_counter.count(frame)
                output_frame = object_counter.visualize()

                if record:
                    output_video.write(output_frame)

                if not headless:
                    debug_window_size = settings.DEBUG_WINDOW_SIZE
                    resized_frame = cv2.resize(output_frame, debug_window_size)
                    cv2.imshow('Debug', resized_frame)

            processing_frame_rate = round(cv2.getTickFrequency() / (cv2.getTickCount() - _timer), 2)
            frames_processed = round(cap.get(cv2.CAP_PROP_POS_FRAMES))
            frames_count = round(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            logger.debug('Frame processed.', extra={
                'meta': {
                    'label': 'FRAME_PROCESS',
                    'frames_processed': frames_processed,
                    'frame_rate': processing_frame_rate,
                    'frames_left': frames_count - frames_processed,
                    'percentage_processed': round((frames_processed / frames_count) * 100, 2),
                },
            })

            ret, frame = cap.read()
    finally:
        # end capture, close window, close log file and video object if any
        cap.release()
        if not headless:
            cv2.destroyAllWindows()
        if record:
            output_video.release()
        logger.info('Processing ended.', extra={
            'meta': {
                'label': 'END_PROCESS',
                'counts': object_counter.get_counts(),
            },
        })
        write_check(videoName[-1][0:-4],'True')
        if restart == True: run()

if __name__ == '__main__':
    run()
