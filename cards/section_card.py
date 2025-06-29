from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QComboBox, QVBoxLayout, QHBoxLayout,
    QFrame, QSizePolicy, QScrollArea, QLineEdit, QMessageBox, QLayout, QGridLayout
)
from PyQt5.QtCore import Qt
from Data import Data
from Data import ClassData
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class SectionComparisonCard(QWidget):
    def __init__(self):
        super().__init__()
        self.section_1 = {}
        self.section_2 = {}
        self.setStyleSheet("background-color: #f0f0f0;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

       # === Input Panel ===
        input_panel_layout = QHBoxLayout()
        input_panel_layout.setContentsMargins(15, 15, 15, 15)
        input_panel_layout.setSpacing(30)

        # Left Input Panel
        left_input_layout = QHBoxLayout()
        left_input_layout.setSpacing(10)
        left_input_layout.setAlignment(Qt.AlignLeft)

        left_text_field = QLineEdit()  
        left_text_field.setFixedWidth(350)
        left_text_field.setPlaceholderText("Enter range OR Student")
        left_input_layout.addWidget(left_text_field)
        left_add_button = QPushButton("Add")
        left_add_button.setFixedSize(90, 30)
        left_add_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 10px;
                padding: 6px 20px;
            }
        """)
        left_input_layout.addWidget(left_add_button)
        self.left_class_data = ClassData("Left")
        ClassData.clone_data()
        self.left_text_field = left_text_field  # Save reference
        left_add_button.clicked.connect(self.handle_left_add)


        # Right Input Panel
        right_input_layout = QHBoxLayout()
        right_input_layout.setSpacing(10)
        right_input_layout.setAlignment(Qt.AlignRight)

        right_text_field = QLineEdit() 
        right_text_field.setPlaceholderText("Enter range OR Student")
        right_text_field.setFixedWidth(350)
        right_input_layout.addWidget(right_text_field)

        right_add_button = QPushButton("Add")
        right_add_button.setFixedSize(90, 30)
        right_add_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 10px;
                padding: 6px 20px;
            }
        """)
        right_input_layout.addWidget(right_add_button)
        self.right_class_data = ClassData("Right")
        ClassData.clone_data()
        self.right_text_field = right_text_field  
        right_add_button.clicked.connect(self.handle_right_add)
        
        right_input_layout.addWidget(QLabel("Subject:"))
        self.course_select = QComboBox()
        self.course_select.setFixedWidth(150)
        self.course_select.setStyleSheet("""                        
            QComboBox {
                padding: 6px;
                border-radius: 8px;
                background-color: #f0f0f0;
                color: black;
            }
        """)
        right_input_layout.addWidget(self.course_select)
        compare_btn = QPushButton("Compare")
        compare_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 10px;
                padding: 6px 20px;
            }
        """)
        compare_btn.clicked.connect(self.handle_compare_clicked)

        
        input_panel_layout.addLayout(left_input_layout)
        input_panel_layout.addSpacing(50)
        input_panel_layout.addWidget(compare_btn)
        input_panel_layout.addSpacing(60)
        input_panel_layout.addLayout(right_input_layout)

        main_layout.addLayout(input_panel_layout)


        #  Scroll 
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        scroll_content = QWidget()
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(30)

        # Left Cards
        layout1 = QVBoxLayout()
        layout1.setSpacing(15)
        
        self.card1 = self.create_card(stretch_vertical=True)
        self.card1.setMinimumHeight(400)
        self.card1_label = QLabel()
        self.card1_label.setWordWrap(True)
        self.card1.layout().addWidget(self.card1_label)
        
        self.card2 = self.create_card(stretch_vertical=True)
        self.card2.setMinimumHeight(400)
        self.card2_label = QLabel()
        self.card2_label.setWordWrap(True)
        self.card2.layout().addWidget(self.card2_label)
        
        self.card3 = self.create_card(stretch_vertical=True)
        self.card3.setMinimumHeight(400)
        self.card3_label = QLabel()
        self.card3_label.setWordWrap(True)
        self.card3.layout().addWidget(self.card3_label)
        
        self.card4 = self.create_card(stretch_vertical=True)
        self.card4.setMinimumHeight(400)
        self.card4_label = QLabel()
        self.card4_label.setWordWrap(True)
        self.card4.layout().addWidget(self.card4_label)
        
        
        self.card5 = self.create_card(stretch_vertical=True)
        self.card5.setMinimumHeight(400)
        self.card5_label = QLabel()
        self.card5_label.setWordWrap(True)
        self.card5.layout().addWidget(self.card5_label)
        
        # self.card6 = self.create_card(stretch_vertical=True)
        # self.card6_label = QLabel()
        # self.card6_label.setWordWrap(True)
        # self.card6.layout().addWidget(self.card6_label)
        
        layout1.setSpacing(10)
        layout1.addWidget(self.card1)
        layout1.addWidget(self.card2)
        layout1.addWidget(self.card3)
        layout1.addWidget(self.card4)
        layout1.addWidget(self.card5)
        #layout1.addWidget(self.card6)
        layout1.addStretch()
        
       

       
        divider = QFrame()
        divider.setFixedWidth(3)
        divider.setStyleSheet("background-color: black;")

        # Right Cards
        self.card7= self.create_card(stretch_vertical=True)
        self.card7.setMinimumHeight(400)
        self.card7_label = QLabel()
        self.card7_label.setWordWrap(True)
        self.card7.layout().addWidget(self.card7_label)
        
        self.card8= self.create_card(stretch_vertical=True)
        self.card8.setMinimumHeight(400)
        self.card8_label = QLabel()
        self.card8_label.setWordWrap(True)
        self.card8.layout().addWidget(self.card8_label)
        
        self.card9= self.create_card(stretch_vertical=True)
        self.card9.setMinimumHeight(400)
        self.card9_label = QLabel()
        self.card9_label.setWordWrap(True)
        self.card9.layout().addWidget(self.card9_label)
        
        self.card10= self.create_card(stretch_vertical=True)
        self.card10.setMinimumHeight(400)
        self.card10_label = QLabel()
        self.card10_label.setWordWrap(True)
        self.card10.layout().addWidget(self.card10_label)
        
        self.card11= self.create_card(stretch_vertical=True)
        self.card11.setMinimumHeight(400)
        self.card11_label = QLabel()
        self.card11_label.setWordWrap(True)
        self.card11.layout().addWidget(self.card11_label)
        
        # self.card12= self.create_card(stretch_vertical=True)
        # self.card12_label = QLabel()
        # self.card12_label.setWordWrap(True)
        # self.card12.layout().addWidget(self.card12_label)
        
        
        
        layout2 = QVBoxLayout()
        layout2.setSpacing(10)
        layout2.addWidget(self.card7)
        layout2.addWidget(self.card8)
        layout2.addWidget(self.card9)
        layout2.addWidget(self.card10)
        layout2.addWidget(self.card11)
       # layout2.addWidget(self.card12)
        layout1.addStretch()
        

        content_layout.addLayout(layout1)
        content_layout.addWidget(divider)
        content_layout.addLayout(layout2)

        scroll_content.setLayout(content_layout)
        scroll_area.setWidget(scroll_content)

        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
    
    def handle_left_add(self):
        try:
           
            if not hasattr(Data, 'students') or not Data.students:
                QMessageBox.critical(self, "Data Error", "No student data loaded. Please upload a file first.")
                return

            text = self.left_text_field.text().upper().strip()
            ClassData.clone_data()
            if not text:
                QMessageBox.warning(self, "Input Error", "Please enter a roll number or range.")
                return

            try:
                if '-' in text and ' - ' in text:
                    
                    parts = text.split(' - ')
                    if len(parts) != 2:
                        raise ValueError("Invalid range format")
                    start, end = parts[0].strip(), parts[1].strip()
                    students = self.left_class_data.add_by_range(start, end)
                    if not students:
                        QMessageBox.information(self, "No Match", "No students found in this range.")
                    else:
                        QMessageBox.information(self, "Success", f"Added {len(students)} students.")
                else:
                   
                    students = self.left_class_data.add_student(text)
                    
                    if text not in self.left_class_data.students:
                        QMessageBox.information(self, "Not Found", "Roll number not found.")
                    else:
                        QMessageBox.information(self, "Success", f"Student {text} added.")
                    
                # for student in self.left_class_data.students:
                #print(self.left_class_data.students)


            except Exception as e:
                QMessageBox.critical(self, "Error", f"Invalid input: {e}")
            
        
            self.section_1 = self.left_class_data.students
        
        except Exception as e:
            QMessageBox.critical(self, "System Error", f"Initialization failed: {str(e)}")
    
    def handle_right_add(self):
        try:
            
            if not hasattr(Data, 'students') or not Data.students:
                QMessageBox.critical(self, "Data Error", "No student data loaded. Please upload a file first.")
                return

            text = self.right_text_field.text().strip()
            ClassData.clone_data()
            if not text:
                QMessageBox.warning(self, "Input Error", "Please enter a roll number or range.")
                return

            try:
                if '-' in text and ' - ' in text:
                    parts = text.split(' - ')
                    if len(parts) != 2:
                        raise ValueError("Invalid range format")
                    start, end = parts[0].strip(), parts[1].strip()
                    students = self.right_class_data.add_by_range(start, end)
                    if not students:
                        QMessageBox.information(self, "No Match", "No students found in this range.")
                    else:
                        QMessageBox.information(self, "Success", f"Added {len(students)} students.")
                else:
                    students = self.right_class_data.add_student(text)
                    if text not in self.right_class_data.students:
                        QMessageBox.information(self, "Not Found", "Roll number not found.")
                    else:
                        QMessageBox.information(self, "Success", f"Student {text} added.")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Invalid input: {e}")
            
            self.section_2 = self.right_class_data.students
        except Exception as e:
            QMessageBox.critical(self, "System Error", f"Initialization failed: {str(e)}")
    

    def create_input_panel(self, title):
        layout = QVBoxLayout()
        layout.setSpacing(6)

        section_label = QLabel(f"<b>{title}</b>")
        section_label.setStyleSheet("font-size: 16px;")

        range_label = QLabel("Select Range")
        add_button = QPushButton("Add")
        subject_label = QLabel("Subject:")
        combo_box = QComboBox()
        combo_box.addItems(["Math", "Physics", "CS", "English"])  # Sample data

        for widget in [range_label, add_button, subject_label, combo_box]:
            widget.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                }
                QPushButton {
                    background-color: black;
                    color: white;
                    border-radius: 8px;
                    padding: 4px 10px;
                }
                QComboBox {
                    background-color: white;
                    padding: 4px;
                    border: 1px solid #ccc;
                    border-radius: 6px;
                }
            """)

        layout.addWidget(section_label)
        layout.addWidget(range_label)
        layout.addWidget(add_button)
        layout.addWidget(subject_label)
        layout.addWidget(combo_box)

        return layout


    def update_courses(self):
        self.course_select.clear()
        self.course_select.addItem("")
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

        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

        if fixed_width:
            card.setFixedWidth(fixed_width)

        if stretch_vertical:
            card.setMinimumHeight(300)  
            card.setSizePolicy(card.sizePolicy().horizontalPolicy(), QSizePolicy.Expanding)

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)  

        if title:
            label = QLabel(title)
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

        card.setLayout(layout)
        return card


    def handle_compare_clicked(self):
        if not hasattr(self, 'left_class_data') or not hasattr(self, 'right_class_data'):
            QMessageBox.warning(self, "Comparison Error", 
                            "Both classes must be loaded before comparing.")
            return
            
        if not self.left_class_data or not self.right_class_data:
            QMessageBox.warning(self, "Comparison Error", 
                            "Both classes must have data before comparing.")
            return
            
        try:
            self.clear_card(self.card1)
            self.clear_card(self.card7)
            self.clear_card(self.card2)
            self.clear_card(self.card8)

            left_status = self.left_class_data.student_status()   
            right_status = self.right_class_data.student_status()
            
            if not all(key in left_status for key in ['Enrolled students', 'Dismissed students', 
                                                    'Probation students', 'Good students']):
                raise ValueError("Left class student status data is incomplete")
                
            if not all(key in right_status for key in ['Enrolled students', 'Dismissed students', 
                                                    'Probation students', 'Good students']):
                raise ValueError("Right class student status data is incomplete")

            
            left_bar = Data.student_status_barchart(
                left_status['Enrolled students'],left_status['Dismissed students'],left_status['Probation students'],left_status['Good students'])
            right_bar = Data.student_status_barchart(
                right_status['Enrolled students'],right_status['Dismissed students'],right_status['Probation students'],right_status['Good students'] )
            
            left_bar_canvas = FigureCanvas(left_bar)
            left_bar_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            left_bar_canvas.setMinimumHeight(250)
            right_bar_canvas = FigureCanvas(right_bar)
            
            left_gpa_stats = self.left_class_data.gpa_analysis()
            right_gpa_stats = self.right_class_data.gpa_analysis()
            

            if not left_gpa_stats or not right_gpa_stats:
                raise ValueError("Missing GPA analysis data")
                
            left_gpa_counts = left_gpa_stats.get("gpa_counts", {})
            right_gpa_counts = right_gpa_stats.get("gpa_counts", {})

            left_graph = Data.plot_gpa_distribution(left_gpa_counts)
            right_graph = Data.plot_gpa_distribution(right_gpa_counts)
            
            gpa_left_canvas = FigureCanvas(left_graph)
            gpa_right_canvas = FigureCanvas(right_graph)
            
            grid_layout = QGridLayout()
            self.replace_card_layout(self.card3, grid_layout)
            chart_data = [
                ("Average GPA", round(left_gpa_stats.get('average_gpa', 0), 2)),
                ("Average CGPA", round(left_gpa_stats.get('average_cgpa', 0), 2)),
                ("Highest GPA", round(left_gpa_stats.get('highest_gpa', 0))),
                ("Highest CGPA", round(left_gpa_stats.get('highest_cgpa', 0))),
            ]
            
            for i, (title, value) in enumerate(chart_data):
                fig = Data.guage_chart(title, value)
                canvas = FigureCanvas(fig)
                canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                row = i // 2
                col = i % 2
                grid_layout.addWidget(canvas, row, col)

            grid_layout2 = QGridLayout()
            self.replace_card_layout(self.card9, grid_layout2)
            chart_data = [
                ("Average GPA", round(right_gpa_stats.get('average_gpa', 0), 2)),
                ("Average CGPA", round(right_gpa_stats.get('average_cgpa', 0), 2)),
                ("Highest GPA", round(right_gpa_stats.get('highest_gpa', 0))),
                ("Highest CGPA", round(right_gpa_stats.get('highest_cgpa', 0))),
            ]
            
            for i, (title, value) in enumerate(chart_data):
                fig = Data.guage_chart(title, value)
                canvas = FigureCanvas(fig)
                row = i // 2
                col = i % 2
                grid_layout2.addWidget(canvas, row, col)
            
            
            self.card2.layout().addWidget(gpa_left_canvas)
            self.card8.layout().addWidget(gpa_right_canvas)
            self.card1.layout().addWidget(left_bar_canvas)
            self.card7.layout().addWidget(right_bar_canvas)
                
            
            if self.course_select.currentText() != "":
                self.clear_card(self.card4)
                self.clear_card(self.card10)
                self.clear_card(self.card5)
                self.clear_card(self.card11)
                
                subject = self.course_select.currentText().strip()
                
                try:
                    left_stats, left_plot = self.left_class_data.grade_distribution(subject)
                    right_stats, right_plot = self.right_class_data.grade_distribution(subject)

                    self.populate_card(self.card5, left_stats)
                    self.populate_card(self.card11, right_stats)
                    
                    left_canvas = FigureCanvas(left_plot)
                    right_canvas = FigureCanvas(right_plot)
                    
                    self.card4.layout().addWidget(left_canvas)
                    self.card10.layout().addWidget(right_canvas)
                except Exception as e:
                    QMessageBox.warning(self, "Course Comparison Error", 
                                    f"Failed to compare course data: {str(e)}")
                    
        except Exception as e:
            QMessageBox.critical(self, "Comparison Error", 
                            f"An error occurred during comparison: {str(e)}")
            self.clear_all_comparison_cards()
            
    
    def clear_all_comparison_cards(self):
        cards = [self.card1, self.card2, self.card3, self.card4, self.card5,
                self.card7, self.card8, self.card9, self.card10, self.card11]
        for card in cards:
            self.clear_card(card)        
            

    def replace_card_layout(self, card: QFrame, new_layout: QLayout):
        old_layout = card.layout()
        if old_layout is not None:
            
            while old_layout.count():
                item = old_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
            
            QWidget().setLayout(old_layout)  

        card.setLayout(new_layout)

    def populate_card(self, card: QFrame, data: dict):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)

        def create_item_label(text):
            if "Passed:" in text or "A Grade" in text:
                bg_color = "#d4edda"  # light green
                text_color = "#155724"
            elif "Failed:" in text or "F Grade" in text:
                bg_color = "#f8d7da"  # light red
                text_color = "#721c24"
            else:
                bg_color = "#f0f4f8"  # default light gray
                text_color = "#333333"

            label = QLabel(text)
            label.setStyleSheet(f"""
                QLabel {{
                    background-color: {bg_color};
                    border-radius: 8px;
                    padding: 6px 12px;
                    font-size: 12pt;
                    color: {text_color};
                }}
            """)
            return label


        # Column 1
        col1 = QVBoxLayout()
        col1.setSpacing(8)
        for text in [
            f"Total Students: {data['total_students']}",
            f"Passed: {data['passed']}",
            f"Failed: {data['failed']}",
            f"Passed %: {data['passed_percentage']}%",
        ]:
            col1.addWidget(create_item_label(text))

        # Column 2
        col2 = QVBoxLayout()
        col2.setSpacing(8)
        grades = list(data["grades"].items())
        for i in range(4):
            col2.addWidget(create_item_label(f"{grades[i][0]}: {grades[i][1]}"))

        # Column 3
        col3 = QVBoxLayout()
        col3.setSpacing(8)
        for i in range(4, 8):
            col3.addWidget(create_item_label(f"{grades[i][0]}: {grades[i][1]}"))

        layout.addLayout(col1)
        layout.addLayout(col2)
        layout.addLayout(col3)

        self.replace_card_layout(card, layout)

    
    def clear_card(self, card):
        layout = card.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()