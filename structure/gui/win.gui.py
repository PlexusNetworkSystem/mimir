import os
import re
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QScrollArea, QComboBox, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super(CustomTitleBar, self).__init__(parent)
        self.setAutoFillBackground(True)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title = QLabel("MIMIR - Chat App")
        self.title.setStyleSheet("color: #f0f0f0; font-weight: bold; padding-left: 10px;")
        layout.addWidget(self.title)

        self.minimize_button = QPushButton("─")
        self.minimize_button.setFixedSize(20, 20)
        self.minimize_button.clicked.connect(self.parent().showMinimized)
        layout.addWidget(self.minimize_button)

        self.maximize_button = QPushButton("□")
        self.maximize_button.setFixedSize(20, 20)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.maximize_button)

        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(20, 20)
        self.close_button.clicked.connect(self.parent().close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        self.start_drag_position = None

    def toggle_maximize(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
        else:
            self.parent().showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_drag_position = event.globalPos() - self.parent().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.start_drag_position is not None:
            self.parent().move(event.globalPos() - self.start_drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_drag_position = None
            event.accept()

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('MIMIR - Chat App')
        self.setGeometry(100, 100, 400, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #f0f0f0;
                font-weight: bold;
            }
            QComboBox, QPushButton, QTextEdit, QScrollArea {
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                color: #f0f0f0;
                background-color: #2a2a2a;
            }
            QComboBox::drop-down {
                border: none;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
            QTextEdit::placeholder-text {
                color: #5a5a5a;
            }
        """)

        layout = QVBoxLayout()

        title_bar = CustomTitleBar(self)
        layout.addWidget(title_bar)

        model_selection_layout = QHBoxLayout()
        model_label = QLabel('Model:', self)
        model_selection_layout.addWidget(model_label)

        self.model_combo_box = QComboBox(self)
        self.model_combo_box.addItem('Logical')
        self.model_combo_box.addItem('Creative')
        model_selection_layout.addWidget(self.model_combo_box)

        layout.addLayout(model_selection_layout)

        self.chat_log = QTextEdit(self)
        self.chat_log.setReadOnly(True)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.chat_log)
        layout.addWidget(scroll_area)

        input_button_layout = QHBoxLayout()

        self.user_input = QTextEdit(self)
        self.user_input.setPlaceholderText('Prompt...')
        self.user_input.setLineWrapMode(QTextEdit.WidgetWidth)
        self.user_input.setFixedHeight(int(self.user_input.fontMetrics().lineSpacing() * 3.5))
        input_button_layout.addWidget(self.user_input)

        send_button = QPushButton('Send', self)
        input_button_layout.addWidget(send_button)

        reset_button = QPushButton('Reset Context', self)
        input_button_layout.addWidget(reset_button)

        layout.addLayout(input_button_layout)
        send_button.setStyleSheet('font-size: 18px; height: 40px;')
        reset_button.setStyleSheet('font-size: 18px; height: 40px;')

        self.setLayout(layout)
        send_button.clicked.connect(self.send_message)
        reset_button.clicked.connect(self.reset_context)
        self.model_combo_box.currentIndexChanged.connect(self.change_model)

    def send_message(self):
        message = self.user_input.toPlainText().strip()

        if message:
            self.chat_log.append(f'Client: {message}')
            response = self.generate_response()
            self.chat_log.append(f'MIMIR: {response}')
            self.user_input.clear()

    def change_model(self):
        model = self.model_combo_box.currentText()
        self.chat_log.clear()

    def reset_context(self):
        self.chat_log.clear()
        self.chat_log.append("SYSTEM: context is reseted")
        print("LOG: reset_context...")
        model_type = self.model_combo_box.currentText().lower()
        if sys.platform.startswith('win'):
            command = f"cd ..\\.. & python structure\\main.system\\reset_context.py --model-type {model_type}"
        else:
            command = f"cd ../.. ; python structure/main.system/reset_context.py --model-type {model_type}"
        os.system(command)
        self.user_input.clear()

    def generate_response(self):
        with open('../main.system/check.txt', 'r') as f:
            model_type = self.model_combo_box.currentText().lower()
            prompt = self.user_input.toPlainText().strip()
            if sys.platform.startswith('win'):
                command = f"cd ..\\.. & python structure\\main.system\\main.py --prompt \"{prompt}\" --model-type {model_type}"
            else:
                command = f"cd ../.. ; python structure/main.system/main.py --prompt '{prompt}' --model-type {model_type}"
            print(command)
            os.system(command)
            # check if answer is ready or not
            while re.search("1", f.readline()):
                with open('../main.system/check.txt', 'w') as f:
                    # write 0 to indicate the response is read
                    f.write("0")
                with open('../main.system/response.txt', 'r+') as f:
                    f.write("")
                    response = f.read(-1)
                    return response

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.show()
    sys.exit(app.exec_())
