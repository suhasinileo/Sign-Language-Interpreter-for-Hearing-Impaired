import speech_recognition as sr
import tkinter as tk
from PIL import Image, ImageTk
import os
#import easygui as eg

# Predefined characters
isl_chars = list("abcdefghijklmnopqrstuvwxyz")  # Assuming you want to recognize lowercase letters

exit_phrases = ['thank you', 'bye', 'goodbye', 'exit']

class ImageLabel(tk.Label):
    def __init__(self, master=None):
        super().__init__(master)
        self.image = None  # To hold a reference to the image

    def load(self, image_path):
        try:
            im = Image.open(image_path)
            im.resize((800,800))
            self.image = ImageTk.PhotoImage(im)  # Keep a reference
            self.config(image=self.image)  # Set the image on the label
        except FileNotFoundError:
            print(f"Image '{image_path}' not found.")

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio).lower()
        except (sr.UnknownValueError, sr.RequestError):
            return None

def display_character_images(recognized_text):
    root = tk.Tk()
    lbl = ImageLabel(root)
    lbl.pack()

    for char in recognized_text:
        if char in isl_chars:
            img_path = os.path.join('letters', f'{char}.jpg')
            lbl.load(img_path)
            root.update()  # Update the label to show the new image
            root.after(800)  # Wait for 0.8 seconds before the next image

    # Close the window after displaying all characters
    root.after(800 * len(recognized_text) + 20, root.destroy)
    root.mainloop()  # Start the Tkinter event loop

def show_start_menu():
    def on_start():
        root.destroy()  # Close the menu
        start_listening()

    root = tk.Tk()
    root.title("Speech to Sign Language Converter")
    root.geometry("400x300")  # Set the window size
    root.configure(bg="#f0f0f0")  # Background color

    # Title Label
    title_label = tk.Label(root, text="Hearing Impairment Assistant", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
    title_label.pack(pady=20)

    # if you want to add a n image
    # img = ImageTk.PhotoImage(Image.open("your_image.png"))
    # img_label = tk.Label(root, image=img, bg="#f0f0f0")
    # img_label.pack(pady=10)

    # Start Listening Button
    start_button = tk.Button(root, text="Start Listening", command=on_start, width=20, height=2, bg="#4CAF50", fg="white", font=("Helvetica", 12))
    start_button.pack(pady=10)

    # Exit Button
    exit_button = tk.Button(root, text="Exit", command=root.quit, width=20, height=2, bg="#f44336", fg="white", font=("Helvetica", 12))
    exit_button.pack(pady=10)

    root.mainloop()

def start_listening():
    while True:
        recognized_text = recognize_speech()
        if recognized_text:
            print(f'You said: {recognized_text}')

            # Check for exit phrases
            if any(exit_phrase in recognized_text for exit_phrase in exit_phrases):
                print("Exiting...")
                break

            display_character_images(recognized_text)
        else:
            print("No valid speech recognized. Listening continues...")

if __name__ == "__main__":
    show_start_menu()

