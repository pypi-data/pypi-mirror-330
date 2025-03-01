import tkinter as tk
from tkinter import ttk
import numpy as np
from mnist.lib import *
from PIL import Image, ImageTk
import random
import click
import os
from itertools import chain
class DrawingApp:
    def __init__(self, root, model_path):
        self.root = root
        self.root.title("Number Drawing App")
        
        # Add auto-center and auto-scale variables
        self.auto_center = tk.BooleanVar(value=False)
        self.auto_scale = tk.BooleanVar(value=False)
        # Add callbacks for auto-center and auto-scale changes
        self.auto_center.trace_add('write', self._on_auto_center_change)
        self.auto_scale.trace_add('write', self._on_auto_scale_change)
        
        # Store the initial model path
        self.current_model_path = model_path
        
        # Load available models
        self.available_models = self._get_available_models()
        
        # Load the model and test data
        self._load_model(model_path)
        
        # Create main display frame to hold all three panels
        main_frame = tk.Frame(root)
        main_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create drawing panel (left)
        canvas_frame = tk.Frame(main_frame)
        canvas_frame.pack(side=tk.LEFT, expand=True, fill='both', padx=(0,5))
        
        # Create canvas
        self.canvas = tk.Canvas(canvas_frame, width=400, height=400, bg='white')
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        
        # Create ASCII display panel (middle)
        ascii_frame = tk.Frame(main_frame)
        ascii_frame.pack(side=tk.LEFT, expand=True, fill='both', padx=5)
        
        # Create ASCII display area using Text widget
        self.text_display = tk.Text(ascii_frame, width=28, height=28, 
                                  font=('Courier', 20))
        self.text_display.pack(expand=True, fill='both')
        # Initialize with empty grid
        empty_grid = '\n'.join([' ' * 28 for _ in range(28)])
        self.text_display.insert('1.0', empty_grid)
        
        # Create PNG display panel (right)
        png_frame = tk.Frame(main_frame)
        png_frame.pack(side=tk.LEFT, expand=True, fill='both', padx=(5,0))
        
        # Create PNG image display using Label and initialize with empty image
        self.image_label = tk.Label(png_frame)
        self.image_label.pack(expand=True, fill='both')
        # Initialize with empty image
        empty_matrix = np.zeros((28, 28))
        empty_image = mnist_to_image(empty_matrix, scale=10, invert=True)
        self.photo = ImageTk.PhotoImage(empty_image)
        self.image_label.config(image=self.photo)
        
        # Initialize drawing variables
        self.prev_x = None
        self.prev_y = None
        
        # Bind mouse events
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-2>', lambda e: self.clear_canvas())
        
        # Create buttons frame
        button_frame = tk.Frame(root)
        button_frame.pack(fill=tk.X)
        
        # Create model selector
        model_label = tk.Label(button_frame, text="Model:")
        model_label.pack(side=tk.LEFT, padx=5)
        
        self.model_selector = ttk.Combobox(button_frame, state="readonly", width=20)
        self.model_selector['values'] = [name for name, _ in self.available_models]
        # Set default value to the current model
        for i, (name, path) in enumerate(self.available_models):
            if path == self.current_model_path:
                self.model_selector.current(i)
                break
        self.model_selector.pack(side=tk.LEFT, padx=5)
        self.model_selector.bind('<<ComboboxSelected>>', self._on_model_change)
        
        # Create clear button
        clear_button = tk.Button(button_frame, text="Clear Canvas", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Create detect button
        detect_button = tk.Button(button_frame, text="Detect Number", command=self.show_matrix)
        detect_button.pack(side=tk.LEFT, padx=5)
        
        # Create load test image button
        test_button = tk.Button(button_frame, text="Load Test Image", command=self.load_test_image)
        test_button.pack(side=tk.LEFT, padx=5)
        
        # Add auto-center checkbox
        center_check = tk.Checkbutton(button_frame, text="Auto-Center", 
                                    variable=self.auto_center)
        center_check.pack(side=tk.LEFT, padx=5)
        
        # Add auto-scale checkbox
        scale_check = tk.Checkbutton(button_frame, text="Auto-Scale", 
                                    variable=self.auto_scale)
        scale_check.pack(side=tk.LEFT, padx=5)
        
        # Create detection label below buttons
        self.detection_label = tk.Label(root, text="Draw a number in the left panel", font=('Arial', 25))
        self.detection_label.pack(pady=10)
        
        # Create label for right-click instruction with smaller font and gray color
        self.result_label = tk.Label(root, text="right-click to clear canvas", 
                                   font=('Arial', 16), fg='gray')
        self.result_label.pack(pady=5)
        
    def paint(self, event):
        x, y = event.x, event.y
        
        if self.prev_x and self.prev_y:
            self.canvas.create_line(self.prev_x, self.prev_y, x, y, 
                                  width=30, fill='black', 
                                  capstyle=tk.ROUND, smooth=tk.TRUE)
        
        self.prev_x = x
        self.prev_y = y

    
    def reset(self, event):
        self.prev_x = None
        self.prev_y = None
        # Show matrix after releasing mouse
        self.show_matrix()
        
    def clear_canvas(self):
        self.canvas.delete("all")
        self.detection_label.config(text="Draw a number",)
        
        # Initialize ASCII display with empty grid
        self.text_display.delete('1.0', tk.END)
        empty_grid = '\n'.join([' ' * 28 for _ in range(28)])
        self.text_display.insert('1.0', empty_grid)
        
        # Initialize PNG display with empty image
        empty_matrix = np.zeros((28, 28))
        empty_image = mnist_to_image(empty_matrix, scale=10, invert=True)
        self.photo = ImageTk.PhotoImage(empty_image)
        self.image_label.config(image=self.photo)
        
        print(f"# Canvas cleared")

    def find_bounding_box(self):
        """Find the bounding box of the drawing on the canvas"""
        # Get all items on canvas
        items = self.canvas.find_all()
        if not items:
            return None
        
        # Initialize bounds
        x1, y1, x2, y2 = float('inf'), float('inf'), float('-inf'), float('-inf')
        
        # Find the bounding box that contains all drawn items
        for item in items:
            bounds = self.canvas.bbox(item)
            if bounds:
                ix1, iy1, ix2, iy2 = bounds
                x1 = min(x1, ix1)
                y1 = min(y1, iy1)
                x2 = max(x2, ix2)
                y2 = max(y2, iy2)
        
        if x1 == float('inf'):
            return None
            
        return x1, y1, x2, y2
    
    def recenter_drawing(self):
        """Recenter the drawing on the canvas"""
        bbox = self.find_bounding_box()
        if not bbox:
            return
            
        x1, y1, x2, y2 = bbox
        
        # Calculate the center of the drawing
        drawing_center_x = (x1 + x2) / 2
        drawing_center_y = (y1 + y2) / 2
        
        # Calculate the center of the canvas
        canvas_center_x = self.canvas.winfo_width() / 2
        canvas_center_y = self.canvas.winfo_height() / 2
        
        # Calculate the move offset
        move_x = canvas_center_x - drawing_center_x
        move_y = canvas_center_y - drawing_center_y
        
        # Move all items
        for item in self.canvas.find_all():
            self.canvas.move(item, move_x, move_y)

    def scale_drawing(self):
        """Scale the drawing to fit the canvas with padding"""
        bbox = self.find_bounding_box()
        if not bbox:
            return
            
        x1, y1, x2, y2 = bbox
        
        # Calculate current drawing dimensions
        drawing_width = x2 - x1
        drawing_height = y2 - y1
        
        # Calculate target dimensions (with 10% padding)
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        target_width = canvas_width * 0.9  # 90% of canvas width
        target_height = canvas_height * 0.9  # 90% of canvas height
        
        # Calculate scale factor while maintaining aspect ratio
        scale_x = target_width / drawing_width
        scale_y = target_height / drawing_height
        scale_factor = min(scale_x, scale_y)  # Use smaller scale to fit both dimensions
        
        # Calculate the center of the drawing
        drawing_center_x = (x1 + x2) / 2
        drawing_center_y = (y1 + y2) / 2
        
        # Scale all items around their center
        for item in self.canvas.find_all():
            # Get item's coordinates
            coords = self.canvas.coords(item)
            # Apply scaling transformation around the center
            new_coords = []
            for i in range(0, len(coords), 2):
                x, y = coords[i], coords[i+1]
                # Translate to origin relative to drawing center
                dx = x - drawing_center_x
                dy = y - drawing_center_y
                # Scale
                dx *= scale_factor
                dy *= scale_factor
                # Translate back
                new_coords.extend([dx + drawing_center_x, dy + drawing_center_y])
            # Update item's coordinates
            self.canvas.coords(item, *new_coords)
            
            # Scale line width
            if self.canvas.type(item) == "line":
                current_width = float(self.canvas.itemcget(item, "width"))
                self.canvas.itemconfig(item, width=current_width * scale_factor)

    def show_matrix(self):
        """Display both ASCII and PNG representations of the drawing"""
        
        # Apply auto-scale and auto-center if enabled
        if self.auto_scale.get():
            self.scale_drawing()  # Scale first
        if self.auto_center.get():
            self.recenter_drawing()  # Then center
        
        matrix = self.canvas_to_matrix()

        result = self.detect(matrix)

        # Update detection label with result
        self.detection_label.config(text=f"Detected as: {result}")
        
        # Keep right-click instruction unchanged
        self.result_label.config(text="Right click to clear canvas")
        
        # Update ASCII display
        self.text_display.delete('1.0', tk.END)
        ascii_rep = mnist_matrix_text(matrix)
        self.text_display.insert('1.0', ascii_rep)
        
        # Print matrix representation to console
        print("\nMatrix representation (28x28):")
        print(ascii_rep)
        print("-" * 28)

        # Update PNG display
        image = mnist_to_image(matrix, scale=10, invert=True)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep a reference!
        

    def canvas_to_matrix(self, matrix_size=(28, 28)):
        # Get canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # First create a binary matrix of the full canvas size
        full_matrix = np.zeros((canvas_height, canvas_width))
        
        # For each pixel in the canvas, check if there's a line
        for y in range(canvas_height):
            for x in range(canvas_width):
                if self.canvas.find_overlapping(x, y, x+1, y+1):
                    full_matrix[y, x] = 1
        
        # Now resize this matrix to MNIST size (28x28)
        # Calculate the size of each cell in the target matrix
        cell_width = canvas_width // matrix_size[1]
        cell_height = canvas_height // matrix_size[0]
        
        # Create the final matrix
        matrix = np.zeros(matrix_size)
        
        # For each cell in the target matrix, compute a weighted average of the region
        # including neighboring pixels for more realistic fuzzy edges
        for i in range(matrix_size[0]):
            for j in range(matrix_size[1]):
                # Get the center of the current cell
                y_center = i * cell_height + cell_height // 2
                x_center = j * cell_width + cell_width // 2
                
                # Define a larger region around the cell for sampling
                sample_radius = int(cell_width * 1.5)  # Adjust this for more/less fuzziness
                
                y_start = max(0, y_center - sample_radius)
                y_end = min(canvas_height, y_center + sample_radius)
                x_start = max(0, x_center - sample_radius)
                x_end = min(canvas_width, x_center + sample_radius)
                
                # Get the region
                region = full_matrix[y_start:y_end, x_start:x_end]
                
                if region.size > 0:
                    # Calculate distances from center for gaussian-like weighting
                    y_coords, x_coords = np.ogrid[y_start:y_end, x_start:x_end]
                    distances = np.sqrt((y_coords - y_center)**2 + (x_coords - x_center)**2)
                    
                    # Create gaussian-like weights
                    weights = np.exp(-(distances**2) / (2 * (sample_radius/2)**2))
                    weights = weights / weights.sum()  # Normalize weights
                    
                    # Calculate weighted average
                    matrix[i, j] = np.sum(region * weights)
        
        # Normalize and enhance contrast slightly
        if matrix.max() > 0:  # Only normalize if there's any drawing
            matrix = matrix / matrix.max()  # Normalize to 0-1
            # Apply mild contrast enhancement
            matrix = np.clip(matrix * 1.2, 0, 1)
        
        # Flatten the matrix as required by the model
        matrix = matrix.flatten()
        
        return matrix
    
    def detect(self, matrix):
        # Print total number of lines on canvas
    
        if self.model is None:
            return 'Error: Model not loaded'
        
        # Flatten the 28x28 matrix into a 1D array of 784 elements
        flattened = matrix.reshape(1, -1)
        
        # Use the model to predict
        try:
            print(f"# Predicting")
            result = str(self.model.predict(flattened)[0])
            print(f"# The detected number is: {result}")
        except Exception as e:
            result = f"Error during prediction: {e}"
        
        return result

    def load_test_image(self):
        """Load and draw a random test image from MNIST dataset"""
        if self.test_data is None:
            self.result_label.config(text="Error: Test data not loaded",
                                   font=('Arial', 20))
            return
            
        # Clear the canvas first
        self.clear_canvas()
        
        # Get a random test image
        index = random.randint(0, len(self.test_data[0]) - 1)
        test_image = self.test_data[0][index]
        actual_digit = self.test_data[1][index]
        
        # Scale the image to canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Reshape to 28x28 and scale values to 0-1
        img_matrix = test_image.reshape(28, 28)
        
        # Draw each pixel as a rectangle on the canvas
        pixel_width = canvas_width / 28
        pixel_height = canvas_height / 28
        
        for i in range(28):
            for j in range(28):
                if img_matrix[i, j] > 0.1:  # Only draw non-white pixels
                    x1 = j * pixel_width
                    y1 = i * pixel_height
                    x2 = (j + 1) * pixel_width
                    y2 = (i + 1) * pixel_height
                    # Scale the intensity to determine the fill color (0=white, 1=black)
                    gray_value = int(255 * (1 - img_matrix[i, j]))
                    color = f'#{gray_value:02x}{gray_value:02x}{gray_value:02x}'
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        
        # Show the matrix and update displays
        self.show_matrix()
        
        # Get the prediction from the model
        matrix = self.canvas_to_matrix()
        predicted_digit = self.detect(matrix)
        
        # Update label with both actual and predicted digits
        self.result_label.config(
            text=f"Test image loaded - Actual: {actual_digit}, Predicted: {predicted_digit}",
            font=('Arial', 20)
        )

    def _on_auto_center_change(self, *args):
        """Callback when auto-center checkbox changes"""
        # Only rerun detection if there's something drawn
        if self.canvas.find_all():
            self.show_matrix()
            
    def _on_auto_scale_change(self, *args):
        """Callback when auto-scale checkbox changes"""
        # Only rerun detection if there's something drawn
        if self.canvas.find_all():
            self.show_matrix()

    def _on_model_change(self, event):
        """Handle model selection change"""
        selection = self.model_selector.get()
        for name, path in self.available_models:
            if name == selection:
                self.current_model_path = path
                load_model(path)
                break

    def _get_available_models(self):
        """Get list of available model files from data directory"""
        models = []

        data_dir = [os.path.dirname(DEFAULT_MODEL_PATH), os.getcwd()]
        
        def get_model_paths(dirname):
            for file in os.listdir(dirname):
                if file.endswith('_model.gz'):
                    path = os.path.join(dirname, file)
                    yield (file, path)
        
        models = map(get_model_paths, data_dir)
        models = list(chain(*models))
        return models

    def _load_model(self, model_path):
        """Load the specified model and its test data"""
        try:
            self.model = load_model(model_path)
            _, _, self.test_data = load_data()
            print(f"# Model loaded successfully from {model_path}")
            print(f"# Test data loaded successfully")
        except Exception as e:
            print(f"Error loading model {model_path}: {e}")
            self.model = None
            self.test_data = None

def main(model=DEFAULT_MODEL_PATH):
    """MNIST Drawing Recognition GUI"""
    root = tk.Tk()
    app = DrawingApp(root, model_path=model)
    root.mainloop()

if __name__ == '__main__':
    main()

