import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image, ImageTk

class GraphPaperGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Graph Paper Generator")

        # Define default values
        self.defaults = {
            'width': 8.5,
            'height': 11,
            'squares_per_inch': 4,
            'line_color': '#000000',
            'line_thickness': 0.5,
            'line_style': 'solid'  # 'solid' or 'dotted'
        }

        # Left Frame for inputs
        self.left_frame = tk.Frame(master)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        # Right Frame for image preview
        self.right_frame = tk.Frame(master)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky='ne')

        self.setup_ui()
        self.generate_preview()

    def setup_ui(self):
        row = 0
        tk.Label(self.left_frame, text="Width (inches):").grid(row=row, column=0, sticky='w')
        self.width_entry = tk.Entry(self.left_frame, width=10)
        self.width_entry.grid(row=row, column=1, sticky='w')
        self.width_entry.insert(0, str(self.defaults['width']))

        row += 1
        tk.Label(self.left_frame, text="Height (inches):").grid(row=row, column=0, sticky='w')
        self.height_entry = tk.Entry(self.left_frame, width=10)
        self.height_entry.grid(row=row, column=1, sticky='w')
        self.height_entry.insert(0, str(self.defaults['height']))

        row += 1
        tk.Label(self.left_frame, text="Squares per inch:").grid(row=row, column=0, sticky='w')
        self.squares_entry = tk.Entry(self.left_frame, width=10)
        self.squares_entry.grid(row=row, column=1, sticky='w')
        self.squares_entry.insert(0, str(self.defaults['squares_per_inch']))

        row += 1
        tk.Label(self.left_frame, text="Line color:").grid(row=row, column=0, sticky='w')
        self.color_button = tk.Button(self.left_frame, text="Choose Color", command=self.choose_color)
        self.color_button.grid(row=row, column=1, sticky='w')

        row += 1
        tk.Label(self.left_frame, text="Line thickness:").grid(row=row, column=0, sticky='w')
        self.thickness_entry = tk.Entry(self.left_frame, width=10)
        self.thickness_entry.grid(row=row, column=1, sticky='w')
        self.thickness_entry.insert(0, str(self.defaults['line_thickness']))

        row += 1
        tk.Label(self.left_frame, text="Line style:").grid(row=row, column=0, sticky='w')
        self.line_style_var = tk.StringVar()
        self.line_style_combobox = ttk.Combobox(self.left_frame, textvariable=self.line_style_var, values=('solid', 'dotted'), state='readonly')
        self.line_style_combobox.grid(row=row, column=1, sticky='w')
        self.line_style_combobox.set(self.defaults['line_style'])

        row += 1
        self.preview_button = tk.Button(self.left_frame, text="Preview", command=self.generate_preview)
        self.preview_button.grid(row=row, columnspan=2, pady=(10,0))

        row += 1
        self.save_button = tk.Button(self.left_frame, text="Save as PDF", command=self.save_pdf)
        self.save_button.grid(row=row, columnspan=2)

        row += 1
        self.reset_button = tk.Button(self.left_frame, text="Reset to Defaults", command=self.reset_to_defaults)
        self.reset_button.grid(row=row, columnspan=2, pady=(10,0))

        self.image_label = tk.Label(self.right_frame)
        self.image_label.pack()

        # Copyright Notice
        row += 1
        tk.Label(self.left_frame, text="Copyright R&D BioTech Alaska", font=('Arial', 8, 'italic')).grid(row=row, column=0, columnspan=2, sticky='w', pady=5)	

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose line color")
        if color_code:
            self.defaults['line_color'] = color_code[1]

    def reset_to_defaults(self):
        self.width_entry.delete(0, tk.END)
        self.width_entry.insert(0, str(self.defaults['width']))
        self.height_entry.delete(0, tk.END)
        self.height_entry.insert(0, str(self.defaults['height']))
        self.squares_entry.delete(0, tk.END)
        self.squares_entry.insert(0, str(self.defaults['squares_per_inch']))
        self.thickness_entry.delete(0, tk.END)
        self.thickness_entry.insert(0, str(self.defaults['line_thickness']))
        self.line_style_combobox.set(self.defaults['line_style'])

    def generate_graph_paper(self):
        # Use the full dimensions for PDF generation
        width = float(self.width_entry.get())
        height = float(self.height_entry.get())
        return self.create_graph_paper_figure(width, height)

    def generate_preview(self):
        # Use smaller dimensions for preview
        preview_width = float(self.width_entry.get()) / 4
        preview_height = float(self.height_entry.get()) / 4
        fig, ax = self.create_graph_paper_figure(preview_width, preview_height)
        self.display_figure(fig)

    def create_graph_paper_figure(self, width, height):
        squares_per_inch = int(self.squares_entry.get())
        line_color = self.defaults['line_color']
        line_thickness = float(self.thickness_entry.get())
        line_style = 'dotted' if self.line_style_var.get() == 'dotted' else 'solid'

        fig, ax = plt.subplots(figsize=(width, height), dpi=100, facecolor='white')
        ax.set_facecolor('white')
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)

        linestyle = ':' if line_style == 'dotted' else '-'
        x_lines = np.arange(0, width, 1/squares_per_inch)
        y_lines = np.arange(0, height, 1/squares_per_inch)
        for x in x_lines:
            ax.axvline(x, color=line_color, linewidth=line_thickness, linestyle=linestyle)
        for y in y_lines:
            ax.axhline(y, color=line_color, linewidth=line_thickness, linestyle=linestyle)

        ax.axis('off')
        fig.tight_layout(pad=0)
        return fig, ax

    def display_figure(self, fig):
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        buf = canvas.get_renderer().buffer_rgba()
        image = Image.frombuffer("RGBA", canvas.get_width_height(), buf, "raw", "RGBA", 0, 1)
        image.thumbnail((200, 200))  # Adjusted preview size
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        plt.close(fig)

    def save_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if file_path:
            fig, ax = self.generate_graph_paper()
            fig.savefig(file_path, format='pdf', facecolor='white', edgecolor='none')
            plt.close(fig)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.attributes('-topmost', True)  # Keep window on top initially
        root.after(500, lambda: root.attributes('-topmost', False))  # Then allow it to behave normally
        app = GraphPaperGenerator(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        raise
