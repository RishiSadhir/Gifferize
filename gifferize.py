
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("welcome.html")

@app.route('/display', methods=['GET', 'POST'])
def display():
    if request.method == 'POST':
        x = ""
        x += "link : " + request.form['link'] + " "  
        x += "start : " + request.form['start'] + " "
        x += "end : " + request.form['end']
        return x
    else:
        return "error!"


@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)
