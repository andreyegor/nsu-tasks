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


class Node:
    db_name = None
    variables = {}

    def __init__(self, tokens, db_name=None):
        if db_name:
            __class__.db_name = db_name
        self.tokens = tokens
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
        for i in range(len(self.action)):
            if type(self.action[i]) == Node:
                self.action[i] = self.action[i].compile()
            if (
                type(self.action[i]) == str
                and self.action[i].startswith("{")
                and self.action[i].endswith("}")
            ):
                self.action[i] = str_to_list_constructor(self.action[i])

        dot = {".": dot_func_constructor}
        commands = {
            "is": is_constructor,
            "in": in_constructor,
            "contains": contains_constructor,
        }
        logicals = {"and": and_constructor, "or": or_constructor}
        self.replace_bin_op(dot)
        self.replace_bin_op(commands)
        self.replace_bin_op(logicals)

        if self.action == ["get", "records"]:
            out = self.walk(lambda x: True)
        elif self.action[:2] == ["get", "records"] and len(self.action) > 3:
            if self.action[2] == "from":
                db_var = self.action[3]
                if len(self.action) > 5 and self.action[4] == "where":
                    out = self.walk(self.action[5], __class__.variables[db_var])
                else:
                    out = self.walk(lambda x: True, __class__.variables[db_var])
            elif self.action[:3] == ["get", "records", "where"]:
                out = self.walk(self.action[3])
        else:
            out = self.action[0]
                
        for i, e in enumerate(self.action):
            if e == "as":
                __class__.variables[self.action[i + 1]] = out
                out = lambda: []
        return out

    def replace_bin_op(self, keywords):
        i = 0
        touched = False
        while i < len(self.action):
            if self.action[i] in keywords:
                touched = i
                self.action[i] = keywords[self.action[i]](
                    self.action[i - 1], self.action[i + 1]
                )
                del self.action[i + 1]
                del self.action[i - 1]
            i += 1
        return touched

    def walk(self, function, from_variable=None):
        def fvinner():
            yield from filter(function, from_variable())

        def inner():
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

        return fvinner if from_variable else inner

    def tokenize(line):
        # TODO хлипенько
        tokens = [""]
        string = False
        arr = False
        for e in line:
            if e in "}{":
                if not (not arr and not tokens[-1]):
                    tokens.append("")
                arr = not arr
                tokens[-1 if e == "{" else -2] += e
            elif arr:
                tokens[-1] += e
            elif e == '"':
                if not (not string and not tokens[-1]):
                    tokens.append("")
                string = not string
            elif string:
                tokens[-1] += e
            elif e in "().":
                if tokens[-1]:
                    tokens.append(e)
                else:
                    tokens[-1] = e
                tokens.append("")
            elif e in " ":
                if tokens[-1]:
                    tokens.append("")
            else:
                tokens[-1] += e
        if tokens[-1] == "":
            del tokens[-1]
        return tokens
