from flask import Flask, request, render_template, Response, jsonify
from werkzeug.utils import secure_filename
import os

import base64
import uuid
import zmq
import time

import cv2

# Define a flask app
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# video = cv2.VideoCapture("Flask-Server-Folder/vedio/video1.mp4")
# video = cv2.VideoCapture("Flask-Server-Folder/vedio/sample1.mp4")
# video = cv2.VideoCapture(0)
video = cv2.VideoCapture("Flask-Server-Folder/vedio/video2.mp4")


@app.route("/predict", methods=["POST"])
def get_predictions():
    if request.json["start"] == "True":

        iter_ = 1

        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        _rid = "{}".format(str(uuid.uuid4()))
        socket.setsockopt_string(zmq.IDENTITY, _rid)
        socket.connect("tcp://localhost:5576")
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)

        while True:
            start_time = time.time()

            success, frame = video.read()
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if not success:
                break

            cv2.imshow("output", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            # if cv2.waitKey(1) == ord("q"):
            #     break

            _, img_encode = cv2.imencode(".jpg", frame)
            img_str = base64.b64encode(img_encode).decode("utf-8")

            obj = socket.send_json({"payload": img_str, "_rid": _rid})

            received_reply = False
            while not received_reply:
                sockets = dict(poll.poll(1000))
                if socket in sockets:
                    if sockets[socket] == zmq.POLLIN:
                        result_dict = socket.recv_json()
                        predictions = result_dict["preds"]
                        print(predictions)

                        received_reply = True
                        root = "Flask-Server-Folder"
                        txt_file_path = os.path.join(root, "results.txt")
                        with open(txt_file_path, "a+") as op_file:
                            op_file.writelines(predictions + "\n")

                        iter_ += 1
                        end_time = time.time()
                        time_diff = end_time - start_time
                        print(f"time taken : {time_diff} \n")

            # print("inner while closed")

        # socket.close()
        # context.term()

        video.release()
        # cv2.waitKey(0)
        cv2.destroyAllWindows()
        return jsonify("completed")


@app.route("/uploader", methods=["POST"])
def upload_file():
    predictions = ""

    if request.method == "POST":
        f = request.files["file"]

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, "static", "uploads", secure_filename(f.filename)
        )
        f.save(file_path)

        global img_str
        with open(file_path, "rb") as image_file:
            img_str = base64.b64encode(image_file.read()).decode("utf-8")

            # img_str = base64.b64encode(image_file.read())
            # print(img_str)

        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        _rid = "{}".format(str(uuid.uuid4()))
        socket.setsockopt_string(zmq.IDENTITY, _rid)
        socket.connect("tcp://localhost:5576")
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        obj = socket.send_json({"payload": img_str, "_rid": _rid})

        received_reply = False
        while not received_reply:
            sockets = dict(poll.poll(1000))
            if socket in sockets:
                if sockets[socket] == zmq.POLLIN:
                    result_dict = socket.recv_json()
                    predictions = result_dict["preds"]

                    received_reply = True
                    root = "Flask-Server-Folder"
                    txt_file_path = os.path.join(root, "results.txt")
                    with open(txt_file_path, "a+") as op_file:
                        op_file.writelines(predictions + "\n")

                    return render_template(
                        "upload.html", predictions=predictions, display_image=f.filename
                    )

        socket.close()
        context.term()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port="4114")
