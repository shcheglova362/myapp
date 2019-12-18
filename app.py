from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)
    education = db.Column(db.Text)
    age = db.Column(db.Integer)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)


@app.route('/')
def question_page():
    questions = Questions.query.all()
    return render_template(
        'questions.html',
        questions=questions
    )


@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('question_page'))
    gender = request.args.get('gender')
    education = request.args.get('education')
    age = request.args.get('age')
    user = User(
        age=age,
        gender=gender,
        education=education
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    q3 = request.args.get('q3')
    q4 = request.args.get('q4')
    q5 = request.args.get('q5')
    answer = Answers(id=user.id, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5)
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('stats'))


@app.route('/stats')
def stats():
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age)
    ).one()
    all_info['age_av'] = age_stats[0]
    all_info['total_count'] = User.query.count()
    all_info['part'] = db.session.query(func.max(Answers.id)).one()[0]
    all_info['q1_mean'] = db.session.query(func.avg(Answers.q1)).one()[0]
    all_info['q2_mean'] = db.session.query(func.avg(Answers.q2)).one()[0]
    all_info['q3_mean'] = db.session.query(func.avg(Answers.q3)).one()[0]
    all_info['q4_mean'] = db.session.query(func.avg(Answers.q4)).one()[0]
    all_info['q5_mean'] = db.session.query(func.avg(Answers.q5)).one()[0]
    labels = [
        'Ответ 1', 'Ответ 2', 'Ответ 3', 'Ответ 4',
        'Ответ 5'
    ]

    values = [all_info['q1_mean'], all_info['q2_mean'], all_info['q3_mean'],
              all_info['q4_mean'], all_info['q5_mean']]
    return render_template('results.html', labels=labels, values=values, all_info=all_info)
    # return render_template('results.html', all_info=all_info)


if __name__ == '__main__':
    app.run()
