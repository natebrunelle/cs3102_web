import os
import random
import sys
import tkinter as tk
from tkinter import scrolledtext
import argparse


###############

# Usage: modify your problems_to_grade.txt file and tograde.txt file to represent the problems and 
# students you are grading for this assignment respectively

# Select a command for opening a pdf. You must be able to simply append the name of the pdf file
# to the command and have it work (3 choices are provided for you, they work with linux)

# Run with python3 to grade students randomly
# Run with python3 and a computing id as a command-line argument to grade a particular student

###############


##########GUI###########
# inputs to take: problem #, score, comments
#####################

pdf_open_command = "xdg-open"
#pdf_open_command = "google-chrome"
#pdf_open_command = "evince -f"


assigned_to_grade_filename = 'tograde.txt'
has_graded_filename = 'hasgraded.txt'
problems_filename = 'problems.txt'
problems_to_grade_filename = 'problems_to_grade.txt'

problems_file = open(problems_filename)
all_problems = list(map(lambda s: s.strip(), problems_file.read().strip().split()))#['1','2','3']
print(all_problems)

problems_to_grade_file = open(problems_to_grade_filename)
problems_to_grade = list(map(lambda s: s.strip(), problems_to_grade_file.read().strip().split()))#['2','3']

num_graded = 0



assigned_to_grade_file = open(assigned_to_grade_filename)
to_grade = {}
for line in assigned_to_grade_file.readlines():
    line = line.strip()
    if len(line)>0:
        to_grade[line] = [False for i in all_problems]
assigned_to_grade_file.close()
print(to_grade)

has_graded_file = open(has_graded_filename)
for line in has_graded_file.readlines():
    line = line.strip()
    if len(line)>0:
        cells = line.split(',')
        to_grade[cells[0]][all_problems.index(cells[1])] = True
        num_graded += 1
has_graded_file.close()
print(to_grade)

def entergrade(student, problem, score, comment):
    global num_graded
    feedback_file_name = student + problem + '.txt'
    feedback_file = open(feedback_file_name, 'w')
    print(score, file=feedback_file)
    print(comment, file=feedback_file)
    feedback_file.close()
    has_graded_file = open(has_graded_filename, 'a')
    print(student + ',' + problem, file=has_graded_file)
    has_graded_file.close()
    to_grade[student][all_problems.index(problem)] = True
    num_graded += 1
    
def fetchgrade(student, problem):
    if not student in to_grade or not to_grade[student][all_problems.index(problem)]:
        return None
    feedback_file_name = student + problem + '.txt'
    feedback_file = open(feedback_file_name)
    score = float(feedback_file.readline().strip())
    comment = feedback_file.read()
    feedback_file.close()
    return score,comment
    
def next_student():
    global student
    studs = list(to_grade.keys())
    random.shuffle(studs)
    for stud in studs:
        done = True
        for prob in problems_to_grade:
            done = done and to_grade[stud][all_problems.index(prob)]
        if not done:
            student = stud
            return stud
    return
    
def display_student(student):
    percent = (num_graded / (len(to_grade)*len(problems_to_grade)))*100
    print(str(percent) + "% graded")
    if student is None:
        return
    print("Now grading " + student)
    os.system(pdf_open_command + " " + student + '.pdf')

parser = argparse.ArgumentParser()
parser.add_argument("--student", "-s", help="individual student to grade")
parser.add_argument("--cli", "-c", action="store_true", help="use CLI instead of gui")

args = parser.parse_args()

student_provided = args.student is not None
student = args.student if student_provided else next_student()
display_student(student)


########################################################

#GUI

########################################################
scores = []
comments = []

def submit():
    for problem in problems_to_grade:
        i = problems_to_grade.index(problem)
        score = float(scores[i].get().strip())
        comment = comments[i].get('1.0', tk.END).strip()
        print(score,comment)
        entergrade(student, problem, score, comment)
    if student_provided:
        gui.destroy()
        return
    if next_student() is None:
        gui.destroy()
    else:
        v.set("Now grading " + student)
        display_student(student)
        

def buildwindow(window):
    row = 1
    for problem in problems_to_grade:
        # problem number label
        prob_lbl = tk.Label(window, text="Problem "+problem, font=("Courier", 20))
        prob_lbl.grid(column=0, row=row)
        row += 1
    
        # Score entry
        score_lbl = tk.Label(window, text="Score ")
        score_lbl.grid(column=0,row=row)
        score_text = tk.Entry(window, width = 10)
        scores.append(score_text)
        score_text.grid(column = 1, row=row)
        row += 1
        
        #Comment entry
        comment_lbl = tk.Label(window, text="Comment ")
        comment_lbl.grid(column=0,row=row)
        comment_text = scrolledtext.ScrolledText(window, width = 60, height = 5)
        comments.append(comment_text)
        comment_text.grid(column = 1, row=row)
        row += 1
        
    #Buttons
    submit_btn = tk.Button(window, text="Submit", command=submit)
    submit_btn.grid(column = 1, row = row)
    
    row += 1

use_gui = not args.cli

if not student is None:
    if use_gui:
        gui = tk.Tk()
        gui.geometry('600x600')
        title = "Now grading " + student if student_provided else "Grading random students"
        v = tk.StringVar()
        v.set("Now grading " + student)
        gui.title(title)
        grading_label = tk.Label(gui, textvariable=v, font=("Courier", 10))
        grading_label.grid(column = 0, row=0)
        buildwindow(gui)

        gui.mainloop()
    else:
        while student is not None:
            display_student(student)
            for problem in problems_to_grade:
                print("Grading {}".format(problem))
                i = problems_to_grade.index(problem)
                score = float(input("score: "))
                comment = input("comment: ")
                entergrade(student, problem, score, comment)
            if student_provided:
                break
            if next_student() is None:
                break

else:
    print("No Students left to grade!")

