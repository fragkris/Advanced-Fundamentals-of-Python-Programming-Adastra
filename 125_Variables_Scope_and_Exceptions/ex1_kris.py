"""
- When the program run it asks for a directory to read a txt file.
The directory should be provided in this format: 'diskdrive:\[optional_folder]\[--]\[--]\[--]\file.txt.
- File degrees.txt is included for testing.
- Since the program does not serve a real purpose and the task does not require anything else,
the output file saves in the project folder as output.txt.
- I was not sure if the code should write the data that is already in Fahrenheit. If not, rows 72 and 73
can be deleted or commented.
"""


import re
from os import path

"""
clear_file clears all empty lines on a text file.
"""
def clear_file(file):
    with open(file) as reader, open(file, 'r+') as writer:
        for line in reader:
            if line.strip():
                writer.write(line)
        writer.truncate()


"""
reead_text_file and write_text_file - self explanatory
"""
def read_text_file(file_path):
    with open(file_path) as f:
        return f.readlines()


def write_text_file(text, file_path):
    with open(file_path, 'a') as f:
        f.write(text + '\n')



"""
validate_input_path checks if the directory is valid and if the given file is '.txt'. 
Recursively calls itself until valid string is given.
"""
def validate_input_path(input_path):
    patter_dir = re.compile('([A-Z]:([^/]*/)*)(.*)')
    if patter_dir.match(input_path):
        if not path.exists(input_path):
            return validate_input_path(input("File does not exist. Try again.\n"))
        if input_path[-4:] != '.txt':
            return validate_input_path(input("Only .txt files are supported. Try again.\n"))
        else:
            return input_path
    else:
        return validate_input_path(input("Invalid directory. Try again.\n"))




"""
Main part. Could be optimized and split into more functions, but it is enough for the given task.
"""

if __name__ == "__main__":
    pattern_celc = re.compile('(-?[\d]+)[c|C]{1}\\b')
    pattern_fare = re.compile('(-?[\d]+)[f|F]{1}\\b')
    for line in read_text_file(validate_input_path(str(input("Please enter or paste a valid input text file location\n")))):
        if pattern_celc.match(line):
            if len(line[:-2]) > 1:
                celsius = line[:-2]
            else:
                celsius = line[:1]
            fahrenheit = str(round(float(celsius) * 9 / 5 + 32, 1)) + 'F'
            write_text_file(fahrenheit, "output.txt")
#   The two rows below can be commented if not needed.
        elif pattern_fare.match(line):
            write_text_file(line, "output.txt")
    clear_file("output.txt")

