from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QFrame, QSizePolicy, QMessageBox
    
)
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import Qt
from Data import Data
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas




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


class ProfileCard(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setStyleSheet("""
                           QWidget{
                               background-color: #f0f0f0;
                            }
                           """)

       
        main_layout = QVBoxLayout()
        self.student_window = None 
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        

        # === Input Panel ===
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(15, 15, 15, 15)
        input_layout.setSpacing(10)

        subject_label = QLabel("Search:")
        subject_label.setStyleSheet("background-color: #ffffff;")
        
        
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Enter Roll No")
        self.subject_input.setFixedWidth(250)
        self.subject_input.setStyleSheet("""                        
            QLineEdit {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 6px;
            }
        """)


        search_btn = QPushButton("Search")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 10px;
                padding: 6px 20px;
            }
        """)
        search_btn.clicked.connect(self.on_search_clicked)


        input_layout.addWidget(subject_label)
        input_layout.addWidget(self.subject_input)
        input_layout.addSpacing(10)
      
        input_layout.addSpacing(10)
        input_layout.addWidget(search_btn)
        input_layout.addStretch()
        input_layout.addStretch()

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


        self.card3 = self.create_card()
        self.card3.setMaximumWidth(800)
        grid_layout.addWidget(self.card3, 1,0)
        
        self.card4 = self.create_card("Card 4")
        grid_layout.addWidget(self.card4, 1,1)
        

        left_container = QWidget()
        left_container.setLayout(grid_layout)
        left_container.setStyleSheet("background-color: #f0f0f0;")

        card_area_layout.addWidget(left_container, 2)
        # card_area_layout.addWidget(side_card, 1)
        

        main_layout.addLayout(card_area_layout)
        self.setLayout(main_layout)


            
    def on_search_clicked(self):
        try:
           
            roll_no = self.subject_input.text().upper().strip()
            if not roll_no:
                raise ValueError("Please enter a roll number to search")

            if not hasattr(Data, 'students') or not Data.students:
                raise ValueError("No student data available. Please load data first.")

            result = Data.search_student(roll_no)
            if not result:
                raise ValueError(f"No student found with roll number: {roll_no}")

            try:
                rank = Data.get_rank(roll_no)
                gpa_stats = Data.gpa_analysis()
            except Exception as e:
                raise ValueError(f"Could not retrieve ranking or GPA statistics: {str(e)}")

            required_fields = ['name', 'GPA', 'CGPA', 'Status', 'courses']
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"Missing required student data field: {field}")

            try:
                for layout in [self.card1.layout(), self.card2.layout(), 
                            self.card3.layout(), self.card4.layout()]:
                    clear_layout(layout)

                capsule_layout = QVBoxLayout()
                capsule_layout.setSpacing(15)
                capsule_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
                
                capsules = [
                    (f"Name: {result['name']}", "#DDEEFF", "#003366"),
                    (f"GPA: {result['GPA']}", "#E6FFCC", "#336600"),
                    (f"CGPA: {result['CGPA']}", "#FFE6E6", "#990000"),
                    (f"Rank: {rank}", "#FFF3CD", "#8A6D3B"),
                    (f"Status: {result['Status']}", "#CCE5FF", "#004085")
                ]


                capsule_widgets = []
                max_width = 0

                for text, bg, fg in capsules:
                    label = QLabel(text)
                    label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
                    label.setAlignment(Qt.AlignCenter)
                    label.setStyleSheet(f"""
                        background-color: {bg};
                        color: {fg};
                        font-size: 18px;
                        font-weight: bold;
                        border-radius: 20px;
                        padding: 8px 20px;
                    """)
                    label.adjustSize()
                    max_width = max(max_width, label.sizeHint().width())
                    capsule_widgets.append(label)

                
                for label in capsule_widgets:
                    label.setMinimumWidth(max_width)
                    capsule_layout.addWidget(label)

                self.card1.layout().addLayout(capsule_layout)

                try:
                    prev_gpa = ((result['CGPA']*2)-result['GPA']) if result['CGPA'] and result['GPA'] else 0
                    fig2 = Data.plot_gpa_progress(result['GPA'], prev_gpa)
                    graph2 = FigureCanvas(fig2)
                    self.card2.layout().addWidget(graph2)
                except Exception as e:
                    raise ValueError(f"Could not create GPA progress chart: {str(e)}")

                try:
                    gauge_grid = QGridLayout()
                    gauge_grid.setSpacing(10)

                    avg_gpa = round(gpa_stats['average_gpa'], 2) if 'average_gpa' in gpa_stats else 0
                    avg_cgpa = round(gpa_stats['average_cgpa'], 2) if 'average_cgpa' in gpa_stats else 0
                    stu_gpa = round(result['GPA'], 2) if result['GPA'] else 0
                    stu_cgpa = round(result['CGPA'], 2) if result['CGPA'] else 0

                    gauges = [
                        ("Batch Average GPA", avg_gpa),
                        ("Student GPA", stu_gpa),
                        ("Batch Average CGPA", avg_cgpa),
                        ("Student CGPA", stu_cgpa),
                    ]

                    for i, (title, value) in enumerate(gauges):
                        fig = Data.guage_chart(title, value)
                        canvas = FigureCanvas(fig)
                        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                        gauge_grid.addWidget(canvas, i // 2, i % 2)

                    self.card3.layout().addLayout(gauge_grid)
                except Exception as e:
                    raise ValueError(f"Could not create gauge charts: {str(e)}")

                try:
                    fig = Data.plot_student_marks(result)
                    graph = FigureCanvas(fig)
                    self.card4.layout().addWidget(graph)
                except Exception as e:
                    raise ValueError(f"Could not create marks chart: {str(e)}")

            except Exception as e:
                raise ValueError(f"Error displaying student data: {str(e)}")

        except ValueError as e:

            for layout in [self.card1.layout(), self.card2.layout(),
                        self.card3.layout(), self.card4.layout()]:
                clear_layout(layout)

            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Warning)
            error_msg.setWindowTitle("Search Error")
            error_msg.setText("Could not complete search")
            error_msg.setInformativeText(str(e))
            error_msg.exec_()

            error_label = QLabel(f"<span style='color:red; font-size: 16px;'>{str(e)}</span>")
            error_label.setAlignment(Qt.AlignCenter)
            self.card1.layout().addWidget(error_label)
        
     

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

