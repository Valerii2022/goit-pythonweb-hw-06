from sqlalchemy.orm import Session
from models import SessionLocal, Student, Subject, Grade, Teacher, Group

def select_1():
    session = SessionLocal()
    result = session.query(Student.name, (SessionLocal.query(Grade.grade).filter(Grade.student_id == Student.id).label("avg_grade"))).order_by("avg_grade desc").limit(5).all()
    session.close()
    return result

def select_2(subject_name):
    session = SessionLocal()
    result = session.query(Student.name, (SessionLocal.query(Grade.grade).filter(Grade.subject_id == Subject.id).label("avg_grade"))).join(Subject).filter(Subject.name == subject_name).order_by("avg_grade desc").first()
    session.close()
    return result
