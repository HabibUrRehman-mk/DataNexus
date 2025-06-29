from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QFrame, QSizePolicy, QListWidget, QMessageBox
    
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



class HomeCard(QWidget):
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

        
        list_btn = QPushButton("Perform Analysis")
        list_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 10px;
                padding: 6px 20px;
            }
        """)
        
        list_btn.clicked.connect(self.on_analysis_clicked)

        
        input_layout.addStretch()
        input_layout.addStretch()
        input_layout.addWidget(list_btn)

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
        
        grid_layout.setColumnStretch(0, 2) 
        grid_layout.setColumnStretch(1, 2) 

        grid_layout.setRowStretch(0, 1)  
        grid_layout.setRowStretch(1, 1)  


        self.card3 = self.create_card()
        grid_layout.addWidget(self.card3, 1,0)
        
        self.card4 = self.create_card()
        grid_layout.addWidget(self.card4, 1,1)
        
        self.side_card = self.create_card(fixed_width=200, stretch_vertical=True)

        left_container = QWidget()
        left_container.setLayout(grid_layout)
        left_container.setStyleSheet("background-color: #f0f0f0;")

        card_area_layout.addWidget(left_container, 2)
        card_area_layout.addWidget(self.side_card, 1)

        main_layout.addLayout(card_area_layout)
        self.setLayout(main_layout)
    
    
    def on_analysis_clicked(self):
        try:
            if not hasattr(Data, 'students') or not Data.students:
                raise ValueError("No data file loaded. Please select a file first.")

            try:
                bar_fig, good, prb, dis, total, pie_fig = Data.student_status()
            except Exception as e:
                raise ValueError(f"Failed to process student status: {str(e)}")

            try:
                layout = self.card1.layout()
                clear_layout(layout)
                
                capsule_layout = QVBoxLayout()
                capsule_layout.setSpacing(5)

                capsules = [
                    ("Total Enrolled", total, "#DDEEFF"),
                    ("Good Standing", good, "#C8E6C9"),
                    ("Probation", prb, "#FFF9C4"),
                    ("Dismissed", dis, "#FFCDD2")
                ]

                for text, value, color in capsules:
                    capsule = QLabel(f"  {text}: {value}  ")
                    capsule.setStyleSheet(f"""
                        QLabel {{
                            border: 2px solid {color};
                            background-color: {color};
                            border-radius: 15px;
                            padding: 8px 16px;
                            font-family: Arial;
                            font-size: 18px;
                            font-weight: bold;
                        }}
                    """)
                    capsule.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
                    capsule_layout.addWidget(capsule)

                pie_canvas = FigureCanvas(pie_fig)
                right_widget = QWidget()
                right_widget.setLayout(capsule_layout)
                right_widget.setStyleSheet("background-color: white;")

                content_layout = QHBoxLayout()
                content_layout.setSpacing(20)
                content_layout.addWidget(pie_canvas)
                content_layout.addWidget(right_widget)
                layout.addLayout(content_layout)
            except Exception as e:
                raise ValueError(f"Error setting up status card: {str(e)}")

            try:
                layout2 = self.card2.layout()
                clear_layout(layout2)
                
                gpa_stats = Data.gpa_analysis()
                if not gpa_stats or "gpa_counts" not in gpa_stats:
                    raise ValueError("Invalid GPA analysis data")
                    
                gpa_counts = gpa_stats["gpa_counts"]
                gpa_graph = Data.plot_gpa_distribution(gpa_counts)
                gpa_canvas = FigureCanvas(gpa_graph)
                layout2.addWidget(gpa_canvas)
            except Exception as e:
                raise ValueError(f"Error setting up GPA distribution card: {str(e)}")

            try:
                layout3 = self.card3.layout()
                clear_layout(layout3)
                bar_canvas = FigureCanvas(bar_fig)
                layout3.addWidget(bar_canvas)
            except Exception as e:
                raise ValueError(f"Error setting up bar chart card: {str(e)}")

            try:
                layout4 = self.card4.layout()
                clear_layout(layout4)
                
                if not gpa_stats:
                    raise ValueError("No GPA stats available for gauge charts")
                    
                avg_gpa = round(gpa_stats.get('average_gpa', 0), 2)
                avg_cgpa = round(gpa_stats.get('average_cgpa', 0), 2)
                high_gpa = round(gpa_stats.get('highest_gpa', 0), 2)
                high_cgpa = round(gpa_stats.get('highest_cgpa', 0), 2)
                
                gauges = [
                    ("Average GPA", avg_gpa),
                    ("Average CGPA", avg_cgpa),
                    ("Highest GPA", high_gpa),
                    ("Highest CGPA", high_cgpa),
                ]

                gauge_grid = QGridLayout()
                gauge_grid.setSpacing(10)

                for i, (title, value) in enumerate(gauges):
                    fig = Data.guage_chart(title, value)
                    canvas = FigureCanvas(fig)
                    canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    gauge_grid.addWidget(canvas, i // 2, i % 2)

                layout4.addLayout(gauge_grid)
            except Exception as e:
                raise ValueError(f"Error setting up gauge charts: {str(e)}")

      
            try:
                layout5 = self.side_card.layout()
                clear_layout(layout5)
                
                if not hasattr(Data, 'all_courses') or not Data.all_courses:
                    raise ValueError("No course data available")
                    
                courses = Data.all_courses
                course_text = "<div align='center'><b>Course List</b><br><br>"
                for course in sorted(courses):
                    course_text += f"<p style='line-height: 150%; margin: 0;'>{course}</p>"
                course_text += "</div>"
                
                label = QLabel()
                label.setText(course_text)
                label.setWordWrap(True)
                label.setStyleSheet("font-family: Arial; font-size: 20px;")
                label.setAlignment(Qt.AlignTop)
                layout5.addWidget(label)
            except Exception as e:
                raise ValueError(f"Error setting up course list: {str(e)}")

        except Exception as e:
           
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setWindowTitle("Analysis Error")
            error_msg.setText("Failed to complete analysis")
            error_msg.setInformativeText(str(e))
            error_msg.setStandardButtons(QMessageBox.Ok)
            error_msg.exec_()

            for layout in [self.card1.layout(), self.card2.layout(), 
                        self.card3.layout(), self.card4.layout(), 
                        self.side_card.layout()]:
                clear_layout(layout)
                

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

    
    
