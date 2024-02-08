from subprocess import run
from os import chdir
from sys import argv

# python 4.py C:\...\tmp-algo-4-test-repo 49ae10... 861ded... "python script.py"

if len(argv)!=5:
    print(f"Instead of 4 arguments, {len(argv)} were submitted. Provide arguments in the format: [path to repo] [first commit] [last commit] [run command]")
    print(argv)
    exit(1)

if run("git --version", capture_output=True).returncode == 1:
    print("It seems like you don't have Git installed on your system.")
    exit(1)

_, path, start, end, command = argv

chdir(path)

res = run(f"git rev-list {start} {end}", capture_output=True)
if res.returncode:
    raise (
        ValueError(res.stderr.decode().split("\n")[0])
        if res.returncode == 128
        else Exception
    )
commits = list(res.stdout.decode().split("\n"))[:-1]

left = -1
right = len(commits)
while right - left - 1:
    mid = (right + left) // 2
    run(f"git checkout {commits[mid]}", capture_output=True)
    if (res := run(command, capture_output=True)).returncode:
        left = mid
        print(f"commit {commits[mid]} is bad")
    else:
        right = mid
        print(f"commit {commits[mid]} is good")
        
if left == -1:
    print("There is no bad commits")
    run(f"git checkout {commits[0]}")
else:
    print(f"Commit {commits[left]} is first bad commit")
    run(f"git checkout {commits[left]}")