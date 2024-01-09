import sys
import math
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QTimer, QTime, QDate, QStringListModel, QDateTime
import time
import sqlite3

week_day = {1: 'Понедельник',
            2: 'Вторник',
            3: 'Среда',
            4: 'Четверг',
            5: 'Пятница',
            6: 'Суббота',
            7: 'Воскресенье'}

melody = {'Волшебство': 'ringtones/Волшебство.mp3',
          'Дива': 'ringtones/Дива.mp3',
          'Гроза и гитара': 'ringtones/Гроза и гитара.mp3',
          'Щебетание птиц': 'ringtones/Щебетание птиц.mp3',
          'Осенний deep house': 'ringtones/Осенний deep house.mp3',
          'Труба': 'ringtones/Труба.mp3',
          'Утро, Природа, Вода, Птички': 'ringtones/Утро, Природа, Вода, Птички.mp3'}


class Clock(QMainWindow):
    def __init__(self):
        super().__init__()
        self.slm = QStringListModel()
        self.timer_list = QStringListModel()
        self.timer = QTimer()
        uic.loadUi('main.ui', self)
        self.pixmap_clock = QPixmap('clock.png')
        self.x0 = 125  # центр циферблата по оси X
        self.y0 = 125  # центр циферблата по оси Y
        self.r0 = 75  # длина секундной стрелки
        self.r1 = 75  # длина минутной стрелки
        self.r2 = 50  # длина часовой стрелки
        self.sec = 0
        self.time = 0
        self.start = False
        self.stopwatchTime = time.time()
        self.stopwatch = QTimer()
        self.time_str = ''
        self.count = 0
        self.qList = []
        self.time_r = 0
        self.content = ''
        self.start_timer = False
        self.qTimer_list = []
        self.text_timer = ''
        self.t_timer = QTimer()
        self.timerTime = 0
        self.timeTimer_res = 0
        self.timeTimer_str = ''
        self.timerTimer = time.time()
        self.sec_timer = 0
        self.timer_name = ''
        self.addtimeTimer = 0
        self.alarm_time = 0
        self.alarm_days = ''
        self.melody = ''
        self.alarm_name = ''
        self.alarm_call = False
        self.qalarmList = []
        self.alarmList = QStringListModel()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Часы')
        self.label.setPixmap(self.pixmap_clock)
        self.timer.timeout.connect(self.showDateTime)
        self.timer.start(1000)
        self.stopwatch.timeout.connect(self.showStopwatch)
        self.stopwatch.start(100)
        self.pushButton_5.clicked.connect(self.start_stopwatch)
        self.pushButton_4.clicked.connect(self.reset_stopwatch)
        self.pushButton_6.clicked.connect(self.flag)
        self.comboBox_7.activated.connect(self.handleActivated)
        self.pushButton_7.clicked.connect(self.timerStart)
        self.listView_2.clicked.connect(self.on_click_timer)
        self.pushButton_10.clicked.connect(self.delTimer)
        self.t_timer.timeout.connect(self.showTimer)
        self.t_timer.start(1000)
        self.pushButton_12.clicked.connect(self.timerReset)
        self.pushButton_8.clicked.connect(self.addTimer)
        self.pushButton_2.clicked.connect(self.lotCall)
        self.pushButton.clicked.connect(self.oneCall)
        self.pushButton_3.clicked.connect(self.addAlarm)
        self.scrollArea.setWidgetResizable(True)


    def addAlarm(self):
        try:
            self.alarm_time = self.timeEdit.time()
            self.alarm_name = self.lineEdit.text()
            if self.alarm_name != '':
                lab_name = '0' * (2 - len(str(self.alarm_time.hour()))) + \
                           str(self.alarm_time.hour()) + ':' + '0' * (2 - len(str(self.alarm_time.minute()))) + \
                           str(self.alarm_time.minute()) + ' ' + self.alarm_name
            else:
                lab_name = '0' * (2 - len(str(self.alarm_time.hour()))) + \
                           str(self.alarm_time.hour()) + ':' + '0' * (2 - len(str(self.alarm_time.minute()))) + \
                           str(self.alarm_time.minute())
            # self.qalarmList.append(lab_name)
            # self.alarmList.setStringList(self.qalarmList)
            # self.listView_3.setModel(self.alarmList)
            Alarm(self.alarm_time, lab_name)
        except Exception as e:
            print(e)

    def lotCall(self):
        self.alarm_call = True
        self.groupBox.setEnabled(True)

    def oneCall(self):
        self.alarm_call = False
        self.groupBox.setEnabled(False)

    def paintEvent(self, event):
        self.pixmap_clock = QPixmap('clock.png')
        qp = QPainter(self.pixmap_clock)
        qp.begin(self)
        self.drawLines(qp)
        self.label.setPixmap(self.pixmap_clock)
        qp.end()

    # Циферблат
    def drawLines(self, qp):
        hour = self.sec // 60 // 12
        min = self.sec // 60
        sec = self.sec
        pen = QPen(Qt.black, 5)
        qp.setPen(pen)
        x_min = int(self.x0 + self.r1 * math.sin(math.pi / 30 * min))
        y_min = int(self.y0 - self.r1 * math.cos(math.pi / 30 * min))
        qp.drawLine(self.x0, self.y0, x_min, y_min)
        pen = QPen(Qt.black, 7)
        qp.setPen(pen)
        x_hour = int(self.x0 + self.r2 * math.sin(math.pi / 30 * hour))
        y_hour = int(self.x0 - self.r2 * math.cos(math.pi / 30 * hour))
        qp.drawLine(self.x0, self.y0, x_hour, y_hour)
        pen = QPen(Qt.blue, 5)
        qp.setPen(pen)
        x_sec = int(self.x0 + self.r0 * math.sin(math.pi / 30 * sec))
        y_sec = int(self.x0 - self.r0 * math.cos(math.pi / 30 * sec))
        qp.drawLine(self.x0, self.y0, x_sec, y_sec)

    # Метод считывания и отображения системного времени
    def showDateTime(self):
        current_time = QTime.currentTime()
        self.time = current_time.toString('hh:mm')
        self.sec = current_time.hour() * 60 * 60 + current_time.minute() * 60 + current_time.second()
        if self.content == '12-часовой':
            if current_time.hour() > 12:
                current_time = current_time.addSecs(-43200)
        label_time = current_time.toString('hh:mm:ss')
        self.label_2.setText(label_time)
        current_date = QDate.currentDate()
        label_date = current_date.toString('dd.MM.yyyy')
        b = f'{label_date}\n{week_day[current_date.dayOfWeek()]}'
        self.label_3.setText(b)

    def handleActivated(self, index):
        self.content = self.comboBox_7.itemText(index)

    # Метод работы секундомера
    def showStopwatch(self):
        if self.start:
            self.time_r = int(time.time() - self.stopwatchTime)
            hours = self.time_r // 3600
            minutes = (self.time_r % 3600) // 60
            seconds = self.time_r % 60

            if hours > 99:
                self.start = False
                self.pushButton_5.setText('Старт')
            else:
                hours = str(hours)
                minutes = str(minutes)
                seconds = str(seconds)
                self.time_str = '0' * (2 - len(hours)) + hours + ':' + '0' * (
                        2 - len(minutes)) + minutes + ':' + '0' * (2 - len(seconds)) + seconds
                self.label_8.setText(self.time_str)
        else:
            self.stopwatchTime = time.time() - self.time_r

    # Кнопка старт/стоп секундомера
    def start_stopwatch(self):
        if self.start:
            self.pushButton_5.setText('Старт')
            self.start = False
        else:
            self.pushButton_5.setText('Пауза')
            self.start = True

    # Кнопка заново секундомера
    def reset_stopwatch(self):
        self.start = False
        self.pushButton_5.setText('Старт')
        self.label_8.setText('00:00:00')
        self.stopwatchTime = time.time()
        self.qList = []
        self.slm.setStringList(self.qList)
        self.count = 0
        self.time_r = 0

    # Кнопка флаг секундомера
    def flag(self):
        if f'{self.count}. {self.time_str}' not in self.qList and self.time_str != '':
            self.count += 1
            self.qList.append(f'{self.count}. {self.time_str}')
            self.slm.setStringList(self.qList)
            self.listView.setModel(self.slm)

    def on_click_timer(self, index):
        self.text_timer = self.listView_2.currentIndex().data()

    def showTimer(self):
        if self.start_timer:
            self.timeTimer_res = self.sec_timer - int(time.time() - self.timerTimer)
            print(self.timeTimer_res)
            hours = str(self.timeTimer_res // 3600)
            minutes = str((self.timeTimer_res % 3600) // 60)
            seconds = str(self.timeTimer_res % 60)
            self.timeTimer_str = '0' * (2 - len(hours)) + hours + ':' + '0' * (
                    2 - len(minutes)) + minutes + ':' + '0' * (2 - len(seconds)) + seconds
            self.label_9.setText(self.timeTimer_str)
            if self.timeTimer_str == '00:00:00':
                self.start_timer = False
                self.pushButton_7.setText('Старт')
        else:
            self.timerTimer = time.time() - (self.sec_timer - self.timeTimer_res)

    def timerStart(self):
        if self.start_timer:
            self.start_timer = False
            self.pushButton_7.setText('Старт')
        else:
            if self.text_timer == '':
                if self.timeTimer_res == 0:
                    self.time_timer = self.timeEdit_2.time()
                    if self.time_timer != QTime(0, 0, 0):
                        self.start_timer = True
                        self.timerTimer = time.time()
                        self.pushButton_7.setText('Пауза')
                        self.sec_timer = int(self.time_timer.hour() * 3600 + self.time_timer.minute() * 60 + \
                                             self.time_timer.second())
                else:
                    self.start_timer = True
                    self.pushButton_7.setText('Пауза')

    def timerReset(self):
        self.start_timer = False
        self.pushButton_7.setText('Старт')
        self.timeTimer_res = 0
        self.label_9.setText('00:00:00')

    def delTimer(self):
        if self.text_timer != '':
            print(self.text_timer)
            del self.qTimer_list[self.qTimer_list.index(self.text_timer)]
            self.timer_list.setStringList(self.qTimer_list)
            self.listView_2.setModel(self.timer_list)
            self.text_timer = ''

    def addTimer(self):
        con = sqlite3.connect('Clock.db')
        cur = con.cursor()
        self.timer_name = self.lineEdit_2.text()
        self.addtimeTimer = self.timeEdit_2.time()
        db_time = f'{str(self.addtimeTimer.hour())}:{str(self.addtimeTimer.minute())}:{str(self.addtimeTimer.second())}'
        print([db_time])
        if self.time != QTime(0, 0, 0):
            if self.timer_name != '':
                lab_name = self.timer_name + '0' * (2 - len(str(self.addtimeTimer.hour()))) + \
                           str(self.addtimeTimer.hour()) + ':' + '0' * (2 - len(str(self.addtimeTimer.minute()))) + \
                           str(self.addtimeTimer.minute()) + ':' + '0' * \
                           (2 - len(str(self.addtimeTimer.second()))) + str(self.addtimeTimer.second())
                cur.execute(f'INSERT INTO timer(Имя,Время) values({self.timer_name},{db_time})')

            else:
                lab_name = '0' * (2 - len(str(self.addtimeTimer.hour()))) + str(self.addtimeTimer.hour()) + \
                           ':' + '0' * (2 - len(str(self.addtimeTimer.minute()))) + \
                           str(self.addtimeTimer.minute()) + ':' + '0' * \
                           (2 - len(str(self.addtimeTimer.second()))) + str(self.addtimeTimer.second())
                print(lab_name, db_time)
                try:
                    cur.execute(f'INSERT INTO timer(Время) values({db_time})')
                except Exception as e:
                    print(e)
            self.qTimer_list.append(lab_name)
            self.timer_list.setStringList(self.qTimer_list)
            self.listView_2.setModel(self.timer_list)
            con.commit()
            con.close()


class Alarm(QMainWindow):
    def __init__(self, this_time, this_name):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.alarm_timer = QTimer()
        self.alarm_timer.timeout.connect(self.showAlarm)
        self.cur_time = 0
        self.this_alarm_time = this_time
        self.this_alarm_name = this_name
        self.chBox = QCheckBox(text=self.this_alarm_name)
        self.initUI()

    def initUI(self):
        self.scrollArea.setWidget(self.chBox)
        # self.verticalLayout_3.addWidget(self.scrollArea)
        print(self.this_alarm_name)

    def showAlarm(self):
        self.cur_time = QDateTime.currentDateTime()
        self.alarm_timer.start(1000)
        print(self.cur_time.time())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Clock()
    ex.show()
    sys.exit(app.exec())
