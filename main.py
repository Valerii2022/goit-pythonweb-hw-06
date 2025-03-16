import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Teacher, Group, Student, Subject, Grade, Base
from datetime import datetime

engine = create_engine("postgresql://postgres:secret@localhost:5432/postgres")
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--action", choices=["create", "list", "update", "remove"], required=True)
parser.add_argument("-m", "--model", choices=["Teacher", "Group", "Student", "Subject", "Grade"], required=True)
parser.add_argument("-n", "--name", help="Name", required=False)
parser.add_argument("--id", type=int, help="ID", required=False)
parser.add_argument("--group_id", type=int, help="Group ID", required=False)
parser.add_argument("--teacher_id", type=int, help="Teacher ID", required=False)
parser.add_argument("--subject_id", type=int, help="Subject ID", required=False)
parser.add_argument("--value", type=int, help="Grade value", required=False)
parser.add_argument("--date_received", type=str, help="Grade date (YYYY-MM-DD)", required=False)

args = parser.parse_args()
session = SessionLocal()

def perform_action():
    if args.model == "Teacher":
        if args.action == "create":
            if not args.name:
                print("Error: Name is required to create a Teacher.")
                return
            teacher = Teacher(name=args.name)
            session.add(teacher)
            session.commit()
            print(f"Teacher {args.name} created with ID {teacher.id}.")

        elif args.action == "list":
            teachers = session.query(Teacher).all()
            if teachers:
                print("Teachers List:")
                for t in teachers:
                    print(f"{t.id}: {t.name}")
            else:
                print("No teachers found.")

        elif args.action == "update":
            if not args.id or not args.name:
                print("Error: ID and Name are required to update a Teacher.")
                return
            teacher = session.query(Teacher).get(args.id)
            if teacher:
                teacher.name = args.name
                session.commit()
                print(f"Teacher ID {args.id} updated to {args.name}.")
            else:
                print(f"Teacher with ID {args.id} not found.")

        elif args.action == "remove":
            if not args.id:
                print("Error: ID is required to remove a Teacher.")
                return
            teacher = session.query(Teacher).get(args.id)
            if teacher:
                session.delete(teacher)
                session.commit()
                print(f"Teacher ID {args.id} removed.")
            else:
                print(f"Teacher with ID {args.id} not found.")

    elif args.model == "Group":
        if args.action == "create":
            if not args.name:
                print("Error: Name is required to create a Group.")
                return
            group = Group(name=args.name)
            session.add(group)
            session.commit()
            print(f"Group {args.name} created with ID {group.id}.")

        elif args.action == "list":
            groups = session.query(Group).all()
            if groups:
                print("Groups List:")
                for g in groups:
                    print(f"{g.id}: {g.name}")
            else:
                print("No groups found.")

        elif args.action == "update":
            if not args.id or not args.name:
                print("Error: ID and Name are required to update a Group.")
                return
            group = session.query(Group).get(args.id)
            if group:
                group.name = args.name
                session.commit()
                print(f"Group ID {args.id} updated to {args.name}.")
            else:
                print(f"Group with ID {args.id} not found.")

        elif args.action == "remove":
            if not args.id:
                print("Error: ID is required to remove a Group.")
                return
            group = session.query(Group).get(args.id)
            if group:
                session.delete(group)
                session.commit()
                print(f"Group ID {args.id} removed.")
            else:
                print(f"Group with ID {args.id} not found.")

    elif args.model == "Student":
        if args.action == "create":
            if not args.name or not args.group_id:
                print("Error: Name and Group ID are required to create a Student.")
                return
            student = Student(name=args.name, group_id=args.group_id)
            session.add(student)
            session.commit()
            print(f"Student {args.name} created with ID {student.id}.")

        elif args.action == "list":
            students = session.query(Student).all()
            if students:
                print("Students List:")
                for s in students:
                    print(f"{s.id}: {s.name}, Group: {s.group.name}")
            else:
                print("No students found.")

        elif args.action == "update":
            if not args.id or not args.name or not args.group_id:
                print("Error: ID, Name, and Group ID are required to update a Student.")
                return
            student = session.query(Student).get(args.id)
            if student:
                student.name = args.name
                student.group_id = args.group_id
                session.commit()
                print(f"Student ID {args.id} updated to {args.name}.")
            else:
                print(f"Student with ID {args.id} not found.")

        elif args.action == "remove":
            if not args.id:
                print("Error: ID is required to remove a Student.")
                return
            student = session.query(Student).get(args.id)
            if student:
                session.delete(student)
                session.commit()
                print(f"Student ID {args.id} removed.")
            else:
                print(f"Student with ID {args.id} not found.")

    elif args.model == "Subject":
        if args.action == "create":
            if not args.name or not args.teacher_id:
                print("Error: Name and Teacher ID are required to create a Subject.")
                return
            subject = Subject(name=args.name, teacher_id=args.teacher_id)
            session.add(subject)
            session.commit()
            print(f"Subject {args.name} created with ID {subject.id}.")

        elif args.action == "list":
            subjects = session.query(Subject).all()
            if subjects:
                print("Subjects List:")
                for s in subjects:
                    print(f"{s.id}: {s.name}, Teacher: {s.teacher.name}")
            else:
                print("No subjects found.")

        elif args.action == "update":
            if not args.id or not args.name or not args.teacher_id:
                print("Error: ID, Name, and Teacher ID are required to update a Subject.")
                return
            subject = session.query(Subject).get(args.id)
            if subject:
                subject.name = args.name
                subject.teacher_id = args.teacher_id
                session.commit()
                print(f"Subject ID {args.id} updated to {args.name}.")
            else:
                print(f"Subject with ID {args.id} not found.")

        elif args.action == "remove":
            if not args.id:
                print("Error: ID is required to remove a Subject.")
                return
            subject = session.query(Subject).get(args.id)
            if subject:
                session.delete(subject)
                session.commit()
                print(f"Subject ID {args.id} removed.")
            else:
                print(f"Subject with ID {args.id} not found.")

    elif args.model == "Grade":
        if args.action == "create":
            if not args.student_id or not args.subject_id or not args.value or not args.date_received:
                print("Error: Student ID, Subject ID, Value, and Date are required to create a Grade.")
                return
            date_received = datetime.strptime(args.date_received, "%Y-%m-%d")
            grade = Grade(student_id=args.student_id, subject_id=args.subject_id, value=args.value, date_received=date_received)
            session.add(grade)
            session.commit()
            print(f"Grade created for Student ID {args.student_id}, Subject ID {args.subject_id} with value {args.value}.")

        elif args.action == "list":
            grades = session.query(Grade).all()
            if grades:
                print("Grades List:")
                for g in grades:
                    print(f"ID: {g.id}, Student: {g.student.name}, Subject: {g.subject.name}, Value: {g.value}, Date: {g.date_received}")
            else:
                print("No grades found.")

        elif args.action == "update":
            if not args.id or not args.value or not args.date_received:
                print("Error: ID, Value, and Date are required to update a Grade.")
                return
            date_received = datetime.strptime(args.date_received, "%Y-%m-%d")
            grade = session.query(Grade).get(args.id)
            if grade:
                grade.value = args.value
                grade.date_received = date_received
                session.commit()
                print(f"Grade ID {args.id} updated with value {args.value} and date {date_received}.")
            else:
                print(f"Grade with ID {args.id} not found.")

        elif args.action == "remove":
            if not args.id:
                print("Error: ID is required to remove a Grade.")
                return
            grade = session.query(Grade).get(args.id)
            if grade:
                session.delete(grade)
                session.commit()
                print(f"Grade ID {args.id} removed.")
            else:
                print(f"Grade with ID {args.id} not found.")

perform_action()

session.close()
