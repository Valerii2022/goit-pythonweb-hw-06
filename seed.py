from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Group, Student, Teacher, Subject, Grade
import random, datetime

engine = create_engine("postgresql://postgres:secret@localhost:5432/postgres")
Session = sessionmaker(bind=engine)
session = Session()

faker = Faker()

# Заповнення груп
groups = [Group(name=f"Group {i+1}") for i in range(3)]
session.add_all(groups)
session.commit()

# Заповнення викладачів
teachers = [Teacher(name=faker.name()) for _ in range(4)]
session.add_all(teachers)
session.commit()

# Заповнення предметів
subjects = [Subject(name=faker.word(), teacher=random.choice(teachers)) for _ in range(6)]
session.add_all(subjects)
session.commit()

# Заповнення студентів
students = [Student(name=faker.name(), group=random.choice(groups)) for _ in range(40)]
session.add_all(students)
session.commit()

# Заповнення оцінок
for student in students:
    for subject in subjects:
        for _ in range(random.randint(10, 20)):
            grade = Grade(
                student=student,
                subject=subject,
                value=random.randint(1, 5),
                date_received=faker.date_this_decade()
            )
            session.add(grade)

session.commit()
session.close()
