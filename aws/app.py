from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect, session, jsonify
# from flask_sqlalchemy import SQLAlchemy
import database as db

app = Flask(__name__)
app.secret_key = '12345'
client = db.establish_connection()
client = db.initialize_db(client)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key= True)
#     content = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)
#
#     def __repr__(self):
#         return '<Course %r>' % self.id
#
# with app.app_context():
#     db.create_all()


@app.route('/login/',  methods=['POST','GET'])
def login():
    student = {'id': '', 'name': ""}
    if request.method == 'POST':
        student['name'] = request.form['name']
        student['id'] = request.form['id']
        if not db.is_iterator_empty(db.is_student(client, student['id'], student['name'])):
            session['student'] = student
            return redirect('/home/')
        else:
            session['student'] = student
            return redirect('/register')
    else:
        return render_template('login.html', student=student)



@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if db.is_iterator_empty(db.is_student_id(client, session['student']['id'])):
            if db.is_successful(db.create_student(client, session['student']['id'], session['student']['name'])):
                return redirect('/home/')
            else:
                return "AN ERROR OCCURS!"
        else:
            return register()
            # return render_template("register.html", exist=True, student=session['student'])
    else:
        return render_template('register.html', exist=False, student=session['student'])


@app.route('/', methods=['GET'])
def index():
    return redirect('/login/')
    # return render_template('test.html')

# @app.route('/yes')
# def agree():
#     return render_template('test1.html')

@app.route('/home/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        course_code = request.form['content']
        result = db.direct_enroll_student_into_course(client, course_code, session['student']['id'])
        if db.is_successful(result):
            return redirect('/home/')
        else:
            return 'There is an issue' # Todo
    else:
        course_result = db.student_select_course(client, session['student']['id'])
        courses = db.display_course(course_result)
        print("****"*10)
        print(courses)
        print(session['student'])
        return render_template('home.html', courses=courses, student=session['student'])

@app.errorhandler(404)
def page_not_found(error):
    return 'Sorry, the requested page could not be found.', 404


@app.route('/delete/<int:id>')
def delete(id):
    if  not db.is_iterator_empty(db.if_students_in_course(client, id, session['student']['id'])):
        db.delete_student_in_course(client,id, session['student']['id'])
        return redirect('/home')
    else:
        return 'There is a problem in the deleting that task'


# @app.route('/update/<int:id>', methods=['GET','POST'])
# def update(id):
#     new_course_id
#     course_to_update = db.display_course(db.if_students_in_course(client, id, session['student']['id']))
#     if request.method =='POST':
#          course_to_update.content = request.form['content']
#          try:
#              db.session.commit()
#              return redirect('/home')
#          except:
#              return 'There is an error of updating'
#     else:
#         if len(course_to_update) > 0:
#             return render_template('update.html', course=course_to_update)
#         else:
#             return 'There is no course for the student'

@app.route('/api/info', methods=['GET'])
def info():
    if request.method == 'GET':
        return jsonify(db.get_course_info(client)) 

@app.route('/api/add/<int:sid>/<int:cid>')
def add(sid, cid):
    result = db.direct_enroll_student_into_course(client, cid, sid)
    if db.is_successful(result):
        return jsonify({'message': 'Request successful'}), 200
    else:
        return jsonify({'message': 'Bad request'}), 400

@app.route('/api/remove/<int:sid>/<int:cid>')
def remove(sid, cid):
    if  not db.is_iterator_empty(db.if_students_in_course(client, cid, sid)):
        db.delete_student_in_course(client,cid, sid)
        return jsonify({'message': 'Request successful'}), 200
    else:
        return jsonify({'message': 'Bad request'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

