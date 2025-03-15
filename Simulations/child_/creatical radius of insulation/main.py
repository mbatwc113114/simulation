import scipy
from math import log, pi
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog


def open_window(parent_window):
    # Create child window
    child = ctk.CTkToplevel()
    child.title("Heat Transfer Simulation")
    child.geometry("1000x600")
    
    # Function to go back to parent
    def back_to_parent():
        child.destroy()
        parent_window.deiconify()  # Show parent window again
    
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
            ax.plot(x, y, label="Heat Transfer Rate", color="black")
            ax.scatter(max_x, max_y, color="red", label=f"Max Q: {max_y:.2f} at Radius={max_x:.5f}")
            
            # Annotate max point
            ax.annotate(
    f"({max_x:.5f}, {max_y:.2f})",
    (max_x, max_y),
    textcoords="offset points",
    xytext=(-40, -30),  # Moves the annotation down and left to stay inside
    ha="center",  # Center horizontally
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1),  # Adds a box around text
    arrowprops=dict(arrowstyle="->", lw=1.5)
)

            
            # Labels and legend
            ax.set_xlabel("Radius")
            ax.set_ylabel("Q")
            ax.set_title("Heat Transfer Rate vs Radius",pad=20)
            ax.legend()
            ax.grid()
            
            # Refresh canvas
            canvas.draw()
            
            # Update result text
            result_text.configure(text=f"Max Q: {max_y:.2f} at Radius={max_x:.5f}")
            error_label.configure(text="")
        except Exception as e:
            error_label.configure(text=f"Error: {e}")

    # Input variables
    x_fact_var = ctk.StringVar(value="0.00001")
    ri_var = ctk.StringVar(value="0.00125")
    k_var = ctk.StringVar(value="0.25")
    l_var = ctk.StringVar(value="1.0")
    h_var = ctk.StringVar(value="10")
    ti_var = ctk.StringVar(value="100")
    to_var = ctk.StringVar(value="25")
    n_var = ctk.StringVar(value="10000")

    # Create frames
    input_frame = ctk.CTkFrame(child)
    input_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=10, pady=10, expand=False)
    
    graph_frame = ctk.CTkFrame(child)
    graph_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, padx=10, pady=10, expand=True)

    # Input fields with labels
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
    
    for i, (label_text, var) in enumerate(fields):
        frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        frame.pack(pady=5, fill=ctk.X)
        
        label = ctk.CTkLabel(frame, text=label_text)
        label.pack(side=ctk.LEFT, padx=5)
        
        entry = ctk.CTkEntry(frame, textvariable=var, width=120)
        entry.pack(side=ctk.RIGHT, padx=5)

    # Result display
    result_text = ctk.CTkLabel(input_frame, text="", font=("Arial", 12, "bold"))
    result_text.pack(pady=10)
    
    # Error message label
    error_label = ctk.CTkLabel(input_frame, text="", text_color="red")
    error_label.pack(pady=5)
    
    # Button frame
    button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
    button_frame.pack(pady=10, fill=ctk.X)
    
    # Simulate Button
    simulate_btn = ctk.CTkButton(
        button_frame, 
        text="Simulate", 
        command=update_graph,
        fg_color="#3498db"
    )
    simulate_btn.pack(side=ctk.LEFT, padx=5, expand=True, fill=ctk.X)
    
    # Back Button
    back_btn = ctk.CTkButton(
        button_frame, 
        text="Back to Main", 
        command=back_to_parent,
        fg_color="#2c3e50"
    )
    back_btn.pack(side=ctk.RIGHT, padx=5, expand=True, fill=ctk.X)

# save plot 
    def save_graph():
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("All Files", "*.*")])
        if file_path:
            fig.savefig(file_path, dpi=300, bbox_inches="tight")


    save_btn = ctk.CTkButton(
    button_frame, 
    text="Save Graph", 
    command=save_graph,
    fg_color="#27ae60")
    
    save_btn.pack(side=ctk.LEFT, padx=5, expand=True, fill=ctk.X)


    # Create Matplotlib figure
    fig = Figure(figsize=(6, 6), dpi=120)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor('#9f9f9f')  # Dark background
    ax.set_facecolor('#9f9f9f')  # Dark plot area
    
    # Set text color to white for better visibility
    ax.xaxis.label.set_color('yellow')
    ax.yaxis.label.set_color('yellow')
    ax.title.set_color('yellow')
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    
    # Embed Matplotlib figure in customtkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)
    
    # Run initial simulation
    update_graph()
    
    # Make the window take focus
    child.lift()
    child.focus_force()

# This is needed if you run this script directly
if __name__ == "__main__":
    # For testing only
    root = ctk.CTk()
    root.withdraw()
    open_window(root)
    root.mainloop()