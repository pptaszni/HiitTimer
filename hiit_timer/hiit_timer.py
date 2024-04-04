"""
Author: Pawel Ptasznik
"""

from PySide6.QtCore import QObject, Signal, Slot


class HiitTimer(QObject):
    timeUpdateSignal = Signal(int, int, int) # hours, minutes, seconds
    def __init__(self):
        super().__init__()
        self.workingTimeSec = 0
        self.restTimeSec = 0

    def start(self):
        pass

    def pause(self):
        pass

    @Slot()
    def testEmit(self):
        self.timeUpdateSignal.emit(12, 43, 56)
