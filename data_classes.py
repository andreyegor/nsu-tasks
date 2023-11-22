import json
from typing import Self


class Person:
    FIELDS = ("name", "birthday", "id")

    def __init__(self, name: str, birthday: str, id: int) -> None:
        self.name = name
        self.birthday = birthday
        self.id = id

    @classmethod
    def create_from_json(cls, line: str) -> Self:
        loaded = json.loads(line)
        if type(loaded) != dict:
            raise ValueError
        kwargs = {}
        for field, value in loaded.items():
            if field not in cls.FIELDS:  # TODO заглушка
                raise ValueError
            kwargs[field] = value
        return cls(**kwargs)

    def to_json(self) -> str:
        return json.dumps({field: getattr(self, field) for field in self.FIELDS})

    def __hash__(self) -> int:
        hash(self.id)

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id


class Student(Person):
    FIELDS = Person.FIELDS + ("department", "group", "student_id")

    def __init__(
        self, name: str, birthday: str, id: int, department, group, student_id
    ) -> None:
        Person.__init__(self, name, birthday, id)
        self.department = department
        self.group = group
        self.student_id = student_id

    def __str__(self) -> str:
        return f"Student {self.name} from group {self.group}, {self.department}"


class Teacher(Person):
    FIELDS = Person.FIELDS + ("course", "groups", "students")

    def __init__(
        self, name: str, birthday: str, id: int, course, groups, students
    ) -> None:
        Person.__init__(self, name, birthday, id)
        self.course = course
        self.groups = groups
        self.students = students

    def __str__(self) -> str:
        return f"Teacher {self.name} on course {self.course}. Works with {len(self.groups)} groups and {len(self.students)} students."


class AssistantStudent(Student, Teacher):
    FIELDS = Student.FIELDS + tuple(
        filter(lambda f: f not in Student.FIELDS, Teacher.FIELDS)
    )

    def __init__(
        self,
        name: str,
        birthday: str,
        id: int,
        department,
        group,
        student_id,
        course,
        groups,
        students,
    ) -> None:
        Student.__init__(self, name, birthday, id, department, group, student_id)
        Teacher.__init__(self, name, birthday, id, course, groups, students)

    def __str__(self) -> str:
        return f"Student {self.name} from group {self.group}, {self.department}. Also teaches {self.course} in {len(self.groups)} groups and mentors {len(self.students)} students."
