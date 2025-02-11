import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import dede_collection  # Importiamo il file separato per "Dede's Collection"


# 🔹 Percorso del file CSV della lista IBA
CSV_FILE_PATH = "data/cocktails.csv"

# 🔹 Dizionario per mappare nome drink → immagine
image_name_mapping = {
    "CL": ("CL.jpg","Cuba Libre"),
    "FC": ("FC.jpg","French Connection"),
    "HN": ("HN.jpg","Horses Neck"),
    "V": ("V.jpg","Vesper"),
    "RSP": ("RSP.jpg","Russian Spring Punch"),
    "VE": ("VE.jpg","VE.N.TO"),
    "Black-Russian": ("BlackRussian.jpg", "Black Russian"),
    "Bloody-Mary": ("BloodyMary.jpg", "Bloody Mary"),
    "Champagne-Cocktail": ("ChampagneCocktail.jpg", "Champagne Cocktail"),
    "Corpse-Reviver-2": ("CorpseReviver2.jpg", "Corpse Reviver 2"),
    "French-75": ("French75.jpg", "French 75"),
    "Golden-Dream": ("GoldenDream.jpg", "Golden Dream"),
    "Hemingway-Special": ("HemingwaySpecial.jpg", "Hemingway Special"),
    "Irish-Coffee": ("IrishCoffee.jpg", "Irish Coffee"),
    "Long-Island-Ice-Tea": ("LongIslandIceTea.jpg", "Long Island Ice Tea"),
    "Mai-Tai": ("MaiTai.jpg", "Mai Tai"),
    "Mint-Julep": ("MintJulep.jpg", "Mint Julep"),
    "Moscow-Mule": ("MoscowMule.jpg", "Moscow Mule"),
    "Pina-Colada": ("PinaColada.jpg", "Pina Colada"),
    "Pisco-Sour": ("PiscoSour.jpg", "Pisco Sour"),
    "Sea-Breeze": ("SeaBreeze.jpg", "Sea Breeze"),
    "Sex-on-the-Beach": ("SexontheBeach.jpg", "Sex on the Beach"),
    "Singapore-Sling": ("SingaporeSling.jpg", "Singapore Sling"),
    "Tequila-Sunrise": ("TequilaSunrise.jpg", "Tequila Sunrise"),
    "Bees-Knees": ("BeesKnees.jpg", "Bees Knees"),
    "Dark-n-stormy": ("Darknstormy.jpg", "Dark 'n' Stormy"),
    "Espresso-Martini": ("EspressoMartini.jpg", "Espresso Martini"),
    "French-Martini": ("FrenchMartini.jpg", "French Martini"),
    "Lemon-drop-Martini": ("LemondropMartini.jpg", "Lemon Drop Martini"),
    "Naked-and-Famous": ("NakedandFamous.jpg", "Naked and Famous"),
    "New-York-Sour": ("NewYorkSour.jpg", "New York Sour"),
    "Old-Cuban": ("OldCuban.jpg", "Old Cuban"),
    "Paper-Plane": ("PaperPlane.jpg", "Paper Plane"),
    "Spicy-Fifty": ("SpicyFifty.jpg", "Spicy Fifty"),
    "Suffering-Bastard": ("SufferingBastard.jpeg", "Suffering Bastard"),
    "Tommys-Margarita": ("TommysMargarita.jpg", "Tommys Margarita"),
    "Trinidad-Sour": ("TrinidadSour.jpg", "Trinidad Sour"),
    "Yellow-Bird": ("YellowBird.jpg", "Yellow Bird"),
    "Angel-Face": ("AngelFace.jpg","Angel Face"),
    "Clover-Club": ("CloverClub.jpg", "Clover Club"),
    "Dry-Martini": ("DryMartini.jpg","Dry Martini"),
    "Gin-Fizz": ("GinFizz.jpg","Gin Fizz"),
    "Hanky-Panky": ("HankyPanky.jpg", "Hanky Panky"),
    "John-Collins": ("JohnCollins.jpg","John Collins"),
    "Last-Word": ("Lastword.jpg","Last Word"),
    "Mary-Pickford": ("MaryPickford.jpg","Mary Pickford"),
    "Monkey-Gland": ("MonkeyGland.jpg","Monkey Gland"),
    "Old-Fashioned": ("OldFashioned.jpg","Old Fashioned"),
    "Porto-Flip": ("PortoFlip.jpg","Porto Flip"),
    "Ramos-Fizz": ("RamosFizz.jpg","Ramos Fizz"),
    "Rusty-Nail": ("RustyNail.jpg","Rusty Nail"),
    "Vieux-Carr": ("VieuxCarr.jpg","Vieux Carr"),
    "Whiskey-Sour": ("WhiskeySour.jpg","Whiskey Sour"),
    "White-Lady": ("WhiteLady.jpg","White Lady"),
    "Between-the-Sheets": ("BetweentheSheets.jpg","Between-the-Sheets")

}

# 🔹 Funzione per caricare il CSV
def load_csv(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8', sep=';')
        return df.dropna(subset=['NOME'])  # Assicuriamoci che "NOME" sia la colonna corretta
    except Exception as e:
        messagebox.showerror("Errore", f"Errore nel caricamento del file CSV: {e}")
        return None

# 🔹 Creazione della finestra principale
#root = tk.Tk()
# Nasconde la finestra principale finché non si inserisce la password

# 🔹 Caricare l'immagine di sfondo
sfondo_image = Image.open("static/images/images/sfondo.jpg")
sfondo_image = sfondo_image.resize((600, 750), Image.Resampling.LANCZOS)
sfondo_photo = ImageTk.PhotoImage(sfondo_image)

# 🔹 Creare una label per lo sfondo
sfondo_label = tk.Label(root, image=sfondo_photo)
sfondo_label.place(relwidth=1, relheight=1)  # Occupa tutta la finestra
root.title("Drink Collection")
root.geometry("600x750")

# 🔹 Variabili di stato
current_image = None
selected_category = None


# 🔹 Funzione per mostrare la schermata iniziale
def show_main_screen():
    category_combobox.pack(side=tk.TOP, pady=10)
    category_button.pack(side=tk.TOP, pady=5)

    # Nascondiamo gli elementi della selezione secondaria
    back_button.pack_forget()
    combobox.pack_forget()
    button_show.pack_forget()
    info_text.pack_forget()
    img_label.pack_forget()

# 🔹 Funzione per mostrare la selezione della categoria
def show_category_selection():
    global selected_category
    selected_category = category_combobox.get()

    # Nasconde la prima selezione
    category_combobox.pack_forget()
    # 🔹 Rimuoviamo lo sfondo e cambiamo il colore in celeste
    sfondo_label.place_forget()  # Nasconde l'immagine di sfondo
    root.configure(bg="#ADD8E6")  # Cambia lo sfondo in celeste

    category_button.pack_forget()

    # Mostra la seconda selezione
    back_button.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
    combobox.pack(side=tk.TOP, pady=10)
    button_show.pack(side=tk.TOP, pady=5)
    info_text.pack_forget()
    img_label.pack_forget()

    # Carica la lista dei drink per la categoria selezionata
    if selected_category == "Lista IBA":
        load_iba_list()
    elif selected_category == "Dede's Collection":
        load_dede_list()

# 🔹 Funzione per tornare alla schermata iniziale
def reset_to_category_selection():
    show_main_screen()

# 🔹 Carica i drink della Lista IBA con i nomi leggibili
def load_iba_list():
    df = load_csv(CSV_FILE_PATH)
    if df is not None:
        drink_names = []
        for name in df["NOME"].str.strip().unique():
            if name in image_name_mapping:
                drink_names.append(image_name_mapping[name][1])  # Nome leggibile
            else:
                drink_names.append(name.replace("-", " "))  # Rimuove trattini

        combobox.config(values=sorted(drink_names))

# 🔹 Carica i drink di Dede's Collection
def load_dede_list():
    drink_names = dede_collection.get_dede_drinks()
    combobox.config(values=drink_names)

# 🔹 Mostra i dettagli del drink selezionato
def show_drink_details():
    full_drink_name = ""
    global current_image
    drink_name = combobox.get()
    if not drink_name:
        messagebox.showwarning("Input vuoto", "Per favore, seleziona un drink.")
        return

    # 🔹 Cancella immagine precedente e resetta eventuale testo
    img_label.config(image=None, text="")
    current_image = None

    # 🔹 Determina la categoria e carica i dati dal CSV giusto
    if selected_category == "Lista IBA":
        df = load_csv(CSV_FILE_PATH)
        full_drink_name = next((key for key, val in image_name_mapping.items() if val[1] == drink_name), drink_name)
        drink_info = df[df["NOME"].str.strip().str.lower() == full_drink_name.lower()]
    elif selected_category == "Dede's Collection":
        drink_info = dede_collection.get_dede_drink_details(drink_name)
    else:
        return

    # 🔹 Mostra i dettagli se il drink esiste nel CSV
    if not drink_info.empty:
        info_text.delete(1.0, tk.END)
        row = drink_info.iloc[0]
        info_text.insert(tk.END, f"Drink: {row['NOME']}\n")
        info_text.insert(tk.END, f"Classe: {row.get('CLASSE', 'Dato non disponibile')}\n")
        info_text.insert(tk.END, f"Gradazione: {row.get('GRADAZIONE', 'Dato non disponibile')}\n")
        info_text.insert(tk.END, f"Bicchiere: {row.get('BICCHIERE', 'Dato non disponibile')}\n\n")

        info_text.insert(tk.END, "Ingredienti:\n")
        for i in range(0, 9):
            ingrediente_col = f"INGREDIENTE{'.' + str(i) if i > 0 else ''}"
            quantita_col = f"QUANTITA{'.' + str(i) if i > 0 else ''}"

            ingrediente = str(row.get(ingrediente_col, "")).strip()
            quantità = str(row.get(quantita_col, "")).strip()

            if ingrediente.lower() == "nan":
                ingrediente = ""
            if quantità.lower() == "nan":
                quantità = ""

            if ingrediente:
                info_text.insert(tk.END, f"  - {ingrediente}: {quantità}\n")

    # 🔹 Cerca immagine
    image_filename = f"static/images/images/{drink_name.replace(' ', '')}.jpg"
    if not os.path.exists(image_filename) and full_drink_name in image_name_mapping:
        image_filename = f"static/images/images/{image_name_mapping[full_drink_name][0]}"

    print(f"Caricamento immagine: {image_filename}")

    if os.path.exists(image_filename):
        img = Image.open(image_filename).resize((250, 250), Image.Resampling.LANCZOS)
        current_image = ImageTk.PhotoImage(img)
        img_label.config(image=current_image)
        img_label.image = current_image
    else:
        img_label.config(image=None, text="Immagine non trovata")

    info_text.pack(pady=10)
    img_label.pack(pady=10)

# 🔹 UI
category_combobox = ttk.Combobox(root, values=["Dede's Collection", "Lista IBA", "Altri"], width=30, font=('Arial', 12))
category_button = tk.Button(root, text="Conferma", command=show_category_selection, font=('Arial', 12))

back_button = tk.Button(root, text="← Indietro", command=reset_to_category_selection, font=('Arial', 12))
combobox = ttk.Combobox(root, width=30, font=('Arial', 14))
button_show = tk.Button(root, text="Mostra Dettagli", command=show_drink_details, font=('Arial', 14))

info_text = tk.Text(root, height=15, width=50, font=('Arial', 14))
img_label = tk.Label(root)

# Mostriamo la schermata iniziale
show_main_screen()

root.mainloop()
