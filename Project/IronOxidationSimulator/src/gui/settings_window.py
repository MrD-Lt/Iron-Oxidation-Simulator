"""
settings_window.py
----------------------
Author: Dongzi Ding
Created: 2023-06-26
Modified: 2023-08-14
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QTextEdit


class SettingsWindow(QWidget):
    """
    A window displaying user settings and associated instructions.

    Attributes:
        - main_window (QWidget): Reference to the main application window.
        - guide_textedit (QTextEdit): Text area displaying guidance for selected settings.
        - scroll_area (QScrollArea): Scroll area housing the guide text.
        - option_label (QLabel): Label showing current selected options.
    """

    def __init__(self, parent=None):
        """Initialize the SettingsWindow with its components."""
        super().__init__(parent)

        h_layout = QHBoxLayout()

        self.guide_textedit = QTextEdit(self)
        self.guide_textedit.setReadOnly(True)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.guide_textedit)
        self.scroll_area.setWidgetResizable(True)

        self.option_label = QLabel()

        h_layout.addWidget(self.scroll_area)
        h_layout.addWidget(self.option_label)

        layout = QVBoxLayout()
        layout.addLayout(h_layout)
        self.setLayout(layout)

        self.main_window = parent
        self.main_window.settings.settings_changed.connect(self.update_content)
        self.update_content()

        max_width = self.sizeHint().width()
        self.guide_textedit.setMaximumWidth(max_width)
        self.scroll_area.setMaximumWidth(max_width)

    def update_content(self):
        """Update the content displayed based on the user's selected settings."""
        selected_options = [option for option, selected in self.main_window.settings.func_current_options.items() if
                            selected]
        input_option = self.main_window.settings.input_current_option
        save_option = self.main_window.settings.save_current_option

        # Initialize guide_text with HTML formatting for colored text
        guide_text = ""

        # Check selected options and provide corresponding guidance in red text
        if not selected_options:
            guide_text += '<span style="color: red;">Please select at least one feature.</span><br>'
        elif input_option == "None":
            guide_text += '<span style="color: red;">Please select an input method.</span><br>'
        else:
            guide_text += "You can now input your data.<br>"

        # Provide guidance for multiple selected features in red text
        if len(selected_options) > 1:
            guide_text += '<span style="color: red;"><br>Please note: <br>When multiple features are selected, ' \
                          'you can only use manual input and cannot upload files.</span><br>'

        func_guide_text = []

        # Provide specific guidance for each selected feature
        if 'reaction order analysis' in selected_options:
            func_guide_text.append("For reaction order analysis, please input your data in:<br>"
                                   "If import file: Excel format,<br>"
                                   "log[Fe], logR0, Δlog[Fe] absolute, Δlog[Fe] upper, Δlog[Fe] lower,<br>"
                                   "ΔlogR0 absolute, ΔlogR0 upper, ΔlogR0 lower<br>"
                                   "in different columns.<br>"
                                   "If manually input: follow the instructions.")

        if 'initial rate analysis' in selected_options:
            func_guide_text.append("For initial rate analysis, please input your data in:<br>"
                                   "If import file: Excel format,<br>"
                                   "Time (seconds), [Fe2+] (uM), Threshold (5%-20%)<br>"
                                   "in different columns.<br>"
                                   "If manually input: follow the instructions.")

        if 'rate const analysis' in selected_options:
            func_guide_text.append("For rate const analysis, please input your data in:<br>"
                                   "If import file: Excel format,<br>"
                                   "Time (seconds), [Fe2+] (uM)<br>"
                                   "in different columns.<br>"
                                   "If manually input: follow the instructions.")

        if '3D plane plot' in selected_options:
            func_guide_text.append("For 3D plane plot, please input your data in:<br>"
                                   "If import file: Excel format,<br>"
                                   "pH, ΔpH, logFe, ΔlogFe, logR, ΔlogR<br>"
                                   "in different columns.<br>"
                                   "If manually input: follow the instructions.")

        # Combine all guidance texts
        divider = "<br>" + "-" * 30 + "<br>"  # HTML divider
        if func_guide_text:
            guide_text += '<br>' + divider.join(func_guide_text)

        # Set the final guide text with HTML formatting
        self.guide_textedit.setHtml(guide_text)

        # Display selected options and settings
        self.option_label.setText(
            f"Selected options: {', '.join(selected_options) or 'None'}<br>"
            f"Input method  : {input_option}<br>"
            f"Content saved : {save_option}"
        )
