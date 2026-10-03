import tkinter as tk
import random
import os
import sys
from PIL import Image, ImageTk

def ruta(nombre):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, nombre)

# --- Config ---
IMAGEN = ruta("dvd.png")
ALTO_LOGO = 120
VELOCIDAD = 4

COLORES = [(255, 75, 75), (75, 255, 75), (75, 155, 255), (255, 255, 75),
           (255, 75, 255), (75, 255, 255), (255, 149, 75), (255, 255, 255)]

# --- Preparar imagen ---
base = Image.open(IMAGEN).convert("RGBA")
escala = ALTO_LOGO / base.height
base = base.resize((int(base.width * escala), ALTO_LOGO), Image.LANCZOS)

pixeles = list(base.getdata())
br, bg_, bb, ba = pixeles[0]
fondo_transparente = ba < 10

mascara = []
for r, g, b, a in pixeles:
    if fondo_transparente:
        mascara.append(255 if a > 10 else 0)
    else:
        if a < 10 or (abs(r - br) < 60 and abs(g - bg_) < 60 and abs(b - bb) < 60):
            mascara.append(0)
        else:
            mascara.append(255)

def logo_coloreado(color):
    img = Image.new("RGBA", base.size, (0, 0, 0, 0))
    img.putdata([(color[0], color[1], color[2], m) for m in mascara])
    return ImageTk.PhotoImage(img)

# --- Ventana ---
root = tk.Tk()
root.title("DVD")
root.geometry("800x600")
root.configure(bg="black")
try:
    root.iconbitmap(ruta("DVD_Drive_icon.ico"))
except Exception:
    pass
root.bind("<Escape>", lambda e: root.destroy())

canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)
root.update()
W, H = canvas.winfo_width(), canvas.winfo_height()

def al_redimensionar(e):
    global W, H
    W, H = e.width, e.height
canvas.bind("<Configure>", al_redimensionar)

lw, lh = base.size
logos = []   # cada logo: {"id", "img", "dx", "dy"}

def crear_logo(x, y, color=None):
    if color is None:
        color = random.choice(COLORES)
    img = logo_coloreado(color)
    item = canvas.create_image(x, y, anchor="nw", image=img)
    dx = VELOCIDAD * random.choice([-1, 1])
    dy = VELOCIDAD * random.choice([-1, 1])
    logo = {"id": item, "img": img, "dx": dx, "dy": dy}
    logos.append(logo)
    # al clicar este logo, sale otro
    canvas.tag_bind(item, "<Button-1>", lambda e: al_clicar(x))
    return logo

def al_clicar(_=None):
    # nuevo logo en posicion aleatoria dentro de la ventana
    x = random.randint(0, max(1, W - lw))
    y = random.randint(0, max(1, H - lh))
    crear_logo(x, y)

# logo inicial en blanco
primero = crear_logo(100, 100, (255, 255, 255))

def mover():
    for lg in logos:
        canvas.move(lg["id"], lg["dx"], lg["dy"])
        x, y = canvas.coords(lg["id"])
        toca = False
        if x <= 0 or x + lw >= W:
            lg["dx"] = -lg["dx"]
            toca = True
        if y <= 0 or y + lh >= H:
            lg["dy"] = -lg["dy"]
            toca = True
        if toca:
            lg["img"] = logo_coloreado(random.choice(COLORES))
            canvas.itemconfig(lg["id"], image=lg["img"])
    root.after(16, mover)

mover()
root.mainloop()
