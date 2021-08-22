from bot import Raider
import time
from multiprocessing import Process
import os

from flask_bootstrap import Bootstrap
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
backProc = None

def construct_init():

    init = ["-u", 'bot.py', 'raid3', 'dragon'] 

    return init

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/Execute_bot/')
def SomeFunction():
    #r = bot_process.raid('raid3', 'dragon')  
    #init = construct_init()
    global backProc
    raid = Raider('raid3', 'dragon')
    backProc = Process(target=raid.main_loop(), args=(), daemon=True)
    backProc.start()    
    return 'started: ' + str(backProc.pid)

        
    #p.start()
    '''
    print('In SomeFunction')

    #BOT_STATE = 0
    raid = Raider('raid3', 'dragon')    

    BOT_STATE = 1

    while BOT_STATE:

        if len(raid.actions) == 0:
            print('No actions left, quiting')
            break

        raid.main_loop()
        time.sleep(30)
        print("trying action...")

    '''
@app.route('/Stop_bot/')
def SomeFunction2():
    print('Stoping process')
    if backProc:
        backProc.terminate()
        print('Terminated')




if __name__ == '__main__':
   app.run(debug=True, use_reloader=False)