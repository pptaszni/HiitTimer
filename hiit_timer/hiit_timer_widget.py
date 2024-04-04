import sys

from PySide6.QtGui import QColorConstants, QColor
from PySide6.QtCore import (
    QTime,
    Slot
)
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLCDNumber,
    QMainWindow,
    QPushButton,
    QTimeEdit,
    QVBoxLayout,
    QWidget
)

from .hiit_timer import HiitTimer, TimerState

class HiitTimerWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hiit Timer")
        self.workTimeEdit = QTimeEdit()
        self.workTimeEdit.setDisplayFormat("hh::mm::ss")
        self.restTimeEdit = QTimeEdit()
        self.restTimeEdit.setDisplayFormat("hh::mm::ss")
        self.startPushButton = QPushButton("start")
        self.pausePushButton = QPushButton("pause/resume")
        self.timerDisplay = QLCDNumber()
        self.roundNbLabel = QLabel("Round 0")
        self.hiitTimer = HiitTimer()
        self.__initLayout()
        self.__makeConnections()

    def __initLayout(self):
        mainLayout = QHBoxLayout()
        settingsLayout = QGridLayout()
        settingsLayout.addWidget(QLabel("Work time"), 0, 0)
        settingsLayout.addWidget(self.workTimeEdit, 0, 1)
        settingsLayout.addWidget(QLabel("Rest time"), 1, 0)
        settingsLayout.addWidget(self.restTimeEdit, 1, 1)
        settingsLayout.addWidget(self.startPushButton, 2, 0)
        settingsLayout.addWidget(self.pausePushButton, 2, 1)
        displayLayout = QVBoxLayout()
        self.__setWidgetColor(self.timerDisplay, QColorConstants.Red)
        self.__setWidgetColor(self.roundNbLabel, QColorConstants.Red)
        self.timerDisplay.setDigitCount(9)
        self.timerDisplay.display("00:00:00")
        displayLayout.addWidget(self.timerDisplay, 5)
        displayLayout.addWidget(self.roundNbLabel, 1, Qt.AlignHCenter)
        mainLayout.addLayout(settingsLayout)
        mainLayout.addLayout(displayLayout)
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def __makeConnections(self):
        self.hiitTimer.timeUpdateSignal.connect(self.timeUpdate)
        self.hiitTimer.bgColorUpdate.connect(self.bgColorUpdate)
        self.hiitTimer.roundUpdateSignal.connect(self.roundNumberUpdate)

        self.startPushButton.clicked.connect(self.startTimer)
        self.pausePushButton.clicked.connect(self.pauseResume)

        self.workTimeEdit.userTimeChanged.connect(self.configureTimer)
        self.restTimeEdit.userTimeChanged.connect(self.configureTimer)

    def __setWidgetColor(self, widget, qColor):
        p = widget.palette()
        p.setColor(widget.backgroundRole(), qColor)
        widget.setPalette(p)
        widget.setAutoFillBackground(True)

    @Slot()
    def configureTimer(self):
        workTimeSec = QTime(0,0,0,0).secsTo(self.workTimeEdit.time())
        restTimeSec = QTime(0,0,0,0).secsTo(self.restTimeEdit.time())
        self.hiitTimer.configure(workTimeSec, restTimeSec)
        print("configureTimer ", workTimeSec, ", ", restTimeSec)

    @Slot()
    def startTimer(self):
        print("startTimer")
        self.hiitTimer.start()

    @Slot()
    def pauseResume(self):
        print("pauseResume")
        if self.hiitTimer.currentState() == TimerState.IDLE:
            self.hiitTimer.resume()
        else:
            self.hiitTimer.pause()

    @Slot(int, int, int)
    def timeUpdate(self, hours, minutes, seconds):
        self.timerDisplay.display(f"{hours:02}" + ":" + f"{minutes:02}" + ":" + f"{seconds:02}")

    @Slot(QColor)
    def bgColorUpdate(self, color):
        print("color: ", color)
        self.__setWidgetColor(self.timerDisplay, color)
        self.__setWidgetColor(self.roundNbLabel, color)

    @Slot(int)
    def roundNumberUpdate(self, roundNb):
        print("roundNb: ", roundNb)
        self.roundNbLabel.setText("Round " + str(roundNb))
