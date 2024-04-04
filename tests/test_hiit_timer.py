"""
Author: Pawel Ptasznik
"""

import pytest
import unittest
import sys

from PySide6.QtWidgets import (
    QApplication,
)
from PySide6 import QtTest

from .context import hiit_timer # pylint: disable=E0611
from hiit_timer import HiitTimer

def test_timer_starts_and_stops():
    app = QApplication(sys.argv)
    sut = HiitTimer()
    mo = sut.metaObject()
    signalIndex = mo.indexOfSignal("timeUpdateSignal(int, int, int)")
    tuSignal = mo.method(signalIndex)
    spy = QtTest.QSignalSpy(sut, tuSignal)
    sut.configure(2, 1)
    sut.start()
    # assert spy.wait(1000)
    QtTest.QTest.qWait(10000)
