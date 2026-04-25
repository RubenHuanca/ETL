import pandas as pd

def extract():
    catalog = pd.read_csv("data/Catalog_Orders.txt", sep=",", engine="python", on_bad_lines="skip")
    
    cols = ["ID","INV","DATE","CATALOG","PCODE","QTY","custnum"]
    web = pd.read_csv(
        "data/Web_orders.txt",
        sep=";",
        quotechar='"',
        names=cols,
        skiprows=1,        
        engine="python"
    )    
    # Arregla el orden incorrecto de las columnas
    web.columns = ["ID","INV","PCODE","DATE","CATALOG","QTY","custnum"]

    products = pd.read_csv("data/products.txt", sep=",")

    return catalog, web, products