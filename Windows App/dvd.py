import tkinter as tk
import random
import os
import sys
from PIL import Image, ImageTk

def ruta(nombre):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, nombre)

# --- Config ---
IMAGEN = ruta("dvd.png")   # tu imagen, en la misma carpeta que este script
ALTO_LOGO = 120      # altura del logo en pixeles
VELOCIDAD = 4

COLORES = [(255, 75, 75), (75, 255, 75), (75, 155, 255), (255, 255, 75),
           (255, 75, 255), (75, 255, 255), (255, 149, 75), (255, 255, 255)]

# --- Preparar imagen ---
base = Image.open(IMAGEN).convert("RGBA")
escala = ALTO_LOGO / base.height
base = base.resize((int(base.width * escala), ALTO_LOGO), Image.LANCZOS)

pixeles = list(base.getdata())

# Color de la esquina = fondo de referencia
br, bg_, bb, ba = pixeles[0]
fondo_transparente = ba < 10

# Mascara: el logo = todo lo que NO sea el fondo
mascara = []
for r, g, b, a in pixeles:
    if fondo_transparente:
        # el fondo es transparente -> el logo son los pixeles opacos
        mascara.append(255 if a > 10 else 0)
    else:
        # el fondo es un color solido -> el logo es lo que difiere de el
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

img_actual = logo_coloreado((255, 255, 255))   # empieza en blanco
logo = canvas.create_image(100, 100, anchor="nw", image=img_actual)
lw, lh = base.size
dx = dy = VELOCIDAD

def cambiar_color():
    global img_actual
    img_actual = logo_coloreado(random.choice(COLORES))
    canvas.itemconfig(logo, image=img_actual)

def mover():
    global dx, dy
    canvas.move(logo, dx, dy)
    x, y = canvas.coords(logo)
    toca = False
    if x <= 0 or x + lw >= W:
        dx = -dx
        toca = True
    if y <= 0 or y + lh >= H:
        dy = -dy
        toca = True
    if toca:
        cambiar_color()
    root.after(16, mover)

mover()
root.mainloop()
