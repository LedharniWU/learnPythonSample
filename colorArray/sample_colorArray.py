from flask import Flask, render_template
import numpy as np
import cv2

app = Flask(__name__)

@app.route("/")
def index():

    list = [[[0,63,127],[63,200,0],[255,0,127]],[[0,63,127],[63,127,0],[255,0,127]]]
    #データ保存箇所
    img_gray = np.array(list,dtype = np.uint8)
 
    cv2.imwrite('static/img/img_gray.jpg', img_gray)

    ctx = {}

    return render_template("index.html", ctx=ctx)

app.run(port=8000, debug=True)

