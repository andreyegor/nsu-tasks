import io
import sys
from typing import TextIO

import db_classes
from db_request import Database


def solution(requests: TextIO, db_name: str, output: TextIO) -> None:
    db = Database(
        db_name, [db_classes.Student, db_classes.Teacher, db_classes.AssistantStudent]
    )
    for request in requests:
        if request.endswith("\n"):
            request = request[:-1]
        for out in db.request(request):
            output.write(str(out) + "\n")


debug_input = (
    """get records where (department is "ММФ" or group is 19301)""".splitlines()
)
debug = 0
if __name__ == "__main__":
    if debug:
        solution(debug_input, "db.txt", sys.stdout)
    print("$ ", end="")
    for line in sys.stdin:
        solution(io.StringIO(line.strip()), "db.txt", sys.stdout)
        print("$ ", end="")
