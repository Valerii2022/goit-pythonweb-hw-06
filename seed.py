import random
from datetime import datetime
from faker import Faker
from sqlalchemy.orm import Session
from models import SessionLocal, Student, Group, Teacher, Subject, Grade

fake = Faker()

def seed_database():
    session = SessionLocal()

    groups = [Group(name=f"Group {i+1}") for i in range(3)]
    session.add_all(groups)
    session.commit()

    teachers = [Teacher(name=fake.name()) for _ in range(4)]
    session.add_all(teachers)
    session.commit()

    subjects = [Subject(name=fake.word(), teacher=random.choice(teachers)) for _ in range(6)]
    session.add_all(subjects)
    session.commit()

    students = [Student(name=fake.name(), group=random.choice(groups)) for _ in range(40)]
    session.add_all(students)
    session.commit()

    for student in students:
        for subject in subjects:
            for _ in range(random.randint(10, 20)):
                grade = Grade(
                    student=student,
                    subject=subject,
                    grade=random.uniform(2.0, 5.0),
                    date_received=fake.date_this_year()
                )
                session.add(grade)

    session.commit()
    session.close()

if __name__ == "__main__":
    seed_database()
