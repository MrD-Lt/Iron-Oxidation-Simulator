from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, \
    QListWidgetItem, QCheckBox, QMessageBox, QTabWidget

class DataInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 用于展示需要哪些tabs
        self.main_window = parent.main_window
        # 输入数据的类型列表
        self.input_data = None
        self.data_types = {
            'reaction order analysis': ['log[Fe]', 'logR0', 'Δlog[Fe] absolute', 'Δlog[Fe] upper', 'Δlog[Fe] lower',
                                        'ΔlogR0 absolute', 'ΔlogR0 upper', 'ΔlogR0 lower'],
            'initial rate analysis': ['Time (seconds)', 'ln[Fe2+] (uM)', 'Threshold (5%-20%)'],
            'other function': ['different', 'list', 'of', 'data', 'types']
        }

        self.tab_widget = QTabWidget()
        self.list_widgets = {}
        self.input_fields = {function: {data_type: QLineEdit() for data_type in self.data_types[function]} for function
                             in
                             self.data_types.keys()}
        self.check_boxes = {function: {data_type: QCheckBox("Ready") for data_type in self.data_types[function]} for
                            function in
                            self.data_types.keys()}

        selected_features = []
        for option, selected in self.main_window.settings.func_current_options.items():
            if selected:
                selected_features.append(option)

        for function in selected_features:
            data_types = self.data_types[function]
            tab = QWidget()
            layout = QHBoxLayout()
            v_layout = QVBoxLayout()

            # 创建全选/反选的复选框
            select_all_checkbox = QCheckBox("Select all")
            select_all_checkbox.stateChanged.connect(self.select_all)
            v_layout.addWidget(select_all_checkbox)

            list_widget = QListWidget()
            for data_type in data_types:
                item = QListWidgetItem(data_type)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Unchecked)
                list_widget.addItem(item)

            list_widget.itemClicked.connect(self.update_input_fields)
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

            self.confirm_button = QPushButton("Confirm")
            self.confirm_button.clicked.connect(self.confirm_input)
            layout.addWidget(self.confirm_button)

            tab.setLayout(layout)
            self.tab_widget.addTab(tab, function)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

    def select_all(self, state):
        current_tab = self.tab_widget.tabText(self.tab_widget.currentIndex())
        list_widget = self.list_widgets[current_tab]
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            item.setCheckState(QtCore.Qt.Checked if state == QtCore.Qt.Checked else QtCore.Qt.Unchecked)
            self.input_fields[current_tab][item.text()].setEnabled(state == QtCore.Qt.Checked)
            self.check_boxes[current_tab][item.text()].setEnabled(state == QtCore.Qt.Checked)

    def update_input_fields(self, item):
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
        else:
            print(f"Missing data type: {data_type} for function/tab: {current_tab}")

    def confirm_input(self):
        selected_data_types = [self.list_widgets[self.tab_widget.tabText(self.tab_widget.currentIndex())].item(i).text()
                               for i in range(self.list_widgets[self.tab_widget.tabText(self.tab_widget.currentIndex())].count())
                               if self.list_widgets[self.tab_widget.tabText(self.tab_widget.currentIndex())].item(i).checkState() == QtCore.Qt.Checked]

        current_tab = self.tab_widget.tabText(self.tab_widget.currentIndex())
        for data_type in selected_data_types:
            if self.input_fields[current_tab][data_type].text():
                print(f"{data_type} input field text: {self.input_fields[current_tab][data_type].text()}")
                self.check_boxes[current_tab][data_type].setChecked(True)

        if all(self.check_boxes[current_tab][data_type].isChecked() for data_type in selected_data_types):
            self.input_data = self.get_input_data()
            print(f"input_data: {self.input_data}")
            self.accept()
            for input_field in self.input_fields[current_tab].values():
                input_field.clear()
        else:
            QMessageBox.critical(self, "Invalid input", "Please input all the required data.", QMessageBox.Ok)
            self.input_data = None

    def get_input_data(self):
        input_data = {
            self.tab_widget.tabText(i): {
                data_type: self.input_fields[self.tab_widget.tabText(i)][data_type].text().split()

                for data_type in self.data_types[self.tab_widget.tabText(i)]
                if self.check_boxes[self.tab_widget.tabText(i)][data_type].isChecked()
            }
            for i in range(self.tab_widget.count())
        }
        print(f"input_data: {input_data}")
        numeric_data = {
            func: {
                data_type: list(map(float, values))
                for data_type, values in input_data[func].items()
            }
            for func in input_data.keys()
        }
        return numeric_data
