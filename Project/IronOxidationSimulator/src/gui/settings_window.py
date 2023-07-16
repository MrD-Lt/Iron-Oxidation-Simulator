from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout


class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建一个 QHBoxLayout 实例
        h_layout = QHBoxLayout()

        self.guide_label = QLabel()  # 更改为 self.guide_label
        self.option_label = QLabel()  # 新增
        h_layout.addWidget(self.guide_label)
        h_layout.addWidget(self.option_label)  # 新增

        # 将 QHBoxLayout 添加到主 QVBoxLayout 中
        layout = QVBoxLayout()
        layout.addLayout(h_layout)
        self.setLayout(layout)

        self.main_window = parent
        self.main_window.settings.settings_changed.connect(self.update_content)
        self.update_content()  # 更新初始内容

    def update_content(self):
        # 更新窗口内容
        selected_options = [option for option, selected in self.main_window.settings.func_current_options.items() if
                            selected]
        input_option = self.main_window.settings.input_current_option
        save_option = self.main_window.settings.save_current_option
        # 根据选项设置提示文字
        if not selected_options:
            guide_text = "Please select at least one feature."
        elif input_option == "None":
            guide_text = "Please select an input method."
        else:
            guide_text = "You can now input your data."

        # 添加功能相关的提示文字
        func_guide_text = []
        if 'reaction order analysis' in selected_options:
            func_guide_text.append("For reaction order analysis, please input your data in format A.")
        if 'option2' in selected_options:
            func_guide_text.append("For Option 2, please input your data in format B.")
        if 'option3' in selected_options:
            func_guide_text.append("For Option 3, please input your data in format C.")
        # 如果有功能相关的提示文字，则添加到 guide_text 中
        if func_guide_text:
            guide_text += '\n' + '\n'.join(func_guide_text)

        # 显示提示文字
        self.guide_label.setText(guide_text)

        # 显示选项
        self.option_label.setText(
            f"Selected options: {', '.join(selected_options) or 'None'}\n"
            f"Input method  : {input_option}\n"
            f"Content saved : {save_option}"
        )

