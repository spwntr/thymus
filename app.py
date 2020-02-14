from random import randint
from flask import Flask, render_template
import data

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/questions')
def questions():
    return render_template('questions.html', questions=data.get_questions_as_dict())


@app.route('/question/<string:q_id>/')
def question(q_id):
    return render_template('question.html', question=data.get_question_by_id(q_id))


@app.route('/random')
def random():
    return render_template('question.html', question=data.get_question_by_id(randint(1, 427).__str__()))


if __name__ == '__main__':
    app.run(debug=True)
