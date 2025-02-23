import customtkinter as ctk
from configparser import ConfigParser
import subprocess  # Para ejecutar Unreal.exe
from PIL import Image  # Para cargar la imagen del banner
import sys
import os

# Función para obtener la ruta correcta de los archivos
def resource_path(relative_path):
    """ Obtiene la ruta del archivo, compatible con PyInstaller """
    if hasattr(sys, '_MEIPASS'):  # Si el programa está en un exe
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)  # Si se ejecuta como .py

# Configuración inicial de CustomTkinter (modo oscuro)
ctk.set_appearance_mode("Dark")

# Color base deseado para fondos y menús desplegables
base_color = "#121212"
menu_color = "#121212"  # Puedes cambiarlo si deseas otro color para los dropdowns

# Cargar archivo de configuración (manteniendo mayúsculas/minúsculas)
config = ConfigParser()
config.optionxform = str
config.read("UBS.ini")

comboboxes = {}

skins_por_modelo = {
    "UBS.FemaleOneBuddy": ["Female1Skins.Drace", "Female1Skins.Gina", "Female1Skins.Nikita", "Female1Skins.Raquel", "Female1Skins.Tamika", "Female1Skins.femgib1", "Female1skins.t_blue", "Female1skins.t_red", "Female1skins.t_green", "Female1skins.t_yellow"],
    "UBS.FemaleTwoBuddy": ["Female2Skins.Sonya", "Female2Skins.Katryn", "Female2Skins.Dimitra", "Female2Skins.Fem2Gib", "Female2skins.t_blue", "Female2skins.t_red", "Female2skins.t_green", "Female2skins.t_yellow"],
    "UBS.MaleOneBuddy": ["Male1Skins.Kurgan", "Male1Skins.Carter", "Male1Skins.t_blue", "Male1Skins.t_red", "Male1Skins.t_yellow", "Male1Skins.t_green"],
    "UBS.MaleTwoBuddy": ["Male2Skins.Kristoph", "Male2Skins.Ash", "Male2Skins.Ivan", "Male2Skins.Kristoph", "Male2Skins.t_blue", "Male2Skins.t_red", "Male2Skins.t_green", "Male2Skins.t_yellow"],
    "UBS.MaleThreeBuddy": ["Male3Skins.Bane", "Male3Skins.Dante", "Male3Skins.Dregor", "Male3Skins.Krige", "Male3Skins.t_blue", "Male3Skins.t_red", "Male3Skins.t_yellow", "Male3Skins.t_green"]
}

def guardar_config():
    """Guarda los cambios en UBS.ini sin espacios alrededor del '=' y respetando mayúsculas"""
    required_sections = ["UBS.UnrealBuddyItem", "ubs.UBSMut", "ubs.UnrealBuddy"]
    for section in required_sections:
        if not config.has_section(section):
            config.add_section(section)
    for key, combobox in comboboxes.items():
        section, option = key
        if config.has_section(section):
            config.set(section, option, combobox.get())
    with open("UBS.ini", "w") as configfile:
        config.write(configfile, space_around_delimiters=False)
        
def cancelar_config():
    root.quit()

def ejecutar_unreal():
    try:
        subprocess.run(["Unreal.exe"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al intentar ejecutar Unreal.exe: {e}")

def actualizar_skins(selected_value=None):
    modelo_seleccionado = buddyType.get()
    skins_posibles = skins_por_modelo.get(modelo_seleccionado, [])
    if skins_posibles:
        buddySkin.configure(values=skins_posibles)
        buddySkin.set(skins_posibles[0])
    else:
        buddySkin.configure(values=["Seleccionar..."])
        buddySkin.set("Seleccionar...")

def create_labeled_combobox(frame, label_text, values, config_section, config_key, width=250, dropdown_fg_color=menu_color, **kwargs):
    label = ctk.CTkLabel(frame, text=label_text, fg_color=base_color)
    label.pack(side="left", padx=5)
    combobox = ctk.CTkComboBox(frame, values=values, width=width, dropdown_fg_color=dropdown_fg_color, **kwargs)
    combobox.set(config.get(config_section, config_key, fallback=values[0]))
    combobox.pack(side="right", fill="x", expand=False)
    comboboxes[(config_section, config_key)] = combobox
    return combobox

def create_label_frame(master, title, text_color="#6ec291", **kwargs):
    frame = ctk.CTkFrame(master, fg_color=base_color, **kwargs)
    title_label = ctk.CTkLabel(frame, text=title, font=("Arial", 20, "bold"), text_color=text_color)  # Aquí cambiamos fg_color por text_color
    title_label.pack(padx=10, pady=(10, 0), anchor="w")
    return frame

root = ctk.CTk()
root.title("Unreal - Buddy System Coop - Configurator")

# Ruta del icono y banner
icon_path = resource_path("ico/unreal_logo_w.ico")
banner_path = resource_path("ico/unreal_Banner.png")

root.iconbitmap(icon_path)  # Establecer el ícono
root.geometry("600x950")
ctk.set_appearance_mode("dark") # Modo oscuro
ctk.set_default_color_theme("green")
root.configure(fg_color=base_color)

# CTkScrollableFrame ya se crea con el color de fondo deseado (no se accede a atributos internos)
scrollable_frame = ctk.CTkScrollableFrame(root, fg_color=base_color)
scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

try:
    banner_pil = Image.open(banner_path)
    banner_img = ctk.CTkImage(banner_pil, size=(banner_pil.width, banner_pil.height))
    banner_label = ctk.CTkLabel(scrollable_frame, image=banner_img, text="", fg_color=base_color)  # Usa base_color si lo tienes definido
except Exception as e:
    print("No se pudo cargar la imagen del banner:", e)
    banner_label = ctk.CTkLabel(scrollable_frame, text="Unreal - Buddy System Coop - Configurator", font=("Arial", 20), fg_color=base_color)  # Usa base_color

banner_label.pack(pady=33, padx=70)

button_frame = ctk.CTkFrame(scrollable_frame, fg_color=base_color)
button_frame.pack(pady=20)

# Botón Guardar
save_button = ctk.CTkButton(button_frame, text="Guardar", command=guardar_config, 
                             fg_color="#6ec291", text_color="#121212", 
                             corner_radius=10, hover_color="#4a9e74")  # Curvatura y color hover
save_button.pack(side="left", padx=10)

# Botón Cancelar
cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=cancelar_config, 
                               fg_color="#6ec291", text_color="#121212", 
                               corner_radius=10, hover_color="#4a9e74")  # Curvatura y color hover
cancel_button.pack(side="left", padx=10)

# Botón Ejecutar Unreal
run_button = ctk.CTkButton(button_frame, text="Ejecutar Unreal", command=ejecutar_unreal, 
                            fg_color="#6ec291", text_color="#121212", 
                            corner_radius=10, hover_color="#4a9e74")  # Curvatura y color hover
run_button.pack(side="left", padx=10)



bot_frame = create_label_frame(scrollable_frame, "BOT:", corner_radius=8)
bot_frame.pack(fill="x", padx=20, pady=10)

bRandomBuddies_frame = ctk.CTkFrame(bot_frame, fg_color="#121212")
bRandomBuddies_frame.pack(fill="x", pady=5)
create_labeled_combobox(
    bRandomBuddies_frame,
    "Amigo aleatorio:", ["True", "False"],
    "UBS.UnrealBuddyItem",
    "bRandomBuddies",
    fg_color="#121212",
    text_color="#6ec291",
    dropdown_fg_color="#121212",
    dropdown_text_color="white",
    dropdown_hover_color="#2b2b2b",
)

bRespawnBuddies_frame = ctk.CTkFrame(bot_frame, fg_color="#121212")
bRespawnBuddies_frame.pack(fill="x", pady=5)

create_labeled_combobox(
    bRespawnBuddies_frame,
    "Reaparecer:", ["True", "False"],
    "UBS.UnrealBuddyItem",
    "bRespawnBuddies",
    fg_color="#121212",
    text_color="#6ec291",
    dropdown_fg_color="#121212",
    dropdown_text_color="white",
    dropdown_hover_color="#2b2b2b"
)

buddyType_frame = ctk.CTkFrame(bot_frame, fg_color="#121212")
buddyType_frame.pack(fill="x", pady=5)
buddyType = create_labeled_combobox(
    buddyType_frame,
    "Modelo:", ["UBS.FemaleOneBuddy", "UBS.FemaleTwoBuddy", "UBS.MaleOneBuddy", "UBS.MaleTwoBuddy", "UBS.MaleThreeBuddy"],
    "UBS.UnrealBuddyItem",
    "BuddyType",
    fg_color="#121212",
    text_color="#6ec291",
    dropdown_fg_color="#121212",
    dropdown_text_color="white",
    dropdown_hover_color="#2b2b2b",
    command=actualizar_skins
)

buddySkin_frame = ctk.CTkFrame(bot_frame, fg_color="#121212")
buddySkin_frame.pack(fill="x", pady=5)
buddySkin = create_labeled_combobox(
    buddySkin_frame, "Skin:", ["Seleccionar..."], "UBS.UnrealBuddyItem", "BuddySkin",
    fg_color="#121212", text_color="#6ec291", dropdown_fg_color="#121212",
    dropdown_text_color="white", dropdown_hover_color="#2b2b2b"
)
actualizar_skins()

favoriteWeapon_frame = ctk.CTkFrame(bot_frame, fg_color="#121212")
favoriteWeapon_frame.pack(fill="x", pady=5)
create_labeled_combobox(
    favoriteWeapon_frame, "Arma Favorita:",
    ["UnrealShare.DispersionPistol", "UnrealShare.AutoMag", "UnrealShare.Stinger", "UnrealShare.ASMD", "UnrealShare.Eightball", "UnrealShare.FlakCannon", "UnrealShare.RazorJack", "UnrealShare.GESBioRifle", "UnrealShare.Rifle", "UnrealShare.Minigun", "Upack.CARifle"],
    "UBS.UnrealBuddyItem", "FavoriteWeapon",
    fg_color="#121212", text_color="#6ec291", dropdown_fg_color="#121212",
    dropdown_text_color="white", dropdown_hover_color="#2b2b2b"
)

ia_frame = create_label_frame(scrollable_frame, "SALUD:", corner_radius=8)
ia_frame.pack(fill="x", padx=20, pady=10)

startupHealth_frame = ctk.CTkFrame(ia_frame, fg_color="#121212")
startupHealth_frame.pack(fill="x", pady=5)
create_labeled_combobox(
    startupHealth_frame, "Salud inicial:",
    ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100", "200", "300", "400", "500", "600", "700", "800", "900"],
    "ubs.UnrealBuddy", "startupHealth",
    fg_color="#121212", text_color="#6ec291", dropdown_fg_color="#121212",
    dropdown_text_color="white", dropdown_hover_color="#2b2b2b"
)

comport_frame = create_label_frame(scrollable_frame, "COMPORTAMIENTO:", corner_radius=8)
comport_frame.pack(fill="x", padx=20, pady=10)

bKillNali_frame = ctk.CTkFrame(comport_frame, fg_color="#121212")
bKillNali_frame.pack(fill="x", pady=5)
create_labeled_combobox(
    bKillNali_frame, "Matar Nali:", ["True", "False"], "ubs.UnrealBuddy", "bKillNali",
    fg_color="#121212", text_color="#6ec291", dropdown_fg_color="#121212",
    dropdown_text_color="white", dropdown_hover_color="#2b2b2b"
)

bKillBots_frame = ctk.CTkFrame(comport_frame, fg_color="#121212")
bKillBots_frame.pack(fill="x", pady=5)
create_labeled_combobox(
    bKillBots_frame, "Matar Bots:", ["True", "False"], "ubs.UnrealBuddy", "bKillBots",
    fg_color="#121212", text_color="#6ec291", dropdown_fg_color="#121212",
    dropdown_text_color="white", dropdown_hover_color="#2b2b2b"
)

items_frame = create_label_frame(scrollable_frame, "INVENTARIO PREDETERMINADO:", corner_radius=8)
items_frame.pack(fill="x", padx=20, pady=10)

bReplaceHUD_frame = ctk.CTkFrame(items_frame, fg_color="#121212")
bReplaceHUD_frame.pack(fill="x", pady=5)
create_labeled_combobox(
    bReplaceHUD_frame, "HUD de amigo:", ["True", "False"], "ubs.UBSMut", "bReplaceHUD",
    fg_color="#121212", text_color="#6ec291", dropdown_fg_color="#121212",
    dropdown_text_color="white", dropdown_hover_color="#2b2b2b"
)

for i in range(16):
    item_frame = ctk.CTkFrame(items_frame, fg_color="#121212")
    item_frame.pack(fill="x", pady=2)
    create_labeled_combobox(
        item_frame, f"Item o Arma[{i}]",  # ← Cambié ":" por ","
        ["", "UBS.BuddyArmor", "UnrealShare.DispersionPistol", "UnrealShare.AutoMag", "UnrealShare.Stinger", "UnrealShare.ASMD", "UnrealShare.Eightball", "UnrealShare.FlakCannon", "UnrealShare.RazorJack", "UnrealShare.GESBioRifle", "UnrealShare.Rifle", "UnrealShare.Minigun", "UnrealShare.FlashLight", "UnrealShare.Armor", "UnrealShare.weaponpowerup", "Upack.CARifle"],
        "ubs.UBSMut", f"GiveBuddyItem[{i}]",
        fg_color="#121212", text_color="#6ec291", dropdown_fg_color="#121212",
        dropdown_text_color="white", dropdown_hover_color="#2b2b2b"
    )

root.mainloop()
