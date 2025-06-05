import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
import cv2
from easygui import buttonbox
import os
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string

def func():
    r = sr.Recognizer()
    
    isl_gif = [...]  # Same list as before — no change needed here
    arr = list(string.ascii_lowercase)  # Simpler way to get a-z

    # Directories
    letter_images_dir = r'C:\Users\suhas\Desktop\project\app\pro\letters'
    gif_images_dir = r'C:\Users\suhas\Desktop\project\app\pro\ISL_Gifs'

    class ImageLabel(tk.Label):
        def load(self, im):
            if isinstance(im, str):
                im = Image.open(im)
            self.loc = 0
            self.frames = []

            try:
                for _ in count(1):
                    self.frames.append(ImageTk.PhotoImage(im.copy()))
                    im.seek(im.tell() + 1)
            except EOFError:
                pass

            self.delay = im.info.get('duration', 100)

            if len(self.frames) == 1:
                self.config(image=self.frames[0])
            else:
                self.next_frame()

        def unload(self):
            self.config(image=None)
            self.frames = None

        def next_frame(self):
            if self.frames:
                self.loc = (self.loc + 1) % len(self.frames)
                self.config(image=self.frames[self.loc])
                self.after(self.delay, self.next_frame)

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            print("Say something...")
            audio = r.listen(source)

            try:
                a = r.recognize_sphinx(audio)
                print("You said:", a)
                a = a.lower().translate(str.maketrans('', '', string.punctuation))

                if a in ['goodbye', 'good bye', 'bye']:
                    print("Goodbye!")
                    break

                elif a in isl_gif:
                    gif_path = os.path.join(gif_images_dir, f'{a}.gif')
                    if os.path.exists(gif_path):
                        root = tk.Tk()
                        lbl = ImageLabel(root)
                        lbl.pack()
                        lbl.load(gif_path)
                        root.mainloop()
                    else:
                        print(f"GIF not found for: {a}")

                else:
                    for char in a:
                        if char in arr:
                            img_path = os.path.join(letter_images_dir, f'{char}.jpg')
                            if os.path.exists(img_path):
                                img = Image.open(img_path)
                                img_np = np.asarray(img)
                                plt.imshow(img_np)
                                plt.axis('off')
                                plt.draw()
                                plt.pause(0.8)
                            else:
                                print(f"Image not found for: {char}")
                    plt.close()

            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Sphinx error; {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

# GUI loop
while True:
    image = r"C:\Users\suhas\Desktop\project\app\pro\signlang.png"
    msg = "HEARING IMPAIRMENT ASSISTANT"
    choices = ["Live Voice", "All Done!"]
    reply = buttonbox(msg, image=image, choices=choices)
    if reply == "Live Voice":
        func()
    elif reply == "All Done!":
        break
