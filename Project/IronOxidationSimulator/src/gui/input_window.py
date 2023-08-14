"""
input_window.py
----------------------
Author: Dongzi Ding
Created: 2023-06-27
Modified: 2023-08-14
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QFileDialog, QLabel, QDialog

from ..utils.input_help import DataInputDialog
from ..utils import regression_analysis
from ..utils import initial_rate
from ..utils import rate_const
from ..utils import plane3D_plot


class InputWindow(QWidget):
    """
    A QWidget class that represents the input window for user data.

    Attributes:
        - input_changed (pyqtSignal): Signal emitted when the input changes.
    """

    input_changed = pyqtSignal()

    def __init__(self, parent=None):
        """
        Initializes the InputWindow with a parent widget.

        Args:
            - parent (QWidget, optional): The parent widget of the input window. Defaults to None.
        """
        super().__init__(parent)
        self.main_window = parent
        self.data = {}
        self.filename = None

        layout = QVBoxLayout()

        self.plane3D_plotter = plane3D_plot.Plane3DPlotter()
        self.data_readers = {
            "reaction order analysis": regression_analysis.read_data,
            "initial rate analysis": initial_rate.read_data,
            "rate const analysis": rate_const.read_data,
            "3D plane plot": self.plane3D_plotter.read_data,
        }

        self.manual_input_group = QGroupBox("Manual Input")
        manual_input_layout = QVBoxLayout()
        self.manual_input_button = QPushButton("Confirm")
        manual_input_layout.addWidget(self.manual_input_button)
        self.manual_input_group.setLayout(manual_input_layout)
        layout.addWidget(self.manual_input_group)

        self.file_input_group = QGroupBox("Import File")
        file_input_layout = QVBoxLayout()
        self.file_path_label = QLabel()
        self.file_browse_button = QPushButton("Browse File")
        file_input_layout.addWidget(self.file_path_label)
        file_input_layout.addWidget(self.file_browse_button)
        self.file_input_group.setLayout(file_input_layout)
        layout.addWidget(self.file_input_group)

        self.setLayout(layout)
        self.main_window.settings.settings_changed.connect(self.update_content)
        self.manual_input_button.clicked.connect(self.manual_input)
        self.file_browse_button.clicked.connect(self.browse_file)
        self.manual_input_group.setEnabled(False)
        self.file_input_group.setEnabled(False)

    def update_content(self):
        """
        Updates the input method based on the user's selected option.
        """
        input_option = self.main_window.settings.input_current_option
        if input_option == "Manual Input":
            self.manual_input_group.setEnabled(True)
            self.file_input_group.setEnabled(False)
        elif input_option == "Import File":
            self.manual_input_group.setEnabled(False)
            self.file_input_group.setEnabled(True)
        else:
            self.manual_input_group.setEnabled(False)
            self.file_input_group.setEnabled(False)

    def manual_input(self):
        """
        Handles the manual input of data by the user.
        """
        dialog = DataInputDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            user_input_data = dialog.input_data
            selected_functions = [func for func, selected in self.main_window.settings.func_current_options.items() if
                                  selected]
            for func in self.data_readers.keys():
                try:
                    self.data[func] = user_input_data[func]
                    self.input_changed.emit()
                except:
                    continue
            self.main_window.button_area.update_start_button()

    def browse_file(self):
        """
        Handles the file browsing and data extraction for the selected features.
        """
        file_path, _ = QFileDialog.getOpenFileName()
        if file_path:
            self.filename = file_path
            self.file_path_label.setText(file_path)
            for func_option, selected in self.main_window.settings.func_current_options.items():
                if selected:
                    data_reader = self.data_readers.get(func_option)
                    if data_reader is not None:
                        self.data[func_option] = data_reader(file_path)
                        self.emit_input_changed()
            self.main_window.button_area.update_start_button()

    def emit_input_changed(self):
        """
        Emits the input_changed signal.
        """
        self.input_changed.emit()

    def clear_data(self):
        """
        Clears the stored data.
        """
        self.data = {}

    def reset(self):
        """
        Resets the input window to its default state.
        """
        self.clear_data()
        self.filename = None
        self.file_path_label.clear()

