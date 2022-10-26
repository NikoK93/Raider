from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QPlainTextEdit,
                                QVBoxLayout, QWidget, QCheckBox, QComboBox)
from PyQt5.QtCore import QProcess
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import sys
import time
import bot
import random
import argparse
import multiprocessing


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.p = None

        self.btn = QPushButton("Execute")
        self.btn.pressed.connect(self.slotStart)
        self.btn_stop = QPushButton("Stop")
        self.btn_stop.pressed.connect(self.slotStop)
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        # Dungeons
        self.cb = QComboBox()
        self.cb.addItems(['minotaur','dragon', 'spider', 'ice_golem', 'fire_knight'])
        self.cb.activated[str].connect(self.onSelected)

        self.cb_dt = QComboBox()
        self.cb_dt.addItems(['hard', 'normal'])
        self.cb_dt.activated[str].connect(self.onSelected_dt)

        # Action
        self.cb_action = QComboBox()
        self.cb_action.addItems([None, 'dragon', 'spider', 'ice_golem', 'fire_knight', 'minotaur',
        'force', 'spirit', 'magic', 'void', 'arcane', 
        'arena', 'tag_arena', 'FW', 'doom_tower','mini_routine',
        'UNM', 'NM', 'routine', 'routine_market_refresh'])
        self.cb_action.activated[str].connect(self.onSelected_action)

        # Bot variables
        self.b1 = QCheckBox("Energy spender last")
        self.b1.setChecked(False)
        self.b1.stateChanged.connect(self.clickBox)

        self.b2 = QCheckBox("Leveling")
        self.b2.setChecked(False)
        self.b2.stateChanged.connect(self.clickBox2)

        self.b3 = QCheckBox("Gem refill")
        self.b3.setChecked(False)
        self.b3.stateChanged.connect(self.clickBox3)

        self.b4 = QCheckBox("Action one time only")
        self.b4.setChecked(False)
        self.b4.stateChanged.connect(self.clickBox4)

        self.dungeon = 'dragon'
        self.dt_difficulty = 'hard'
        self.action = None
        self.leveling = False
        self.gem_refill = False
        self.energy_spender_last = False
        self.action_one_time = False
        self.dungeon_runs = 0

        # Add widgets
        l = QVBoxLayout()
        l.addWidget(self.btn)
        l.addWidget(self.btn_stop)
        l.addWidget(self.text)
        l.addWidget(self.b1)
        l.addWidget(self.b2)
        l.addWidget(self.b3)
        l.addWidget(self.b4)
        l.addWidget(self.cb)
        l.addWidget(self.cb_dt)
        l.addWidget(self.cb_action)

        w = QWidget()
        w.setLayout(l)

        self.setCentralWidget(w)


    def onSelected(self, value):
        self.dungeon = value
        print(self.dungeon)
    
    def onSelected_dt(self, value):
        self.dt_difficulty = value
        print(self.dt_difficulty)

    def onSelected_action(self, value):
        self.action = value
        print(self.action)

    def clickBox(self, state):

        if state == QtCore.Qt.Checked:
            self.energy_spender_last = True
            print('Checked')
        else:
            self.energy_spender_last = False
            print('Unchecked')
            
    def clickBox2(self, state):

        if state == QtCore.Qt.Checked:
            self.leveling = True
            print('Checked')
        else:
            self.leveling = False
            print('Unchecked')

    def clickBox3(self, state):

        if state == QtCore.Qt.Checked:
            self.gem_refill = True
            print('Checked')
        else:
            self.gem_refill = False
            print('Unchecked')

    def clickBox4(self, state):

        if state == QtCore.Qt.Checked:
            self.action_one_time = True
            print('Checked')
        else:
            self.action_one_time = False
            print('Unchecked')


    def message(self, s):
        self.text.appendPlainText(s)

    def construct_init(self):

        init = ["-u", 'bot.py'] 

        init.append('-c raid3')
        init.append(f'-u {self.dungeon}')

        if self.action:
            init.append(f"-a {self.action}")
        if self.leveling:
            init.append("-l")
        if self.dungeon_runs != 0:
            init.append(f'-d {self.dungeon_runs}')
        if self.energy_spender_last:
            init.append("-e")
        if self.gem_refill:
            init.append('-g')
        if self.action_one_time:
            init.append('-o')
        
        if self.dt_difficulty == 'normal':
            init.append('-t normal')
        else:
            init.append('-t hard')

        return init
        

    def start_process(self):
        if not self.p:

            self.message("Executing process")
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.

            init = self.construct_init()
            self.p.start("python", init)

     
    def slotStart(self):
        self.btn.setEnabled(False)
        self.start_process()
        self.btn.setEnabled(True)

    def slotStop(self):
        self.btn_stop.setEnabled(False)
        self.stopExecuting()
        self.btn_stop.setEnabled(True)

    def stopExecuting(self):
        print("Quiting actions")
        if self.p:
            self.p.kill()

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    def process_finished(self):
        self.message("Process finished.")
        self.p = None


app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec_()