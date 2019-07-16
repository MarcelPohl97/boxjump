from tkinter import *

root = Tk()
game_root = Canvas(root, width=600, height=200)
game_root.pack()

class Player:
    def __init__(self):
        self.player_id = game_root.create_rectangle(20, 20, 0, 0, fill="red")
        self.x = 0
        self.y = 0
        game_root.bind_all('<KeyPress>', self.OnKeyPress)
        game_root.bind_all('<KeyRelease>', self.OffKeyPress)

    def move(self):
        c = game_root.coords(self.player_id)

    def OnKeyPress(self, event):
        self.key = event.keysym
        if self.key == "w":
            print("I jump now")

    def OffKeyPress(self, event):
        self.key = event.keysym
        if self.key == "w":
            print("I Stop jumping")


p = Player()

while True:
    p.move()
    root.update()
    root.after(6)