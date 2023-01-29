from flask import Flask, request, render_template
import json

app = Flask(__name__)


@app.route('/')
def home():
    title = "Stocker - Track and predict stock movement"
    return render_template('index.html', title=title)


@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()

    result = json.loads(output)

    print(result)

    print(type(result))

    return result


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
