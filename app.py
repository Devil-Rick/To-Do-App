from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

# creating the database uri (using SQL Lite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ToDoList.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# creating the database
data = SQLAlchemy(app)

# creating the schema using classes


class ToDo(data.Model):
    sno = data.Column(data.Integer, primary_key=True)
    title = data.Column(data.String(200), nullable=False)
    desc = data.Column(data.String(500), nullable=False)
    date = data.Column(data.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo = ToDo(title=request.form['title'], desc=request.form['desc'])
        data.session.add(todo)
        data.session.commit()
    works = ToDo.query.all()
    return render_template('index.html', work=works)


@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        toUpd = ToDo.query.filter_by(sno=sno).first()
        toUpd.title = request.form['title']
        toUpd.desc = request.form['desc']
        data.session.add(toUpd)
        data.session.commit()
        return redirect('/')

    toUpd = ToDo.query.filter_by(sno=sno).first()

    return render_template('update.html', todo=toUpd)


@app.route('/delete/<int:sno>')
def delete(sno):
    toDel = ToDo.query.filter_by(sno=sno).first()
    data.session.delete(toDel)
    data.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
