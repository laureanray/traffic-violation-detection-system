from .. import socketio
import time
import datetime
import eventlet
eventlet.monkey_patch()


def emit_log(logstring):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    socketio.emit('log', {'data': '[' + st + '] ' + logstring })