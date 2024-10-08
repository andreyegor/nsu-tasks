# Задачи Асм

## 1. Check digit

Cчитать символ и напечатать 1, если ввели цифру

## 2. [Echo symbol](./2.asm)

считать символ, и
a. тут же напечатать его
b. напечатать следующий в ASCII
c. остановиться по &lt;enter&gt;

## 3. [Hex calc](./3.asm)

a. считать два 16-ричных числа (беззнаковых, &lt;=8 цифр, цифры в любом регистре)
b. считать символ операции (+, -, &amp;, |)
c. напечатать результат операции
Проверять корректность ввода, выдавать ошибку при вводе некорректных символов
или вводе слишком большого числа. Выполнять арифметику по модулю 2^32.

## 4. [BCD calc](./4.asm)

a. считать два десятичных числа (знаковых, &lt;=7 цифр), перевести в BCD-формат
b. считать символ операции (+, -)
c. напечатать результат операции
Каждое действие (чтение/печать/сложение/вычитание чисел) должно быть выделено
в функцию, принимающую/возвращающую числа в BCD-формате.
Описание формата (packed) binary-coded decimal:

* каждая десятичная цифра занимает полубайт
* в младшем полубайте кодируется знак: ‘+’ =&gt; A, ‘-‘ =&gt; B
Примеры: “337” =&gt; 0x337A, “-12345” =&gt; 0x12345B

## 5. [a*b](./5.asm)

a. реализовать функцию умножения двух чисел, используя след.равенство:
a*b = a*(2^b1 + 2^b2 + … + 2^bk), где
b1, … bk – позиции единичных битов в b
b. воспользоваться функциями чтения/печати чисел из задачи 3 (hex calc) для
тестирования

## 6. [x/10, x%10, x*10](./6.asm)

a. div10(x) = (x &lt; 10) ? 0 : {
1/10 = ½ *1/5
= ½* (¼ – 1/20)
= ½ *(¼ - ½* 1/10)
}
b. mod10(x) = x - 10*div10(x)
c. x*10 без использования функции из задачи 5
d. протестировать функции на разных значениях
6*. (+2 балла):
Пусть K – количество значащих бит числа x. Сколько рекурсивных вызовов делается в
функции div10? Как сократить количество рекурсивных вызовов вдвое? Втрое? В
четыре раза?

## 7. [ReadDecimal, PrintDecimal](./7.asm)

Проверять корректность ввода, выдавать ошибку при вводе некорректных символов
или вводе слишком большого числа.

## 8. [Decimal calc](./8.asm)

a. считать два десятичных числа (знаковых, помещающихся в 32 бита)
b. считать символ операции (+, -, *)
c. напечатать результат операции
Делать проверки и выдавать ошибку при переполнении.

## 9. [a/b](./9.asm)

a. реализовать алгоритм деления чисел «в столбик» (в двоичной системе)
b. определить функции sdiv(a, b) &amp; udiv(a, b), протестировать их на разных значениях

10*. isqrt(x) (4 балла):
a. вычислить целочисленный квадратный корень «в столбик»
b. icbrt(x) (+3 балла): вычислить кубический корень

## 10*. isqrt(x)

a. вычислить целочисленный квадратный корень «в столбик»
b. icbrt(x) (+3 балла): вычислить кубический корень

## 11. [Load file + file length, command line args](./11.asm)

a. принять имя файла как аргумент командной строки, открыть файл на чтение
b. написать функцию int flength(int fd), которая возвращает размер
открытого файла, не меняя текущей позиции в нём
c. прочитать файл в буфер, выделенный в динамической памяти
d. напечатать имя файла и его размер

## 12. [Count lines, strchr, unit tests](./12.asm)

a. написать функцию char*strchr(char* str, char ch), которая ищет
символ в zero-terminated строке (поведение соответствует функции из C stdlib)
b. написать юнит-тесты на strchr, дающие хорошее покрытие функции
Юнит-тесты – это файл следующего вида:
.include “strchr.asm”
.include “testLib.asm”
FUNC strchr, “strchr”
OK 0 “abcde” &#39;a&#39;
OK 3 “fffwwqw” &#39;w&#39;
OK 2 “abcde” &#39;a&#39;
NONE “abcdef” &#39;Q&#39;
NONE “” &#39;?&#39;
NONE “abcde” &#39;e&#39;
DONE
А также включаемые файлы (“testLib.asm”, имя может отличаться), содержащие
необходимые объявления функций и макросов, и скрипты для запуска.

Запуск данного юнит-теста должен приводить к печати:
Testing function strchr...
Test falied: strchr(“abcde”, &#39;a&#39;) results in OK(0),
expected OK(2)
Test falied: strchr(“abcde”, &#39;e&#39;) results in OK(4),
expected NONE
Passed: 4, failed: 2
c. принять имя файла как аргумент командной строки, загрузить файл в память
d. посчитать и напечатать количество строк в файле, используя функцию strchr

## 13. [Print file contents annotated with line numbers](./13.asm)

a. принять имя файла как первый аргумент командной строки
b. принять число N, как (опциональный) второй аргумент командной строки
c. загрузить файл в память, построить таблицу строк (массив указателей на строки,
индексированный номером строки)
d. если N задано, то напечатать последние N строк файла, аннотированные номером
строки (вывод должен соответствовать команде `cat –n &lt;file&gt;| tail –n N`)
e. если N не задано, то считать, что N равно количеству строк в файле

## 14. [Simple grep](./14.asm)

a. написать простейший вариант утилиты grep – поиск и печать строк файла,
содержащих заданную подстроку (без поддержки regular expressions &amp; case-
insensitive поиска)
b. поиск делать через функцию strstr (C stdlib-like), которую надо реализовать и
покрыть юнит-тестами (см. задачу 12)
c. поддержать опции –v, -n, -c
d. (+1 балл): поддержать опцию -i (считаем, что опция не влияет на не-ASCII
символы)

## 15. [Simple wc](./15.asm)

a. написать простейший вариант утилиты wc (word count) – вывод количества слов,
строк, символов и т.п.
b. поддержать опции –с, -l, -L, -w
c. опцию -w реализовать с помощью функций strspan, strcspan (написать их и
покрыть юнит-тестами)

## 16. [MSD radix sort](./16.asm)

a. реализовать функцию сортировки строк в лексикографическом порядке, используя
алгоритм MSD radix sort
b. все временные данные/буфера, нужные для работы radix sort, выделять в
автоматической памяти
c. написать программу, которая загружает заданный (аргументом командной строки)
текстовый файл &lt;filename&gt; в память, сортирует его строки, и выводит результат в
файл &lt;filename&gt;.sorted
d. написать тесты – набор текстовых файлов + скрипты, которые прогоняют
программу на этом наборе и сравнивают вывод с образцом
 скрипты писать на скриптовом языке (python, bash, etc.)
