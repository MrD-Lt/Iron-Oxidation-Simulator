"""
mainwindow.py
----------------------
Author: Dongzi Ding
Created: 2023-06-25
Modified: 2023-08-14

Main window for the application.
This module provides the main application window for the PyQt5-based GUI application.
It includes menu bars for feature selections, input settings, save settings, help, and developer contact.
"""

import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QAction
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
import sys
from src.gui.settings_window import SettingsWindow
from src.gui.input_window import InputWindow
from src.gui.button_area import ButtonArea
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices


class MainWindow(QMainWindow):
    """
    The main window for the PyQt5-based GUI application.
    """
    def __init__(self, parent=None):
        """Initializes the main window, setting up the layout and components."""
        super().__init__(parent)

        self.setFixedSize(1024, 768)

        self.menu = self.menuBar()

        self.settings = Settings()

        self.feature_actions = {
            "reaction order analysis": QAction("reaction order analysis", self, checkable=True),
            "initial rate analysis": QAction("initial rate analysis", self, checkable=True),
            "rate const analysis": QAction("rate const analysis", self, checkable=True),
            "3D plane plot": QAction("3D plane plot", self, checkable=True),
        }
        self.func_menu = self.menu.addMenu("Feature selections")
        for action in self.feature_actions.values():
            self.func_menu.addAction(action)
            action.triggered.connect(self.update_func_option)

        self.input_menu = self.menu.addMenu("Input settings")
        self.input_menu.addAction("Manual Input", self.select_option5)
        self.import_file_action = self.input_menu.addAction("Import File", self.select_option6)

        self.save_menu = self.menu.addMenu("Save settings")
        self.save_menu.addAction("Yes", self.select_option7)
        self.save_menu.addAction("No", self.select_option8)


        self.help_menu = self.menu.addMenu("Contact with developer")
        self.help_menu.addAction("Github", self.open_contact)
        self.help_menu.addAction("Email", self.open_contact)
        self.help_menu.addAction("Website", self.open_contact)

        self.settings_window = SettingsWindow(self)
        self.input_window = InputWindow(self)
        self.button_area = ButtonArea(self)

        self.settings.settings_changed.connect(self.check_calculate_button_state)
        self.input_window.input_changed.connect(self.check_calculate_button_state)

        self.check_calculate_button_state()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.settings_window)
        self.layout.addWidget(self.input_window)
        self.layout.addWidget(self.button_area)
        self.central_widget.setLayout(self.layout)

    def update_func_option(self, checked):
        """Updates the current function option based on the menu selection."""
        action = self.sender()
        option = action.text()
        self.settings.func_current_options[option] = checked
        self.settings.settings_changed.emit()
        selected_features = sum(self.settings.func_current_options.values())
        self.import_file_action.setEnabled(selected_features <= 1)
        self.check_calculate_button_state()

    def check_calculate_button_state(self):
        """Checks if the 'Calculate' button should be enabled."""
        has_input = any(self.input_window.data.values())
        func_selected = any(self.settings.func_current_options.values())
        self.button_area.calculate_button.setEnabled(has_input and func_selected)

    def select_option1(self):
        self.settings.set_func_option("reaction order analysis")

    def select_option2(self):
        self.settings.set_func_option("initial rate analysis")

    def select_option3(self):
        self.settings.set_func_option("rate const analysis")

    def select_option4(self):
        self.settings.set_func_option("3D plane plot")

    def select_option5(self):
        self.settings.set_input_option("Manual Input")

    def select_option6(self):
        self.settings.set_input_option("Import File")

    def select_option7(self):
        self.settings.set_save_option("Yes")

    def select_option8(self):
        self.settings.set_save_option("No")


    def open_contact(self):
        """Opens the appropriate contact method based on the menu selection."""
        action = self.sender()
        option = action.text()

        if option == "Github":
            url = "https://github.com/edsml-dd1522"
        elif option == "Email":
            url = "mailto:dongzi.ding22@imperial.ac.uk"
        else:  # option == "Website"
            url = "https://edsml-dd1522.github.io/"

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Open External Application")
        msg_box.setText("You are about to open an external resources. Do you wish to continue?")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.setDefaultButton(QMessageBox.Cancel)

        if msg_box.exec_() == QMessageBox.Ok:
            QDesktopServices.openUrl(QUrl(url))

    def toggle_option(self, checked, option):
        """Toggles the current function option."""
        if checked:
            self.settings.func_current_option = option
        else:
            self.settings.func_current_option = "None"
        self.settings.settings_changed.emit()


class Settings(QObject):
    """
        Represents application settings.

        Attributes:
            - func_current_options (dict): Current functional options selected.
    """
    settings_changed = pyqtSignal()

    def __init__(self):
        """Initializes the application settings with default values."""
        super().__init__()

        self.func_current_options = {option: False for option in
                                     ["reaction order analysis", "initial rate analysis",
                                      "rate const analysis", "3D plane plot"]}

        self.func_current_option = "None"
        self.input_current_option = "None"
        self.save_current_option = "No"

    def set_func_option(self, option):
        """Sets the current function option."""
        self.func_current_option = option
        self.settings_changed.emit()

    def set_input_option(self, option):
        """Sets the current input option."""
        self.input_current_option = option
        self.settings_changed.emit()

    def set_save_option(self, option):
        """Sets the current save option."""
        self.save_current_option = option
        self.settings_changed.emit()

    def reset(self):
        """Resets the settings to default values."""
        self.save_current_option = "No"
        self.input_current_option = "None"
        self.func_current_options = {option: False for option in
                                     ["reaction order analysis", "initial rate analysis",
                                      "rate const analysis", "3D plane plot"]}
        self.settings_changed.emit()


def resource_path(relative_path):
    """
    Gets the absolute path to a resource, works in both development and PyInstaller contexts.

    Args:
        - relative_path (str): The relative path to the resource.

    Returns:
        The absolute path to the resource.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    with open(resource_path("ui/style.qss")) as f:
        qss = f.read()
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)

    main_window = MainWindow()
    QTimer.singleShot(100, main_window.show)  # Delay the window show by 100ms

    sys.exit(app.exec_())
