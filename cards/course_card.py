from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QFrame, QSizePolicy, QListWidget, QListWidgetItem,QMessageBox
    
)
from Data import Data
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



from PyQt5.QtCore import Qt

def clear_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
            elif child_layout is not None:
                clear_layout(child_layout)


class CourseCard(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setStyleSheet("""
                           QWidget{
                               background-color: #f0f0f0;
                            }
                           """)
        

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        

        
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(15, 15, 15, 15)
        input_layout.setSpacing(10)

        subject_label = QLabel("Subject:")
        subject_label.setStyleSheet("background-color: #ffffff;")

        
        self.course_select = QComboBox()
        self.course_select.setFixedWidth(250)
        self.course_select.setStyleSheet("""                        
            QComboBox {
                padding: 6px;
                border-radius: 8px;
                background-color: #f0f0f0;
                color: black;
            }
        """)
        
        
       


        submit_btn = QPushButton("Submit")
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 10px;
                padding: 6px 20px;
            }
        """)
        failed_btn = QPushButton("Failed")
        failed_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 10px;
                padding: 6px 20px;
            }
        """)
        failed_btn.clicked.connect(self.show_failed_students)

        passed_btn = QPushButton("Passed")
        passed_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 10px;
                padding: 6px 20px;
            }
        """)
        passed_btn.clicked.connect(self.show_passed_students)

        submit_btn.clicked.connect(self.on_submit_clicked)
        

        input_layout.addWidget(subject_label)
       # input_layout.addWidget(self.subject_input)
        input_layout.addSpacing(10)
       # input_layout.addWidget(function_label)
        input_layout.addWidget(self.course_select)
        input_layout.addSpacing(10)
        input_layout.addWidget(submit_btn)
        input_layout.addStretch()
        input_layout.addWidget(failed_btn)
        input_layout.addWidget(passed_btn)

        main_layout.addLayout(input_layout)
        
       

        
        

      
        card_area_layout = QHBoxLayout()
        card_area_layout.setContentsMargins(15, 0, 15, 15)
        card_area_layout.setSpacing(15)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        # Card 1 
        
        self.card1 = self.create_card()
        self.card1_label = QLabel()
        self.card1_label.setWordWrap(True)
        self.card1.layout().addWidget(self.card1_label)

        # Card 2
        
        self.card2 = self.create_card()
        self.card2_label = QLabel()
        self.card2_label.setWordWrap(True)
        self.card2.layout().addWidget(self.card2_label)

        grid_layout.addWidget(self.card1, 0, 0)
        grid_layout.addWidget(self.card2, 0, 1)


        self.wide_card = self.create_card("Wide Card")
        grid_layout.addWidget(self.wide_card, 1, 0, 1, 2)


        self.side_card = self.create_card( fixed_width=400, stretch_vertical=True)

        left_container = QWidget()
        left_container.setLayout(grid_layout)
        left_container.setStyleSheet("background-color: #f0f0f0;")

        card_area_layout.addWidget(left_container, 2)
        card_area_layout.addWidget(self.side_card, 1)
        

        main_layout.addLayout(card_area_layout)
        self.setLayout(main_layout)
    

    def on_submit_clicked(self):
        try:

            if not hasattr(Data, 'students') or not Data.students:
                raise ValueError("No data file loaded. Please select a file first.")

            subject_text = self.course_select.currentText()
            if not subject_text:
                raise ValueError("No course selected. Please select a course from the dropdown.")

            try:
                stats_0 = Data.subject_stats(subject_text)
                grade_stats = Data.grade_distribution(subject_text)
                if not stats_0 or not grade_stats:
                    raise ValueError("Could not retrieve course statistics")
                stats = {**stats_0, **grade_stats}
            except Exception as e:
                raise ValueError(f"Error processing course data: {str(e)}")

            try:
                fig_donut = Data.create_donut_chart(stats)
                donut_canvas = FigureCanvas(fig_donut)

                layout = self.card1.layout()
                clear_layout(layout)

                layout.addWidget(donut_canvas)

                pill_data = [
                    ("Course", subject_text, "#0078D7", "#FFFFFF"),
                    ("Total Students", stats.get("total_students", "N/A"), "#FFB900", "#000000"),
                    ("Passed", stats.get("passed", "N/A"), "#107C10", "#FFFFFF"),
                    ("Failed", stats.get("failed", "N/A"), "#D83B01", "#FFFFFF"),
                    ("Average Marks", f"{stats.get('average_marks', 0):.2f}", "#5C2D91", "#FFFFFF"),
                ]

                pill_container = QVBoxLayout()
                pill_container.setSpacing(10)

                for label_text, value, bg_color, text_color in pill_data:
                    pill = QLabel(f"{label_text}: {value}")
                    pill.setStyleSheet(f"""
                        background-color: {bg_color};
                        color: {text_color};
                        font-family: Arial;
                        font-size: 18px;
                        padding: 6px 16px;
                        border-radius: 20px;
                        margin: 4px;
                    """)
                    pill.setAlignment(Qt.AlignCenter)
                    pill_container.addWidget(pill)

                layout.addLayout(pill_container)


            except Exception as e:
                raise ValueError(f"Error setting up course statistics: {str(e)}")


            try:
                grades = grade_stats.get("grades", {})
                layout2 = self.card2.layout()
                clear_layout(layout2)

                left_col = QVBoxLayout()
                right_col = QVBoxLayout()

                grade_keys = ["A Grade", "A- Grade", "B+ Grade", "B- Grade", 
                            "C+ Grade", "C- Grade", "D Grade", "F Grade"]

                for i, grade in enumerate(grade_keys):
                    label = QLabel(f"{grade:<3}: {grades.get(grade, 0)}")
                    label.setStyleSheet("font-family: Arial; font-size: 16px; font-weight: bold")
                    if i < 4:
                        left_col.addWidget(label)
                    else:
                        right_col.addWidget(label)

                grades_layout = QHBoxLayout()
                grades_layout.addLayout(left_col)
                grades_layout.addSpacing(20)
                grades_layout.addLayout(right_col)

                layout2.addLayout(grades_layout)
            except Exception as e:
                raise ValueError(f"Error setting up grade distribution: {str(e)}")

            try:
                fig = Data.standard_deviation(subject_text)
                if fig:
                    canvas = FigureCanvas(fig)
                    wide_layout = self.wide_card.layout()
                    clear_layout(wide_layout)
                    wide_layout.addWidget(canvas)
            except Exception as e:
                raise ValueError(f"Error setting up standard deviation chart: {str(e)}")


            try:
                self.show_failed_students()
            except Exception as e:
                raise ValueError(f"Error displaying failed students: {str(e)}")

        except Exception as e:

            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setWindowTitle("Submission Error")
            error_msg.setText("Failed to process course data")
            error_msg.setInformativeText(str(e))
            error_msg.setStandardButtons(QMessageBox.Ok)
            error_msg.exec_()
            
            for layout in [self.card1.layout(), self.card2.layout(), self.wide_card.layout()]:
                clear_layout(layout)
          
           
            
            
    def show_failed_students(self):
        try:
            if not hasattr(Data, 'students') or not Data.students:
                raise ValueError("No data file loaded. Please select a file first.")

            subject_text = self.course_select.currentText()
            if not subject_text:
                raise ValueError("No course selected. Please select a course from the dropdown.")

            try:
                failed_list = Data.failed_students(subject_text)
                if not isinstance(failed_list, list):
                    raise ValueError("Invalid data format for failed students")
            except Exception as e:
                raise ValueError(f"Failed to retrieve failed students: {str(e)}")

            layout = self.side_card.layout()
            clear_layout(layout)

            container = QWidget()
            container_layout = QVBoxLayout()
            container.setLayout(container_layout)

            title = QLabel(f"<b>Failed Students in {subject_text}</b>")
            title.setAlignment(Qt.AlignCenter)
            title.setStyleSheet("""
                font-size: 20px;
                padding: 8px 4px;
                margin-bottom: 10px;
                color: #e74c3c;
            """)
            container_layout.addWidget(title)

            list_widget = QListWidget()
        
            for student_id, name in failed_list:
                item = QListWidgetItem(f"{student_id}  -  {name}")
                list_widget.addItem(item)

            list_widget.setStyleSheet("""
                QListWidget {
                    font-size: 20px;
                    padding: 6px;
                }
                QListWidget::item:selected {
                    background-color: #F44336;
                    color: white;
                }
                QListWidget::item:hover {
                    background-color: #F44336;
                }
            """)

            container_layout.addWidget(list_widget)
            layout.addWidget(container)

        except Exception as e:
            
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Warning)
            error_msg.setWindowTitle("Failed Students Error")
            error_msg.setText("Could not display failed students")
            error_msg.setInformativeText(str(e))
            error_msg.exec_()

            layout = self.side_card.layout()
            clear_layout(layout)
           

    def show_passed_students(self):
        try:
          
            if not hasattr(Data, 'students') or not Data.students:
                raise ValueError("No data file loaded. Please select a file first.")

            subject_text = self.course_select.currentText()
            if not subject_text:
                raise ValueError("No course selected. Please select a course from the dropdown.")

            try:
                passed_list = Data.passed_students(subject_text)
                if not isinstance(passed_list, list):
                    raise ValueError("Invalid data format for passed students")
            except Exception as e:
                raise ValueError(f"Failed to retrieve passed students: {str(e)}")

            layout = self.side_card.layout()
            clear_layout(layout)

            container = QWidget()
            container_layout = QVBoxLayout()
            container.setLayout(container_layout)

            title = QLabel(f"<b>Passed Students in {subject_text}</b>")
            title.setAlignment(Qt.AlignCenter)
            title.setStyleSheet("""
                font-size: 20px;
                padding: 8px 4px;
                margin-bottom: 10px;
                color: #009100;
            """)
            container_layout.addWidget(title)
            list_widget = QListWidget()
            
            
            for student_id, name in passed_list:
                item = QListWidgetItem(f"{student_id}  -  {name}")
                list_widget.addItem(item)

            list_widget.setStyleSheet("""
                QListWidget {
                    font-size: 20px;
                    padding: 6px;
                }
                QListWidget::item:selected {
                    background-color: #4CAF50;
                    color: white;
                }
                QListWidget::item:hover {
                    background-color: #4CAF50;
                }
            """)

            container_layout.addWidget(list_widget)
            layout.addWidget(container)

        except Exception as e:
            
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Warning)
            error_msg.setWindowTitle("Passed Students Error")
            error_msg.setText("Could not display passed students")
            error_msg.setInformativeText(str(e))
            error_msg.exec_()

           
            layout = self.side_card.layout()
            clear_layout(layout)
            

    
    def update_courses(self):
        #print("Updating combo box with:", Data.all_courses)
        self.course_select.clear()
        self.course_select.addItems(sorted(Data.all_courses))


    def create_card(self, title=None, fixed_width=None, stretch_vertical=False):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 14px;
                border: 1px solid #dddddd;
            }
        """)
        if fixed_width:
            card.setFixedWidth(fixed_width)
        if stretch_vertical:
            card.setMinimumHeight(300)
            card.setSizePolicy(card.sizePolicy().horizontalPolicy(), QSizePolicy.Expanding)

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)

        if title:  
            label = QLabel(title)
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

        card.setLayout(layout)
        return card

    
    
