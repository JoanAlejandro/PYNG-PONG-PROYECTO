import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import firebase_admin
from firebase_admin import credentials, db
import pygame
import random
import sys

# Inicializar Firebase
cred = credentials.Certificate("database-pyng-p0ng-firebase-adminsdk-fbsvc-8ea6df79e7.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://database-pyng-p0ng-default-rtdb.firebaseio.com/"
})

# Iniciar pygame
pygame.init()

# Configuración básica del juego
ANCHO, ALTO = 800, 600
COLOR_FONDO = (0, 0, 0)
COLOR_BOLA = (255, 255, 255)
COLOR_PALETA = (255, 0, 0)
VELOCIDAD_BOLA = 5
VELOCIDAD_PALETA = 15

def abrir_menu_principal(usuario):
    root.withdraw()
    menu = tk.Tk()
    menu.title("PYNG-P0NG")
    menu.geometry("1000x650")
    menu.configure(bg="black")
    menu.iconbitmap("icono.ico")

    label_Titulo = tk.Label(menu, text="P Y N G   P 0 N G", bg="red", font=("Calibri", 40, "bold"))
    label_Titulo.place(x=330, y=20)
    label_pie = tk.Label(menu, text="Developed by: Joan Muñoz", fg="red", bg="black", font=("Calibri", 20, "italic"))
    label_pie.place(x=690, y=600)
    label_pie = tk.Label(menu, text=f"Jugador \"{usuario}\"", fg="red", bg="black", font=("Calibri", 20, "italic"))
    label_pie.place(x=40, y=600)

    btn_jugar = tk.Button(menu, text="Jugar", command=lambda: iniciar_juego(), fg="red", bg="black", font=("Calibri", 20, "bold"))
    btn_jugar.place(x=40, y=200)
    btn_salir = tk.Button(menu, text="Salir", command=lambda: cerrar_menu(menu), fg="red", bg="black", font=("Calibri", 20, "bold"))
    btn_salir.place(x=40, y=300)

def iniciar_juego():
    # Crear una ventana de Pygame
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("PYNG-P0NG")
    
    # Paletas del jugador y oponente
    jugador = pygame.Rect(30, ALTO // 2 - 60, 20, 120)
    oponente = pygame.Rect(ANCHO - 50, ALTO // 2 - 60, 20, 120)
    
    # Pelota
    bola = pygame.Rect(ANCHO // 2 - 15, ALTO // 2 - 15, 30, 30)
    bola_dx = VELOCIDAD_BOLA
    bola_dy = VELOCIDAD_BOLA
    
    # Reloj para controlar los FPS
    reloj = pygame.time.Clock()

    # Bucle del juego
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento del jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] and jugador.top > 0:
            jugador.y -= VELOCIDAD_PALETA
        if teclas[pygame.K_DOWN] and jugador.bottom < ALTO:
            jugador.y += VELOCIDAD_PALETA

        # Movimiento del oponente (movimiento aleatorio)
        if oponente.centery < bola.centery:
            oponente.y += VELOCIDAD_PALETA
        elif oponente.centery > bola.centery:
            oponente.y -= VELOCIDAD_PALETA

        # Movimiento de la pelota
        bola.x += bola_dx
        bola.y += bola_dy

        # Rebote de la pelota en los bordes
        if bola.top <= 0 or bola.bottom >= ALTO:
            bola_dy = -bola_dy
        if bola.colliderect(jugador) or bola.colliderect(oponente):
            bola_dx = -bola_dx

        # Limpiar la pantalla
        ventana.fill(COLOR_FONDO)

        # Dibujar los elementos
        pygame.draw.rect(ventana, COLOR_PALETA, jugador)
        pygame.draw.rect(ventana, COLOR_PALETA, oponente)
        pygame.draw.ellipse(ventana, COLOR_BOLA, bola)

        # Actualizar la ventana
        pygame.display.flip()

        # Controlar los FPS
        reloj.tick(60)

def cerrar_menu(menu):
    # Cerrar la ventana del menú principal
    menu.destroy()
    
    # Borrar la información de los cuadros de texto
    entry_usuario.delete(0, tk.END)
    entry_contraseña.delete(0, tk.END)
    
    # Volver a mostrar la ventana de inicio de sesión
    root.deiconify()

def registrar_usuario():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    if usuario == "":
        messagebox.showerror("Error", "Digite un nombre de usuario.")
        return
    if contraseña == "":
        messagebox.showerror("Error", "Digite una contraseña.")
        return
    ref = db.reference(f"usuarios/{usuario}")
    if ref.get():
        messagebox.showerror("Error", "El nombre de usuario ya está en uso.")
    else:
        ref.set({"contraseña": contraseña})
        messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")

def logueo():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    if usuario == "":
        messagebox.showerror("Error", "Digite el nombre de usuario.")
        return
    if contraseña == "":
        messagebox.showerror("Error", "Digite la contraseña.")
        return
    ref = db.reference(f"usuarios/{usuario}")
    dato_usuario = ref.get()
    if dato_usuario and dato_usuario.get("contraseña") == contraseña:
        messagebox.showinfo("Bienvenido", f"¡Bienvenido al juego, {usuario}!")
        abrir_menu_principal(usuario)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Crear ventana principal
root = tk.Tk()
root.title("PYNG-P0NG")
root.geometry("1000x650")
root.configure(bg="black")
root.iconbitmap("icono.ico")

# Etiquetas y entradas
label_Titulo = tk.Label(root, text="P Y N G   P 0 N G", bg="red", font=("Calibri", 40, "bold"))
label_Titulo.place(x=330, y=20)
label_pie = tk.Label(root, text="Developed by: Joan Muñoz", fg="red", bg="black", font=("Calibri", 20, "italic"))
label_pie.place(x=690, y=600)
label_usuario = tk.Label(root, text="Usuario:", fg="red", bg="black", font=("Calibri", 25, "underline"))
label_usuario.place(x=40, y=120)
entry_usuario = tk.Entry(root, fg="black", bg="red", font=("Calibri", 25))
entry_usuario.place(x=220, y=120)
label_contraseña = tk.Label(root, text="Contraseña:", fg="red", bg="black", font=("Calibri", 25, "underline"))
label_contraseña.place(x=40, y=180)
entry_contraseña = tk.Entry(root, show="*", fg="black", bg="red", font=("Calibri", 25))
entry_contraseña.place(x=220, y=180)
img = PhotoImage(file="IMG1.png")
label_img = tk.Label(root, image=img, bg="black")
label_img.place(x=700, y=220)

# Botones
btn_registrar = tk.Button(root, text="Registrarse", command=registrar_usuario, fg="red", bg="black", font=("Calibri", 25, "bold"))
btn_registrar.place(x=40, y=300)
btn_logueo = tk.Button(root, text="Iniciar Sesión", command=logueo, fg="red", bg="black", font=("Calibri", 25, "bold"))
btn_logueo.place(x=40, y=380)

root.mainloop()
