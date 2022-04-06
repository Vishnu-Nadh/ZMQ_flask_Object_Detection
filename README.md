# Improving Performance of Deep Learning Based Object Detection Flask App with ZMQ

This project focus on to improving the performance of deep learning based web app using Python Library ZeroMQ. The library will help transform the Genaral monolith programme of a flask application into two routes which can run parallaly. As an example resnet model is used here for object detection both from image and vedio, with which preparing the model will run though first route and will be kept ready for detection whenever input image is passed though other route, and There by improve the performance and speed of detection.

## Tech Stac

- **Client:** HTML, CSS

- **Server:** Python with libraries tensorflow, numpy, ZMQ, OpenCV, Pillow

- **API Framework:** Python Flask==2.0.3

## Run App Locally

To run the App locally exactly python version 3.6 should be installed in your computer

Clone the project

Go to the project directory you want to clone the project files

```bash
  cd your-project-directory
```

```bash
  git clone https://github.com/DATAHUB-AI/ZMQ-DIP.git
```

Install dependencies

Create a python environment using conda (preferably) in your project directory. Then install the dependencies as follows.

note : tensorflow 1.14.0 is required here which may not availabe with pip installer. Hence use conda installer.

```bash
  conda install -c conda-forge tensorflow=1.14
  pip install -r requirements.txt
```

Start the model server

```bash
    python Model-Server-Folder/resnet_model_server.py
```

The above server will be continously running (until it is force stopped) which will prepare the model for detection and will keep it ready to use.

Now select a new terminal window to run the flask server and run the following python file

```bash
    python Flask-Server-Folder/app.py
```

Press Enter and visit the app from local host url shown in the terminal. This url will lead to web application for object detection from image.

To run the object detection from vedio use postman or any other api testing software.
sent the json request from postman to the route "http://192.168.1.3:4114/predict" in the following format

{
"start": "True"
}

The detection results will be saved automatically to "Flask-Server-Folder/results.txt" file.

