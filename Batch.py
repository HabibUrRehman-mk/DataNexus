# import Data

# class Batch:
#     def Batch(filepath):
#         Data.read_data(filepath)

        

# import plotly.graph_objects as go

# fig = go.Figure(go.Indicator(
#     mode = "gauge+number",
#     value = 270,
#     gauge = {
#         'axis': {'range': [None, 500]},
#         'bar': {'color': "darkblue"},
#     }
# ))

# fig.update_layout(
#     title = {'text': "Speedometer"},
#     height=400
# )

# fig.show()



# import plotly.graph_objects as go

# # cgpa_value = 3.2  # Change this value to test different CGPAs



# def gpa_chart(cgpa_value):
#     fig = go.Figure(go.Indicator(
#     mode = "gauge+number",
#     value = cgpa_value,
#     gauge = {
#         'axis': {'range': [0, 4], 'tickwidth': 1, 'tickcolor': "darkgray"},
#         'bar': {'color': "black"},
#         'steps': [
#             {'range': [0.0, 1.0], 'color': "darkred"},
#             {'range': [1.0, 2.0], 'color': "red"},
#             {'range': [2.0, 3.0], 'color': "orange"},
#             {'range': [3.0, 3.55], 'color': "yellowgreen"},
#             {'range': [3.55, 4.0], 'color': "green"}
#         ],
#         'threshold': {
#             'line': {'color': "black", 'width': 4},
#             'thickness': 0.75,
#             'value': cgpa_value
#         }
#     }
# ))

#     fig.update_layout(
#         title = {'text': "CGPA Gauge"},
#         height=400
#     )

#     fig.show()

# gpa_chart(3.45)



import plotly.graph_objects as go
import plotly.io as pio

def gpa_chart(cgpa_value):
    # Configure to display in IDE (try different renderers if needed)
    pio.renderers.default = "vscode"  # Alternatives: "svg", "notebook", "vscode"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=cgpa_value,
        number={'font': {'size': 40}},
        gauge={
            'axis': {'range': [0, 4], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0.0, 1.0], 'color': "darkred"},
                {'range': [1.0, 2.0], 'color': "red"},
                {'range': [2.0, 3.0], 'color': "orange"},
                {'range': [3.0, 3.55], 'color': "yellowgreen"},
                {'range': [3.55, 4.0], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': cgpa_value
            }
        }
    ))

    fig.update_layout(
        title={'text': "CGPA Gauge"},
        height=400
    )
    
    # This will display in IDE's plot viewer
    fig.show()

# Example usage
gpa_chart(3.56)