from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import re
import io
import base64

app = Flask(__name__)

# Function to plot the equations and return as a byte stream
def plot_equation(equations):
    plt.figure(figsize=(10, 6))
    
    x_vals = np.linspace(-10, 10, 400)
    
    for equation in equations:
        equation = equation.replace(" ", "")
        
        if 'x^' in equation:
            match = re.match(r'y\s*=\s*([+-]?\d*\.?\d*)x\^(\d+)\s*([+-]?\s*\d*\.?\d*)?', equation)
        else:
            match = re.match(r'y\s*=\s*([+-]?\d*\.?\d*)x\s*([+-]?\s*\d*\.?\d*)?', equation)

        if match:
            if 'x^' in equation:
                coefficient = float(match.group(1)) if match.group(1) else 1  # Default to 1 if omitted
                power = int(match.group(2))
                intercept = float(match.group(3)) if match.group(3) else 0  # Default to 0 if omitted
                y_vals = coefficient * (x_vals ** power) + intercept
            else:
                slope = float(match.group(1)) if match.group(1) else 1  # Default to 1 if omitted
                intercept = float(match.group(2)) if match.group(2) else 0  # Default to 0 if omitted
                y_vals = slope * x_vals + intercept
                
            plt.plot(x_vals, y_vals, label=equation, linewidth=2)  # Plot each equation with a label

        else:
            return None  # Return None if invalid format
    
    plt.axhline(0, color='black', linewidth=0.5, ls='--')  # x-axis
    plt.axvline(0, color='black', linewidth=0.5, ls='--')  # y-axis
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.grid(True)
    plt.title("Plot of the Equations")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)  # Seek to the beginning of the BytesIO buffer
    
    # Encode the image to base64
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_img = None
    error = None
    equations_list = request.form.getlist('equation')  # Preserve equations list between POST requests

    if request.method == 'POST':
        # Handle deletion
        if 'delete' in request.form:
            delete_index = int(request.form.get('delete'))  # Get the index of the equation to delete
            if 0 <= delete_index < len(equations_list):
                del equations_list[delete_index]  # Remove the equation by index

        # Handle adding a new equation
        new_equation = request.form.get('new_equation')  # Get the new equation from the form
        if new_equation:
            equations_list.append(new_equation)  # Append new equation to the list

        # If there are equations, plot them
        if len(equations_list) > 0:
            plot_img = plot_equation(equations_list)
            if plot_img is None:
                error = "Invalid equation format. Please enter in the form y = mx^n + b or y = mx + b."
        else:
            error = "Please enter at least one equation."

    return render_template('index.html', plot_img=plot_img, error=error, equations_list=equations_list)

if __name__ == "__main__":
    app.run(debug=True)
