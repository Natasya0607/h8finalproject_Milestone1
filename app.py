from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class StudentModel(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    age = db.Column(db.Integer)
    class_name = db.Column(db.String())

def create_table():
    with app.app_context():
        db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        class_name = request.form['class_name']

        new_student = StudentModel(
            name=name,
            email=email,
            age=age,
            class_name=class_name
        )
        db.session.add(new_student)
        db.session.commit()

        return redirect('/submit')

    return render_template('register.html')

@app.route('/submit')
def submit():
    students = StudentModel.query.all()
    return render_template('submit.html', students=students)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
