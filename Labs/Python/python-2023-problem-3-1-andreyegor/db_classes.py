import json
from dataclasses import dataclass, fields
from typing import Any


@dataclass
class Person:
    name: str
    birthday: str
    id: int

    @classmethod
    def create_from_json(cls, line: str) -> Any:
        loaded = json.loads(line)
        if type(loaded) != dict:
            raise ValueError("Строка не является обьектом JSON")
        kwargs = {}
        for field, value in loaded.items():
            if (field, type(value)) not in ((field.name, field.type) for field in fields(cls)):
                raise ValueError(f"Не существует поля {field} или оно не хранит этот тип данных")
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
        return hash(self.id)

    def __eq__(self, value: object) -> bool:
        return type(self) == type(value) and self.id == value.id


@dataclass
class Student(Person):
    department: str
    group: int
    student_id: int

    def __str__(self) -> str:
        return f"Student {self.name} from group {self.group}, {self.department}"


@dataclass
class Teacher(Person):
    course: str
    groups: list
    students: list

    def __str__(self) -> str:
        return f"Teacher {self.name} on course {self.course}. Works with {len(self.groups)} groups and {len(self.students)} students."


@dataclass
class AssistantStudent(Student, Teacher):
    def __str__(self) -> str:
        return f"{super().__str__()}. Also teaches {self.course} in {len(self.groups)} groups and mentors {len(self.students)} students."
