import scipy
from math import log, pi
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to update the graph
def update_graph():
    try:
        # Get values from input fields
        x_fact = float(x_fact_var.get())
        ri = float(ri_var.get())
        k = float(k_var.get())
        l = float(l_var.get())
        h = float(h_var.get())
        ti = float(ti_var.get())
        to = float(to_var.get())
        n = int(n_var.get())

        # Generate x values (radius)
        x = [i * x_fact for i in range(round(ri * 1000), n)]

        # Compute Q values
        y = [
            (ti - to) / ((log(xi / ri) / (2 * pi * k * l)) + (1 / (2 * pi * l * h * xi)))
            for xi in x
        ]

        # Find max Q and corresponding radius
        max_y = max(y)
        max_index = y.index(max_y)
        max_x = x[max_index]

        # Clear previous plot
        ax.clear()

        # Plot graph
        ax.plot(x, y, label="Heat Transfer Rate", color="blue")
        ax.scatter(max_x, max_y, color="red", label=f"Max Q: {max_y:.2f} at Radius={max_x:.5f}")

        # Annotate max point
        ax.annotate(f"({max_x:.5f}, {max_y:.2f})",
                    (max_x, max_y),
                    textcoords="offset points",
                    xytext=(-50,10),
                    arrowprops=dict(arrowstyle="->", lw=1.5))

        # Labels and legend
        ax.set_xlabel("Radius")
        ax.set_ylabel("Q")
        ax.set_title("Heat Transfer Rate vs Radius")
        ax.legend()
        ax.grid()

        # Refresh canvas
        canvas.draw()

    except Exception as e:
        error_label.config(text=f"Error: {e}")

# Create main window
root = tk.Tk()
root.title("Heat Transfer Simulation")

# Input variables
x_fact_var = tk.StringVar(value="0.00001")
ri_var = tk.StringVar(value="0.00125")
k_var = tk.StringVar(value="0.25")
l_var = tk.StringVar(value="1.0")
h_var = tk.StringVar(value="10")
ti_var = tk.StringVar(value="100")
to_var = tk.StringVar(value="25")
n_var = tk.StringVar(value="10000")

# Input fields
fields = [
    ("x_fact", x_fact_var),
    ("ri (Inner Radius)", ri_var),
    ("k (Thermal Conductivity)", k_var),
    ("l (Length)", l_var),
    ("h (Heat Transfer Coeff.)", h_var),
    ("ti (Initial Temp)", ti_var),
    ("to (Surrounding Temp)", to_var),
    ("n (Iterations)", n_var),
]

for i, (label, var) in enumerate(fields):
    ttk.Label(root, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
    ttk.Entry(root, textvariable=var).grid(row=i, column=1, padx=5, pady=5)

# Simulate Button
ttk.Button(root, text="Simulate", command=update_graph).grid(row=len(fields), column=0, columnspan=2, pady=10)

# Error message label
error_label = tk.Label(root, text="", fg="red")
error_label.grid(row=len(fields)+1, column=0, columnspan=2)

# Create Matplotlib figure
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)

# Embed Matplotlib figure in Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=2, rowspan=len(fields) + 2, padx=10, pady=10)

# Run Tkinter event loop
root.mainloop()
