from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.label = QLabel()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.main_window = parent
        self.main_window.settings.settings_changed.connect(self.update_content)
        self.update_content()  # 更新初始内容

    def update_content(self):
        # 更新窗口内容
        self.label.setText(
            f"Current option: {self.main_window.settings.func_current_option}\n"
            f"Input method  : {self.main_window.settings.input_current_option}\n"
            f"Content saved : {self.main_window.settings.save_current_option}")


