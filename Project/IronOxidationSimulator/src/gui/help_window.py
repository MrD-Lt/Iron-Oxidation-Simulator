"""
help_window.py
----------------------
Author: Dongzi Ding
Created: 2023-07-06
Modified: 2023-08-14
"""

import sys
import os
import subprocess
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox


class HelpWindow(QMainWindow):
    """
    A QMainWindow class that represents the help window.

    Attributes:
        parent (QWidget): The parent widget of the help window.
    """

    def __init__(self, parent=None):
        """
        Initializes the HelpWindow with a parent widget.

        Args:
            parent (QWidget, optional): The parent widget of the help window. Defaults to None.
        """
        super().__init__(parent)

        # Dynamically load the UI file using the uic module
        try:
            uic.loadUi('src/ui/welcome.ui', self)
        except:
            uic.loadUi('ui/welcome.ui', self)

        self.setFixedSize(450, 300)
        self.setWindowTitle("Welcome!")

        # Connect the exit button to the close method
        self.ExitButton.clicked.connect(self.close)

        # Connect the Manual button's clicked signal to the open_pdf_manual method
        self.Manual.clicked.connect(self.open_pdf_manual)

    def open_pdf_manual(self):
        """
        Opens the PDF manual located in the assets directory. The method of opening depends on the OS.
        """
        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "manual.pdf")
        if not os.path.isfile(pdf_path):
            QMessageBox.critical(self, "File Not Found",
                                 "The manual file does not exist.  Please check the GitHub page or reinstall the "
                                 "software.",
                                 QMessageBox.Ok)
            return
        if sys.platform.startswith('darwin'):  # macOS
            subprocess.call(('open', pdf_path))
        elif sys.platform.startswith('linux'):  # Linux
            subprocess.call(('xdg-open', pdf_path))
        elif sys.platform.startswith('win32'):  # Windows
            os.startfile(pdf_path)
