import json
from dataclasses import dataclass, fields
from typing import Any

from constructors import *


@dataclass
class Person:
    name: str
    birthday: str
    id: int

    @classmethod
    def create_from_json(cls, line: str) -> Any:
        loaded = json.loads(line)
        if type(loaded) != dict:
            raise ValueError
        kwargs = {}
        for field, value in loaded.items():
            if field not in (field.name for field in fields(cls)):
                raise ValueError("Нет такого поля")
            kwargs[field] = value
        return cls(**kwargs)

    def to_json(self) -> str:
        return json.dumps(
            {
                field: getattr(self, field)
                for field in (field.name for field in fields(self))
            }
        )

    def __hash__(self) -> int:
        hash(self.id)

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id


@dataclass
class Student(Person):
    department: int
    group: int
    student_id: int

    def __str__(self) -> str:
        return f"Student {self.name} from group {self.group}, {self.department}"


@dataclass
class Teacher(Person):
    course: int
    groups: list
    students: list

    def __str__(self) -> str:
        return f"Teacher {self.name} on course {self.course}. Works with {len(self.groups)} groups and {len(self.students)} students."


@dataclass
class AssistantStudent(Student, Teacher):
    def __str__(self) -> str:
        return f"Student {self.name} from group {self.group}, {self.department}. Also teaches {self.course} in {len(self.groups)} groups and mentors {len(self.students)} students."
