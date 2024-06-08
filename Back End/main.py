import openai
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import re
import cv2

# Set your OpenAI API key
openai.api_key = 'sk-proj-nI1DC8WFh8zQbWh4kz2gT3BlbkFJ7KVEQVEpiCGykCVZCgc9'

def extract_python_code(response):
    # Use regex to extract code between ```python and the next ```
    match = re.search(r'```python(.*?)```', response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        raise ValueError("No valid Python code found in the response.")
    
def generate_code(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    code = response['choices'][0]['message']['content']
    return code

def generate_display_formula(equation):
    prompt = f"""
    Generate the Python code to create a 3D formula to display at the beginning of the video. The formula should represent the equation: {equation}.
    The formula should be rendered in 3D, with a large font size and a bold color. It should be centered in the frame.
    The background should be black, and the formula should be in a bright color to stand out.
    The formula should be displayed for 2 seconds before fading out.
    """
    return generate_code(prompt)

def generate_plot_code(equation):
    prompt = f"""
    Generate a Python code to visualize a 3D mathematical equation and save it as a 10-second video. The equation is: {equation}.
    Use Matplotlib and Numpy libraries to plot the 3D graph of the equation. The code should include the following steps:
    1. Create a meshgrid for x and y.
    2. Calculate the z values using the equation.
    3. Plot the 3D graph using Matplotlib.
    4. Generate frames by rotating (not too fast) the plot in every possible angle and direction.
    5. Compile the frames into a ten-second video using OpenCV and save it as '3d_plot.mp4'.
    """
    return generate_code(prompt)

def generate_properties_summary(equation):
    prompt = f"""
    Generate a Python code to display a summary of the properties of the equation: {equation}. The summary should include the following information:
    1. The type of equation (e.g., linear, quadratic, trigonometric).
    2. The number of variables in the equation.
    3. The range of values for each variable.
    4. The domain and range of the equation.
    5. Any special properties of the equation (e.g., symmetry, periodicity).
    The summary should be concise and informative, suitable for display at the end of the video.
    The summary should appear in the same background with the same font size and same color as the formula.
    The summary should be displayed for 3 seconds before fading out.
    """
    return generate_code(prompt)

def execute_code(code):
    exec(code, globals())

def pipeline(equation):
    """
    Divide the task into sub-tasks and generate code for each sub-task using different prompts.
    1. Create a formula to display before the video starts.
    2. Generate the code to create a 3D video of the equation.
    3. Summarize the equation's properties and display them at the end of the video.
    4. Combine all the generated code into a single Python script.
    """
    # Display the formula at the beginning
    formula_code = extract_python_code(generate_display_formula(equation))
    
    # Generate the 3D plot video
    plot_code = extract_python_code(generate_plot_code(equation))
    
    # Summarize the properties at the end
    summary_code = extract_python_code(generate_properties_summary(equation))
    
    # Combine all parts into a single script
    final_code = f"""
{formula_code}

{plot_code}

{summary_code}

if __name__ == "__main__":
    # Ensure all the required functions and variables are executed in the correct order
    main()
    """
    
    print("Final combined code:\n")
    print(final_code)
    
    # Execute the final combined code
    execute_code(final_code)

def main():
    equation = input("Enter a mathematical equation (e.g., z = np.sin(np.sqrt(x**2 + y**2))): ")
    pipeline(equation)

if __name__ == "__main__":
    main()
