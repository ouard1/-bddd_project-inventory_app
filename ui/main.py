import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Grid Window")
window.geometry("1100x700")

# Define grid size
num_rows = 8
num_cols = 13
cell_size = 83  # Pixels

# Configure rows
for i in range(num_rows):
    window.rowconfigure(i, weight=1, minsize=cell_size)

# Configure columns
for i in range(num_cols):
    window.columnconfigure(i, weight=1, minsize=cell_size)

# Example: Create a label in each cell (optional)
for row in range(num_rows):
    for col in range(num_cols):
        label = tk.Label(window, text=f"Cell ({row},{col})")
        label.grid(row=row, column=col)

window.mainloop()
