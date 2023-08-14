"""
input_help.py
----------------------
Author: Dongzi Ding
Created: 2023-07-28
Modified: 2023-08-14
"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, \
    QListWidgetItem, QCheckBox, QMessageBox, QTabWidget


class DataInputDialog(QDialog):
    """
    A custom dialog for the user to input experimental data.

    Attributes:
    - main_window (QWidget): Reference to the main application window.
    - input_data (dict): Dictionary storing input data after confirmation.
    - data_types (dict): Dictionary defining the expected data types for each tab.
    - tab_widget (QTabWidget): Widget containing tabs for each analysis type.
    - list_widgets (dict): Dictionary storing list widgets for each tab.
    - input_fields (dict): Dictionary storing input fields for each data type and tab.
    - check_boxes (dict): Dictionary storing checkboxes indicating readiness for each data type and tab.
    """

    def __init__(self, parent=None):
        """Initializes the DataInputDialog with its components."""
        super().__init__(parent)

        self.main_window = parent.main_window
        self.input_data = None

        # Define expected data types for each function/tab
        self.data_types = {
            'reaction order analysis': ['log[Fe]', 'logR0', 'Δlog[Fe] absolute', 'Δlog[Fe] upper', 'Δlog[Fe] lower',
                                        'ΔlogR0 absolute', 'ΔlogR0 upper', 'ΔlogR0 lower'],
            'initial rate analysis': ['Time (seconds)', '[Fe2+] (uM)', 'Threshold (5%-20%)'],
            'rate const analysis': ['Time (seconds)', '[Fe2+] (uM)'],
            '3D plane plot': ['pH', 'ΔpH', 'logFe', 'ΔlogFe', 'logR', 'ΔlogR'],
        }

        self.tab_widget = QTabWidget()
        self.list_widgets = {}
        self.input_fields = {function: {data_type: QLineEdit() for data_type in self.data_types[function]} for function
                             in
                             self.data_types.keys()}
        self.check_boxes = {function: {data_type: QCheckBox("Ready") for data_type in self.data_types[function]} for
                            function in
                            self.data_types.keys()}

        selected_features = [option for option, selected in self.main_window.settings.func_current_options.items() if selected]

        # Generate tabs based on selected features
        for function in selected_features:
            self._create_tab_for_function(function)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

    def _create_tab_for_function(self, function):
        """Generate a tab for the given function."""
        data_types = self.data_types[function]
        tab = QWidget()
        layout = QHBoxLayout()
        v_layout = QVBoxLayout()

        select_all_checkbox = QCheckBox("Select all")
        select_all_checkbox.stateChanged.connect(self.select_all)
        v_layout.addWidget(select_all_checkbox)

        list_widget = self._create_list_widget(data_types)
        self.list_widgets[function] = list_widget

        for data_type in data_types:
            current_input_field = self.input_fields[function][data_type]
            current_checkbox = self.check_boxes[function][data_type]

            current_input_field.setEnabled(False)
            current_input_field.textChanged.connect(
                lambda text, chkbox=current_checkbox: chkbox.setChecked(bool(text)))
            current_checkbox.setEnabled(False)

            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(data_type))
            h_layout.addWidget(current_input_field)
            h_layout.addWidget(current_checkbox)
            v_layout.addLayout(h_layout)

        layout.addWidget(list_widget)
        layout.addLayout(v_layout)

        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.confirm_input)
        layout.addWidget(confirm_button)

        tab.setLayout(layout)
        self.tab_widget.addTab(tab, function)

    def _create_list_widget(self, data_types):
        """Creates and returns a QListWidget with items from data_types."""
        list_widget = QListWidget()
        for data_type in data_types:
            item = QListWidgetItem(data_type)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            list_widget.addItem(item)
            list_widget.itemClicked.connect(self.update_input_fields)
        return list_widget

    def select_all(self, state):
        """Selects all items in the current tab's QListWidget."""
        current_tab = self.tab_widget.tabText(self.tab_widget.currentIndex())
        list_widget = self.list_widgets[current_tab]
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            item.setCheckState(QtCore.Qt.Checked if state == QtCore.Qt.Checked else QtCore.Qt.Unchecked)
            self.input_fields[current_tab][item.text()].setEnabled(state == QtCore.Qt.Checked)
            self.check_boxes[current_tab][item.text()].setEnabled(state == QtCore.Qt.Checked)

    def update_input_fields(self, item):
        """Enables or disables the input field and checkbox for a clicked item."""
        current_tab = self.tab_widget.tabText(self.tab_widget.currentIndex())
        data_type = item.text()

        if current_tab in self.input_fields and data_type in self.input_fields[current_tab]:
            current_input_field = self.input_fields[current_tab][data_type]
            current_checkbox = self.check_boxes[current_tab][data_type]

            if item.checkState() == QtCore.Qt.Checked:
                current_input_field.setEnabled(True)
                current_input_field.textChanged.connect(lambda: current_checkbox.setChecked(True))
            else:
                current_input_field.setEnabled(False)
                current_input_field.setText("")
                current_checkbox.setChecked(False)

    def confirm_input(self):
        """Validates and confirms the input data from the current tab."""
        selected_data_types = [self.list_widgets[self.tab_widget.tabText(self.tab_widget.currentIndex())].item(i).text()
                               for i in
                               range(self.list_widgets[self.tab_widget.tabText(self.tab_widget.currentIndex())].count())
                               if self.list_widgets[self.tab_widget.tabText(self.tab_widget.currentIndex())].item(
                i).checkState() == QtCore.Qt.Checked]

        current_tab = self.tab_widget.tabText(self.tab_widget.currentIndex())
        for data_type in selected_data_types:
            if self.input_fields[current_tab][data_type].text():
                self.check_boxes[current_tab][data_type].setChecked(True)

        if all(self.check_boxes[current_tab][data_type].isChecked() for data_type in selected_data_types):
            self.input_data = self.get_input_data()
            self.accept()
            for input_field in self.input_fields[current_tab].values():
                input_field.clear()
        else:
            QMessageBox.critical(self, "Invalid input", "Please input all the required data.", QMessageBox.Ok)

    def get_input_data(self):
        """Converts input strings to numeric data and returns a dictionary."""
        input_data = {
            self.tab_widget.tabText(i): {
                data_type: self.input_fields[self.tab_widget.tabText(i)][data_type].text().split()
                for data_type in self.data_types[self.tab_widget.tabText(i)]
                if self.check_boxes[self.tab_widget.tabText(i)][data_type].isChecked()
            }
            for i in range(self.tab_widget.count())
        }
        numeric_data = {
            func: {
                data_type: list(map(float, values))
                for data_type, values in input_data[func].items()
            }
            for func in input_data.keys()
        }
        return numeric_data
