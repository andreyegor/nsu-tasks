import os
import re
from difflib import unified_diff

RUN = "java -jar /home/mebeb/scripts/rars1_6.jar sm Asm/16.asm pa {file}"  # put here your run command
TEST_FOLDER_PATH = "Asm/16_tests"
TEST_POSTFIX = ".test"
EXPECTED_POSTFIX = ".expected"
ACTUAL_POSTFIX = ".test.sorted"


if __name__ == "__main__":
    tests = dict()
    for root, _, files in os.walk(TEST_FOLDER_PATH):
        for file in files:
            if re.match(".*" + TEST_POSTFIX, file):
                test_name = file[: len(file) - len(TEST_POSTFIX)]
                tests[test_name] = (
                    os.path.abspath(os.path.join(TEST_FOLDER_PATH, file)),
                    os.path.join(
                        TEST_FOLDER_PATH,
                        test_name + EXPECTED_POSTFIX,
                    ),
                    os.path.join(
                        TEST_FOLDER_PATH,
                        test_name + ACTUAL_POSTFIX,
                    ),
                )
                try:
                    os.remove(tests[test_name][2])
                except FileNotFoundError:
                    pass
                
                try:
                    f = open(tests[test_name][1])
                    f.close()
                except FileNotFoundError:
                    raise FileExistsError("Wrong tests")

    for name, (test, expected, actual) in tests.items():
        print(RUN.format(file=test))
        os.system(RUN.format(file=test))
        try:
            f = open(actual)
            f.close()
        except FileNotFoundError:
            print("There is no output file")
            exit()
        with open(expected) as e:
            with open(actual) as a:
                if dfrs := list(unified_diff(e.readlines(), a.readlines())):
                    print(f"Test {name} failed:")
                    for line in dfrs:
                        print(line)
                    exit()
                else:
                    print(f"Test {name} passed")
                    os.remove(actual)

    print("All tests passed!")
