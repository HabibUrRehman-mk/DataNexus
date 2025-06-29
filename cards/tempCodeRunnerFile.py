                clear_layout(layout)

                layout.addWidget(donut_canvas)

                pill_data = [
                    ("Course", subject_text, "#0078D7", "#FFFFFF"),
                    ("Total Students", stats.get("total_students", "N/A"), "#FFB900", "#000000"),
                    ("Passed", stats.get("passed", "N/A"), "#107C10", "#FFFFFF"),
                    ("Failed", stats.get("failed", "N/A"), "#D83B01", "#FFFFFF"),
                    ("Average Marks", f"{stats.get('average_marks', 0):.2f}", "#5C2D91", "#FFFFFF"),
                ]

                pill_container = QHBoxLayout()
                pill_container.setSpacing(10)

                for label_text, value, bg_color, text_color in pill_data:
                    pill = QLabel(f"{label_text}: {value}")
                    pill.setStyleSheet(f"""
                        background-color: {bg_color};
                        color: {text_color};
                        font-family: Arial;
                        font-size: 14px;
                        padding: 6px 16px;
                        border-radius: 20px;
                    """)
                    pill_container.addWidget(pill)

                pill_wrapper = QVBoxLayout()
                pill_wrapper.addSpacing(10)
                pill_wrapper.addLayout(pill_container)
                pill_wrapper.addSpacing(10)

                layout.addLayout(pill_wrapper)