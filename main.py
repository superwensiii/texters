import tkinter as tk
from tkinter import filedialog, Text
from PIL import Image, ImageTk, ImageGrab
import pytesseract

# Set the path to the Tesseract executable if necessary
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize main window
root = tk.Tk()
root.title("Image to txt bitch")
root.geometry("600x500")

# Set the background color of the window to black
root.configure(bg="gray")

# Global variable to hold the loaded image
loaded_image = None

# Add a title label at the top
title_label = tk.Label(root, text="Image to Text bitches", font=("Helvetica", 16, "bold"), fg="white", bg="gray")
title_label.pack(pady=20)

def open_image():
    global loaded_image
    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    
    if file_path:
        # Load and display the image
        loaded_image = Image.open(file_path)
        display_image(loaded_image)

def display_image(image):
    """ Display an image in the img_label and show necessary buttons """
    img_display = image.copy()
    img_display.thumbnail((300, 300))  # Resize for display
    img_tk = ImageTk.PhotoImage(img_display)
    img_label.config(image=img_tk)
    img_label.image = img_tk

    # Show the "Extract Text" and "Back" buttons
    extract_btn.pack(pady=5)
    back_btn.pack(pady=5)

def extract_text():
    global loaded_image
    if loaded_image:
        try:
            # Perform OCR on the loaded image and display the text
            text = pytesseract.image_to_string(loaded_image)
            text_box.delete("1.0", tk.END)  # Clear previous text
            text_box.insert(tk.END, text)    # Display extracted text in the text box
        except Exception as e:
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, "Error: Could not process the image.")
            print("Error during OCR:", e)
    else:
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, "Please upload an image first.")

def go_back():
    # Clear the loaded image, hide the text box, and reset the interface
    global loaded_image
    loaded_image = None
    img_label.config(image="")
    text_box.delete("1.0", tk.END)
    extract_btn.pack_forget()  # Hide the "Extract Text" button
    back_btn.pack_forget()     # Hide the "Back" button

def paste_image(event=None):
    global loaded_image
    try:
        # Grab the image from the clipboard
        loaded_image = ImageGrab.grabclipboard()
        if isinstance(loaded_image, Image.Image):
            display_image(loaded_image)  # Show the pasted image
            extract_text()  # Automatically extract text from the pasted image
        else:
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, "No image found in clipboard.")
    except Exception as e:
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, "Error: Could not paste image from clipboard.")
        print("Error during paste:", e)

# Add buttons and widgets with customized colors for dark background
upload_btn = tk.Button(root, text="Upload Image", command=open_image, bg="white", fg="black")
upload_btn.pack(pady=10)

extract_btn = tk.Button(root, text="Extract Text", command=extract_text, bg="white", fg="gray")
back_btn = tk.Button(root, text="Back", command=go_back, bg="white", fg="gray")

img_label = tk.Label(root, bg="gray")
img_label.pack()

# Text box with white background and black text
text_box = Text(root, wrap='word', height=10, width=50, bg="white", fg="gray", bd=2, relief="sunken")
text_box.pack(pady=10)

# Hide the "Extract Text" and "Back" buttons initially
extract_btn.pack_forget()
back_btn.pack_forget()

# Bind "Ctrl+V" to the paste_image function
root.bind('<Control-v>', paste_image)

root.mainloop()
