from tkinter import *
import time
import random

WIDTH = 800
HEIGHT = 500

tk = Tk()
canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bg="light blue")
tk.title("Jump Around")
canvas.pack()


class Player:
    def __init__(self):
        self.frames_l = [PhotoImage(file="stickman/CG1.gif"),
                         PhotoImage(file="stickman/CG2.gif"),
                         PhotoImage(file="stickman/CG3.gif"),
                         PhotoImage(file="stickman/CG4.gif"),
                         PhotoImage(file="stickman/CG5.gif"),
                         PhotoImage(file="stickman/CG6.gif"),
                         PhotoImage(file="stickman/CG7.gif"),
                         PhotoImage(file="stickman/CG8.gif"),
                         PhotoImage(file="stickman/CG9.gif")]
        self.frames_r = [PhotoImage(file="stickman/CD1.gif"),
                         PhotoImage(file="stickman/CD2.gif"),
                         PhotoImage(file="stickman/CD3.gif"),
                         PhotoImage(file="stickman/CD4.gif"),
                         PhotoImage(file="stickman/CD5.gif"),
                         PhotoImage(file="stickman/CD6.gif"),
                         PhotoImage(file="stickman/CD7.gif"),
                         PhotoImage(file="stickman/CD8.gif"),
                         PhotoImage(file="stickman/CD9.gif")]
        self.frames_r_j = [PhotoImage(file="stickman/1r.gif"),
                         PhotoImage(file="stickman/2r.gif")]

        self.frames_l_j = [PhotoImage(file="stickman/1.gif"),
                           PhotoImage(file="stickman/2.gif")]

        self.image = canvas.create_image(WIDTH / 2, HEIGHT - 100, anchor=NW,
                                         image=self.frames_l[0])
        self.speedx = 0
        self.speedy = 0
        canvas.bind_all("<KeyPress-Left>", self.move)
        canvas.bind_all("<KeyPress-Right>", self.move)
        canvas.bind_all("<KeyPress-space>", self.jump)
        canvas.bind_all("<KeyRelease-Left>", self.stop)
        canvas.bind_all("<KeyRelease-Right>", self.stop)
        self.jumping = False
        self.current_frame = 0
        self.current_frame2 = 0
        self.last_time = time.time()

    def jump(self, event):
        if not self.jumping:
            self.jumping = True
            self.speedy = -20

    def stop(self, event):
        self.speedx = 0

    def move(self, event):
        if event.keysym == 'Right':
            self.speedx = 6
        if event.keysym == 'Left':
            self.speedx = -6

    def animate(self):
        now = time.time()
        if now - self.last_time > 0.05:
            self.last_time = now
            self.current_frame = (self.current_frame + 1) % 9
            self.current_frame2 = (self.current_frame2 +1) % 1
        if self.speedx < 0:
            canvas.itemconfig(self.image, image=self.frames_l[self.current_frame])
        if self.speedx > 0:
            canvas.itemconfig(self.image, image=self.frames_r[self.current_frame])
        if self.speedy < 0:
            canvas.itemconfig(self.image, image=self.frames_r_j[self.current_frame2])
        if self.speedy > 0:
            canvas.itemconfig(self.image, image=self.frames_l_j[self.current_frame2])

    def update(self):
        self.animate()
        self.speedy += 1
        canvas.move(self.image, self.speedx, self.speedy)
        pos = canvas.coords(self.image)
        self.pos = pos
        left, right = pos[0], pos[0] + 35
        top, bottom = pos[1], pos[1] + 60
        # check if player hits a platform
        for plat in platforms:
            if self.speedy > 0:
                hits = canvas.find_overlapping(left, top, right, bottom)
                if plat.image in hits:
                    self.jumping = False
                    self.speedy = 0
                    canvas.coords(self.image, left, plat.top - 60)

        # wrap around edges of screen
        if right > WIDTH:
            canvas.coords(self.image, 0, top)
        if left < 0:
            canvas.coords(self.image, WIDTH - 35, top)


class Platform:
    def __init__(self, x, y, w, h):
        self.image = canvas.create_rectangle(x, y, x + w, y + h, fill="green")
        self.top = y


player = Player()
platforms = []
plat1 = Platform(0, HEIGHT - 40, WIDTH, 40)
platforms.append(plat1)
platforms.append(Platform(150, 205, 100, 40))
platforms.append(Platform(450, 120, 100, 40))
platforms.append(Platform(375, 320, 200, 40))
platforms.append(Platform(45, 20, 100, 40))
score = 0
score_label = canvas.create_text(WIDTH / 2, 30, text="0", font=('Arial', 22))
while True:
    canvas.itemconfig(score_label, text=str(score))
    player.update()
    # die!
    if player.pos[1] > HEIGHT:
        break
    # scroll when player reaches top 1/4 of screen
    if player.pos[1] < HEIGHT / 4 and player.speedy < 0:
        canvas.move(player.image, 0, -player.speedy)
        for plat in platforms:
            canvas.move(plat.image, 0, -player.speedy)
            plat.top -= player.speedy
            if plat.top > HEIGHT:
                score += 10
                canvas.delete(plat.image)
                platforms.remove(plat)
    while len(platforms) < 6:
        newplat = Platform(random.randrange(50, WIDTH - 100),
                           random.randrange(10, 20),
                           random.randrange(100, 150),
                           40)
        platforms.append(newplat)
    tk.update()
    time.sleep(0.01 )