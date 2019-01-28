import sys
import os
import random
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox





#############FILE READ/WRITE#################
tograde_file = open('students.txt')
tograde_rows = tograde_file.readlines()
tograde = []
for row in tograde_rows:
    row = row.strip()
    if(len(row)):
        tograde.append(row)
tograde_file.close()

graded_file = open('graded.txt')
graded_rows = graded_file.readlines()
graded = []
for row in graded_rows:
    row = row.strip()
    if(len(row) and (row in tograde)):
        tograde.remove(row)
tograde_file.close()


print(tograde)






#############GETTING NEXT STUDENT#################


def get_next_student():
    global student
    if(len(tograde) == 0):
        return False
    student = random.choice(tograde)
    os.system('xdg-open ' + student + '.pdf')
    return student
    

student = 'njb2b'
get_next_student()










#############GUI STUFF#################
def exit():
    with open(graded.txt, 'w') as graded_file:
        for student in graded:
            print(student, file=graded_file)
        
    window.destroy()
    


def show_error():
    messagebox.showinfo('Warning!','Could not parse input')

def submit():
    try:
        score = int(score_text.get().strip())
        prob = int(prob_text.get().strip())
        err = False
    except:
        show_error()
        return False
    if(not comments_text.get('1.0', tk.END).strip()):
        show_error()
        return False
    grades_file = open('grades.csv', 'a')
    print(student + ","+score_text.get()+","+prob_text.get(), file=grades_file)
    grades_file.close()
    comment_file = open(student+'comments'+prob_text.get(), 'w')
    print(comments_text.get('1.0', tk.END), file=comment_file)
    comment_file.close()
    graded.append(student)
    tograde.remove(student)
    print('Submitted score of', score_text.get(), 'on problem', prob_text.get(), 'for student', student)
    get_next_student()
    
    
    if(len(graded) == 0):
        exit()
        return False
    return True

def submit_exit():
    if(submit()):
        exit()
    


window = Tk()
window.geometry('600x600')
window.title("Now grading HW10")

curr_row = 0

prob_lbl = Label(window, text="Problem Number")
prob_lbl.grid(column=0, row=curr_row)
prob_text = Entry(window, width = 10)
prob_text.grid(column = 1, row=curr_row)

curr_row += 1

score_lbl = Label(window, text="Score")
score_lbl.grid(column=0, row=curr_row)
score_text = Entry(window, width = 10)
score_text.grid(column = 1, row=curr_row)

curr_row += 1

comments_lbl = Label(window, text="Comments")
comments_lbl.grid(column=0, row=curr_row)
curr_row += 1
comments_text = scrolledtext.ScrolledText(window, width = 60, height = 20)
comments_text.grid(column = 1, row=curr_row)

curr_row += 1


submit_btn = Button(window, text="Submit and continue", command=submit)
submit_btn.grid(column = 0, row = curr_row)

quit_btn = Button(window, text="Submit and exit", command=submit_exit)
quit_btn.grid(column = 1, row = curr_row)

curr_row += 1

window.mainloop()


