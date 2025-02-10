import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import re

# Funzione per caricare il CSV
def load_csv(file_path="data/cocktails.csv"):
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1', sep=';')
        return df
    except Exception as e:
        messagebox.showerror("Errore", f"Errore nel caricamento del file CSV: {e}")
        return None

# Funzione per cercare e visualizzare i dettagli del cocktail selezionato
def show_drink_details():
    drink_name = combobox.get()

    if drink_name == "":
        messagebox.showwarning("Input vuoto", "Per favore, seleziona un drink.")
        return

    df = load_csv()
    if df is not None:
        # Sostituiamo i trattini con spazi per la ricerca
        clean_drink_name = drink_name.replace('-', ' ').strip().lower()

        # Verifica se il nome del drink è presente nel DataFrame
        # Confrontiamo i nomi in modo case-insensitive e rimuoviamo gli spazi extra
        drink_info = df[df['NOME'].str.replace('-', ' ').str.strip().str.lower() == clean_drink_name]

        if not drink_info.empty:
            info_text.delete(1.0, tk.END)
            for _, row in drink_info.iterrows():
                info_text.insert(tk.END, f"Drink: {row['NOME']}\n")
                info_text.insert(tk.END, f"Classe: {row['CLASSE']}\n")
                info_text.insert(tk.END, f"Gradazione: {row['GRADAZIONE']}\n")
                info_text.insert(tk.END, f"Bicchiere: {row['BICCHIERE']}\n")

                # Ingredienti e quantità
                ingredients = [col for col in df.columns if "INGREDIENTE" in col]
                quantities = [col for col in df.columns if "QUANTITA" in col]

                for i, ingredient in enumerate(ingredients):
                    if pd.notna(row[ingredient]):
                        info_text.insert(tk.END, f"{row[ingredient]}: {row[quantities[i]]} \n")
        else:
            messagebox.showinfo("Non trovato", f"Il drink '{drink_name}' non è stato trovato.")
    else:
        messagebox.showerror("Errore", "Impossibile caricare il file CSV.")

# Funzione per pulire i dati (rimuovere caratteri indesiderati)
def clean_data(df):
    # Rimuoviamo eventuali spazi, caratteri indesiderati nei nomi dei drink
    df['NOME'] = df['NOME'].apply(lambda x: re.sub(r"[^A-Za-z0-9\s-]", "", str(x)))  # Rimuove caratteri speciali, eccetto '-'
    df['NOME'] = df['NOME'].str.strip()  # Rimuove spazi all'inizio e alla fine
    df['NOME'] = df['NOME'].apply(lambda x: x.replace("'", "").replace('"', ""))  # Rimuove apici
    df['NOME'] = df['NOME'].apply(lambda x: re.sub(r'\[.*?\]', '', x))  # Rimuove le parentesi quadre
    df['NOME'] = df['NOME'].apply(lambda x: ' '.join(x.split()))  # Rimuove spazi multipli
    return df

# Creazione della finestra dell'app
root = tk.Tk()
root.title("Drink Finder")

# Etichetta e combobox per la selezione del cocktail
label_select = tk.Label(root, text="Seleziona un cocktail:")
label_select.pack(padx=10, pady=10)

# Carichiamo i drink dal CSV e ordiniamoli
df = load_csv()
if df is not None:
    df = clean_data(df)  # Pulisci i dati
    drink_names = df['NOME'].sort_values().unique()  # Ordina in ordine alfabetico e rimuove duplicati
else:
    drink_names = []

# Combobox per selezionare il drink
# Sostituiremo i trattini con spazi solo nella visualizzazione
cleaned_drink_names = [name.replace('-', ' ') for name in drink_names]
combobox = ttk.Combobox(root, values=cleaned_drink_names, width=30)
combobox.pack(padx=10, pady=5)

# Bottone per visualizzare i dettagli
button_show = tk.Button(root, text="Mostra Dettagli", command=show_drink_details)
button_show.pack(pady=10)

# Area di testo per visualizzare i risultati
info_text = tk.Text(root, height=15, width=50)
info_text.pack(padx=10, pady=10)

# Avvio dell'interfaccia grafica
root.mainloop()

