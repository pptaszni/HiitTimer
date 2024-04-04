"""
Author: Pawel Ptasznik
"""

from PySide6.QtCore import (
    QTimer,
    QObject,
    Signal,
    Slot,
    QUrl
)
from PySide6.QtGui import (
    QColorConstants,
    QColor
)
from PySide6.QtMultimedia import QSoundEffect
from enum import Enum


class TimerState(Enum):
    IDLE = 1
    WORK = 2
    REST = 3


class HiitTimer(QObject):
    timeUpdateSignal = Signal(int, int, int)  # hours, minutes, seconds
    bgColorUpdate = Signal(QColor)
    roundUpdateSignal = Signal(int)

    def __init__(self):
        super().__init__()
        self.workingTimeSec = 0
        self.restTimeSec = 0
        self.countdown = 0
        self.periodicClock = QTimer()
        self.roundNb = 0
        self.periodicClock.timeout.connect(self.tickHandler)
        self.periodicClock.start(1000)
        self.state = TimerState.IDLE
        self.resumeState = TimerState.IDLE
        self.dingDong = QSoundEffect()
        self.dingDong.setSource(QUrl.fromLocalFile("resources/Ding-dong.wav"))
        self.dingDong.setVolume(1)

    def start(self):
        print("start")
        self.roundNb = 0
        self.countdown = self.restTimeSec
        self.state = TimerState.REST

    def pause(self):
        print("pause")
        self.resumeState = self.state
        self.state = TimerState.IDLE

    def resume(self):
        print("resume")
        self.state = self.resumeState

    def configure(self, workTime, restTime):
        print("configure: ", workTime, ", ", restTime)
        self.workingTimeSec = workTime
        self.restTimeSec = restTime

    def currentState(self):
        return self.state

    def __idleState(self):
        print("we are idle, nothing to do")
        return TimerState.IDLE

    def __workState(self):
        print("workState ", self.roundNb)
        if self.countdown <= 0:
            self.countdown = self.restTimeSec
            self.timeUpdateSignal.emit(00, 00, 00)
            self.bgColorUpdate.emit(QColorConstants.Yellow)
            self.__makeSound()
            print("switch to REST")
            return TimerState.REST
        seconds = self.countdown
        minutes = seconds // 60
        hours = minutes // 60
        self.timeUpdateSignal.emit(hours, minutes % 60, seconds % 60)
        self.countdown = self.countdown - 1
        return TimerState.WORK

    def __restState(self):
        print("restState ", self.roundNb)
        if self.countdown <= 0:
            self.countdown = self.workingTimeSec
            self.roundNb = self.roundNb + 1
            self.timeUpdateSignal.emit(00, 00, 00)
            self.bgColorUpdate.emit(QColorConstants.Green)
            self.roundUpdateSignal.emit(self.roundNb)
            self.__makeSound()
            print("switch to WORK")
            return TimerState.WORK
        seconds = self.countdown
        minutes = seconds // 60
        hours = minutes // 60
        self.timeUpdateSignal.emit(hours, minutes % 60, seconds % 60)
        self.countdown = self.countdown - 1
        return TimerState.REST

    def __makeSound(self):
        print("ding dong")
        self.dingDong.play()

    @Slot()
    def tickHandler(self):
        print("tick ...")
        if self.state == TimerState.IDLE:
            self.state = self.__idleState()
        elif self.state == TimerState.WORK:
            self.state = self.__workState()
        elif self.state == TimerState.REST:
            self.state = self.__restState()

    @Slot()
    def testEmit(self):
        self.timeUpdateSignal.emit(12, 43, 56)
        self.bgColorUpdate.emit(QColorConstants.Green)
