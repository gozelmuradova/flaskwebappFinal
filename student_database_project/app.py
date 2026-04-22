# app.py
# Gozel Muradova - Flask routes, template rendering, form handling

from flask import Flask, render_template, request, redirect, url_for
import db

app = Flask(__name__)

db.initialize_db()

# M will uncomment these wlater hen api/api.py is ready
# from flask_cors import CORS
# from API.api import api_blueprint
# CORS(app)
# app.register_blueprint(api_blueprint, url_prefix='/api')


# Flask Web Application Routes
# Gozel - server-side routes that render HTML templates

@app.route('/')
def index():
    # Fetch all students and pass them to the template
    students = db.get_all_students()
    return render_template('index.html', students=students)


@app.route('/create', methods=['POST'])
def create():
    first_name     = request.form.get('first_name', '').strip()
    last_name      = request.form.get('last_name', '').strip()
    email          = request.form.get('email', '').strip()
    major          = request.form.get('major', '').strip()
    classification = request.form.get('classification', '').strip()

    if first_name and last_name and email and major and classification:
        db.create_student(first_name, last_name, email, major, classification)

    return redirect(url_for('index'))


@app.route('/view', methods=['GET'])
def view_one():
    student_id = request.args.get('student_id', '').strip()
    student    = None
    error      = None

    if student_id:
        try:
            student = db.get_student_by_id(int(student_id))
            if student is None:
                error = f"No student found with ID {student_id}."
        except ValueError:
            error = "Please enter a valid numeric ID."

    students = db.get_all_students()
    return render_template('index.html', students=students,
                           viewed_student=student, view_error=error,
                           view_id=student_id)


@app.route('/update', methods=['POST'])
def update():
    student_id     = request.form.get('student_id', '').strip()
    first_name     = request.form.get('first_name', '').strip()
    last_name      = request.form.get('last_name', '').strip()
    email          = request.form.get('email', '').strip()
    major          = request.form.get('major', '').strip()
    classification = request.form.get('classification', '').strip()

    if student_id and first_name and last_name and email and major and classification:
        try:
            db.update_student(int(student_id), first_name, last_name,
                              email, major, classification)
        except ValueError:
            pass

    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete():
    student_id = request.form.get('student_id', '').strip()
    if student_id:
        try:
            db.delete_student(int(student_id))
        except ValueError:
            pass

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)