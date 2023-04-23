# import required libraries 
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QScrollArea, QComboBox, QLabel, QHBoxLayout
import sys, os
import re


class ChatApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('MIMIR - Chat App')
        self.setGeometry(100, 100, 400, 600)

        layout = QVBoxLayout()

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
        self.update_window_title(model)
    
    def reset_context(self):
        self.chat_log.clear()
        self.chat_log.append("SYSTEM: context is reseted")
        print("LOG: reset_context...")
        command = f"cd ../.. ;python structure/main.system/reset_context.py --model-type {self.model_combo_box.currentText().lower()}"
        os.system(command)
        self.user_input.clear()
    def update_window_title(self, input):
        prompt = f'MIMIR - {input}'
        if len(prompt) > 25:
            prompt = prompt[:22] + '...'
        self.setWindowTitle(prompt)
    def generate_response(self):
       with open('../main.system/check.txt', 'r') as f:
           command = "notify-send -a Plexus\ Amarok 'Mimir is thinking...';cd ../.. ;python structure/main.system/main.py --prompt '{}' --model-type {}".format(self.user_input.toPlainText().strip(), self.model_combo_box.currentText().lower())
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
