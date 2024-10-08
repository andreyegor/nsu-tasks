﻿# Задача #2
## Вариант: 1
## Условие:

Вы опять услышали распространенное мнение, что Python совершенно не приспособлен для системного программирования и никакого отношения к нему не имеет.
На этот раз чаша вашего терпения переполнилась. Помня про то, как Гвидо ван Россум использовал Python для написания базовых программ под OS Amoeba, вы решаете повторить его путь. 

Начинать будете с реализации собственного shell-а!
В первой версии поддержим небольшой набор команд и ограниченную функциональность:

1. Необходимо поддержать команды для работы с каталогами:
   * **pwd** -- выводит текущую рабочую директорию
   * **cd** \<_dir_\> -- меняет текущую рабочую директорию на указанную. Работает как с абсолютными, так и с относительными путями
   * **mkdir** \<_name_\> -- создает новую директорию с заданным именем в текущей рабочей директории. Если директория с таким именем уже существовала, выводит "cannot create directory 'name': file exists".
   * **ls** [\<_dir_\>] -- выводит список всех файлов в указанной директории (или в текущей рабочей директории, если dir не указан), в алфавитном порядке

2. Команды **cat** \<_file1_\> [\<_file2_\>, \<_file3_\>, ...] и **tac** \<_file_, [\<_file2_\>, \<_file3_\>, ...] выводящие содержимое указанных файлов в прямом и обратном порядке соответственно.

3. Поддержать перенаправление вывода команд: операторы **>** и **>>**

4. Наконец, реализовать команду **tree** \<_dir_\>, печатающую структуру указанной директории в виде дерева. Ветки при этом должны следовать сверху вниз в алфавитном порядке. Кроме того команда может принимать следующие дополнительные аргументы:
   * -L \<_level_\> -- указывает до какого уровня нужно показывать структуру директории. Если этот параметр не указан, то глубина не ограничена.
   * -P "\<_pattern_\>" -- задает паттерн, которому должны удовлетворять файлы, чтобы команда их распечатала. Для простоты будем считать паттерн - обычным регулярным выражением (в синтаксисе Python).
   Обратите внимание, в настоящей команде `tree` используется немного другой формат паттернов (подробнее в `man tree`).

![ex-(benevolent dictator for life)](./pictures/saint_guido.jpg)

## Формат входных данных:

Вам необходимо реализовать функцию <code>solution(script: TextIO, output: TextIO) -> None</code> в файле <code>shell.py</code>, которая принимает на вход два уже открытых файла для входных и выходных данных.

В первом файле **script** записана последовательность команд (по одной на строчку), которые нужно выполнить в вашем shell-е. 

## Формат выходных данных:
В выходной файл **output** нужно записать последовательный вывод всех выполненных команд (в случае, если их вывод не перенаправлялся в файл с помощью > или >>).
Вывод каждой следующей команды начинается с новой строки.

При оформлении вывода команды **tree** стоит ориентироваться на настоящую линуксовую команду **tree** (и на соответствующие тесты).

## Пример входных и выходных данных:

| изначальная структура каталогов                                                                                                                                                                                                                                               | input                                                                                                 | output                                                                                                                                                   |
|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
| <pre>.<br/>├── dir1 <br/>│   └── dir2 <br/>│       └── another_text_file.txt <br/>└── some_text_file.txt </pre>                                                                                                                                                               | mkdir test <br/>cd test<br/>cd ..<br/>ls<br/>mkdir test2<br/>ls                                       | dir1 some_text_file.txt test<br/>dir1 some_text_file.txt test test2                                                                                      |
||||
| <pre>.<br/>├── dir1 <br/>│   └── dir2 <br/>│       └── another_text_file.txt <br/>└── some_text_file.txt </pre> <br/> Содержимое файлов: <br/> <br/> some_text_file.txt: <br/> just some text  <br/><br/> another_text_file.txt: <br/> and some more text <br/> and even more | cat ./some_text_file.txt ./dir1/dir2/another_text_file.txt > result.txt <br/> tac result.txt <br/> ls | and even more <br/> just some text and some more text <br/> dir1 result.txt some_text_file.txt                                                                                             |
||||
| <pre>.<br/>├── dir1 <br/>│   └── dir2 <br/>│       ├── abcd.doc<br/>│       ├── another_text_file.txt<br/>│       └── test.py<br/>└── some_text_file.txt                                                                                                                      | tree                                                                                                  | <pre>.<br/>├── dir1 <br/>│   └── dir2 <br/>│       ├── abcd.doc<br/>│       ├── another_text_file.txt<br/>│       └── test.py<br/>└── some_text_file.txt |
||||
| <pre>.<br/>├── dir1 <br/>│   └── dir2 <br/>│       ├── abcd.doc<br/>│       ├── another_text_file.txt<br/>│       └── test.py<br/>└── some_text_file.txt                                                                                                                      | tree -L 1                                                                                             | <pre>.<br/>├── dir1 <br/>└── some_text_file.txt                                                                                                          |
||||
| <pre>.<br/>├── dir1 <br/>│   └── dir2 <br/>│       ├── abcd.doc<br/>│       ├── another_text_file.txt<br/>│       └── test.py<br/>└── some_text_file.txt                                                                                                                      | tree -P ".*\.py"                                                                                        | <pre>.<br/>└── dir1 <br/>    └── dir2 <br/>        └── test.py                                                                                           |

## Замечание:

Обратите внимание, что файл shell.py можно запускать и отдельно, без тестов из `shell_test.py`. В таком случае вместо обработки набора команд (скрипта) запустится интерактивный режим,
где вам будет предложено вводить команды по одной, чтобы они сразу же исполнялись. Таким образом, вы получите тот самый привычный вам shell. 
Этот режим отлично подходит для отладки... и веселья!

## Дополнительные задания:

Если вам захочется еще попрактиковаться, то можно:

* Поддержать распознавание командой `tree` шаблонов в классическом юниксном стиле с помощью, например, библиотеки [glob](https://docs.python.org/3/library/glob.html)
* Добавить completion и историю для вашей командной строки (см. [readline](https://docs.python.org/3/library/readline.html) и [pyreadline3](https://github.com/pyreadline3/pyreadline3))
* Реализовывать другие команды, которые вам больше нравятся.