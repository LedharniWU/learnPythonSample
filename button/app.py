from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return "nothing"

app.run(port=8000, debug=True)