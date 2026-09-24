Python 3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
name="Andrew"
name[0]='X'
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    name[0]='X'
TypeError: 'str' object does not support item assignment
name.split()
['Andrew']
test="This is a simple character sequence to practice on"
test.split()
['This', 'is', 'a', 'simple', 'character', 'sequence', 'to', 'practice', 'on']
test.split("s")
['Thi', ' i', ' a ', 'imple character ', 'equence to practice on']
test.split("character")
['This is a simple ', ' sequence to practice on']
test.split("s", 3)
['Thi', ' i', ' a ', 'imple character sequence to practice on']
words=test.split()
words
['This', 'is', 'a', 'simple', 'character', 'sequence', 'to', 'practice', 'on']
" ".join(words)
'This is a simple character sequence to practice on'
"...".join(words)
'This...is...a...simple...character...sequence...to...practice...on'
test.upper()
'THIS IS A SIMPLE CHARACTER SEQUENCE TO PRACTICE ON'
test.lower()
'this is a simple character sequence to practice on'
test.title()
'This Is A Simple Character Sequence To Practice On'
test.isupper()
False
test.islower()
False
test
'This is a simple character sequence to practice on'
"qwerty123".isalnum()
True
"qwert43ty**(".isalnum()
False
"letters".isalpha()
True
"letters123".isalpha()
False
"let ters".isalpha()
False
"12345".isalpha()
False
"123abc".isdigit()
False
"1234".isdigit()
True
"     ".isspace()
True
" a a ".isspace()
False
"A string".ljust()
Traceback (most recent call last):
  File "<pyshell#28>", line 1, in <module>
    "A string".ljust()
TypeError: ljust expected at least 1 argument, got 0
"A string".ljust(20)
'A string            '
"A string".rjust(50)
'                                          A string'
"A string".center(45)
'                   A string                  '
"    A string                         ".strip()
'A string'
l1=[0, 'one', 2.0, [1,2,3], False]
l1
[0, 'one', 2.0, [1, 2, 3], False]
1l
SyntaxError: invalid decimal literal
l1
[0, 'one', 2.0, [1, 2, 3], False]
l1[0]
0
>>> l1[1]
'one'
>>> l1[1:3]
['one', 2.0]
>>> l2=l1
>>> l2
[0, 'one', 2.0, [1, 2, 3], False]
>>> l1
[0, 'one', 2.0, [1, 2, 3], False]
>>> l2[0]='zero'
>>> l1
['zero', 'one', 2.0, [1, 2, 3], False]
>>> l2
['zero', 'one', 2.0, [1, 2, 3], False]
>>> l3=l1.copy()
>>> l3
['zero', 'one', 2.0, [1, 2, 3], False]
>>> l3[1]=000
>>> l3
['zero', 0, 2.0, [1, 2, 3], False]
>>> l1
['zero', 'one', 2.0, [1, 2, 3], False]
>>> l2
['zero', 'one', 2.0, [1, 2, 3], False]
>>> l3
['zero', 0, 2.0, [1, 2, 3], False]
>>> my_list = []
>>> my_list.append(1)
>>> my_list.append(2)
>>> my_list.append(3)
>>> my_list
[1, 2, 3]
>>> print(my_list.pop())
3
>>> my_list
[1, 2]
>>> my_list.append(4)
>>> my_list
[1, 2, 4]
