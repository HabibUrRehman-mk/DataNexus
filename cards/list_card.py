from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem,QHeaderView
from Data import Data  

class ResultListCard(QWidget):
    def __init__(self):
        super().__init__()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search by Roll No")
        self.search_box.textChanged.connect(self.filter_table)
        self.search_box.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid #aaa;
                padding: 8px;
                font-size: 16px;
            }
        """)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Roll No", "Name", "GPA", "CGPA", "Status"])
        self.table_widget.setSortingEnabled(True)
        
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                font-size: 18px;
                gridline-color: gray;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                color: black;
                font-size: 20px;
                padding: 6px;
                font-weight: bold;
                border: 1px solid #ccc;
            }
        """)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(self.search_box)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        self.load_data()
    
    def update_data(self):
        self.table_widget.setRowCount(0)

        
        data = Data.students
        self.table_widget.setRowCount(len(data))

        for row_index, (roll_no, student) in enumerate(data.items()):
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(roll_no))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(student["name"]))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(str(student["GPA"])))
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(str(student["CGPA"])))
            self.table_widget.setItem(row_index, 4, QTableWidgetItem(student["Status"]))
            
        #self.table_widget.resizeColumnsToContents()



    def load_data(self):
        data = Data.students

        self.table_widget.setRowCount(len(data))

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
            if item:
                self.table_widget.setRowHidden(row, search_text not in item.text().lower())
