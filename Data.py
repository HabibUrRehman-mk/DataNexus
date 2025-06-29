import openpyxl
import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout
import sys
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
            
            if len(rows) < 2 or not rows[0] or not rows[0][0]:
                raise ValueError("Invalid file structure: missing roll number in the first cell.")

            roll_no_value = str(rows[0][0]).strip()
            pattern = r"^[A-Z]{2}\d{2}-[A-Z]{3}-\d{3}$"  # e.g., FA23-BCS-001

            if not re.match(pattern, roll_no_value):
                raise ValueError(f"Invalid roll number format: '{roll_no_value}'. Expected format: FA23-BCS-000")
                
           
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
            raise
    
    

    @staticmethod
    def search_student(roll_no):
        if roll_no in Data.students:
            return Data.students[roll_no]
        else:
            print("Student not found.")
    
    @staticmethod
    def plot_student_marks(student_data):
        courses = list(student_data['courses'].keys())
        marks = [int(mark) for mark in student_data['courses'].values()]

        fig, ax = plt.subplots(figsize=(6, 5))
        bars = ax.bar(courses, marks, color="#0D742C", edgecolor='black')

        ax.set_title(f"Marks of {student_data['name']}")
        ax.set_xlabel('Courses')
        ax.set_ylabel('Marks (%)')

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height}%',
                    ha='center', va='bottom')


        plt.xticks(rotation=45, ha='right') 
        ax.set_ylim(0, 100)
        ax.grid(axis='y', linestyle='--', alpha=0.4)

        fig.tight_layout()

        return fig
    
    
    def plot_gpa_progress(gpa, cgpa):
        x = ["Previous", "Current"]
        y = [cgpa, gpa]

        if gpa > cgpa:
            color = "green"
            label = "Improved"
            marker = '>'
        elif gpa < cgpa:
            color = "red"
            label = "Declined"
            marker = '>'
        else:
            color = "gray"
            label = "No Change"
            marker = '|'

        fig, ax = plt.subplots()

        ax.plot(x, y, color=color, linewidth=2, label=label)
        ax.plot(x[1], y[1], marker=marker, color=color, markersize=10)

        ax.set_title("Student GPA Progress", fontsize=14)
        ax.set_ylabel("GPA", fontsize=12)
        ax.set_ylim(0, 4.0)

        ax.grid(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(True)
        ax.spines["bottom"].set_visible(True)

        ax.legend()
        return fig

    @staticmethod
    def subject_stats(coursename):
        all_marks_sum = 0
        count = 0
        passed = 0
        failed = 0
        avg_marks = 0  

        for student_id, data in Data.students.items():
            if coursename not in data['courses']:
                continue

            marks = int(data['courses'][coursename])
            if marks >= 50:
                all_marks_sum += marks
                passed += 1
            else:
                failed += 1
            count += 1

        if passed > 0:
            avg_marks = all_marks_sum / passed

        return {
            "total_students": count,
            "passed": passed,
            "failed": failed,
            "average_marks": avg_marks
        }


    @staticmethod
    def student_status():
        good_students = 0
        probation_students = 0
        dismissed_students = 0
        enrolled_students = 0

        for student_id, data in Data.students.items():
            status = data.get('Status', '')
            if status == "GAS":
                good_students += 1
            elif status == "PRB":
                probation_students += 1
            elif status in ("DI", "DIS"):
                dismissed_students += 1
            enrolled_students += 1

        names = (
            f'DIS ({dismissed_students})',
            f'PRB ({probation_students})',
            f'GAS ({good_students})',
            f'Total ({enrolled_students})'
        )
        values = (dismissed_students, probation_students, good_students, enrolled_students)
        colours = ['black', '#FF5733', '#01b041', '#3680B8']

        # Bar chart
        bar_fig = Figure(figsize=(3, 2))
        bar_ax = bar_fig.add_subplot(111)
        bar_ax.barh(names, values, color=colours)
        bar_ax.set_title("Student Status")

        # Pie chart
        

        pie_fig = Figure(figsize=(3.5, 3.5))
        pie_ax = pie_fig.add_subplot(111)

        pievalues = [dismissed_students, probation_students, good_students]
        pienames = ['Dismissed', 'Probation', 'Good']
        colours = ["#000000", "#f05526", '#24a024']

        wedges, _ = pie_ax.pie(
            pievalues,
            colors=colours,
            wedgeprops={'edgecolor': 'white'},
            startangle=140
        )

        pie_ax.legend(
            wedges,
            pienames,
            title="Student Performance",
            loc="lower right",
            bbox_to_anchor=(1, 0.5)  
        )

        pie_fig.tight_layout()
        
        return  bar_fig, good_students, probation_students, dismissed_students, enrolled_students,pie_fig

    

    @staticmethod
    def failed_students(coursename):
        failed_students = []
        for student_id, data in Data.students.items():
            if coursename in data['courses'] and int(data['courses'][coursename]) < 50:
                failed_students.append((student_id, data['name']))
        return failed_students
    
    @staticmethod
    def passed_students(coursename):
        passed_students = []
        for student_id, data in Data.students.items():
            if coursename in data['courses'] and int(data['courses'][coursename]) > 50:
                passed_students.append((student_id, data['name']))
        return passed_students

    
    @staticmethod
    def grade_distribution(coursename):
        A_grade = A_neg_grade = B_plus_grade = B_neg_grade = 0
        C_plus_grade = C_neg_grade = D_grade = F_grade = 0
        total_student = passed = 0
        marks_std = []

        for student_id, data in Data.students.items():
            if coursename in data['courses']:
                try:
                    marks = int(data['courses'][coursename])
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

        # Calculate extra stats
        if total_student > 0:
            passed_percentage = (passed / total_student) * 100
            std_dev = np.std(marks_std, ddof=1) if len(marks_std) > 1 else 0.0
        else:
            passed_percentage = 0.0
            std_dev = 0.0

        return {
            "course": coursename,
            "grades": {
                "A Grade": A_grade,
                "A- Grade": A_neg_grade,
                "B+ Grade": B_plus_grade,
                "B- Grade": B_neg_grade,
                "C+ Grade": C_plus_grade,
                "C- Grade": C_neg_grade,
                "D Grade": D_grade,
                "F Grade": F_grade,
            },
            "total_students": total_student,
            "passed": passed,
            "failed": F_grade,
            "passed_percentage": round(passed_percentage, 2),
            "standard_deviation": round(std_dev, 2)
        }
    

    @staticmethod
    def student_status_barchart(enrolled_students, dismissed_students, probation_students, good_students):
        # Create a new Figure object
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)  # 1x1 grid, first subplot

        # Data
        names = (
            f'DIS ({dismissed_students})',
            f'PRB ({probation_students})',
            f'GAS ({good_students})',
            f'Total ({enrolled_students})'
        )
        values = (dismissed_students, probation_students, good_students, enrolled_students)
        colours = ['black', '#FF5733', '#01b041', '#3680B8']

        # Plot on the axis object instead of using plt directly
        ax.barh(names, values, color=colours)
        ax.set_title("Student Status")

        return fig  # Return the figure



    
    @staticmethod
    def gpa_analysis():
        highestgpa = 0.00
        highestcgpa = 0.00
        gpasum = 0
        cgpasum = 0
        above_35 = 0
        above_3 = 0
        above_25 = 0
        above_2 = 0
        below2 = 0
        gpacount = cgpacount = 0

        for student_id, data in Data.students.items():
            gpa = float(data['GPA'])
            cgpa = float(data['CGPA'])

            if gpa >= 3.5:
                above_35 += 1
            elif gpa >= 3.0:
                above_3 += 1
            elif gpa >= 2.5:
                above_25 += 1
            elif gpa >= 2.0:
                above_2 += 1
            else:
                below2 += 1

            highestgpa = max(highestgpa, gpa)
            highestcgpa = max(highestcgpa, cgpa)

            gpasum += gpa
            cgpasum += cgpa
            gpacount += 1
            cgpacount += 1

        average_gpa = gpasum / gpacount if gpacount > 0 else 0
        average_cgpa = cgpasum / cgpacount if cgpacount > 0 else 0

        
        return {
            "gpa_counts": [above_35, above_3, above_25, above_2, below2],
            "average_gpa": average_gpa,
            "average_cgpa": average_cgpa,
            "highest_gpa": highestgpa,
            "highest_cgpa": highestcgpa
        }

    @staticmethod
    def plot_gpa_distribution(gpa_counts, range=['3.5-4.0', '3.0-3.5', '2.5-3.0', '2.0-2.5', '<2.0'], 
                            xlabel='GPA Range', ylabel='Number of Students', 
                            title='GPA Distribution of Students'):
        
        gpa_ranges = range
        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot(111)

        bars = ax.bar(gpa_ranges, gpa_counts, color="#0D6F6E", edgecolor='black')
        
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(axis='y', linestyle='--', alpha=0.2)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval + 0.5, int(yval), 
                    ha='center', va='bottom')

        max_count = max(gpa_counts)
        padding = max(1, max_count * 0.1)  
        ax.set_ylim(0, max_count + padding)
        
        fig.tight_layout()
        return fig

    @staticmethod   
    def create_donut_chart(stats):
        
        labels = ['Passed', 'Failed']
        sizes = [stats['passed'], stats['failed']]
        colors = ['#4CAF50', '#F44336']

        fig, ax = plt.subplots(figsize=(1.5, 1.5))  # smaller size for donut

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops=dict(width=0.4)
        )

        centre_circle = plt.Circle((0, 0), 0.6, color='white', fc='white', linewidth=0)
        ax.add_artist(centre_circle)

        ax.axis('equal')
        plt.tight_layout()
        return fig
    
    
    @staticmethod
    def standard_deviation_plot(marks_std, title="Student Marks Distribution"):
        if not isinstance(marks_std, (list, np.ndarray, pd.Series)):
            raise ValueError("Marks should be a list, NumPy array, or Pandas Series.")
        
        marks_std = np.array(marks_std)
        mean_val = np.mean(marks_std)
        std_dev = np.std(marks_std)

        fig = Figure(figsize=(10, 4))
        ax = fig.add_subplot(111)

        sns.stripplot(x=marks_std, jitter=True, color='blue', alpha=0.7, ax=ax)
        ax.axvline(mean_val, color='red', linestyle='dashed', label=f'Mean: {mean_val:.2f}')
        ax.axvline(mean_val + std_dev, color='green', linestyle='dashed', label=f'Mean + 1 SD: {mean_val + std_dev:.2f}')
        ax.axvline(mean_val - std_dev, color='green', linestyle='dashed', label=f'Mean - 1 SD: {mean_val - std_dev:.2f}')
        ax.set_title(title)
        ax.set_xlabel("Marks")
        ax.legend()

        return fig
    
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

       # print(f"========================== {coursename} =============================")
        #print(f"Total students: {count}\nPassed students: {passed} \nFailed Students: {failed}")

        if count > 0:
            if passed > 0:
                avg_marks = all_marks_sum / passed
               # print(f"Average marks (of passed students): {avg_marks:.2f}")
                #print(f"Passed percentage: {passed / count * 100:.2f} %")

            if len(marks_std) > 1:
                standard_deviation = np.std(marks_std, ddof=0) 
                #print(f"Standard deviation of course: {standard_deviation:.2f}")
            #else:
                #print("Standard deviation is 0 as there's only one student.")

            return Data.standard_deviation_plot(marks_std, f"{coursename} Marks Distribution")
    
    @staticmethod
    def get_rank(roll_no):
        if roll_no not in Data.students:
            return "Student not found."

       
        cgpa_list = [
            (r_no, student["CGPA"])
            for r_no, student in Data.students.items()
            if isinstance(student["CGPA"], (int, float))
        ]

        
        sorted_cgpa = sorted(cgpa_list, key=lambda x: x[1], reverse=True)
        for rank, (r_no, _) in enumerate(sorted_cgpa, start=1):
            if r_no == roll_no:
                return rank

        return "Rank not found due to invalid CGPA."




   
   
    @staticmethod
    def batch_analysis():
        Data.student_status()
        Data.gpa_analysis()
        all_courses=set()
        all_courses=Data.all_courses
        for course in all_courses:
            Data.standard_deviation(course)
    
   

    @staticmethod
    def guage_chart(title: str, callout_value: float):
        import numpy as np
        import matplotlib.pyplot as plt

        values = [4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.0]
        colors = ['#4dab6d', "#72c66e", "#c1da64", "#f6ee54", "#fabd57", "#f36d54", "#ee4d55"]

        num_bars = len(colors)
        bar_angles = np.linspace(0, np.pi, num_bars, endpoint=True)
        bar_width = np.pi / (num_bars - 1)

        fig = plt.figure(figsize=(3.5, 3))
        ax = fig.add_subplot(projection="polar")

        bar_bottom = 2
        bar_height = 0.5

        ax.bar(
            x=bar_angles,
            width=bar_width,
            height=bar_height,
            bottom=bar_bottom,
            linewidth=3,
            edgecolor="white",
            color=colors,
            align="edge"
        )

        
        label_angles = np.linspace(0, np.pi, len(values), endpoint=True)
        label_radius = bar_bottom + bar_height + 0.3
        for angle, val in zip(label_angles, values):
            ax.text(angle, label_radius, str(val), ha="center", va="center", fontsize=10)

        def get_callout_angle(val):
            if val >= values[0]:  
                return label_angles[0]
            if val <= values[-1]:  
                return label_angles[-1]

            for i in range(len(values) - 1):
                v1, v2 = values[i], values[i + 1]
                if v1 >= val >= v2:
                    a1, a2 = label_angles[i], label_angles[i + 1]
                    t = (val - v2) / (v1 - v2)
                    return a1 + t * (a2 - a1)
            return label_angles[-1]

        callout_angle = get_callout_angle(callout_value)
        callout_radius = bar_bottom + bar_height - 0.1

        ax.annotate(
            str(callout_value),
            xy=(callout_angle, callout_radius),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="wedge,tail_width=0.5", color="black", shrinkA=0),
            bbox=dict(boxstyle="circle", facecolor="black", linewidth=2.0),
            fontsize=10,
            color="white",
            ha="center",
            va="center"
        )

        ax.set_title(title)
        ax.set_axis_off()
        ax.set_thetamin(0)
        ax.set_thetamax(180)

        plt.tight_layout()
        return fig


            
def extract_roll_suffix(roll_no):
        """Extract numeric suffix like 242 from FA23-BCS-242"""
        match = re.search(r'(\d+)$', roll_no)
        return int(match.group(1)) if match else None

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
        """Add students based on roll number range"""
        start_num = extract_roll_suffix(start)
        end_num = extract_roll_suffix(end)

        if start_num is None or end_num is None:
            return {}

        for roll in ClassData.student_data:
            roll_normalized = roll.strip().upper()
            roll_num = extract_roll_suffix(roll_normalized)
            if roll_num is not None and start_num <= roll_num <= end_num:
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
        return {
            "gpa_counts": [above_3_5, above_3_0, above_2_5, above_2_0, below_2_0],
            "average_gpa": average_gpa,
            "average_cgpa": average_cgpa,
            "highest_gpa": highest_gpa,
            "highest_cgpa": highest_cgpa
        }


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


        if total_student > 0:
            passed_percentage = (passed / total_student) * 100
            std_dev = np.std(marks_std, ddof=1) if len(marks_std) > 1 else 0.0
        else:
            passed_percentage = 0.0
            std_dev = 0.0
        
        std_graph = Data.standard_deviation_plot(marks_std,f"{coursename} Marks Distribution")

        return {
            "course": coursename,
            "grades": {
                "A Grade": A_grade,
                "A- Grade": A_neg_grade,
                "B+ Grade": B_plus_grade,
                "B- Grade": B_neg_grade,
                "C+ Grade": C_plus_grade,
                "C- Grade": C_neg_grade,
                "D Grade": D_grade,
                "F Grade": F_grade,
            },
            "total_students": total_student,
            "passed": passed,
            "failed": F_grade,
            "passed_percentage": round(passed_percentage, 2),
            "standard_deviation": round(std_dev, 2)
            
        } , std_graph

if __name__ == "__main__":
    
    filepath = "" 
    Data.read_data(filepath)  
   