import openpyxl
import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
import copy


class Data:

    students = {}  
    all_courses = set()  
    @staticmethod
    def read_data(filepath):
        try:
            wb = openpyxl.load_workbook(filepath)
            ws = wb.active

            def clean_course_name(course):
                if isinstance(course, str):
                    return re.sub(r"\s|\(.*?\)", "", course) 
                return ""
            
            rows = list(ws.iter_rows(values_only=True))

            for i in range(0, len(rows), 2):  
                roll_no = clean_course_name(str(rows[i][0]))  
                name = str(rows[i][1]).strip()  

                if i + 1 >= len(rows):  
                    break
                gpa = rows[i][9] if 9 < len(rows[i]) else "N/A"
                cgpa = rows[i][10] if 10 < len(rows[i]) else "N/A"
                status = str(rows[i][11]) if 11 < len(rows[i]) else "N/A"

                gpa = float(gpa) if isinstance(gpa, (int, float)) else "N/A"
                cgpa = float(cgpa) if isinstance(cgpa, (int, float)) else "N/A"

                # Skip Student if Status is "RL"
                if status == "RL":
                    continue

                courses = {}

                for col in range(2, len(rows[i]) - 3):  # Course columns
                    course = str(rows[i][col])  # Course code (Odd row)
                    marks = rows[i + 1][col]  # Marks (Even row)

                    if course == "--" or not course or "Unnamed" in course:  # Ignore invalid courses
                        continue

                    clean_course = clean_course_name(course)

                    if re.match(r"^[A-Z]+[0-9]+$", clean_course):  # Valid course format (e.g., CSC101)
                        courses[clean_course] = marks
                        Data.all_courses.add(clean_course)  # Add to class variable

                # Store student data in class variable
                Data.students[roll_no] = {
                    "name": name,
                    "courses": courses,
                    "GPA": gpa,
                    "CGPA": cgpa,
                    "Status": status
                }
        except Exception as e:
            print('Error occured while reading file ',e)

    @staticmethod
    def search_student(roll_no):
        if roll_no in Data.students:
            print(Data.students[roll_no])
        else:
            print("Student not found.")

    @staticmethod
    def subject_stats(coursename):
        all_marks_sum = 0
        count = 0
        passed=0
        failed=0

        for student_id, data in Data.students.items():  
            if coursename not in data['courses']:  
                continue
        
            marks = int(data['courses'][coursename])  
            if marks>=50:
                all_marks_sum += marks  
                passed += 1 
            else:
                failed +=1
            count+=1
        if passed > 0:  
            avg_marks = all_marks_sum / passed
            print(f"========================== {coursename} =============================")
            print(f"Average marks: {avg_marks:.2f} \nTotal students: {count}\nPassed students {passed} \nFailed Students {failed}")
        else:
            print(f"========================== {coursename} =============================")
            print(f"Total students: {count}\nPassed students: {passed} \nFailed Students: {failed}")

    @staticmethod
    def student_status_piechart(dismissed_students,probation_students,good_students):
        colours=['black','#FF5733','#01b041','#3680B8']
        pienames = ['Dismissed', 'Probation', 'Good']
        pievalues = [int(dismissed_students), int(probation_students), int(good_students)]
        # Adjust figure size
        plt.figure(figsize=(5, 5))  
        plt.pie(pievalues, labels=pienames, colors=colours,wedgeprops={'edgecolor': 'white'}) 
        plt.legend(title="Student Performance", loc="best")

        # Show the plot
        plt.show()

    @staticmethod
    def student_status_barchart(enrolled_students,dismissed_students,probation_students,good_students):
        #Graph to show the student status
        names=(f'DIS ({dismissed_students})',f'PRB ({probation_students})',f'GAS ({good_students})',f'Total ({enrolled_students})')
        values=(dismissed_students,probation_students,good_students,enrolled_students)
        colours=['black','#FF5733','#01b041','#3680B8']
        #adjust figure size
        plt.figure(figsize=(6,4))
        plt.barh(names,values,color=colours)
        plt.title("Student status")
        # plt.grid(True)
        plt.show()

    @staticmethod
    def student_status ():
        good_students=0
        probation_students=0
        dismissed_students=0
        enrolled_students=0
        for student_id,data in Data.students.items():
            if data['Status'] == "GAS":
                good_students+=1
            elif data['Status'] == "PRB":
                # print(student_id,data,"\n")
                probation_students+=1
            elif data['Status'] == "DI" or data['Status'] == "DIS" :
                dismissed_students+=1
            enrolled_students+=1
        # print("Enrolled students:",enrolled_students)
        # print("Good standing students:",good_students)
        # print("Probation students:",probation_students)
        # print("Dismissed students:",dismissed_students)

        
        # Data.student_status_piechart(dismissed_students,probation_students,good_students)
        # this function will return the values of following in form of dictionary and you can access by using ['enrolled_student'] just like array indexing
        # Data.student_status_barchart(enrolled_students,dismissed_students,probation_students,good_students)
        result = {"Enrolled students":enrolled_students,"Good students":good_students,"Probation students":probation_students,
                "Dismissed students":dismissed_students}
        return result
    
    @staticmethod
    def failed_students(coursename):
        failed_students = []
        for student_id, data in Data.students.items():
            if coursename in data['courses'] and int(data['courses'][coursename]) < 50:
                failed_students.append(student_id)
                failed_students.append(data['name'])
        return failed_students

    @staticmethod
    def grade_distribution(coursename):

        A_grade = A_neg_grade = B_plus_grade = B_neg_grade = 0
        C_plus_grade = C_neg_grade = D_grade = F_grade = 0
        total_student = passed = 0
        marks_std = []  

        for student_id, data in Data.students.items():
            if coursename in data['courses']:
                try:
                    marks = int(data['courses'][coursename])  # Convert marks safely
                    marks_std.append(marks)  

                    if marks >= 85:
                        A_grade += 1
                        passed += 1
                    elif marks >= 80:
                        A_neg_grade += 1
                        passed += 1
                    elif marks >= 75:
                        B_plus_grade += 1
                        passed += 1
                    elif marks >= 68:
                        B_neg_grade += 1
                        passed += 1
                    elif marks >= 64:
                        C_plus_grade += 1
                        passed += 1
                    elif marks >= 58:
                        C_neg_grade += 1
                        passed += 1
                    elif marks >= 50:
                        D_grade += 1
                        passed += 1
                    else:
                        F_grade += 1

                    total_student += 1  

                except ValueError:
                    print(f"Warning: Invalid marks for {student_id} in {coursename}, skipping.")

        print(f"========================== {coursename} =============================")
        print(f"A Grade: {A_grade}\nA- Grade: {A_neg_grade}\nB+ Grade: {B_plus_grade}\nB- Grade: {B_neg_grade}")
        print(f"C+ Grade: {C_plus_grade}\nC- Grade: {C_neg_grade}\nD Grade: {D_grade}\nF Grade: {F_grade}")
        print(f"Total students: {total_student}")
        print(f"Total Passed students: {passed}")
        print(f"Total Failed students: {F_grade}")

        if total_student > 0 and len(marks_std) > 1:  
            print(f'Passed percentage: {passed / total_student * 100:.2f} %')
            standard_deviation = np.std(marks_std, ddof=1)  # Use ddof=1 for sample data
            print(f"Standard deviation of course: {standard_deviation:.2f}")
        elif len(marks_std) == 1:
            print("Standard deviation is 0 as there's only one student.")
        else:
            print("No valid student marks found for this course.")

    @staticmethod
    def gpa_analysis():
        highest_gpa = 0.0
        highest_cgpa = 0.0
        gpa_sum = 0
        cgpa_sum = 0
        count = 0

        above_3_5 = 0
        above_3_0 = 0
        above_2_5 = 0
        above_2_0 = 0
        below_2_0 = 0

        for student_id, data in Data.students.items():
            gpa = float(data['GPA'])
            cgpa = float(data['CGPA'])

            if gpa >= 3.5:
                above_3_5 += 1
            elif gpa >= 3.0:
                above_3_0 += 1
            elif gpa >= 2.5:
                above_2_5 += 1
            elif gpa >= 2.0:
                above_2_0 += 1
            else:
                below_2_0 += 1

            if gpa > highest_gpa:
                highest_gpa = gpa
            if cgpa > highest_cgpa:
                highest_cgpa = cgpa

            gpa_sum += gpa
            cgpa_sum += cgpa
            count += 1

        average_gpa = (gpa_sum / count) if count > 0 else 0.0
        average_cgpa = (cgpa_sum / count) if count > 0 else 0.0

        result = {
            'above_3.5': above_3_5,
            'above_3.0': above_3_0,
            'above_2.5': above_2_5,
            'above_2.0': above_2_0,
            'below_2.0': below_2_0,
            'highest_gpa': highest_gpa,
            'highest_cgpa': highest_cgpa,
            'average_gpa': round(average_gpa, 2),
            'average_cgpa': round(average_cgpa, 2)
        }

        return result

    @staticmethod
    def standard_deviation_plot(marks_std, title="Student Marks Distribution"):

                if not isinstance(marks_std, (list, np.ndarray, pd.Series)):
                    raise ValueError("Marks should be a list, NumPy array, or Pandas Series.")
                
                marks_std = np.array(marks_std)  # Convert to NumPy array if not already
                mean_val = np.mean(marks_std)
                std_dev = np.std(marks_std)
                df = pd.DataFrame({"Marks": marks_std})
                plt.figure(figsize=(10, 5))
                sns.stripplot(x=df["Marks"], jitter=True, color='blue', alpha=0.7)
                plt.axvline(mean_val, color='red', linestyle='dashed', label=f'Mean: {mean_val:.2f}')
                plt.axvline(mean_val + std_dev, color='green', linestyle='dashed', label=f'Mean + 1 SD: {mean_val + std_dev:.2f}')
                plt.axvline(mean_val - std_dev, color='green', linestyle='dashed', label=f'Mean - 1 SD: {mean_val - std_dev:.2f}')
                plt.title(title)
                plt.xlabel("Marks")
                plt.legend()
                plt.show()

    @staticmethod
    def standard_deviation(coursename):
        all_marks_sum = 0
        count = 0
        passed = 0
        failed = 0
        marks_std = []
    
        for student_id, data in Data.students.items():
            if coursename not in data['courses']:  
                continue
    
            marks = int(data['courses'][coursename])  
            marks_std.append(marks)
    
            if marks >= 50:
                all_marks_sum += marks  
                passed += 1 
            else:
                failed += 1
    
            count += 1
    
        print(f"========================== {coursename} =============================")
        print(f"Total students: {count}\nPassed students: {passed} \nFailed Students: {failed}")
    
        if count > 0:
            if passed > 0:
                avg_marks = all_marks_sum / passed
                print(f"Average marks (of passed students): {avg_marks:.2f}")
                print(f"Passed percentage: {passed / count * 100:.2f} %")
            
            if len(marks_std) > 1:
                standard_deviation = np.std(marks_std, ddof=0) 
                print(f"Standard deviation of course: {standard_deviation:.2f}")
            else:
                print("Standard deviation is 0 as there's only one student.")
            Data.standard_deviation_plot(marks_std, f"{coursename} Marks Distribution")
    
    @staticmethod
    def batch_analysis():
        # printing the values returned by function in form of a dictionary
        status=Data.student_status()
        print(status['Enrolled students'])
        print(status['Good students'])
        print(status['Probation students'])
        print(status['Dismissed students'])
        # passing values to other fuction which were returned by dictionary
        chart=Data.student_status_barchart(status['Enrolled students'],status['Dismissed students'],status['Probation students'],status['Good students'])
        chart=Data.student_status_piechart(status['Dismissed students'],status['Probation students'],status['Good students'])

        # printing the values returned by function in form of a dictionary
        gpa_analysis=Data.gpa_analysis()
        print(gpa_analysis['above_3.5'])
        print(gpa_analysis['above_3.0'])
        print(gpa_analysis['above_2.5'])
        print(gpa_analysis['above_2.0'])
        print(gpa_analysis['below_2.0'])
        print(gpa_analysis['highest_cgpa'])
        print(gpa_analysis['highest_gpa'])
        print(gpa_analysis['average_cgpa'])
        print(gpa_analysis['average_gpa'])
        
        # all courses offered 
        all_courses=set()
        all_courses=Data.all_courses
        for course in all_courses:
            print(course)

    @staticmethod
    def subject_analysis():
        print('under process')
    

class ClassData:
    student_data = {}
    courses=()

    @staticmethod
    def clone_data():
        ClassData.student_data = copy.deepcopy(Data.students)
        ClassData.courses = copy.deepcopy(Data.all_courses)

    def __init__(self, class_name):
        self.class_name = class_name
        self.students = {}

    def add_by_range(self, start, end):
        """Add students based on roll number range """
        start_num = int(start[-3:])
        end_num = int(end[-3:])
        for roll in ClassData.student_data:
            roll_num = int(roll[-3:])
            if start_num <= roll_num <= end_num:
                self.students[roll] = ClassData.student_data[roll]
        return self.students

    def add_student(self, roll_no):
        """Add a single student by roll number """
        if roll_no in ClassData.student_data:
            self.students[roll_no] = ClassData.student_data[roll_no]

    def gpa_analysis(self):
        highest_gpa = 0.0
        highest_cgpa = 0.0
        gpa_sum = 0
        cgpa_sum = 0
        count = 0

        above_3_5 = 0
        above_3_0 = 0
        above_2_5 = 0
        above_2_0 = 0
        below_2_0 = 0

        for student_id, data in self.students.items():
            gpa = float(data['GPA'])
            cgpa = float(data['CGPA'])

            if gpa >= 3.5:
                above_3_5 += 1
            elif gpa >= 3.0:
                above_3_0 += 1
            elif gpa >= 2.5:
                above_2_5 += 1
            elif gpa >= 2.0:
                above_2_0 += 1
            else:
                below_2_0 += 1

            if gpa > highest_gpa:
                highest_gpa = gpa
            if cgpa > highest_cgpa:
                highest_cgpa = cgpa

            gpa_sum += gpa
            cgpa_sum += cgpa
            count += 1

        average_gpa = (gpa_sum / count) if count > 0 else 0.0
        average_cgpa = (cgpa_sum / count) if count > 0 else 0.0

        result = {
            'above_3.5': above_3_5,
            'above_3.0': above_3_0,
            'above_2.5': above_2_5,
            'above_2.0': above_2_0,
            'below_2.0': below_2_0,
            'highest_gpa': highest_gpa,
            'highest_cgpa': highest_cgpa,
            'average_gpa': round(average_gpa, 2),
            'average_cgpa': round(average_cgpa, 2)
        }

        return result

    def student_status (self):
        good_students=0
        probation_students=0
        dismissed_students=0
        enrolled_students=0
        for student_id,data in self.students.items():
            if data['Status'] == "GAS":
                good_students+=1
            elif data['Status'] == "PRB":
                # print(student_id,data,"\n")
                probation_students+=1
            elif data['Status'] == "DI" or data['Status'] == "DIS" :
                dismissed_students+=1
            enrolled_students+=1

        result = {"Enrolled students":enrolled_students,"Good students":good_students,"Probation students":probation_students,
                "Dismissed students":dismissed_students}
        return result
    
    def grade_distribution(self,coursename):

        A_grade = A_neg_grade = B_plus_grade = B_neg_grade = 0
        C_plus_grade = C_neg_grade = D_grade = F_grade = 0
        total_student = passed = 0
        marks_std = []  

        for student_id, data in self.students.items():
            if coursename in data['courses']:
                try:
                    marks = int(data['courses'][coursename])  # Convert marks safely
                    marks_std.append(marks)  

                    if marks >= 85:
                        A_grade += 1
                        passed += 1
                    elif marks >= 80:
                        A_neg_grade += 1
                        passed += 1
                    elif marks >= 75:
                        B_plus_grade += 1
                        passed += 1
                    elif marks >= 68:
                        B_neg_grade += 1
                        passed += 1
                    elif marks >= 64:
                        C_plus_grade += 1
                        passed += 1
                    elif marks >= 58:
                        C_neg_grade += 1
                        passed += 1
                    elif marks >= 50:
                        D_grade += 1
                        passed += 1
                    else:
                        F_grade += 1

                    total_student += 1  

                except ValueError:
                    print(f"Warning: Invalid marks for {student_id} in {coursename}, skipping.")

        print(f"========================== {coursename} =============================")
        print(f"A Grade: {A_grade}\nA- Grade: {A_neg_grade}\nB+ Grade: {B_plus_grade}\nB- Grade: {B_neg_grade}")
        print(f"C+ Grade: {C_plus_grade}\nC- Grade: {C_neg_grade}\nD Grade: {D_grade}\nF Grade: {F_grade}")
        print(f"Total students: {total_student}")
        print(f"Total Passed students: {passed}")
        print(f"Total Failed students: {F_grade}")

        if total_student > 0 and len(marks_std) > 1:  
            print(f'Passed percentage: {passed / total_student * 100:.2f} %')
            standard_deviation = np.std(marks_std, ddof=1)  # Use ddof=1 for sample data
            print(f"Standard deviation of course: {standard_deviation:.2f}")
        elif len(marks_std) == 1:
            print("Standard deviation is 0 as there's only one student.")
        else:
            print("No valid student marks found for this course.")
        Data.standard_deviation_plot(marks_std,"E")





if __name__ == "__main__":
    filepath = "FA23-BCS-3.xlsx" 
    Data.read_data(filepath)  
    # Data.search_student("FA23-BCS-273")  
    # Data.subject_stats("CSC241")
    # Data.student_status()
    # print(Data.failed_students("CSC241"))
    # Data.grade_distribution("CSC241")
    # all_courses=set()
    # all_courses=Data.all_courses
    # # for course in all_courses:
    # #     Data.grade_distribution(course)
    # print(Data.failed_students('CSC241'))
    # print(Data.student_status())
    # Data.gpa_analysis()
    # Data.batch_analysis()
    ClassData.clone_data()
    # for student in ClassData.student_data.items():
    #     print(student)
    E = ClassData("E")
    E.add_by_range('FA23-BCS-242', 'FA23-BCS-300')
    E.add_by_range('FA23-BCS-403', 'FA23-BCS-407')
    E.add_by_range('FA23-BCS-453', 'FA23-BCS-463')
    E.add_student('FA23-BCS-409')
    E.add_student('FA23-BCS-412')
    print(E.gpa_analysis())
    print(E.student_status())
    print(E.grade_distribution('CSC241'))
    status=E.student_status()
    chart=Data.student_status_barchart(status['Enrolled students'],status['Dismissed students'],status['Probation students'],status['Good students'])

    # for roll_no, data in E.students.items():
    #     print("Roll No:", roll_no)
    #     print("Name:", data.get('name', 'N/A'))
    #     print("GPA:", data.get('GPA', 'N/A'))

    # for roll, data in selected_students:
    #     print(roll, data)

    # for roll_no, data in ClassData.student_data.items():
    # for roll_no, data in selected_students.items:
        # print("Roll No:", roll_no)
        # print("Name:", data['name'])
        # print("GPA:", data['GPA'])
        # print("Courses:")
    #     for course, marks in data['courses'].items():
    #         print(f"  {course}: {marks}")
    #     print("-" * 30)



