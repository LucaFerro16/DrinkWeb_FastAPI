import pandas as pd

# Funzione per leggere il CSV e cercare un cocktail
def read_drink_data(file_path="data/cocktails.csv"):
    try:
        # Carica il CSV con il separatore giusto (punto e virgola)
        df = pd.read_csv(file_path, encoding='ISO-8859-1', sep=';')

        # Chiediamo all'utente di inserire il nome di un drink
        drink_name = input("Inserisci il nome del drink che desideri cercare: ").strip()

        # Verifica se il nome del drink è nella colonna 'NOME'
        drink_info = df[df['NOME'].str.contains(drink_name, case=False, na=False)]

        # Se il drink esiste, visualizziamo le informazioni
        if not drink_info.empty:
            for _, row in drink_info.iterrows():
                print(f"Drink: {row['NOME']}")
                print(f"Classe: {row['CLASSE']}")
                print(f"Gradazione: {row['GRADAZIONE']}")
                print(f"Bicchiere: {row['BICCHIERE']}")

                # Ingredienti e quantità
                ingredients = [col for col in df.columns if "INGREDIENTE" in col]
                quantities = [col for col in df.columns if "QUANTITA" in col]

                for i, ingredient in enumerate(ingredients):
                    if pd.notna(row[ingredient]):
                        print(f"{row[ingredient]}: {row[quantities[i]]} ml")
        else:
            print(f"Il drink '{drink_name}' non è stato trovato.")

    except FileNotFoundError:
        print(f"Errore: Il file {file_path} non esiste.")
    except Exception as e:
        print(f"Errore: {e}")

# Chiamata alla funzione per avviare il processo
read_drink_data()
