# 📀 DVD Bouncing Logo

El clásico logotipo de DVD rebotando, desarrollado en **Python** con `tkinter` y `Pillow (PIL)`. El proyecto incluye **dos versiones**:

* 🖥️ **Windows App** — una aplicación en ventana que puedes abrir cuando quieras.
* 💤 **ScreenSaver** — un salvapantallas nativo de Windows (`.scr`) con panel de configuración.

## ✨ Características

* **Físicas de rebote clásicas:** El logotipo se desplaza a unos 60 FPS estables y cambia de dirección de manera realista al chocar con los bordes.
* **Panel de configuración integrado (versión ScreenSaver):** Ajusta la velocidad, gestiona la paleta de colores, elige la imagen y define cuándo cambia de color.
* **Modos de cambio de color:** El logo puede no cambiar nunca, cambiar al rebotar o cambiar cada cierto número de segundos.
* **Soporte para logotipos personalizados:** Admite cualquier imagen (`.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`).
* **Comportamiento nativo de Windows (ScreenSaver):** Responde a los argumentos del sistema `/s` (ejecutar), `/c` (configurar) y `/p` (vista previa).
* **Interrupción inteligente (ScreenSaver):** Se cierra al pulsar cualquier tecla o hacer clic, con una tolerancia de 8 píxeles en el ratón para evitar cierres accidentales.
* **Cambio de fondo opcional:** Modo donde el color de fondo también cambia en sincronía con el logo.
* **Configuración persistente:** Los ajustes del salvapantallas se guardan en `%APPDATA%\dvd_screensaver\config.json`, por lo que funcionan aunque el `.scr` esté instalado en `System32`.

## ⬇️ Descargas (Releases)

Si no quieres compilar nada, en la sección **[Releases](../../releases)** tienes los dos ejecutables listos para usar:

* **`DVD.scr`** — el salvapantallas. Clic derecho > **Instalar**.
* **`dvd.exe`** — la app en ventana. Doble clic para abrirla.

## 📂 Estructura del Proyecto

```text
├── Windows App/
│   ├── dvd.py               # Versión en ventana (800x600, redimensionable)
│   ├── dvd.png              # Logotipo
│   └── DVD_Drive_icon.ico   # Icono de la ventana y del ejecutable
├── ScreenSaver/
│   ├── dvd_screensaver.py   # Versión salvapantallas con configurador
│   ├── dvd.png              # Logotipo por defecto
│   └── DVD_Drive_icon.ico   # Icono del ejecutable y de las ventanas
└── README.md                # Documentación del proyecto
```

## 🛠️ Requisitos para Desarrollo

* Python 3.x
* Pillow:
  ```bash
  pip install Pillow
  ```

Para compilar los ejecutables también necesitas PyInstaller:
```bash
pip install pyinstaller
```

---

## 🖥️ Windows App (versión en ventana)

Abre una ventana de 800×600 (redimensionable) con el logo rebotando. Se cierra con **Esc**.

**Ejecutar desde el código:**
```bash
cd "Windows App"
python dvd.py
```

**Compilar a .exe** (con `dvd.png` y `DVD_Drive_icon.ico` al lado):
```bash
pyinstaller --noconsole --onefile --icon=DVD_Drive_icon.ico --add-data "dvd.png;." --add-data "DVD_Drive_icon.ico;." dvd.py
```
El ejecutable queda en `dist\dvd.exe`.

---

## 💤 ScreenSaver (versión salvapantallas)

### 1. Compilar el ejecutable
En la carpeta `ScreenSaver` (con `dvd.png` y `DVD_Drive_icon.ico` al lado):
```bash
pyinstaller --noconsole --onefile --icon=DVD_Drive_icon.ico --add-data "dvd.png;." --add-data "DVD_Drive_icon.ico;." dvd_screensaver.py
```

### 2. Cambiar la extensión a .scr
En la carpeta `dist`, renombra `dvd_screensaver.exe` a **`DVD.scr`** (o usa `ren dist\dvd_screensaver.exe DVD.scr`).

### 3. Instalar en el sistema
Haz clic derecho sobre `DVD.scr` y selecciona **Instalar**. Se abrirá directamente la ventana de protector de pantalla de Windows con el tuyo ya seleccionado.

> **Opcional:** si no te aparece la opción "Instalar" o quieres que quede siempre disponible en la lista de protectores, copia `DVD.scr` a `C:\Windows\System32` *(requiere permisos de administrador)*.

### ⚙️ Configuración en Windows 11
1. Abre **Configuración** (`Win + I`) > **Personalización** > **Pantalla de bloqueo**.
2. Baja y haz clic en **Protector de pantalla**.
3. Selecciona **DVD** en la lista desplegable.
4. Haz clic en **Configuración** para abrir el panel visual, o define el tiempo de espera para que se active automáticamente.

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia [MIT](LICENSE).
