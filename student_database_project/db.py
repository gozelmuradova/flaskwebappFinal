import sqlite3


def get_db_connection():
    connection = sqlite3.connect('students.db')
    connection.row_factory = sqlite3.Row
    return connection

def initialize_db():
    connection = get_db_connection()

    with open('schema.sql', 'r') as schema_file:
        schema = schema_file.read()
        connection.executescript(schema)

    connection.commit()
    connection.close()


def get_all_students():
    connection = get_db_connection()

    students = connection.execute(
        'SELECT * FROM students ORDER BY last_name, first_name'
    ).fetchall()

    connection.close()
    return students


def get_student_by_id(student_id):
    connection = get_db_connection()

    student = connection.execute(
        'SELECT * FROM students WHERE id = ?',
        (student_id,)
    ).fetchone()

    connection.close()
    return student


def create_student(first_name, last_name, email, major, classification):
    connection = get_db_connection()

    connection.execute(
        '''
        INSERT INTO students (first_name, last_name, email, major, classification)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (first_name, last_name, email, major, classification)
    )

    connection.commit()
    connection.close()


def update_student(student_id, first_name, last_name, email, major, classification):
    connection = get_db_connection()

    connection.execute(
        '''
        UPDATE students
        SET first_name = ?, last_name = ?, email = ?, major = ?, classification = ?
        WHERE id = ?
        ''',
        (first_name, last_name, email, major, classification, student_id)
    )

    connection.commit()
    connection.close()


def delete_student(student_id):
    connection = get_db_connection()

    connection.execute(
        'DELETE FROM students WHERE id = ?',
        (student_id,)
    )

    connection.commit()
    connection.close()