from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QFileDialog, QLabel, QTextEdit


class InputWindow(QWidget):
    # 添加一个信号来在文本改变时发出
    input_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = parent

        layout = QVBoxLayout()

        # 创建手动输入部分
        self.manual_input_group = QGroupBox("Manual Input")
        manual_input_layout = QVBoxLayout()
        self.manual_input_text = QTextEdit()
        self.manual_input_button = QPushButton("Confirm")
        manual_input_layout.addWidget(self.manual_input_text)
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
        self.manual_input_button.clicked.connect(self.manual_input_confirmed)
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

    def manual_input_confirmed(self):
        text = self.manual_input_text.toPlainText()
        # TODO: 处理文本输入
        self.emit_input_changed()  # 在这里发出 input_changed 信号
        self.manual_input_text.clear()

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName()
        if file_path:
            self.file_path_label.setText(file_path)
            # TODO: 处理文件输入
            self.emit_input_changed()  # 发出 input_changed 信号

    def emit_input_changed(self):
        # 当文本改变时发出 input_changed 信号
        self.input_changed.emit()
