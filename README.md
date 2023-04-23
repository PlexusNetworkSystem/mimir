# 🤖 MIMIR - Chat App 📱

MIMIR is an interactive chat application that uses **GPT-3.5** and **Claude-instant** to generate responses to user prompts. The application is implemented in Python 🐍 and PyQt5, and it runs on Windows 🖥️ and Linux 🐧.

# 🌟 Features

    🤖 Allows users to select between two different models: "Logical" and "Creative".
    💬 Displays the chat log in a scrollable text area.
    📝 Provides a text input box where users can enter prompts.
    🙌 Includes two buttons: "Send" to send the prompt to the model and display the response, and "Reset Context" to reset the model's context.
    🎉 Implements a custom title bar with minimize, maximize, and close buttons.
    🚀 Supports drag and drop for window movement.
    🌃 Applies a dark theme to the UI.

# 🔧 Installation

To run the MIMIR chat app, you need to have Python 3.x, PyQt5, and poe-api installed on your system. You can install PyQt5 and poe-api via pip:

```
pip install PyQt5 poe-api
```
Once you have installed the dependencies, you need to add your Poe.com cookie to the config.ini file in the "structure" directory. To do this, open the config.ini file with a text editor, and replace "YOUR_API_KEY_HERE" with your actual cookie.

After you have added your API key, you can run the app by executing the following command in the terminal:

    🖥️ On Windows: Double-click on the "gui.py" file in the "structure/gui" folder to launch the app.
    🐧 On Linux: Run the "main.sh" file in the "structure/gui" folder using the terminal.

# 🚀 Usage

When you run the app, you will see the main window with the title bar and the chat log area. You can select the model you want to use from the drop-down menu on the top of the window.

To start a conversation, enter a prompt in the input box and click the "Send" button. The model will generate a response, which will be displayed in the chat log area. You can continue the conversation by entering more prompts.

If you want to reset the model's context, click the "Reset Context" button. This will clear the model's memory and start a new conversation.

To close the app, click the "X" button on the top-right corner of the window.
