import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import openpyxl
import re
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QLineEdit

class Data:
    students = {}  

    @staticmethod
    def read_data(filepath):
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

            if status == "RL":
                continue

            courses = {}

            for col in range(2, len(rows[i]) - 3):  
                course = str(rows[i][col])  
                marks = rows[i + 1][col]  

                if course == "--" or not course or "Unnamed" in course:
                    continue

                clean_course = clean_course_name(course)

                if re.match(r"^[A-Z]+[0-9]+$", clean_course):  
                    courses[clean_course] = marks

            Data.students[roll_no] = {
                "name": name,
                "courses": courses,
                "GPA": gpa,
                "CGPA": cgpa,
                "Status": status
            }


    

def initUI(self):
    central_widget = QWidget(self)
    self.setCentralWidget(central_widget)

    layout = QVBoxLayout()
    central_widget.setLayout(layout)

    self.search_box = QLineEdit()
    self.search_box.setPlaceholderText("Search by Roll No")
    self.search_box.textChanged.connect(self.filter_table)
    layout.addWidget(self.search_box)
    self.table_widget = QTableWidget()
    layout.addWidget(self.table_widget)
    self.load_data()


class StudentTable(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Data Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()



    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search by Roll No")
        self.search_box.textChanged.connect(self.filter_table)
        layout.addWidget(self.search_box)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        self.load_data()

    def load_data(self):
        data = Data.students

        if not data:
            return

        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(5)  
        self.table_widget.setHorizontalHeaderLabels(["Roll No", "Name", "GPA", "CGPA", "Status"])
        self.table_widget.setSortingEnabled(True)


        for row_index, (roll_no, student) in enumerate(data.items()):
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(roll_no))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(student["name"]))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(str(student["GPA"])))
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(str(student["CGPA"])))
            self.table_widget.setItem(row_index, 4, QTableWidgetItem(student["Status"]))

    
    def filter_table(self):
        search_text = self.search_box.text().strip().lower()

        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, 0) 
            self.table_widget.setRowHidden(row, search_text not in item.text().lower())
        

if __name__ == "__main__":
    filepath = "FA23-BCS-3.xlsx"
    Data.read_data(filepath)

    app = QApplication(sys.argv)
    window = StudentTable()
    window.show()
    sys.exit(app.exec())
