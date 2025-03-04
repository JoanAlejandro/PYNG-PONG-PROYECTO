import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
import firebase_admin
from firebase_admin import credentials, db
import pygame
import sys

# Inicializar Firebase
cred = credentials.Certificate("REEMPLAZAR-CLAVE-PRIVADA-AQUI.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "REEMPLAZAR-URL-AQUI"
})

# Iniciar pygame
pygame.init()
# Configuración de la ventana de Pygame
ANCHO, ALTO = 800, 600

# Función para guardar marcador en Firebase
def guardar_marcador(usuario, puntos_jugador1, puntos_jugador2):
    ref = db.reference(f"usuarios/{usuario}/marcadores")
    marcador = {"puntos_jugador1": puntos_jugador1, "puntos_jugador2": puntos_jugador2}
    ref.push(marcador)

# Función para consultar marcadores
def consultar_marcador(usuario):
    ref = db.reference(f"usuarios/{usuario}/marcadores")
    marcadores = ref.get()
    if not marcadores:
        messagebox.showinfo("Marcadores", "No hay marcadores guardados.")
        return
    ultimos_5 = list(marcadores.values())[-5:]
    texto_marcadores = "\n".join([f"Partida : {m['puntos_jugador1']} - {m['puntos_jugador2']}" for i, m in enumerate(ultimos_5)])
    messagebox.showinfo("Últimos 5 Marcadores", texto_marcadores)

# Función para seleccionar color y dificultad antes de partida
def seleccionar_color(modo, usuario, puntos_jugador1=0, puntos_jugador2=0):
    ventana_color = tk.Tk()
    ventana_color.title("Seleccionar colores")
    ventana_color.geometry("400x300")
    ventana_color.iconbitmap("icono.ico")
    ventana_color.configure(bg="black")

    tk.Label(ventana_color, text="Elige un tema:", fg="red", bg="black", font=("Calibri", 15)).pack(pady=10)

    lista=ttk.Combobox(ventana_color, values=["Rojo y Negro","Azul y Blanco","Verde y Amarillo","Morado y Celeste","Naranja y Gris"])
    lista.pack()
    tk.Label(ventana_color, text="Elige la dificultad:", fg="red", bg="black", font=("Calibri", 15)).pack()
    lista1=ttk.Combobox(ventana_color, values=["Facil","Dificil"])
    lista1.pack()
    #Función para confirmar las opciones elegidas dentro de la funcion
    def confirmar_opcion():
        opcion=lista.get()
        dificultad=lista1.get()
        if opcion=="Rojo y Negro":
            fondo=(0, 0, 0)
            pelota=(255, 255, 255)
            paleta=(255, 0, 0)
        elif opcion=="Azul y Blanco":
            fondo=(255, 255, 255)
            pelota=(0, 0, 255)
            paleta=(0, 0, 128)
        elif opcion=="Verde y Amarillo":
            fondo=(0, 128, 0)
            pelota=(255, 255, 0)
            paleta=(0, 255, 0)
        elif opcion=="Morado y Celeste":
            fondo=(128, 0, 128)
            pelota=(0, 255, 255)
            paleta=(75, 0, 130)
        elif opcion=="Naranja y Gris":
            fondo=(169, 169, 169)
            pelota=(255, 165, 0)
            paleta=(255, 140, 0)
        if dificultad == "Facil":
            velocidad=5
            velocidad_jug=4
            velocidad_cpu=2.5
        elif dificultad == "Dificil":
            velocidad=12
            velocidad_jug=8
            velocidad_cpu=6.5
        ventana_color.destroy()
        iniciar_juego(modo, fondo, pelota, paleta, velocidad, velocidad_jug, velocidad_cpu, usuario, puntos_jugador1=0, puntos_jugador2=0)
        
    btn_confirmar = tk.Button(ventana_color, text="Confirmar",command=confirmar_opcion, fg="red", bg="black", font=("Calibri", 14, "bold"))
    btn_confirmar.pack(pady=20)

# funcion para abrir el menu principal
def abrir_menu_principal(usuario):
    root.withdraw()
    menu = tk.Tk()
    menu.title("PYNG-P0NG")
    menu.geometry("1000x650")
    menu.configure(bg="black")
    menu.iconbitmap("icono.ico")
#configuracion de interfaz tkinter
    label_Titulo = tk.Label(menu, text="P Y N G   P 0 N G", bg="red", font=("Calibri", 40, "bold"))
    label_Titulo.place(x=330, y=20)
    label_pie = tk.Label(menu, text="Developed by: Joan Muñoz", fg="red", bg="black", font=("Calibri", 20, "italic"))
    label_pie.place(x=690, y=600)
    label_pie = tk.Label(menu, text=f"Jugador \"{usuario}\"", fg="red", bg="black", font=("Calibri", 20, "italic"))
    label_pie.place(x=40, y=600)
    label_j1 = tk.Label(menu, text="J1", fg="red", bg="black", font=("Calibri", 20, "italic"))
    label_j1.place(x=450, y=425)
    label_j1 = tk.Label(menu, text="\'W\'", fg="red", bg="black", font=("Calibri", 20, "italic"))
    label_j1.place(x=450, y=470)
    label_j1 = tk.Label(menu, text="\'S\'", fg="red", bg="black", font=("Calibri", 20, "italic"))
    label_j1.place(x=450, y=520)
    label_up = tk.Label(menu, text="^", fg="red", bg="black", font=("Calibri", 20, "italic"))
    label_up.place(x=500, y=462)
    label_up = tk.Label(menu, text="l", fg="red", bg="black", font=("Calibri", 15, "italic"))
    label_up.place(x=503, y=482)
    label_do = tk.Label(menu, text="v", fg="red", bg="black", font=("Calibri", 18, "italic"))
    label_do.place(x=496, y=535)
    label_do = tk.Label(menu, text="l", fg="red", bg="black", font=("Calibri", 15, "italic"))
    label_do.place(x=500, y=517)
    label_j2 = tk.Label(menu, text="J2", fg="red", bg="black", font=("Calibri", 20, "italic"))
    label_j2.place(x=530, y=425)
    label_j2 = tk.Label(menu, text="\'O\'", fg="red", bg="black", font=("Calibri", 20, "italic"))
    label_j2.place(x=530, y=470)
    label_j2 = tk.Label(menu, text="\'L\'", fg="red", bg="black", font=("Calibri", 20, "italic"))
    label_j2.place(x=530, y=520)
    label_control = tk.Label(menu, text="CONTROLES", fg="black", bg="red", font=("Calibri", 15, "italic"))
    label_control.place(x=455, y=395)
    label_linea = tk.Label(menu, text="-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------", fg="red", bg="black", font=("Calibri", 10, "italic"))
    label_linea.place(x=0, y=580)
    btn_jugar = tk.Button(menu, text="Jugar J1 vs CPU", command=lambda: seleccionar_color("cpu", usuario, puntos_jugador1=0, puntos_jugador2=0), fg="red", bg="black", font=("Calibri", 20, "bold"))
    btn_jugar.place(x=410, y=110)
    btn_jugar = tk.Button(menu, text="Jugar J1 vs J2", command=lambda: seleccionar_color("1v1", usuario, puntos_jugador1=0, puntos_jugador2=0), fg="red", bg="black", font=("Calibri", 20, "bold"))
    btn_jugar.place(x=425, y=180)
    btn_marcadr = tk.Button(menu, text="Consultar Marcador",command=lambda: consultar_marcador(usuario), fg="red", bg="black", font=("Calibri", 20, "bold"))
    btn_marcadr.place(x=390, y=250)
    btn_salir = tk.Button(menu, text="Salir", command=lambda: cerrar_menu(menu), fg="red", bg="black", font=("Calibri", 20, "bold"))
    btn_salir.place(x=476, y=320)
    
#Funcion de interfaz de juego
def iniciar_juego(modo, COLOR_FONDO, COLOR_BOLA, COLOR_PALETA, VELOCIDAD_BOLA, VELOCIDAD_PALETA, VELOCIDAD_CPU, usuario, puntos_jugador1=0, puntos_jugador2=0):
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("PYNG-P0NG")
    
    jugador1 = pygame.Rect(30, ALTO // 2 - 60, 20, 120)
    jugador2 = pygame.Rect(ANCHO - 50, ALTO // 2 - 60, 20, 120)
    bola = pygame.Rect(ANCHO // 2 - 15, ALTO // 2 - 15, 30, 30)
    bola_dx, bola_dy = VELOCIDAD_BOLA, VELOCIDAD_BOLA
    
    puntos_jugador1, puntos_jugador2 = 0, 0
    inicio_tiempo = pygame.time.get_ticks()
    reloj = pygame.time.Clock()

    while True:
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - inicio_tiempo) // 1000  # En segundos
        
        if tiempo_transcurrido >= 120 or puntos_jugador1 >= 10 or puntos_jugador2 >= 10:
            pygame.quit()
            guardar_marcador(usuario, puntos_jugador1, puntos_jugador2)
            messagebox.showinfo("Juego Terminado",f"Marcador Final: {puntos_jugador1} - {puntos_jugador2}\nPresiona ACEPTAR para volver al menú principal.")
            return

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and jugador1.top > 0:
            jugador1.y -= VELOCIDAD_PALETA
        if teclas[pygame.K_s] and jugador1.bottom < ALTO:
            jugador1.y += VELOCIDAD_PALETA
        if teclas[pygame.K_o] and jugador2.top > 0:
            jugador2.y -= VELOCIDAD_PALETA
        if teclas[pygame.K_l] and jugador2.bottom < ALTO:
            jugador2.y += VELOCIDAD_PALETA
        
        if modo == "cpu":
            if jugador2.centery < bola.centery:
                jugador2.y += VELOCIDAD_CPU
            elif jugador2.centery > bola.centery:
                jugador2.y -= VELOCIDAD_CPU
        
        bola.x += bola_dx
        bola.y += bola_dy

        if bola.top <= 0 or bola.bottom >= ALTO:
            bola_dy = -bola_dy
        
        if bola.colliderect(jugador1):
            bola_dx = abs(bola_dx)
        elif bola.colliderect(jugador2):
            bola_dx = -abs(bola_dx)
        
        if bola.left <= 0:
            puntos_jugador2 += 1
            bola.x, bola.y = ANCHO // 2 - 15, ALTO // 2 - 15
            bola_dx = VELOCIDAD_BOLA
        elif bola.right >= ANCHO:
            puntos_jugador1 += 1
            bola.x, bola.y = ANCHO // 2 - 15, ALTO // 2 - 15
            bola_dx = -VELOCIDAD_BOLA

        ventana.fill(COLOR_FONDO)
        pygame.draw.rect(ventana, COLOR_PALETA, jugador1)
        pygame.draw.rect(ventana, COLOR_PALETA, jugador2)
        pygame.draw.ellipse(ventana, COLOR_BOLA, bola)
        
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f"{puntos_jugador1} - {puntos_jugador2} | Tiempo: {120 - tiempo_transcurrido}s", True, COLOR_BOLA)
        ventana.blit(texto, (ANCHO // 2 - 100, 20))
        
        pygame.display.flip()
        reloj.tick(60)
# Funcion de cerrar el menu principal y volver al logueo
def cerrar_menu(menu):
    menu.destroy()
    
    entry_usuario.delete(0, tk.END)
    entry_contraseña.delete(0, tk.END)
    
    root.deiconify()

#funcion registrar usuario
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
        
# funcion de logueo
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

# interfaz del menu de logueo
label_linea = tk.Label(root, text="-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------", fg="red", bg="black", font=("Calibri", 10, "italic"))
label_linea.place(x=0, y=580)
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
btn_registrar = tk.Button(root, text="Registrarse", command=registrar_usuario, fg="red", bg="black", font=("Calibri", 25, "bold"))
btn_registrar.place(x=40, y=300)
btn_logueo = tk.Button(root, text="Iniciar Sesión", command=logueo, fg="red", bg="black", font=("Calibri", 25, "bold"))
btn_logueo.place(x=40, y=380)

root.mainloop()