from pydantic.json_schema import SkipJsonSchema

from src.api.api_v1.models.users import RoleEnum



def get_role(role: int):
    if role == student:
        redirect(create_student_func)
    elif role == teacher:
        redirect(teacher_create_func)

def create_student_func(UserCreate, StudentCreate):
    role: SkipJsonSchema(RoleEnum) == RoleEnum.STUDENT


def teacher_create_func(UserCreate, TeacherCreate):
    role: SkipJsonSchema(RoleEnum) == RoleEnum.STUDENT
