import pandas as pd
import os
from PIL import Image, ImageTk

# 🔹 Mappatura drink → immagine
dede_image_mapping = {
    "Lady's Negroni": ("LadysNegroni.jpg", "Lady's Negroni")
}

# 🔹 Funzione per caricare il CSV di Dede
def load_dede_csv(file_path="data/dede_collection.csv"):
    try:
        df = pd.read_csv(file_path, encoding='utf-8', sep=';')
        return df.dropna(subset=['NOME'])  # Assicuriamoci che "NOME" sia la colonna corretta
    except Exception as e:
        print(f"Errore nel caricamento del file CSV di Dede: {e}")
        return None

# 🔹 Funzione per ottenere la lista dei drink di Dede
def get_dede_drinks():
    df = load_dede_csv()
    if df is not None:
        return sorted([dede_image_mapping.get(name, (None, name))[1] for name in df['NOME'].str.strip().unique()])
    return []

# 🔹 Funzione per ottenere i dettagli del drink di Dede
def get_dede_drink_details(drink_name):
    df = load_dede_csv()
    if df is not None:
        full_drink_name = next((key for key, val in dede_image_mapping.items() if val[1] == drink_name), drink_name)
        drink_info = df[df["NOME"].str.strip().str.lower() == full_drink_name.lower()]
        return drink_info  # 🔹 Ora restituisce un DataFrame invece di una stringa!
    return pd.DataFrame()  # 🔹 Se non trova nulla, restituisce un DataFrame vuoto

# 🔹 Funzione per ottenere l'immagine del drink di Dede
def get_dede_drink_image(drink_name):
    # 🔹 Controlliamo il nome corretto nel dizionario
    full_drink_name = next((key for key, val in dede_image_mapping.items() if val[1].lower() == drink_name.lower()), None)

    if full_drink_name:
        # 🔹 Assicuriamoci che l'immagine corrisponda esattamente a "LadysNegroni.jpg"
        image_filename = "static/images/images/LadysNegroni.jpg" if full_drink_name == "Lady's Negroni" else f"static/images/images/{dede_image_mapping.get(full_drink_name, (None, None))[0]}"

        # 🔹 Debug: Stampiamo il percorso dell'immagine per verificare
        print(f"Caricamento immagine: {image_filename}")

        if os.path.exists(image_filename):
            img = Image.open(image_filename).resize((250, 250), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

    return None

