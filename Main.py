# main.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QSizePolicy, QStackedWidget, QPushButton, QFileDialog,QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Data import Data

from cards.home_card import HomeCard
from cards.course_card import CourseCard
from cards.profile_card import ProfileCard
from cards.section_card import SectionComparisonCard
from cards.list_card import ResultListCard




class IconButton(QWidget):
    def __init__(self, icon_path, text):
        super().__init__()
        self.text = text  
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel()
        pixmap = QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("color: white;")

        layout.addWidget(icon_label)
        layout.addWidget(text_label)

        self.setLayout(layout)

        
        self.mouseReleaseEvent = self.on_click
        self.clicked = lambda: None

    def on_click(self, event):
        self.clicked()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Nexus")
        self.setStyleSheet("background-color: white;")
        

        self.stack = QStackedWidget()
        self.button_info = [
            ("graph.jpg", "Batch", HomeCard),
            ("book.jpg", "Course", CourseCard),
            ("profile.jpg", "Profile", ProfileCard),
            ("section.png", "Section", SectionComparisonCard),
            ("icon.png", "List", ResultListCard)
        ]



        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = self.create_sidebar()
        content = self.create_content()

        root_layout.addWidget(sidebar)
        root_layout.addWidget(content)
        

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: black;")
        sidebar.setFixedWidth(120)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        logo_label = QLabel()
        logo_pixmap = QPixmap("dn.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        self.cards = {}

        for index, (icon, name, card_cls) in enumerate(self.button_info):
            btn = IconButton(icon, name)
            btn.clicked = lambda i=index: self.switch_page(i)
            layout.addWidget(btn)

            card_instance = card_cls()
            self.cards[name.lower()] = card_instance
            self.stack.addWidget(card_instance)



        sidebar.setLayout(layout)
        return sidebar

    def create_content(self):
        content_frame = QFrame()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        header = QFrame()
        header.setStyleSheet("""
            background-color: #ffffff;
            border-bottom: 3px solid black;
        """)
        header.setFixedHeight(80)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 10, 10, 0)
        header_layout.setSpacing(10)

        header_label = QLabel("Data Nexus")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        header_label.setFont(font)
        header_label.setStyleSheet("""
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        """)
        header_layout.addWidget(header_label)
        
        

        header_layout.addStretch() 

        choose_file_btn = QPushButton("Choose File")
        choose_file_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 10px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)
        choose_file_btn.clicked.connect(self.choose_file)
        header_layout.addWidget(choose_file_btn)

        header.setLayout(header_layout)

        layout.addWidget(header)
        layout.addWidget(self.stack)
        content_frame.setLayout(layout)
        return content_frame
    
    def show_message(self, title, message, icon):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    def choose_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "",
            "Excel Files (*.xlsx);;All Files (*)",
            options=options
        )

        if file_path:
            print("Selected file path:", file_path)
            if not file_path.lower().endswith('.xlsx'):
                self.show_error_message("Invalid Format", "Only Excel files (.xlsx) are supported.")
                return

            try:
                Data.read_data(file_path)
                print("File read successfully")
                self.cards["course"].update_courses()
                self.cards["section"].update_courses()
                self.cards["list"].update_data()
                

                

                
            except Exception as e:
                print("Error while reading data:", e)
                
                self.show_error_message("File Error", "The selected file could not be read.\n" + str(e))


    def show_error_message(self, title, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
                

            



    def switch_page(self, index):
        self.stack.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
