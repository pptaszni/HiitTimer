#!/usr/bin/env python
"""
Author: Pawel Ptasznik
"""

import sys
from PySide6.QtWidgets import (
    QApplication,
)

from hiit_timer import HiitTimerWidget

if __name__ == "__main__":
    print("Hello, World!")
    app = QApplication(sys.argv)
    htw = HiitTimerWidget()
    htw.show()
    app.exec()
