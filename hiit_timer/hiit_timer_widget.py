import sys

from PySide6.QtGui import QColorConstants
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QGridLayout,
    QHBoxLayout,
    QWidget,
)

from .hiit_timer import HiitTimer

class HiitTimerWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hiit Timer")
        self.workTimeEdit = QTimeEdit()
        self.restTimeEdit = QTimeEdit()
        self.startPushButton = QPushButton("start")
        self.resetPushButton = QPushButton("reset")
        self.timerDisplay = QLCDNumber()
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
        settingsLayout.addWidget(self.resetPushButton, 2, 1)
        displayLayout = QHBoxLayout()
        self.__setWidgetColor(self.timerDisplay, QColorConstants.Red)
        self.timerDisplay.setDigitCount(9)
        self.timerDisplay.display("00:00:00")
        displayLayout.addWidget(self.timerDisplay)
        mainLayout.addLayout(settingsLayout)
        mainLayout.addLayout(displayLayout)
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def __makeConnections(self):
        self.hiitTimer.timeUpdateSignal.connect(self.timeUpdate)
        self.startPushButton.clicked.connect(self.hiitTimer.testEmit)

    def __setWidgetColor(self, widget, qColor):
        p = widget.palette()
        p.setColor(widget.backgroundRole(), qColor)
        widget.setPalette(p)
        widget.setAutoFillBackground(True)

    @Slot(int, int, int)
    def timeUpdate(self, hours, minutes, seconds):
        self.timerDisplay.display(str(hours) + ":" + str(minutes) + ":" + str(seconds))
