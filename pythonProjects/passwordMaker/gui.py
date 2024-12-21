import string
import random
from pathlib import Path
import tkinter.font as tkFont
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox, Label

# files path
OUTPUT_PATH = Path(__file__).resolve().parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# password generator function
def generate():
    wordArray = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    numberArray = list(range(10))
    generatedPassword = [None] * 20
    for i in range(len(generatedPassword)):
        generatedPassword[i] = random.choice(wordArray + list(map(str, numberArray)))
    label1.config(text="".join(generatedPassword))


# open window at center function
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


# copy the generated password function
def copy():
    text1 = label1.cget("text")
    if not text1:
        messagebox.showerror("Error!", "No password has been generated.")
    else:
        text = label1.cget("text")
        window.clipboard_clear()
        window.clipboard_append(text)
        window.update()
        messagebox.showinfo("Success!", "The password has been copied!")


# exit function
def exit():
    window.destroy()


# interface
window = Tk()
window.geometry("300x360")
window.configure(bg="#F8DC83")
center_window(window)

canvas = Canvas(
    window,
    bg="#F8DC83",
    height=360,
    width=300,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_text(
    55.0,
    12.0,
    anchor="nw",
    text="Password Maker",
    fill="#000000",
    font=("Inter", 24 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=generate,
    relief="flat"
)
button_1.place(
    x=85.0,
    y=221.0,
    width=131.0,
    height=40.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=exit,
    relief="flat"
)
button_2.place(
    x=100.0,
    y=320.0,
    width=100.0,
    height=28.0
)

label_font = tkFont.Font(size=11)

label1 = Label(
    font=label_font
)
label1.place(
    x=56.0,
    y=169.0,
    width=205.0,
    height=40.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=copy,
    relief="flat"
)
button_3.place(
    x=20.0,
    y=177.0,
    width=24.0,
    height=24.0
)

canvas.create_rectangle(
    -1.0,
    48.0,
    301.0,
    49.0,
    fill="#000000",
    outline="")

window.resizable(False, False)
window.mainloop()
