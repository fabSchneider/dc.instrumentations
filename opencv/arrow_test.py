from tkinter import * 
import pyautogui

x, y = pyautogui.position()

canvas = Tk()
canvas.title("Arrow Test")
canvas.geometry("700x700")

my_can = Canvas(canvas, width=600, height=600, bg="gray")
my_can.pack(pady=50) 

my_can.create_line(300, 300, x, y, fill="black", width=5, arrow="last")


canvas.mainloop()