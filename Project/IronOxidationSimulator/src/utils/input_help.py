from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, \
    QListWidgetItem, QCheckBox, QMessageBox, QTabWidget


class DataInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 输入数据的类型列表
        self.data_types = ['x', 'y', 'sdx_absolute', 'sdx_upper', 'sdx_lower', 'sdy_absolute', 'sdy_upper', 'sdy_lower']

        self.tab_widget = QTabWidget()

        for function in parent.data_readers.keys():
            tab = QWidget()
            layout = QHBoxLayout()

            h_layout = QVBoxLayout()
            v_layout = QVBoxLayout()

            self.list_widget = QListWidget()
            for data_type in self.data_types:
                item = QListWidgetItem(data_type)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Unchecked)
                self.list_widget.addItem(item)

            self.list_widget.itemClicked.connect(self.update_input_fields)

            self.input_fields = {data_type: QLineEdit() for data_type in self.data_types}
            self.check_boxes = {data_type: QCheckBox("Ready") for data_type in self.data_types}

            for data_type in self.data_types:
                self.input_fields[data_type].setEnabled(False)
                self.check_boxes[data_type].setEnabled(False)
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
        if all(check_box.isChecked() for check_box in self.check_boxes.values()):
            self.accept()
        else:
            QMessageBox.critical(self, "Invalid input", "Please input all the required data.", QMessageBox.Ok)

    def get_input_data(self):
        return {data_type: self.input_fields[data_type].text().split() for data_type in self.data_types if
                self.check_boxes[data_type].isChecked()}
