from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Flask!'


if __name__ == '__main__':
    app.run()

# if __name__ == '__main__':
#     env = resolveJson("config.json")
#     database = env["database"]
