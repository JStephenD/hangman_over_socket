from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'hatdog'

if __name__ == '__main__':
    with open('text.txt', 'w') as f:
        for c in str(dir(app)).split(','):
            f.write(c+'\n')
    app.run(host='2001:4454:5f0:6d00:b515:388:85ac:cfe6', port=5050, debug=True)
# 2001:4454:5f0:6d00:7d19:a85b:a373:595f