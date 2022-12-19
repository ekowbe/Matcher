"""this module handles all the gui stuff"""
from sys import exit, argv
import os
import shutil
from PySide6.QtWidgets import QMainWindow, QGridLayout, QApplication, QFrame, QLineEdit
from PySide6.QtWidgets import QPushButton, QListWidget,QLabel, QFileDialog, QComboBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from run_match import match

FW_FONT = QFont("Monaco")
FW_FONT.setStyleHint(QFont.StyleHint.TypeWriter)
FW_FONT.setFixedPitch(True)

def launchDialog(window, option):
    response = QFileDialog.getOpenFileName(window, 'Open file', 'c:\\', 'Data File (*.csv)')

    # source
    src = response[0]

    # dest
    if option == 'Student Data':
        dest = './student_data.csv'
    elif option == 'Project Data':
        dest = './project_data.csv'
    else:
        exit(0)

    try:
        shutil.copyfile(src, dest)
        print("File copied successfully.")

    # If source and destination are same
    except shutil.SameFileError:
        print("Source and destination represents the same file.")

    # If destination is a directory.
    except IsADirectoryError:
        print("Destination is a directory.")

    # If there is any permission issue
    except PermissionError:
        print("Permission denied.")

    # For other errors
    except:
        print("Error occurred while copying file.")

    return response[0]

# main
def run_gui():
    
    """kicks in GUI"""
    app = QApplication(argv)
    window = QMainWindow()
    layout = QGridLayout()

    # combo
    options = ('Student Data', 'Project Data')
    combo = QComboBox()
    combo.addItems(options)

    layout.addWidget(combo)

    # file picker button
    file_picker_btn = QPushButton('Get File')
    layout.addWidget(file_picker_btn)

    # button
    start_match_btn = QPushButton('Start Match')
    layout.addWidget(start_match_btn)

    # frame
    frame = QFrame()
    frame.setLayout(layout)

    # window
    window.setWindowTitle('YLS EC Application')
    window.setCentralWidget(frame)
    screen_size = app.primaryScreen().availableGeometry()
    window.resize(screen_size.width()//2, screen_size.height()//2)

    # delegate functions
    def fp_btn_delegate():
        launchDialog(window, combo.currentText())

    def sm_btn_delegate():
        # launchMatchScreen(window)
        match()

    # listeners
    file_picker_btn.clicked.connect(fp_btn_delegate)
    start_match_btn.clicked.connect(sm_btn_delegate)


    # show window
    window.show()
    exit(app.exec())

if __name__ == '__main__':
    run_gui()
