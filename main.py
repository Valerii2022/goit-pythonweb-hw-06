import argparse
from models import SessionLocal, Teacher, Group

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--action", choices=["create", "list", "update", "remove"])
parser.add_argument("-m", "--model", choices=["Teacher", "Group"])
parser.add_argument("-n", "--name", help="Name")
parser.add_argument("--id", type=int, help="ID")

args = parser.parse_args()
session = SessionLocal()

if args.action == "create" and args.model == "Teacher":
    teacher = Teacher(name=args.name)
    session.add(teacher)
    session.commit()

elif args.action == "list" and args.model == "Teacher":
    teachers = session.query(Teacher).all()
    for t in teachers:
        print(f"{t.id}: {t.name}")

elif args.action == "update" and args.model == "Teacher":
    teacher = session.query(Teacher).get(args.id)
    teacher.name = args.name
    session.commit()

elif args.action == "remove" and args.model == "Teacher":
    teacher = session.query(Teacher).get(args.id)
    session.delete(teacher)
    session.commit()

session.close()
