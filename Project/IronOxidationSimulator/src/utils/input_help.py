from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, \
    QListWidgetItem, QCheckBox, QMessageBox, QTabWidget


class DataInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 输入数据的类型列表
        self.input_data = None
        self.data_types = {
            'reaction order analysis': ['log[Fe]', 'logR0', 'Δlog[Fe] absolute', 'Δlog[Fe] upper', 'Δlog[Fe] lower', 'ΔlogR0 absolute', 'ΔlogR0 upper', 'ΔlogR0 lower'],
            'other function': ['different', 'list', 'of', 'data', 'types']
        }

        self.tab_widget = QTabWidget()

        for function in parent.data_readers.keys():
            data_types = self.data_types[function]  # Get data types for this function
            tab = QWidget()
            layout = QHBoxLayout()

            v_layout = QVBoxLayout()

            self.list_widget = QListWidget()
            for data_type in data_types:  # Create list widget items according to data types
                item = QListWidgetItem(data_type)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Unchecked)
                self.list_widget.addItem(item)

            self.list_widget.itemClicked.connect(self.update_input_fields)

            self.input_fields = {data_type: QLineEdit() for data_type in data_types}
            self.check_boxes = {data_type: QCheckBox("Ready") for data_type in data_types}

            for data_type in data_types:  # Add input fields and checkboxes according to data types
                self.input_fields[data_type].setEnabled(False)
                self.check_boxes[data_type].setEnabled(False)
                h_layout = QHBoxLayout()  # 在每次添加之前重新创建 h_layout
                h_layout.addWidget(QLabel(data_type))
                h_layout.addWidget(self.input_fields[data_type])
                h_layout.addWidget(self.check_boxes[data_type])
                v_layout.addLayout(h_layout)

            layout.addWidget(self.list_widget)
            layout.addLayout(v_layout)

            self.confirm_button = QPushButton("Confirm")
            self.confirm_button.clicked.connect(self.confirm_input)
            layout.addWidget(self.confirm_button)

            tab.setLayout(layout)
            self.tab_widget.addTab(tab, function)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

    def update_input_fields(self, item):
        data_type = item.text()
        if item.checkState() == QtCore.Qt.Checked:
            self.input_fields[data_type].setEnabled(True)
            self.input_fields[data_type].textChanged.connect(lambda: self.check_boxes[data_type].setChecked(True))
        else:
            self.input_fields[data_type].setEnabled(False)
            self.input_fields[data_type].setText("")
            self.check_boxes[data_type].setChecked(False)

    def confirm_input(self):
        for data_type in self.data_types[self.tab_widget.tabText(self.tab_widget.currentIndex())]:
            # Only check the check box if the input field text is not empty
            if self.input_fields[data_type].text():
                print(f"{data_type} input field text: {self.input_fields[data_type].text()}")  # Added print statement
                self.check_boxes[data_type].setChecked(True)
        if all(check_box.isChecked() for check_box in self.check_boxes.values()):
            self.input_data = self.get_input_data()  # Save the input data
            print(f"input_data: {self.input_data}")  # Print the input_data right after getting it
            self.accept()
            for input_field in self.input_fields.values():
                input_field.clear()  # 清除输入框内容
        else:
            QMessageBox.critical(self, "Invalid input", "Please input all the required data.", QMessageBox.Ok)
            self.input_data = None  # Set self.data to None instead of an empty dict
    def get_input_data(self):
        input_data = {
            self.tab_widget.tabText(i): {
                data_type: self.input_fields[data_type].text().split()
                for data_type in self.data_types[self.tab_widget.tabText(i)]
                if self.check_boxes[data_type].isChecked()
            }
            for i in range(self.tab_widget.count())
        }
        print(f"input_data: {input_data}")  # Added print statement
        numeric_data = {
            func: {
                data_type: list(map(float, values))
                for data_type, values in input_data[func].items()
            }
            for func in input_data.keys()
        }
        return numeric_data
