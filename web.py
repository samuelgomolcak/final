from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect
import MySQLdb  
import time
import math
import random
import serial
import ConfigParser


ser=serial.Serial("/dev/ttyS1",9600)
ser.baudrate=9600

async_mode = None

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock() 

config = ConfigParser.ConfigParser()
config.read('config.cfg')
myhost = config.get('mysqlDB', 'host')
myuser = config.get('mysqlDB', 'user')
mypasswd = config.get('mysqlDB', 'passwd')
mydb = config.get('mysqlDB', 'db')
print myhost

def background_thread(args):
    count = 0
    A=0
    i=0
    dbV = 'nieco'  
    dataCounter = 0 
    dataList = []  
    db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
    while True:
        #ser.write(str(int(9)))
        socketio.sleep(0.5)
        if dict(args).get('A') is not None:
           A = dict(args).get('A')
           A=int(A)
        dbV = dict(args).get('db_value')
        if A==1 or A==2 or A==3 or A==4 or A==5:
            if dbV == 'start':
                if i==0 or i!=A:
                    ser.write(str(A))
                    i=A
                    print(A)
                cas = time.time()
                ser.write(str(int(9)))
                data = ser.readline()
                values = data.split(',')   
                print(values[0])
                print(values[1])
                count += 1
                dataCounter +=1
            
            
            
                dataDict = {
                    "t": time.time(),
                    "x": dataCounter,
                    "y": values[0],
                    "z": values[1],
                    }
                dataList.append(dataDict)
                
                if len(dataList)>0:
                    print (str(dataList))
                    fuj = str(dataList).replace("'", "\"")
                    print fuj
                    cursor = db.cursor()
                    cursor.execute("SELECT count(id) FROM graph")
                    maxid = cursor.fetchone()
                    cursor.execute("INSERT INTO graph (hodnoty) VALUES ('%s')"%(fuj))
                    db.commit()
                dataList = []
                dataCounter = 0
                  
                socketio.emit('my_response',
                                {'data': values[0],'data2': values[1], 'count': count, 'time':cas},
                                namespace='/test')
    db.close()
  
@socketio.on('my_event', namespace='/test')
def test_message(message):   
    session['receive_count'] = session.get('receive_count', 0) + 1 
    session['A'] = message['value']    
    emit('my_response',
         {'data': message['value'], 'count': session['receive_count'], 'ampl':1})
    
@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
    emit('my_response', {'data': 'Connected', 'count': 0})

@app.route('/db')
def db():
  db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  cursor.execute('''SELECT  hodnoty FROM  graph WHERE id=1''')
  rv = cursor.fetchall()
  return str(rv)    

@app.route('/dbdata/<string:num>', methods=['GET', 'POST'])
def dbdata(num):
  db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  print num
  cursor.execute("SELECT hodnoty FROM  graph WHERE id=%s", num)
  rv = cursor.fetchone()
  return str(rv[0])

@app.route('/')
def index():
    return render_template('tabs.html', async_mode=socketio.async_mode)

@socketio.on('db_event', namespace='/test')
def db_message(message):   
#    session['receive_count'] = session.get('receive_count', 0) + 1 
    session['db_value'] = message['value']    
#    emit('my_response',
#         {'data': message['value'], 'count': session['receive_count']})

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()
    
@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)
