import sys
import subprocess
import csv
import os

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow, QPlainTextEdit, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread

class thread_video(QThread):
    def __init__(self):
        QThread.__init__(self)
    def __del__(self):
        self.wait()
    def run(self):
        subprocess.call('py -m main',shell = True)

class thread_try(QThread):
    def __init__(self, mn):
        QThread.__init__(self)
        self.mn = mn
    def __del__(self):
        self.wait()
    def run(self):
        while(True):
            self.mn.update()
            self.sleep(1)

class Manual(QMainWindow):

    def __init__(self):

        super().__init__()
        self.videoName = "."
        self.time = 0
        self.thread_run = False
        self.start_time = ""

        self.count1 = [0,0,0,0]
        self.count2 = [0,0,0,0]
        self.count3 = [0,0,0,0]
        self.count4 = [0,0,0,0]
        self.count5 = [0,0,0,0]

        self.countArray = []
        for i in range(4):
            self.countArray.append([self.count1[i], self.count2[i], self.count3[i], self.count4[i], self.count5[i]])

        self.setWindowTitle('Vehicle Counting App')
        self.setGeometry(100, 100, 650, 580)
        self.move(60, 15)

        self.timeMsg = QLabel('Time :\n' + '0 minute 0 second', parent=self)
        self.timeMsg.setFixedWidth(500)
        self.carMsg = QLabel('Car :', parent=self)
        self.truckMsg = QLabel('Truck :', parent=self)
        self.motorcycleMsg = QLabel('Motorcycle :', parent=self)
        self.busMsg = QLabel('Bus :', parent=self)

        self.msg = [self.timeMsg, self.carMsg, self.motorcycleMsg, self.busMsg, self.truckMsg]
        self.set_msg(self.msg, 25, 35, 'Times', 14)
        
        self.quarterMsg1 = QLabel('0-15 minute', parent = self)
        self.quarterCar1 = QLabel('0', parent = self)
        self.quarterTruck1 = QLabel('0', parent = self)
        self.quarterMotorcycle1 = QLabel('0', parent = self)
        self.quarterBus1 = QLabel('0', parent = self)
        self.quarterCount1 = [self.quarterMsg1, self.quarterCar1, self.quarterTruck1, self.quarterMotorcycle1, self.quarterBus1]
        self.set_msg(self.quarterCount1, 150, 35, 'Times', 14)

        self.quarterMsg2 = QLabel('15-30 minute', parent = self)
        self.quarterCar2 = QLabel('0', parent = self)
        self.quarterTruck2 = QLabel('0', parent = self)
        self.quarterMotorcycle2 = QLabel('0', parent = self)
        self.quarterBus2 = QLabel('0', parent = self)
        self.quarterCount2 = [self.quarterMsg2, self.quarterCar2, self.quarterTruck2, self.quarterMotorcycle2, self.quarterBus2]
        self.set_msg(self.quarterCount2, 250, 35, 'Times', 14)

        self.quarterMsg3 = QLabel('30-45 minute', parent = self)
        self.quarterCar3 = QLabel('0', parent = self)
        self.quarterTruck3 = QLabel('0', parent = self)
        self.quarterMotorcycle3 = QLabel('0', parent = self)
        self.quarterBus3 = QLabel('0', parent = self)
        self.quarterCount3 = [self.quarterMsg3, self.quarterCar3, self.quarterTruck3, self.quarterMotorcycle3, self.quarterBus3]
        self.set_msg(self.quarterCount3, 350, 35, 'Times', 14)

        self.quarterMsg4 = QLabel('45-60 minute', parent = self)
        self.quarterCar4 = QLabel('0', parent = self)
        self.quarterTruck4 = QLabel('0', parent = self)
        self.quarterMotorcycle4 = QLabel('0', parent = self)
        self.quarterBus4 = QLabel('0', parent = self)
        self.quarterCount4 = [self.quarterMsg4, self.quarterCar4, self.quarterTruck4, self.quarterMotorcycle4, self.quarterBus4]
        self.set_msg(self.quarterCount4, 450, 35, 'Times', 14)

        self.quarterMsg5 = QLabel('Total', parent = self)
        self.quarterCar5 = QLabel('0', parent = self)
        self.quarterTruck5 = QLabel('0', parent = self)
        self.quarterMotorcycle5 = QLabel('0', parent = self)
        self.quarterBus5 = QLabel('0', parent = self)
        self.quarterCount5 = [self.quarterMsg5, self.quarterCar5, self.quarterTruck5, self.quarterMotorcycle5, self.quarterBus5]
        self.set_msg(self.quarterCount5, 550, 35, 'Times', 14)

        self.msgArray = [self.quarterCount1, self.quarterCount2, self.quarterCount3, self.quarterCount4, self.quarterCount5]

        self.button_writeenv = QPushButton('Write', parent = self)
        self.button_writeenv.move(25,525)
        self.button_default = QPushButton('Default', parent = self)
        self.button_default.move(125,525)
        self.button_start = QPushButton('Start', parent = self)
        self.button_start.move(500,475)
        self.button_quit = QPushButton('Quit', parent = self)
        self.button_quit.move(500,525)
        self.button_writeresult = QPushButton('Export Data', parent = self)
        self.button_writeresult.move(350,525)
        self.button_writeresult.setFixedWidth(150)
        
        self.videoMsg = QLabel('Directory of video :', parent = self)
        self.videoMsg.move(25,300)
        self.videoMsg.setFixedWidth(500)
        self.videoInput = QPlainTextEdit('',parent = self)
        self.videoInput.setPlaceholderText('ex. VIDEO="./data/videos/จุด 1/เช้า  (เวลากล้องไม่ตรง)/8.00-9.00/2020_0402_091930_004.MP4')
        self.videoInput.setGeometry(25, 330, 350, 50)

        self.startTimeMsg = QLabel('Start time :', parent = self)
        self.startTimeMsg.move(25,385)
        self.startTimeInput = QPlainTextEdit('',parent = self)
        self.startTimeInput.setPlaceholderText('ex. 02/04/2020 09:09:29')
        self.startTimeInput.setGeometry(100, 387, 275, 25)

        self.droiMsg = QLabel('DROI :', parent = self)
        self.droiMsg.move(25,415)
        self.droiInput = QPlainTextEdit('',parent = self)
        self.droiInput.setPlaceholderText('ex. (550, 100), (800, 100), (1000, 370), (480, 370)')
        self.droiInput.setGeometry(75, 417, 300, 25)

        self.lineMsg = QLabel('Line :', parent = self)
        self.lineMsg.move(25,445)
        self.lineInput = QPlainTextEdit('',parent = self)
        self.lineInput.setPlaceholderText('ex. (560, 220), (900, 230)')
        self.lineInput.setGeometry(75, 447, 300, 25)

        self.showVideoMsg = QLabel('Show Video :', parent = self)
        self.showVideoMsg.move(25,475)
        self.showVideo = QComboBox(parent = self)
        self.showVideo.move(100,477)
        self.showVideo.addItem('Yes')
        self.showVideo.addItem('No')

        self.showDroiMsg = QLabel('Show DROI :', parent = self)
        self.showDroiMsg.move(200,475)
        self.showDroi = QComboBox(parent = self)
        self.showDroi.move(275,477)
        self.showDroi.addItem('Yes')
        self.showDroi.addItem('No')

        self.set_event()
        self.show()

    def set_msg(self, msg, x, y, font, size):
        '''
        Set pattern of label
        '''
        for i in range(len(msg)):
            msg[i].move(x, y+ 50*i)
            msg[i].setFont(QFont(font, size))

    def update(self):
        '''
        Update data to GUI
        '''
        with open("./processing/"+ self.videoName +".result","r",encoding='utf-8') as result:
            L = result.readline().split(':')
            for i in range(len(L)):
                if(L[0] == ''):
                    continue
                elif(i == 0):
                    self.time = round(float(L[i]),2)
                    self.timeMsg.setText('Time :\n' + str(int(self.time//60)) + ' minute ' + str(int(self.time - self.time//60*60)) + ' second')
                else:
                    type, count = L[i].split(',')
                    quarter = self.time//900
                    while(quarter > 0):
                        self.countArray[self.time//900] -= self.countArray[quarter-1]
                        quarter -= 1
                    if(type == 'car'):
                        self.countArray[int(self.time//900)][0] = count
                        self.msgArray[int(self.time//900)][1].setText(count)
                    elif(type == 'motorcycle'):
                        self.countArray[int(self.time//900)][1] = count
                        self.msgArray[int(self.time//900)][2].setText(count)
                    elif(type == 'bus'):
                        self.countArray[int(self.time//900)][2] = count
                        self.msgArray[int(self.time//900)][3].setText(count)
                    elif(type == 'truck'):
                        self.countArray[int(self.time//900)][3] = count
                        self.msgArray[int(self.time//900)][4].setText(count)

                    for j in range(4):
                        self.countArray[j][4] = int(self.countArray[0][j])+int(self.countArray[1][j])+int(self.countArray[2][j])+int(self.countArray[3][j])
                    
                    self.quarterCar5.setText(str(self.countArray[0][4]))
                    self.quarterTruck5.setText(str(self.countArray[1][4]))
                    self.quarterMotorcycle5.setText(str(self.countArray[2][4]))
                    self.quarterBus5.setText(str(self.countArray[3][4]))
            '''
            if(self.time >= 1):
                p, q =self.read_check(self.videoName).split(',')
                if(q == 'True'):
                    self.button_start.setText('Start')
                    try:
                        self.myThread.terminate()
                        self.videoThread.terminate()
                    except:
                        None
                    self.thread_run == False
            '''
    
    def write_env(self):
        '''
        Initialize .env file which can change the setting
        '''
        file_env = open(".env","w",encoding='utf-8')
        file_example = open(".env.example","r",encoding='utf-8')
        L = file_example.readlines()
        L[0] = 'VIDEO="' + self.videoInput.toPlainText() + '"\n' #VIDEO="./data/videos/จุด 1/เช้า  (เวลากล้องไม่ตรง)/8.00-9.00/2020_0402_091930_004.MP4"
        L[1] = 'DROI=[' + self.droiInput.toPlainText() + ']\n' #DROI=[(550, 100), (800, 100), (1000, 370), (480, 370)]
        L[3] = 'SHOW_DROI=' + 'True\n' if (self.showDroi.currentIndex()==0) else 'False\n'
        L[12] = 'HEADLESS=' + 'False\n' if (self.showVideo.currentIndex()==0) else 'True\n'
        L[13] = "COUNTING_LINES=[{'label': 'A', 'line': [" + self.lineInput.toPlainText() + ']}]\n' #COUNTING_LINES=[{label: 'A', 'line': [(560, 220), (900, 230)]}]
        self.start_time = self.startTimeInput.toPlainText()
        file_env.writelines(L)
        file_env.close()
        file_example.close()

    def write_default(self):
        '''
        Initialize .env file to the default setting
        '''
        file_example = open(".env.example","r",encoding='utf-8')
        L = file_example.readlines()
        #L[0] = 'VIDEO="./data/videos/จุด 1/เช้า  (เวลากล้องไม่ตรง)/8.00-9.00/2020_0402_091930_004.MP4"\n'
        #L[1] = 'DROI=[(550, 100), (800, 100), (1000, 370), (480, 370)]\n'
        #L[13] = "COUNTING_LINES=[{'label': 'A', 'line': [(519, 230), (900, 230)]}]\n"
        self.videoInput.setPlainText(L[0][7:-2])
        self.startTimeInput.setPlainText('02/04/2020 09:19:29')
        self.droiInput.setPlainText(L[1][6:-2])
        self.showDroi.setCurrentIndex(0)
        self.showVideo.setCurrentIndex(0)
        self.lineInput.setPlainText(L[13][-26:-4])
        file_example.close()

    def write_result(self):
        '''
        Export data to file .csv
        ''' 
        with open('./result/' + self.videoName + '.csv', mode='w', encoding='utf-8') as result_file:
            result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            result_writer.writerow([self.start_time, '0-15 minute', '15-30 minute', '30-45 minute', '45-60 minute', 'Total'])
            result_writer.writerow(['Car', self.countArray[0][0], self.countArray[1][0], self.countArray[2][0], self.countArray[3][0], self.countArray[0][4]])
            result_writer.writerow(['Motorcycle', self.countArray[0][1], self.countArray[1][1], self.countArray[2][1], self.countArray[3][1], self.countArray[1][4]])
            result_writer.writerow(['Bus', self.countArray[0][2], self.countArray[1][2], self.countArray[2][2], self.countArray[3][2], self.countArray[2][4]])
            result_writer.writerow(['Truck', self.countArray[0][3], self.countArray[1][3], self.countArray[2][3], self.countArray[3][3], self.countArray[3][4]])

    def start_click(self):
        '''
        Start thread and delete thread
        '''
        if(self.thread_run == False):
            with open(".env","r",encoding='utf-8') as file:
                A = file.readlines()[0].split('/')
                self.videoMsg.setText('Name of video : ' + A[-1][0:-2])
                self.videoName = A[-1][0:-6]
            file = open("./processing/"+ self.videoName +".result","w")
            file.writelines("0:car,0")
            self.myThread = thread_try(self)
            self.myThread.start()
            
            self.videoThread = thread_video()
            self.videoThread.start()
            
            self.button_start.setText('Pause')
            self.thread_run = True
        else:
            if(self.button_start.text() == 'Pause'):
                self.write_check("True,False", self.videoName)
                self.button_start.setText('Resume')
            elif(self.button_start.text() == 'Resume'):
                self.write_check("False,False", self.videoName)
                self.button_start.setText('Pause')

    def quit_click(self):
        '''
        Delete thread and end process
        '''
        processFile = "./processing/" + self.videoName + ".result"
        checkFile = "./processing/" + self.videoName + ".check"
        if os.path.isfile(processFile):
            os.remove(processFile)
        if os.path.isfile(checkFile):
            os.remove(checkFile)
        try:
            self.myThread.terminate()
            self.videoThread.terminate()
            self.write_check("False,True", self.videoName)
        except:
            None
        sys.exit(0)

    def set_event(self):
        '''
        Set button clicked event
        '''
        self.button_start.clicked.connect(self.start_click)
        self.button_quit.clicked.connect(self.quit_click)
        self.button_writeenv.clicked.connect(self.write_env)
        self.button_default.clicked.connect(self.write_default)
        self.button_writeresult.clicked.connect(self.write_result)

    def read_check(self, name):
        '''
        Check if the video should end or not
        '''
        file_check = open("./processing/"+name + ".check","r",encoding='utf-8')
        return file_check.readline()

    def write_check(self, text, name):
        '''
        Write .check to True or False
        '''
        with open("./processing/" + name + ".check","w",encoding='utf-8') as file_check:
            file_check.write(text)

def run():
    app = QApplication(sys.argv)
    mn = Manual()
    app.exec_()
    try:
        self.myThread.terminate()
        self.videoThread.terminate()
        mn.write_check("False,True", mn.videoName)
    except:
        None
    sys.exit(0)

if __name__ == '__main__':
    run()
