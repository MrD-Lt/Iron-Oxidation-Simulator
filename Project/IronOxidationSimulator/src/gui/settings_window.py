from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QTextEdit


class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建一个 QHBoxLayout 实例
        h_layout = QHBoxLayout()

        self.guide_textedit = QTextEdit(self)  # 使用 QTextEdit 替代 QLabel
        self.guide_textedit.setReadOnly(True)  # 设置为只读模式

        self.scroll_area = QScrollArea(self)  # 创建一个 QScrollArea 实例
        self.scroll_area.setWidget(self.guide_textedit)  # 设置 QTextEdit 为 QScrollArea 的小部件
        self.scroll_area.setWidgetResizable(True)  # 允许小部件调整大小

        self.option_label = QLabel()

        h_layout.addWidget(self.scroll_area)  # 将 QScrollArea 添加到布局中
        h_layout.addWidget(self.option_label)

        # 将 QHBoxLayout 添加到主 QVBoxLayout 中
        layout = QVBoxLayout()
        layout.addLayout(h_layout)
        self.setLayout(layout)

        self.main_window = parent
        self.main_window.settings.settings_changed.connect(self.update_content)
        self.update_content()  # 更新初始内容

        # 设置 guide_textedit 的最大宽度
        max_width = self.sizeHint().width()
        self.guide_textedit.setMaximumWidth(max_width)

        self.scroll_area.setMaximumWidth(max_width)

    def update_content(self):
        # 更新窗口内容
        selected_options = [option for option, selected in self.main_window.settings.func_current_options.items() if selected]
        input_option = self.main_window.settings.input_current_option
        save_option = self.main_window.settings.save_current_option

        # 根据选项设置提示文字
        if not selected_options:
            guide_text = "Please select at least one feature.\n"
        elif input_option == "None":
            guide_text = "Please select an input method.\n"
        else:
            guide_text = "You can now input your data.\n"

        # Check if multiple features are selected and update the guide text accordingly
        if len(selected_options) > 1:
            guide_text += '\nPlease note: \nWhen multiple features are selected, ' \
                          'you can only use manual input and cannot upload files.\n'

        # 添加功能相关的提示文字
        func_guide_text = []

        if 'reaction order analysis' in selected_options:
            func_guide_text.append("For reaction order analysis, please input your data in:\n"
                                   "If import file: Excel format,\n"
                                   "log[Fe], logR0, Δlog[Fe] absolute, Δlog[Fe] upper, Δlog[Fe] lower,\n"
                                   "ΔlogR0 absolute, ΔlogR0 upper, ΔlogR0 lower\n"
                                   "in different columns.\n"
                                   "If manually input: follow the instructions.")

        if 'initial rate analysis' in selected_options:
            func_guide_text.append("For initial rate analysis, please input your data in:\n"
                                   "If import file: Excel format,\n"
                                   "Time (seconds), [Fe2+] (uM), Threshold (5%-20%)\n"
                                   "in different columns.\n"
                                   "If manually input: follow the instructions.")

        if 'rate const analysis' in selected_options:
            func_guide_text.append("For rate const analysis, please input your data in:\n"
                                   "If import file: Excel format,\n"
                                   "Time (seconds), [Fe2+] (uM)\n"
                                   "in different columns.\n"
                                   "If manually input: follow the instructions.")

        if '3D plane plot' in selected_options:
            func_guide_text.append("For 3D plane plot, please input your data in:\n"
                                   "If import file: Excel format,\n"
                                   "pH, ΔpH, logFe, ΔlogFe, logR, ΔlogR\n"
                                   "in different columns.\n"
                                   "If manually input: follow the instructions.")

        # 如果有功能相关的提示文字，则添加到 guide_text，并添加分界线
        divider = "\n" + "-" * 30 + "\n"  # 分界线
        if func_guide_text:
            guide_text += '\n' + divider.join(func_guide_text)

        # 显示提示文字
        self.guide_textedit.setPlainText(guide_text)

        # 显示选项
        self.option_label.setText(
            f"Selected options: {', '.join(selected_options) or 'None'}\n"
            f"Input method  : {input_option}\n"
            f"Content saved : {save_option}"
        )

