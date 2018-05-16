from flask import Flask, render_template, flash, redirect, url_for
import data
from wtforms import Form, RadioField

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


class AnswerForm(Form):
    answer_1 = RadioField
    answer_2 = RadioField
    answer_3 = RadioField
    answer_4 = RadioField
    answer_5 = RadioField


if __name__ == '__main__':
    app.run(debug=True)
