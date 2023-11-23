import json
from typing import Any

from constructors import *


class Person:
    FIELDS = ("name", "birthday", "id")

    def __init__(self, name: str, birthday: str, id: int) -> None:
        self.name = name
        self.birthday = birthday
        self.id = id

    @classmethod
    def create_from_json(cls, line: str) -> Any:
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

#TODO Запихать в класс Node и объеденить его с Expression
def walk(db_name: str) -> any([Student, Teacher, AssistantStudent, None]):
    with open(db_name, "r", encoding="utf-8") as db:
        while line := db.readline():
            for cls in (Student, Teacher, AssistantStudent):
                try:
                    yield cls.create_from_json(line)
                except ValueError:
                    continue
                break
            else:
                yield None

class Expression:
    def __init__(self, tokens = []) -> None:
        self.tokens = tokens

    def append(self, token: str) -> None:
        self.tokens.append(token)

    def calculate(self, db_name) -> Callable:
        if len(self.tokens) == 0:
            print("НОЛЬ ТОКЕОНВ?")
            return ""
        if len(self.tokens) == 1:
            return self.tokens[0]
        if len(self.tokens) == 3:
            left, command, right = self.tokens
            commands = {
                "is": is_constructor,
                "in": in_constructor,
                "contains": contains_constructor,
            }
            assert command in commands
            return commands[command](left, right)
        if self.tokens[0:4] == ["get", "records", "where"]:
            def inner():
                ...
                

class Node:
    def __init__(self, tokens):
        self.tokens = tokens
        self.nodes = []
        self.do = []

    def create_graph(self, db_name):
        cnt = 0
        left = -1
        for i, token in enumerate(self.tokens):
            if token == "(":
                if not cnt:
                    left = i
                cnt += 1
            elif token == ")":
                cnt -= 1
            if cnt == 0:
                if left != -1:
                    nd = Node(self.tokens[left + 1 : i])
                    nd.create_graph(db_name)
                    self.do.append(nd.calculate(db_name))
                    self.nodes.append(nd)
                    left = -1
                else:
                    if not self.do or type(self.do[-1]) != Expression:
                        self.do.append(Expression())
                    self.do[-1].append(token)

    def calculate(self, db_name):
        tokens = []
        for e in self.do:
            if type(e) != str:
                tokens.append(e.calculate(db_name))
        return Expression(tokens).calculate(db_name)
        
        
        
            
