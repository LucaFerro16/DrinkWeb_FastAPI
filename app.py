from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
from fastapi.templating import Jinja2Templates
from main import image_name_mapping

# Creazione dell'app FastAPI
app = FastAPI()

# Configurare i template e i file statici
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Percorsi ai file CSV
COCKTAILS_CSV = "data/cocktails.csv"
DEDE_COLLECTION_CSV = "data/dede_collection.csv"

# Caricamento dei dati
def load_csv(file_path):
    return pd.read_csv(file_path, delimiter=";", encoding="utf-8")

cocktails = load_csv(COCKTAILS_CSV)
dede_collection = load_csv(DEDE_COLLECTION_CSV)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/select", response_class=HTMLResponse)
async def select(request: Request, collection: str = Form(...)):
    if collection == "Dede's Collection":
        drink_list = dede_collection['NOME'].dropna().tolist()
    else:
        drink_list = cocktails['NOME'].dropna().tolist()

    drink_list = sorted(set(drink_list))

    return templates.TemplateResponse("select.html", {"request": request, "collection": collection, "drinks": drink_list})

@app.post("/drink", response_class=HTMLResponse)
async def drink(request: Request, collection: str = Form(...), drink: str = Form(...)):
    if collection == "Dede's Collection":
        drink_data = dede_collection[dede_collection['NOME'] == drink]
    else:
        drink_data = cocktails[cocktails['NOME'] == drink]

    if drink_data.empty:
        return HTMLResponse("Drink non trovato", status_code=404)

    drink_info = drink_data.to_dict(orient='records')[0]

    ingredienti = []
    for i in range(9):
        ing_col = f"INGREDIENTE{'' if i == 0 else '.' + str(i)}"
        qty_col = f"QUANTITA{'' if i == 0 else '.' + str(i)}"
        if pd.notna(drink_info.get(ing_col)) and pd.notna(drink_info.get(qty_col)):
            ingredienti.append(f"{drink_info[ing_col]} - {drink_info[qty_col]}")

    if drink in image_name_mapping:
        image_filename = f"static/images/images/{image_name_mapping[drink][0]}"
    else:
        image_filename = f"static/images/images/{drink.replace(' ', '-').lower()}.jpg"


    return templates.TemplateResponse("drink.html", {
        "request": request,
        "drink_info": drink_info,
        "ingredienti": ingredienti,
        "image_filename": image_filename,
        "drink_name": drink
    })
