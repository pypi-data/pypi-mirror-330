import tkinter as tk
from PIL import Image, ImageTk
import json, gzip
from mnist.lib import *
from pathlib import Path
import random
from io import TextIOWrapper

# Font configuration
DISPLAY_FONT_SIZE = 20  # For the ASCII art display
BUTTON_FONT_SIZE = 18   # For number buttons
STATUS_FONT_SIZE = 16   # For status and help messages

# Color configuration
CORRECT_COLOR = '#e6ffe6'  # Light green
INCORRECT_COLOR = '#ffe6e6'  # Light red
DEFAULT_COLOR = 'white'

class ContestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MNIST Contest")
        self.report_json = DEFAULT_REPORT_PATH
        # Contest state
        self.current_image_data = None
        self.score = 0
        self.total = 0
        self.max_attempts = 10
        
        # Load the test data to get images
        _, _, self.test_data = load_data()
        
        # Load all challenges at startup
        self.load_challenges()
        
        # Create main display frame to hold both visualizations
        display_frame = tk.Frame(root)
        display_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create ASCII display area using Text widget
        self.text_display = tk.Text(display_frame, width=28, height=28, 
                                  font=('Courier', DISPLAY_FONT_SIZE))
        self.text_display.pack(side=tk.LEFT, expand=True, fill='both', padx=(5,2), pady=5)
        
        # Create PNG image display using Label
        self.image_label = tk.Label(display_frame)
        self.image_label.pack(side=tk.LEFT, expand=True, fill='both', padx=(2,5), pady=5)
        
        # Create button frame
        button_frame = tk.Frame(root)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create number buttons (0-9)
        for i in range(10):
            btn = tk.Button(button_frame, text=str(i), width=4,
                          command=lambda x=i: self.check_guess(x),
                          font=('Arial', BUTTON_FONT_SIZE))
            btn.pack(side=tk.LEFT, padx=2)
            
        # Create status label
        self.status_label = tk.Label(root, text="Click a number to make your guess", 
                                   font=('Arial', STATUS_FONT_SIZE))
        self.status_label.pack(pady=5)
        
        # Create help label at bottom
        self.help_label = tk.Label(root, text="Right-click anywhere to advance to next number", 
                                 font=('Arial', STATUS_FONT_SIZE), fg='gray50')
        self.help_label.pack(pady=(0, 5))
        
        # Bind right-click instead of space
        self.root.bind('<Button-2>', lambda e: self.load_next_challenge())
        
        # Start the contest
        self.load_next_challenge()
    
    def load_challenges(self):
        """Load all challenges from report.json at startup"""
        try:
            stream = gzip.open(self.report_json, 'rb') if self.report_json.endswith('.gz') else open(self.report_json, 'rb')
            with TextIOWrapper(stream) as f:
                data = json.load(f) 
                
            if 'errors' not in data:
                raise Exception(f"No errors found in {self.report_json}")
                
            # Convert errors into challenges
            self.challenges = []
            for error in data['errors']:
                challenge = {
                    'imgnum': error['index'],
                    'expected': error['expected'],
                    'predicted': error['predicted']
                }
                self.challenges.append(challenge)
            
            if not self.challenges:
                raise Exception(f"No valid challenges found in {self.report_json}")
                
            # Shuffle and limit to max_attempts
            random.shuffle(self.challenges)
            self.challenges = self.challenges[:self.max_attempts]
                
        except FileNotFoundError:
            raise Exception(f"{self.report_json} not found!")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON format in {self.report_json}!")
        
    def load_next_challenge(self):
        """Load a random challenge from the available challenges"""
        try:
            if not self.challenges or self.total >= self.max_attempts:
                self.show_final_score()
                return
                
            # Select and remove next challenge
            challenge = self.challenges.pop(0)
            
            image_index = challenge['imgnum']
            self.current_image_data = challenge
            
            # Reset colors to default
            self.text_display.configure(bg=DEFAULT_COLOR)
            self.image_label.configure(bg=DEFAULT_COLOR)
            
            # Clear display
            self.text_display.delete('1.0', tk.END)
            
            # Show the ASCII art
            image_matrix = self.test_data[0][image_index]
            text_representation = mnist_matrix_text(image_matrix)
            self.text_display.insert('1.0', text_representation)
            
            # Show the PNG image
            image = mnist_to_image(image_matrix, scale=10, invert=True)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep a reference!
            
            # Update status
            attempts_left = self.max_attempts - self.total
            self.status_label.config(
                text=f"Score: {self.score}/{self.total} - What is this number? ({attempts_left} attempts left)")
            
        except Exception as e:
            self.text_display.delete('1.0', tk.END)
            self.text_display.insert('1.0', f"Error loading challenge: {str(e)}")
            self.image_label.config(image='')
    
    def check_guess(self, number):
        """Check if the user's guess matches the expected number"""
        if not self.current_image_data:
            return
            
        self.total += 1
        expected = self.current_image_data['expected']
        predicted = self.current_image_data['predicted']
        
        if number == expected:
            self.score += 1
            result = "Correct!"
            # Set background to light green for correct answer
            self.text_display.configure(bg=CORRECT_COLOR)
            self.image_label.configure(bg=CORRECT_COLOR)
        else:
            result = f"Wrong! Expected: {expected}"
            # Set background to light red for incorrect answer
            self.text_display.configure(bg=INCORRECT_COLOR)
            self.image_label.configure(bg=INCORRECT_COLOR)
            
        attempts_left = self.max_attempts - self.total
        self.status_label.config(
            text=f"Score: {self.score}/{self.total} - {result} : The model predicted: {predicted} - {attempts_left} attempts left")
    
    def show_final_score(self):
        """Display the final score when all challenges are complete"""
        self.text_display.delete('1.0', tk.END)
        self.image_label.config(image='')  # Clear the image
        final_text = f"""
        Contest Complete!
        
        Final Score: {self.score}/{self.total}
        Accuracy: {(self.score/self.total)*100:.1f}%
        
        Thanks for playing!
        """
        self.text_display.insert('1.0', final_text)
        self.status_label.config(text="Contest Complete!")
        self.help_label.config(text="Close the window to exit")

def main():
    root = tk.Tk()
    app = ContestApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
