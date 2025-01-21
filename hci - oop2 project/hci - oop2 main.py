from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

import sys

from timer import *


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "KAMATI[ME]S"
        self.x = 200
        self.y = 200
        self.width = 300
        self.height = 300

        self.player = QMediaPlayer()  # for playsounds
        self.currentTimer = None  # variable for choosing a timer (Pomodoro, short, long)
        self.mainStart = False  # Master Switch of timer

        self.initUI()

    def initUI(self):
        # window Title
        self.setWindowTitle(self.title)
        self.setGeometry(self.x, self.y, self.width, self.height)

        # icons
        self.setWindowIcon(QIcon('tomato.ico'))
        self.setStyleSheet("background-color: #ff686b;")

        # to create layout
        mainLayout = QVBoxLayout()

        # Add the grid layout for the timer and controls
        gridLayout = self.createGridLayout()
        mainLayout.addLayout(gridLayout)

        # Add the dynamic task list layout
        vboxLayout = self.createVBoxLayout()
        mainLayout.addLayout(vboxLayout)

        # Set the main layout
        self.setLayout(mainLayout)

        # for  seeTime function
        self.updateTimer = QTimer(self)
        self.updateTimer.timeout.connect(self.updateTimerTick)
        self.updateTimer.start(100)

        self.show()

    def createGridLayout(self):

        # Initialization of grid
        layout = QGridLayout()
        layout.setColumnStretch(2, 5)

        # POMODORO BUTTON
        self.pomodoroButton = QPushButton('POMODORO', self)
        self.pomodoroButton.setToolTip("Standard 25 minutes and 5 mins break after")
        self.pomodoroButton.clicked.connect(self.resetTimer)
        self.pomodoroButton.clicked.connect(self.clickSound)
        self.pomodoroButton.clicked.connect(lambda: self.startTimer("pomodoro"))
        self.pomodoroButton.clicked.connect(self.initialLabel)
        self.pomodoroButton.setStyleSheet("background-color : #7dbf59")

        # Short Break BUTTON
        self.shortButton = QPushButton('Short Break', self)
        self.shortButton.setToolTip("5 mins break")
        self.shortButton.clicked.connect(self.resetTimer)
        self.shortButton.clicked.connect(self.clickSound)
        self.shortButton.clicked.connect(lambda: self.startTimer("short"))
        self.shortButton.clicked.connect(self.initialLabel)
        self.shortButton.setStyleSheet("background-color : #7dbf59")

        # Long Break BUTTON
        self.longButton = QPushButton('Long Break', self)
        self.longButton.setToolTip("15 mins break")
        self.longButton.clicked.connect(self.resetTimer)
        self.longButton.clicked.connect(self.clickSound)
        self.longButton.clicked.connect(lambda: self.startTimer("long"))
        self.longButton.clicked.connect(self.initialLabel)
        self.longButton.setStyleSheet("background-color : #7dbf59")
        pixmap = QPixmap(r'C:\Users\TIPQC\Desktop\OOP Project Pomodoro\tomato.jpg')
        self.tomatoPic = QLabel(self)
        self.tomatoPic.setPixmap(pixmap)

        # TIMER LABELLLLLLLL
        self.timerLabel = QLabel("POMODORO", self)
        self.timerLabel.setFont(QFont('Times', 20))
        self.timerLabel.setAlignment(Qt.AlignCenter)
        self.timerLabel.setStyleSheet("border : 2px solid black;"
                                      "background: #ffe4e4")

        # TASK LABEL
        self.taskLabel = QLabel("Tasks", self)
        self.taskLabel.setStyleSheet("border : 2px solid black;"
                                     "background: #ffe4e4")
        self.taskLabel.setFont(QFont('Times', 15))
        self.taskLabel.setAlignment(Qt.AlignCenter)

        # reset BUTTON
        self.resetButton = QPushButton('Reset', self)
        self.resetButton.setToolTip("Reset the timer!")
        self.resetButton.clicked.connect(self.resetTimer)
        self.resetButton.clicked.connect(self.clickSound)
        self.resetButton.clicked.connect(self.initialLabel)
        self.resetButton.setStyleSheet("background-color : #bcdb72")

        # Start button
        self.startButton = QPushButton('start', self)
        self.startButton.setToolTip("Let's start working!")
        self.startButton.setStyleSheet("background-color : #bcdb72")
        self.startButton.setCheckable(True)
        self.startButton.clicked.connect(self.clickSound)
        self.startButton.clicked.connect(self.toggleTimer)

        # edit BUTTON
        self.editButton = QPushButton('Custom', self)
        self.editButton.setToolTip("Customize you timer!")
        self.editButton.setStyleSheet("background-color : #bcdb72")
        self.editButton.clicked.connect(self.resetTimer)
        self.editButton.clicked.connect(self.clickSound)
        self.editButton.clicked.connect(self.customDuration)
        self.editButton.clicked.connect(self.initialLabel)

        # GRID LAYOUTS
        layout.addWidget(self.pomodoroButton, 0, 1)
        layout.addWidget(self.shortButton, 0, 2)
        layout.addWidget(self.longButton, 0, 3)
        layout.addWidget(self.timerLabel, 2, 2)
        layout.addWidget(self.tomatoPic, 3, 2)
        layout.addWidget(self.resetButton, 4, 1)
        layout.addWidget(self.startButton, 4, 2)
        layout.addWidget(self.editButton, 4, 3)
        layout.addWidget(self.taskLabel, 5, 2)

        return layout

    def createVBoxLayout(self):
        layout = QVBoxLayout()

        # Input area of Task
        inputLayout = QHBoxLayout()
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("Enter label text here")
        self.inputField.returnPressed.connect(self.addLabel)

        # Add label button
        self.addButton = QPushButton("Add Label")
        self.addButton.clicked.connect(self.addLabel)
        self.addButton.clicked.connect(self.clickSound)
        self.addButton.setStyleSheet("background-color : #bcdb72")

        # Add input field and button to the input layout
        inputLayout.addWidget(self.inputField)
        inputLayout.addWidget(self.addButton)

        # Scroll area to hold the dynamic layout
        self.scrollArea = QScrollArea()
        self.scrollAreaWidget = QWidget()
        self.scrollAreaLayout = QVBoxLayout()
        self.scrollAreaWidget.setLayout(self.scrollAreaLayout)
        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.scrollArea.setWidgetResizable(True)

        # Add the input layout and scroll area to the main layout
        layout.addLayout(inputLayout)
        layout.addWidget(self.scrollArea)

        return layout

    # ----------------------Task List Functions-------------------------------------------

    def addLabel(self):
        # Get the text from the input field
        text = self.inputField.text().strip()
        if text:
            # Create a task with remove button
            taskLayout = QHBoxLayout()
            taskLabel = QLabel(text)
            removeButton = QPushButton("Remove")
            removeButton.clicked.connect(lambda: self.removeLabel(taskLayout))
            removeButton.clicked.connect(self.clickSound)
            removeButton.setStyleSheet("background-color : white")

            taskLayout.addWidget(taskLabel)
            taskLayout.addWidget(removeButton)
            self.scrollAreaLayout.addLayout(taskLayout)

            # Clear the input field
            self.inputField.clear()

    def removeLabel(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.scrollAreaLayout.removeItem(layout)

    # ---------------------Timer Functions---------------------------------------------------

    # to show the time initially without starting the timer
    def initialLabel(self):
        minutes = self.currentTimer.getRemainingTime() // 600
        seconds = (self.currentTimer.getRemainingTime() // 10) % 60
        self.timerLabel.setText(f"{minutes}:{seconds:02d}")

    # pick a timer function
    def startTimer(self, timerType):
        if timerType == "pomodoro":
            self.currentTimer = PomodoroTimer()
            self.setStyleSheet("background-color: #ff686b;")  # Pomodoro Color

        elif timerType == "short":
            self.currentTimer = ShortBreakTimer()
            self.setStyleSheet("background-color: #97DEE7;")  # Short Break Color

        elif timerType == "long":  # Long Break Color
            self.currentTimer = LongBreakTimer()
            self.setStyleSheet("background-color:  #78C5DC;")

        if self.startButton.isChecked():
            self.mainStart = True

        else:
            self.mainStart = False

    # function to decrement or count the time
    def updateTimerTick(self):
        if self.mainStart and self.currentTimer:
            self.currentTimer.tick()

            if self.currentTimer.isDone():
                self.timerLabel.setText("Take a Break!")
                self.mainStart = False
                self.startButton.setChecked(False)
                self.startButton.setStyleSheet(
                    "background-color: lightgrey" if self.mainStart else "background-color: #bcdb72")
                self.startButton.setText("Start")

                self.ringSound()

            else:
                minutes = self.currentTimer.getRemainingTime() // 600
                seconds = (self.currentTimer.getRemainingTime() // 10) % 60
                self.timerLabel.setText(f"{minutes}:{seconds:02d}")

    # just for start button toggling and change labels
    def toggleTimer(self):

        self.mainStart = self.startButton.isChecked()
        self.startButton.setText("Pause" if self.mainStart else "Start")
        self.startButton.setStyleSheet("background-color: lightgrey" if self.mainStart else "background-color: #bcdb72")

    # to get the custom time
    def customDuration(self):
        self.mainStart = False

        # Get user input for duration in minutes
        minutes, doneMinutes = QInputDialog.getInt(self, 'Set Timer Duration', 'Enter duration in minutes:', 0, 0, 59)

        # Get user input for duration in seconds
        seconds, doneSeconds = QInputDialog.getInt(self, 'Set Timer Duration', 'Enter duration in seconds:', 0, 0, 59)

        if doneMinutes and doneSeconds:  # Check if both inputs were confirmed
            # Convert total time to seconds
            totalDurationInSeconds = (minutes * 60) + seconds

            # timer with the user-defined duration
            self.currentTimer = CustomTimer(totalDurationInSeconds)

            # Update the timer label to reflect the new duration
            self.timerLabel.setText(f"Custom Timer: {minutes} minutes and {seconds} seconds")

        else:
            # User clicked Cancel
            pass

            # resets the time of the timer chosen

    def resetTimer(self):
        if self.currentTimer:
            self.currentTimer.reset()
        self.mainStart = False

        self.startButton.setChecked(False)
        self.startButton.setStyleSheet("background-color: lightgrey" if self.mainStart else "background-color: #bcdb72")
        self.startButton.setText("Start")

    # ringngin sound effect
    def ringSound(self):

        sound_file = 'ring.mp3'
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(sound_file)))
        self.player.play()

    # clicking sound effect
    def clickSound(self):

        soundFile = 'click.mp3'
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(soundFile)))
        self.player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())