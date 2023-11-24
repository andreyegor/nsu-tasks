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


# TODO Запихать в класс Node и объеденить его с Expression


class Node:
    db_name = None

    def __init__(self, tokens, db_name=None):
        if db_name:
            __class__.db_name = db_name
        self.tokens = tokens
        self.nodes = []
        self.action = []

    def create_graph(self):
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
                    nd.create_graph()
                    self.action.append(nd)
                    left = -1
                else:
                    self.action.append(token)

    # TODO в целом экспресшн не особо нужен как класс тут внутри нужно просто втупую идти и если нода то её компилить а иначе вручную по строке
    def compile(self):
        self.action
        for i in range(len(self.action)):
            if type(self.action[i]) == Node:
                self.action[i] = self.action[i].compile()
        commands = {
            "is": is_constructor,
            "in": in_constructor,
            "contains": contains_constructor,
        }
        logicals = {"and": and_constructor, "or": or_constructor}
        self.replace_bin_op(commands)
        self.replace_bin_op(logicals)

        if self.action == ["get", "records"]:
            self.action = [self.walk(lambda x: True)]
        if len(self.action) > 3 and self.action[:3] == ["get", "records", "where"]:
            self.action = [self.walk(self.action[3])]
        return self.action[0]

    def replace_bin_op(self, keywords):
        i = 0
        while i < len(self.action):
            if self.action[i] in keywords:
                self.action[i] = keywords[self.action[i]](
                    self.action[i - 1], self.action[i + 1]
                )
                del self.action[i + 1]
                del self.action[i - 1]
            i += 1

    def walk(self, function):
        with open(__class__.db_name, "r", encoding="utf-8") as db:
            while line := db.readline():
                for cls in (Student, Teacher, AssistantStudent):
                    try:
                        if function(cls.create_from_json(line)):
                            yield cls.create_from_json(line)
                    except ValueError:
                        continue
                    break
                else:
                    yield None
