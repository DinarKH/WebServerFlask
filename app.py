from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    posts = [
        'test',
        'test2',
    ]
    return render_template('home.html', posts=posts)


@app.route('/about/')
def about():
    return 'About page'


if __name__ == '__main__':
    app.run(debug=True)
