from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import create_engine, func
from models import Student, Grade, Subject, Teacher, Group
from tabulate import tabulate

engine = create_engine("postgresql://postgres:secret@localhost:5432/postgres")
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    results = session.query(Student.name, func.round(func.avg(Grade.value), 2).label("avg_grade")) \
        .join(Grade) \
        .group_by(Student.id) \
        .order_by(func.avg(Grade.value).desc()) \
        .limit(5).all()
    return results

def select_2(subject_id):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    result = session.query(Student.name, func.round(func.avg(Grade.value), 2).label("avg_grade")) \
        .join(Grade) \
        .filter(Grade.subject_id == subject_id) \
        .group_by(Student.id) \
        .order_by(func.avg(Grade.value).desc()) \
        .first()
    return result

def select_3(subject_id):
    """Знайти середній бал у групах з певного предмета."""
    group_alias = aliased(Group)
    
    result = (
        session.query(
            group_alias.name.label("Група"),
            func.round(func.avg(Grade.value), 2).label("Середній бал")
        )
        .select_from(Grade)  
        .join(Student, Grade.student_id == Student.id)
        .join(group_alias, Student.group_id == group_alias.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(group_alias.id)
        .all()
    )
    
    return result

def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    result = session.query(func.round(func.avg(Grade.value), 2).label("avg_grade")).scalar()
    return result

def select_5(teacher_id):
    """Знайти які курси читає певний викладач."""
    results = session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
    return results

def select_6(group_id):
    """Знайти список студентів у певній групі."""
    results = session.query(Student.name).filter(Student.group_id == group_id).all()
    return results

def select_7(group_id, subject_id):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    results = session.query(Student.name, Grade.value) \
        .join(Grade) \
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id) \
        .all()
    return results

def select_8(teacher_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    result = session.query(func.round(func.avg(Grade.value), 2).label("avg_grade")) \
        .join(Subject) \
        .filter(Subject.teacher_id == teacher_id) \
        .scalar()
    return result

def select_9(student_id):
    """Знайти список курсів, які відвідує певний студент."""
    results = session.query(Subject.name).join(Grade).filter(Grade.student_id == student_id).distinct().all()
    return results

def select_10(student_id, teacher_id):
    """Список курсів, які певному студенту читає певний викладач."""
    results = session.query(Subject.name) \
        .join(Grade) \
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id) \
        .distinct().all()
    return results

# Тестування роботи функцій

def print_result(title, data, headers):
    """Форматує і друкує дані у вигляді таблиці."""
    print(f"\n{title}")
    print(tabulate(data, headers=headers, tablefmt="grid"))

# print_result("ТОП-5 студентів за середнім балом", select_1(), ["Студент", "Середній бал"])
# print_result("Студент із найвищим балом з предмета (ID=2)", [select_2(2)], ["Студент", "Середній бал"])
# print_result("Середній бал у групах по предмету (ID=3)", select_3(3), ["Група", "Середній бал"])
# print_result("Середній бал по всіх предметах", [[select_4()]], ["Середній бал"])
# print_result("Курси викладача (ID=4)", select_5(4), ["Курс"])
# print_result("Студенти групи (ID=2)", select_6(2), ["Студент"])
# print_result("Оцінки студентів у групі (ID=1) з предмета (ID=1)", select_7(1, 1), ["Студент", "Оцінка"])
# print_result("Середній бал викладача (ID=3)", [[select_8(3)]], ["Середній бал"])
# print_result("Курси студента (ID=10)", select_9(10), ["Курс"])
# print_result("Курси викладача (ID=4) для студента (ID=10)", select_10(10, 4), ["Курс"])

session.close()
