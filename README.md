# Py-Webserver

Tutorial for creating a webapp for viewing live video stream from a rasberry pi or windows desktop, from any device connected to the internet. 


### Installing required packages
Before proceeding make sure you have the following packages installed on the device which host the video stream.

- Python3 --> for coding application
- Flask --> used to create webapp
- OpenCV --> provides camera stream and face recognition
- ngrok --> download executable at https://ngrok.com/ and create an account. 

<details>
  <summary>Open cmd window and type the following to install the required packages</summary>
    pip install Flask (add version details)
    pip install OpenCV
  
</details>

### Setting up files

Create a project directior (folder) and name it Py-Webserver, this is where we will save our python files and html templates.
Next, create a folder and name it templates. Copy and paste the code below into notepad and save the file as index.html in the templates folder.

<details>
  <summary> Py-Webserver/templates --> index.html  </summary>

    <html>
      <head>
    <title>JR Lab Live Streaming</title>
     </head>
     <body>
    <h1>JR Lab Live Streaming</h1>
    <h1>Videoddd Streaming Demonstration</h1>
    <img src="{{ url_for('video_feed') }}">
    <p> @2020 Developed byJR.org</p>
     </body>
    </html>

</details>

Next, open up a python3 file and save it with the name pywebserver.py. Make sure this file is located in your project directory folder (Py-Webserver).  Copy and paste the code below into the python file. 


<details>
  <summary> Py-Webserver/ --> pywebserver.py  </summary>
  
    # pywebserver.py
    # Author: Jesse Redford
    # Date: 5/5/2020
   
    import sys
    import io
    import cv2
    from flask import Flask
    from flask import render_template
    from flask import Response

    sys.path.append(r'C:\Users\Py-Webserver\templates') # Add templates folder to working directory
    
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
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')

    @app.route('/video_feed')
    def video_feed():
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

    if __name__ == "__main__":
        app.run(host = '127.0.0.1', port = 80, debug = False, threaded = True)
       
</details>

### Testing the current script
Once you have completed the steps above, open a your terminal, navagate to the project directory (Py-Webserver), and run the python script by typing python pywebserver.py.  You should the following output on the terminal window.

   	 * Running on http://127.0.0.1:80/

Copy and paste the http line into your webbrowser, you should see a webpage which includes your a live video stream.


### Making your app publicly accessible 

Although testing the script above allows us to view the webapp we created from our host devivce, the link http://127.0.0.1:80/ will not be accesible by other devices in or out of the host devices local network. If you want your app to only be avalible to devices which are connected to your local network, hit Ctrl+C in your terminal then go back to the pywebserver.py file and modify the last line 

      app.run(host = '127.0.0.1', port = 80, debug = False, threaded = True)
      
      to
      
      app.run(host = 'YOUR LOCAL MACHINES IP ADDRESS', port = 80, debug = False, threaded = True)
      
      
If you want to make your webapp avialibe to any device on any network we will need to use ngrok to host a public server.
To do this go to https://ngrok.com/ , download executable, and create an account.  Login to your account and find your authorization key it should look something like this -----------. Next open the ngrok.exe app and save your authorization token to configuration file as shown below.
    
    open cmd
    cd C:\Users\Jesse\Downloads\ngrok-stable-windows-amd64 # path to ngrok.exe 
    authtoken 'your authorization key'

Next run the python script pywebserver.py, open a seperate terminal and paste the following

   	 cd C:\Users\Jesse\Downloads\ngrok-stable-windows-amd64
   	 ngrok http 80 # This creates a tunnel for port 80 on your local machine

Esentailly what we are doing here forwarding the information from our localhost server to ngrok which allows us to bypass your networks firewalls and create a public hosted. After completeing the step above lets verify that a current tunnel is active by going to the link https://dashboard.ngrok.com/status/tunnels. You should see one or two URL links example(https://ef3c35a2.ngrok.io), click on one and your should be brought to your apps webpage. You can now use this link to access the webapp from any device. You can test to make sure this is working by turning on your phones wifi and copy-pasting the URL link above into your browser. 


### Troubleshooting and Closing Remarks
Note if you close/reset the ngrok application or python file and repeat the steps above the URL link provided by ngrok will change. Also if your your local host device is a windows desktop and you run into issues, you may need to set up a inbound and outbound rule by navagating to system settings --> windows security --> firewall & network protection --> advanced setttings. click on inbound rules then under actions select "new rule", set rule type to port then hit next, make sure rule applies to TCP and specific local ports 80, hit next and check allow the connection, hit next and check Domain, Private, Public, hit next then name the rule inbound-pythonport, hit finish and repeate the steps above for an outbound rule. 

    

# Handling http request with AJAX
If you want to run background process (functions in python) that are triggered by events such as clicking a button on your http page, the code below shows an example of how to do just that without refreshing page each time! To start create a new text document and paste in the html code below, save the document in your templates folder with the name json.html.


<details>
  <summary> Py-Webserver/templates --> json.html  </summary>

    <html>
    <head>
    <title>The jQuery Example</title>
    <h2>jQuery-AJAX in FLASK. Execute function on button click</h2>  
  
	  <!-- Create http handler for click button event to run python background process without refreshing page  -->
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"> </script>

	  <script type=text/javascript> $(function() { $("#testbutton").click(function (event) { $.getJSON('/SomeFunction', { },function(data) { }); return false; }); }); </script>
	  <script type=text/javascript> $(function() { $("#upbutton").click(function (event) { $.getJSON('/upbutton', { },function(data) { }); return false; }); }); </script>
	  <script type=text/javascript> $(function() { $("#downbutton").click(function (event) { $.getJSON('/downbutton', { },function(data) { }); return false; }); }); </script> 

    </head>
    <body>        
    
	  <!-- make sure that the button id matches the $("#testbutton") ^^ defined above   -->
    <input type = "button" id = "testbutton" value = "test button Click Here" />
    <input type = "button" id = "upbutton" value = "up button" />
	  <input type = "button" id = "downbutton" value = "down button" />

    </body>    
    </html>
</details>

Next, create a new python3 file, insert the code below, save it with the name webtest.py, run it, then copy and paste the http address that gets displayed in your terminal into your browser.


<details>
  <summary> Py-Webserver/ --> webtest.py  </summary>

    from flask import Flask, render_template 

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('json.html')

    @app.route('/SomeFunction')
    def SomeFunction():
        print('you clicked test button, running somefunction')
        return "Nothing"

    @app.route('/upbutton')
    def upbutton():
        print('you pressed up')
        return "Nothing"

    @app.route('/downbutton')
    def downbutton():
        print('you pressed down')
        return "Nothing"

    if __name__ == '__main__':
        app.run(host='192.168.1.249',port=5002,debug=False, threaded= True)
    
</details>

If everything is working correctly your http page should look like this.

![http page example](https://github.com/Jesse-Redford/Py-Webserver/blob/master/JQuery-AJAX%20in%20FLASK.PNG?raw=true)

Now observer your python terminal while clicking the three buttons we created on the webpage, you should observe the following.

   - test button Click Here ---> terminal --> you clicked test button, running somefunction
   - up button -----> terminal -----> you pressed up
   - down button ----> terminal ----> you pressed down


### Putting it all together
The goal of this project was to create a home monitoring application where you can access a live video stream (from rasberry pi) on any device with an internet connection and be able to modify the position of the camera by controlling the servos connected to the pi  directly from the http site in real time. I also included a dashboard which displays the current temperature, humidity, and brightness of the room. I integrated OpenCVs face_recognition to have the host device automatically start recording the video stream when faces are detected. 

- Hardware Requirments
	- Rasberry Pi
	- USB webcam
	- adafruit 16channel servo hat
	- servo tilt 
	- 2 mg90 servos


<details>
  <summary> Py-Webserver/ --> websurveillance.py  </summary>
    
</details>



