from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QFileDialog, QLabel, QDialog

from utils.input_help import DataInputDialog
from utils.regression_analysis import read_data


class InputWindow(QWidget):
    # 添加一个信号来在文本改变时发出
    input_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.data = {}  # 初始化 self.data 为一个空字典
        self.filename = None  # 添加一个新的属性来存储文件名

        layout = QVBoxLayout()

        # 创建输入方法字典
        self.data_readers = {
            "reaction order analysis": read_data,
            # "other_function": other_data_reader,
        }

        # 创建手动输入部分
        self.manual_input_group = QGroupBox("Manual Input")
        manual_input_layout = QVBoxLayout()
        self.manual_input_button = QPushButton("Confirm")
        manual_input_layout.addWidget(self.manual_input_button)
        self.manual_input_group.setLayout(manual_input_layout)
        layout.addWidget(self.manual_input_group)

        # 创建导入文件部分
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

        # 连接按钮点击事件
        self.manual_input_button.clicked.connect(self.manual_input)
        self.file_browse_button.clicked.connect(self.browse_file)

        # 初始化
        self.manual_input_group.setEnabled(False)
        self.file_input_group.setEnabled(False)

    def update_content(self):
        input_option = self.main_window.settings.input_current_option
        if input_option == "Manual Input":
            self.manual_input_group.setEnabled(True)
            self.file_input_group.setEnabled(False)
        elif input_option == "Import File":
            self.manual_input_group.setEnabled(False)
            self.file_input_group.setEnabled(True)
        else:  # 无
            self.manual_input_group.setEnabled(False)
            self.file_input_group.setEnabled(False)

    def manual_input(self):
        dialog = DataInputDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            for index in range(dialog.tab_widget.count()):
                tab = dialog.tab_widget.widget(index)
                function = self.main_window.settings.func_current_options.keys()[index]
                if self.main_window.settings.func_current_options[function]:
                    self.data[function] = tab.get_input_data()  # 获取用户输入的数据
                    self.emit_input_changed()  # 在这里发出 input_changed 信号
        else:
            self.data = {}

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName()
        if file_path:
            self.filename = file_path  # 保存文件名
            self.file_path_label.setText(file_path)
            # 根据当前选中的功能查找相应的数据读取函数
            for func_option, selected in self.main_window.settings.func_current_options.items():
                if selected:
                    data_reader = self.data_readers.get(func_option)
                    if data_reader is not None:
                        # 读取文件数据
                        self.data[func_option] = data_reader(file_path)  # 直接使用相应的数据读取函数
                        self.emit_input_changed()  # 发出 input_changed 信号
            # Update the "Start" button status
            self.main_window.button_area.update_start_button()

    def emit_input_changed(self):
        # 当文本改变时发出 input_changed 信号
        self.input_changed.emit()

    # 用来清除数据
    def clear_data(self):
        self.data = {}

    def reset(self):
        self.clear_data()
        self.filename = None  # 清除文件名
        self.file_path_label.clear()  # 清除文件路径标签的文本
