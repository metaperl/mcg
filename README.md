# Installation

1. Unzip file.
2. Change to unzipped folder.
3. Type `pip install -r requirements.txt`.
4. Type `python main.py input.dat` or `python main.py input.dat -m A` for mode A
5. Type `python main.py input.dat -m B` for mode B.

# Sample Runs

[~/prg/mcg]$ python ./main.py  --help
usage: main.py [-h] [-m MODE] input-file

    Given an INPUT_FILE of navigation commands and a NAVIGATION_MODE,
for each command, print to standard output a single line consisting of a space-delimited list of floors followed by the total distance in floors that the elevator travels, in parenthesis "(" and ")". The lists of floors begins with the initial floor location followed by the visited floors in the order that the elevator visits them.


positional arguments:
  input-file            None

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  A
[~/prg/mcg]$ python ./main.py  input.dat -m A
10 8 1 (9)
9 1 5 1 6 1 5 (30)
2 4 1 4 2 6 8 (16)
3 7 9 3 7 5 8 7 11 11 1 (36)
7 11 6 10 5 6 8 7 4 12 7 8 9 (40)
6 1 8 6 8 (16)
[~/prg/mcg]$ python ./main.py  input.dat -m B
10 8 1 (9)
9 1 5 6 (13)
2 4 2 1 6 8 (12)
3 5 7 8 9 11 1 (18)
7 11 10 6 5 6 8 12 7 4 8 9 (30)
6 1 6 8 (12)
[~/prg/mcg]$