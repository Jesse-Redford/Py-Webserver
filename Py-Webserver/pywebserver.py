#C:\Users\Jesse/.ngrok2/ngrok.yml
import sys
import io
sys.path.append(r'C:\Users\Jesse\Desktop\WordPress\Apps\templates')
import cv2
from flask import Flask, render_template, Response


app = Flask(__name__)
vc = cv2.VideoCapture(0)

@app.route('/')
def hello_world():
    return render_template('index.html') #'Hello from Flask!'
    
def gen():
    """Video streaming generator function."""
    while True:
        read_return_code, frame = vc.read()
        encode_return_code, image_buffer = cv2.imencode('.jpg', frame)
        io_buf = io.BytesIO(image_buffer)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')



    
if __name__ == "__main__":
    # run current python script 
    # paste this into new cmd window cd C:\Users\Jesse\Downloads\ngrok-stable-windows-amd64
    # find --> ngrok.exe --> type in --> ngrok http 80
    # C:\Users\Jesse\Downloads\ngrok-stable-windows-amd64
    # check current tunnel is active at https://dashboard.ngrok.com/status/tunnels
    # this allows for access from any network / device just use ngrok tunnel link in browser
    app.run(host='127.0.0.1', port=80,debug=False, threaded= True)
    
    #  Test access 
    #app.run(host='192.168.1.249',port=5000,debug=False, threaded= True)
    
    
    
