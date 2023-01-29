from flask import Flask, request, render_template
import json

app = Flask(__name__)


@app.route('/')
def home():
    title = "Stocker - Track and predict stock movement"
    return render_template('index.html', title=title)


@app.route('/test', methods=['POST', 'GET'])
def test():
    output = request.get_json()

    result = json.loads(output)

    return result


@app.route('/results', methods=['POST', 'GET'])
def results():
    t = "STONKS"

    result = request.form
    print()
    print(result)
    print()
    return render_template('results.html', title=t, result=result)


@app.route('/home')
def back():
    title = "Stocker - Track and predict stock movement"
    return render_template('index.html', title=title)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
