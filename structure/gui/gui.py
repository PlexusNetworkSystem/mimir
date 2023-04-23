import os
import sys

if sys.platform.startswith('win'):
    os.system("python win.gui.py")    
    print("win")
else:
    os.system("python3 lin.gui.py")
    print("linux")
