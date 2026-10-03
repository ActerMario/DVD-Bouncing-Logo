import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
import json
import os
import sys
import random
from PIL import Image, ImageTk

# ---------------------------------------------------------------------------
#  Rutas / configuracion persistente
# ---------------------------------------------------------------------------
def recurso(nombre):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, nombre)

APPDATA = os.environ.get("APPDATA", os.path.expanduser("~"))
CARPETA_CFG = os.path.join(APPDATA, "dvd_screensaver")
os.makedirs(CARPETA_CFG, exist_ok=True)
CONFIG = os.path.join(CARPETA_CFG, "config.json")

CONFIG_DEFECTO = {
    "colores": ["#ff4b4b", "#4bff4b", "#4b9bff", "#ffff4b",
                "#ff4bff", "#4bffff", "#ff954b", "#ffffff"],
    "velocidad": 5,
    "imagen": "",                 # vacio = usa la imagen incluida (dvd.png)
    "modo_color": "rebote",       # "nunca" | "rebote" | "intervalo"
    "intervalo_seg": 3,
    "fondo_cambia": False,
}

def cargar_config():
    cfg = dict(CONFIG_DEFECTO)
    try:
        with open(CONFIG, "r", encoding="utf-8") as f:
            cfg.update(json.load(f))
    except Exception:
        pass
    if not cfg["colores"]:
        cfg["colores"] = list(CONFIG_DEFECTO["colores"])
    return cfg

def guardar_config(cfg):
    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

def hex_a_rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def poner_icono(ventana):
    try:
        ventana.iconbitmap(recurso("DVD_Drive_icon.ico"))
    except Exception:
        pass

# ---------------------------------------------------------------------------
#  PANEL DE CONFIGURACION  (/c)
# ---------------------------------------------------------------------------
def abrir_configurador():
    cfg = cargar_config()

    win = tk.Tk()
    win.title("Configuracion - DVD salvapantallas")
    poner_icono(win)
    win.resizable(False, False)
    pad = {"padx": 10, "pady": 6}

    # --- Colores ---
    marco_col = ttk.LabelFrame(win, text="Colores que aparecen")
    marco_col.grid(row=0, column=0, sticky="nsew", **pad)

    lista = tk.Listbox(marco_col, height=6, width=14)
    lista.grid(row=0, column=0, rowspan=3, padx=6, pady=6)
    for c in cfg["colores"]:
        lista.insert("end", c)

    def refrescar_muestra(*_):
        sel = lista.curselection()
        if sel:
            muestra.config(bg=lista.get(sel[0]))
    lista.bind("<<ListboxSelect>>", refrescar_muestra)

    muestra = tk.Label(marco_col, text="   ", width=4, relief="sunken", bg="#ffffff")
    muestra.grid(row=0, column=1, padx=6)

    def anadir_color():
        _, hexc = colorchooser.askcolor()
        if hexc:
            lista.insert("end", hexc)
    def quitar_color():
        sel = lista.curselection()
        if sel:
            lista.delete(sel[0])
    ttk.Button(marco_col, text="Anadir", command=anadir_color).grid(row=1, column=1, padx=6, sticky="ew")
    ttk.Button(marco_col, text="Quitar", command=quitar_color).grid(row=2, column=1, padx=6, sticky="ew")

    # --- Velocidad ---
    marco_vel = ttk.LabelFrame(win, text="Velocidad")
    marco_vel.grid(row=1, column=0, sticky="nsew", **pad)
    var_vel = tk.IntVar(value=cfg["velocidad"])
    ttk.Scale(marco_vel, from_=1, to=20, variable=var_vel,
              orient="horizontal", length=220).grid(row=0, column=0, padx=8, pady=8)
    lbl_vel = ttk.Label(marco_vel, text=str(var_vel.get()))
    lbl_vel.grid(row=0, column=1, padx=6)
    var_vel.trace_add("write", lambda *_: lbl_vel.config(text=str(var_vel.get())))

    # --- Imagen ---
    marco_img = ttk.LabelFrame(win, text="Imagen (logo)")
    marco_img.grid(row=2, column=0, sticky="nsew", **pad)
    var_img = tk.StringVar(value=cfg["imagen"] or "(incluida: dvd.png)")
    ttk.Label(marco_img, textvariable=var_img, width=36).grid(row=0, column=0, padx=6, pady=6)
    def elegir_imagen():
        ruta = filedialog.askopenfilename(
            filetypes=[("Imagenes", "*.png *.gif *.jpg *.jpeg *.bmp")])
        if ruta:
            var_img.set(ruta)
    ttk.Button(marco_img, text="Examinar...", command=elegir_imagen).grid(row=0, column=1, padx=6)

    # --- Cuando cambia el color del logo ---
    marco_modo = ttk.LabelFrame(win, text="El logo cambia de color...")
    marco_modo.grid(row=3, column=0, sticky="nsew", **pad)
    var_modo = tk.StringVar(value=cfg["modo_color"])
    ttk.Radiobutton(marco_modo, text="Nunca", value="nunca",
                    variable=var_modo).grid(row=0, column=0, sticky="w", padx=8)
    ttk.Radiobutton(marco_modo, text="Al rebotar", value="rebote",
                    variable=var_modo).grid(row=1, column=0, sticky="w", padx=8)
    fila = ttk.Frame(marco_modo); fila.grid(row=2, column=0, sticky="w", padx=8, pady=2)
    ttk.Radiobutton(fila, text="Cada", value="intervalo",
                    variable=var_modo).pack(side="left")
    var_int = tk.IntVar(value=cfg["intervalo_seg"])
    ttk.Spinbox(fila, from_=1, to=60, width=4, textvariable=var_int).pack(side="left", padx=4)
    ttk.Label(fila, text="segundos").pack(side="left")

    # --- Fondo ---
    marco_fondo = ttk.LabelFrame(win, text="Fondo")
    marco_fondo.grid(row=4, column=0, sticky="nsew", **pad)
    var_fondo = tk.BooleanVar(value=cfg["fondo_cambia"])
    ttk.Checkbutton(marco_fondo, text="El fondo tambien cambia de color",
                    variable=var_fondo).grid(row=0, column=0, sticky="w", padx=8, pady=6)

    # --- Guardar ---
    def guardar():
        colores = list(lista.get(0, "end"))
        if not colores:
            messagebox.showwarning("Colores", "Deja al menos un color.")
            return
        nueva = {
            "colores": colores,
            "velocidad": int(var_vel.get()),
            "imagen": "" if var_img.get().startswith("(incluida") else var_img.get(),
            "modo_color": var_modo.get(),
            "intervalo_seg": int(var_int.get()),
            "fondo_cambia": bool(var_fondo.get()),
        }
        guardar_config(nueva)
        win.destroy()

    barra = ttk.Frame(win); barra.grid(row=5, column=0, sticky="e", **pad)
    ttk.Button(barra, text="Guardar", command=guardar).pack(side="right", padx=4)
    ttk.Button(barra, text="Cancelar", command=win.destroy).pack(side="right")

    win.mainloop()

# ---------------------------------------------------------------------------
#  SALVAPANTALLAS  (/s)
# ---------------------------------------------------------------------------
def ejecutar_salvapantallas():
    cfg = cargar_config()

    ruta_img = cfg["imagen"] if cfg["imagen"] and os.path.exists(cfg["imagen"]) else recurso("dvd.png")
    base = Image.open(ruta_img).convert("RGBA")
    ALTO = 120
    escala = ALTO / base.height
    base = base.resize((int(base.width * escala), ALTO), Image.LANCZOS)

    pixeles = list(base.getdata())
    br, bg_, bb, ba = pixeles[0]
    fondo_transp = ba < 10
    mascara = []
    for r, g, b, a in pixeles:
        if fondo_transp:
            mascara.append(255 if a > 10 else 0)
        else:
            if a < 10 or (abs(r - br) < 60 and abs(g - bg_) < 60 and abs(b - bb) < 60):
                mascara.append(0)
            else:
                mascara.append(255)

    def logo_coloreado(rgb):
        img = Image.new("RGBA", base.size, (0, 0, 0, 0))
        img.putdata([(rgb[0], rgb[1], rgb[2], m) for m in mascara])
        return ImageTk.PhotoImage(img)

    colores = [hex_a_rgb(c) for c in cfg["colores"]]
    vel = cfg["velocidad"]
    modo = cfg["modo_color"]
    intervalo = cfg["intervalo_seg"] * 1000
    fondo_cambia = cfg["fondo_cambia"]

    root = tk.Tk()
    root.title("DVD")
    poner_icono(root)
    root.configure(bg="black")
    root.attributes("-fullscreen", True)
    root.config(cursor="none")

    canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    root.update()
    W, H = root.winfo_screenwidth(), root.winfo_screenheight()

    color_inicial = (255, 255, 255) if modo == "nunca" else random.choice(colores)
    img_actual = logo_coloreado(color_inicial)
    logo = canvas.create_image(100, 100, anchor="nw", image=img_actual)
    lw, lh = base.size
    dx = dy = vel

    def rgb_hex(rgb):
        return "#%02x%02x%02x" % rgb

    def nuevo_color():
        global_img = logo_coloreado(random.choice(colores))
        canvas.itemconfig(logo, image=global_img)
        canvas.image = global_img          # evitar que el recolector lo borre
        if fondo_cambia:
            canvas.config(bg=rgb_hex(random.choice(colores)))

    # salir al interactuar
    _pos = [None]
    def salir(e=None):
        root.destroy()
    def mov(e):
        if _pos[0] is None:
            _pos[0] = (e.x_root, e.y_root); return
        if abs(e.x_root - _pos[0][0]) > 8 or abs(e.y_root - _pos[0][1]) > 8:
            salir()
    root.bind("<Key>", salir)
    root.bind("<Button>", salir)
    root.bind("<Motion>", mov)
    root.focus_force()

    def mover():
        nonlocal dx, dy
        canvas.move(logo, dx, dy)
        x, y = canvas.coords(logo)
        toca = False
        if x <= 0 or x + lw >= W:
            dx = -dx; toca = True
        if y <= 0 or y + lh >= H:
            dy = -dy; toca = True
        if toca and modo == "rebote":
            nuevo_color()
        root.after(16, mover)

    if modo == "intervalo":
        def tick():
            nuevo_color()
            root.after(intervalo, tick)
        root.after(intervalo, tick)

    mover()
    root.mainloop()

# ---------------------------------------------------------------------------
#  Punto de entrada: Windows manda /s /c /p
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    arg = sys.argv[1][:2].lower() if len(sys.argv) > 1 else "/c"
    if arg == "/p":
        sys.exit(0)            # sin vista previa en el recuadro
    elif arg == "/c":
        abrir_configurador()
    else:                      # /s o sin argumento conocido
        ejecutar_salvapantallas()
