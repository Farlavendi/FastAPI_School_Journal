from api.models import Student


def create_student(student: Student):
    user = student.model_dump()
    return {"success": True, "user": user}


def read_student(student: Student):
    return student


def update_student(student: Student):
    return student


def delete_student(student: Student):
    return student
