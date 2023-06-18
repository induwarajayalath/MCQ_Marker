# -----------------------------Change Accordingly-------------------------------------------
NUMBER_OF_STUDENTS = 118
NUMBER_OF_QUESTIONS = 40
HAVE_MINUS_MARKS = False
CARRY_FORWARD_MINUS_MARKS = False
PORTION_OF_MCQS = 0.8    # 1 means out of 100
ANSWER_SHEET_NAME = 'Manual Marking_Logic.xlsx'
SCAN_DATA_SHEET_NAME = 'IS1115-Scan data.xlsx'
# ------------------------------------------------------------------------------------------

import pandas as pd
import csv
require_cols_logic = []
require_cols_answers = []
flagCount = 0
max_mark = 0
min_mark = 0

mark_analysis = []
question_biased_mark = []
for x in range(NUMBER_OF_QUESTIONS+1):
	question_biased_mark.append(0)
	mark_analysis.append([0,0,0,0,0])

# opening logic sheet
for x in range(10):
	require_cols_logic.append(x)
df_logic = pd.read_excel(ANSWER_SHEET_NAME,usecols = require_cols_logic)

# opening student answer sheet
for x in range(NUMBER_OF_QUESTIONS+1):
	require_cols_answers.append(x)
df_answers = pd.read_excel(SCAN_DATA_SHEET_NAME,usecols = require_cols_answers)

with open('Results_output.csv', 'w', newline='') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	print("\n\n Marks out of "+str(PORTION_OF_MCQS*100)+"\n")
	csvwriter.writerow(["Marks out of",str(PORTION_OF_MCQS*100)])
	csvwriter.writerow([])
	csvwriter.writerow(["Index","Marks",""])
	for student_number in range(NUMBER_OF_STUDENTS):
		student = df_answers.loc[student_number]
		student_total_marks = 0
		for question_number in range(1,NUMBER_OF_QUESTIONS+1):
			# print ("Question number - "+str(question_number)+" Answers - "+str(student[question_number]))

			logic = df_logic.loc[question_number+1]
			answers_for_question = []
			for x in range(5,10):
				answers_for_question.append(logic[x])

			# print(answers_for_question)
			score_for_question = 0;
			if 'BLANK' in student[question_number]:
				continue
			if 'A' in student[question_number]:
				# print ("A")
				if HAVE_MINUS_MARKS:
					score_for_question += answers_for_question[0]
				else:
					score_for_question += max(answers_for_question[0],0)
				mark_analysis[question_number][0]+=1

			if 'B' in student[question_number]:
				# print ("B")
				if HAVE_MINUS_MARKS:
					score_for_question += answers_for_question[1]
				else:
					score_for_question += max(answers_for_question[1],0)
				mark_analysis[question_number][1]+=1

			if 'C' in student[question_number]:
				# print ("C")
				if HAVE_MINUS_MARKS:
					score_for_question += answers_for_question[2]
				else:
					score_for_question += max(answers_for_question[2],0)
				mark_analysis[question_number][2]+=1

			if 'D' in student[question_number]:
				# print ("D")
				if HAVE_MINUS_MARKS:
					score_for_question += answers_for_question[3]
				else:
					score_for_question += max(answers_for_question[3],0)
				mark_analysis[question_number][3]+=1

			if 'E' in student[question_number]:
				# print ("E")
				if HAVE_MINUS_MARKS:
					score_for_question += answers_for_question[4]
				else:
					score_for_question += max(answers_for_question[4],0)
				mark_analysis[question_number][4]+=1


			question_biased_mark[question_number] += score_for_question

			if CARRY_FORWARD_MINUS_MARKS:
				student_total_marks += score_for_question
			else:
				student_total_marks += max(score_for_question,0)

			# print (max(score_for_question,0))
			# print (score_for_question)
		flag = ""
		if round(student_total_marks*100/60/NUMBER_OF_QUESTIONS)<40:
			flag = "LOW"
			flagCount += 1
		mark_to_enter = round(student_total_marks*100*PORTION_OF_MCQS/60/NUMBER_OF_QUESTIONS)
		print (str(student[0])+" | "+str(mark_to_enter) + flag)
		csvwriter.writerow([str(student[0]),str(mark_to_enter) , flag])
		if max_mark < mark_to_enter:
			max_mark = mark_to_enter
		if min_mark > mark_to_enter:
			min_mark = mark_to_enter

	print("\nQ. no.\t | Correct Percentage (Between -100% & 100%) \t| Answer Pattern\n")
	for x in range (1,NUMBER_OF_QUESTIONS+1):
		print("Q"+str(x)+"\t | "+str(round(question_biased_mark[x]/60/NUMBER_OF_STUDENTS*100,1))+" %\t | "+str(mark_analysis[x]))

	print("\nNo of students | "+str(NUMBER_OF_STUDENTS)+"\nNo of fails | "+str(flagCount)+"\nNo of passes | "+str( NUMBER_OF_STUDENTS - flagCount))
	print("Max Mark | "+str(max_mark))
	print("Min Mark | "+str(min_mark))
	print("\nPass Percentage | "+str(round(((NUMBER_OF_STUDENTS-flagCount)/NUMBER_OF_STUDENTS)*100,2))+"%\n")