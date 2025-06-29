# Data Analysis Tool

This tool allows you to perform data analysis on a given Excel file, visualize key metrics, and compare individual student performances.

## Setup

To get started, you need to install the required Python libraries.

1.  **Open your terminal or command prompt.**

2.  **Run the following command to install the necessary libraries:**

    ```bash
    pip install openpyxl pandas numpy matplotlib seaborn pyqt5
    ```

    This command will install:
    * `openpyxl`: For reading and writing Excel files.
    * `pandas`: For data manipulation and analysis.
    * `numpy`: For numerical operations.
    * `matplotlib`: For creating static, animated, and interactive visualizations.
    * `seaborn`: For drawing attractive statistical graphics.
    * `pyqt5`: For building the graphical user interface (GUI).

## Usage

Once the libraries are installed, you can run the analysis tool.

1.  **Execute the Python script for the analysis tool.** (Assuming your script is named `analysis_tool.py` or similar. Please replace with the actual filename if different.)

    ```bash
    python your_analysis_script_name.py
    ```

    This will launch the graphical user interface (GUI) of the analysis tool.

2.  **Select Your Data File:**
    * In the GUI, click the **"Select File"** button, which is located in the **right top corner**.
    * Select the file named `FA23-BCS-A`. (It is assumed this file is present in the same folder where the script is run).

3.  **Perform Analysis:**
    * After selecting the file, click the **"Perform Analysis"** button, which is located **just below** the "Select File" button.
    * This will trigger the data processing and display the results of the analysis within the GUI.

4.  **Compare Student Data:**
    * In the "Comparison" section, enter student roll numbers for comparison in this format: `FA23-BCS-001 - 008`.
    * This format specifies a range of roll numbers from FA23-BCS-001 to FA23-BCS-008. The tool will then fetch and display the data for these students for comparison.

## Sample File

A sample file named `FA23-BCS-A.xlsx` is present in the folder for performing analysis.