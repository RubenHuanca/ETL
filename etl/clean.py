import pandas as pd

def fix_date(date_str):
    try:
        parts = date_str.split(" ")[0].split("/")
        m, y, d = int(parts[0]), int(parts[1]), int(parts[2])
        y += 1900 if y > 50 else 2000
        return pd.Timestamp(year=y, month=m, day=d)
    except:
        return pd.NaT

def clean_catalog(df):
    # print(df["CATALOG"].value_counts())
    df['CATALOG'] = df['CATALOG'].str.upper().replace({
        'SPORT':'SPORTS',
        'SPORST':'SPORTS',
        'SPOTS':'SPORTS',
        'PEST':'PETS',
        'PET':'PETS',
        'PATS':'PETS',
        'PRTS':'PETS',
        'TOY':'TOYS',
        'TOSY':'TOYS',
        'TOTS':'TOYS',
        'GARDNING':'GARDENING',
        'SOFTWARES':'SOFTWARE',
        'SOFTWARS':'SOFTWARE',
        'SOFTWAR':'SOFTWARE',
        'COLLECTIBLE':'COLLECTIBLES',
        'COLECTIBLES':'COLLECTIBLES',
        'COLLECTABLES':'COLLECTIBLES'
    })
    # print(df["CATALOG"].value_counts())

    df['PCODE'] = df['PCODE'].str.upper()
    df['QTY'] = pd.to_numeric(df['QTY'], errors='coerce')
    df['DATE'] = df['DATE'].apply(fix_date)
    df['channel'] = 'CATALOG'

    print(df)
    return df

def clean_web(df):
    # print(df["CATALOG"].value_counts())
    df['CATALOG'] = df['CATALOG'].str.upper().replace({
        'SPORT':'SPORTS',
        'TOY':'TOYS',
        'TOSY':'TOYS',
        'GARDENINGS':'GARDENING',
        'GARDEN':'GARDENING',
        'PET':'PETS'
    })
    # print(df["CATALOG"].value_counts())

    df['PCODE'] = df['PCODE'].str.upper().str.replace('O','0')
    df['DATE'] = pd.to_datetime(df['DATE'], dayfirst=True, errors='coerce')
    # df['QTY'] = df['QTY'].fillna(0).astype(int)
    df['QTY'] = pd.to_numeric(df['QTY'], errors='coerce')
    df['channel'] = 'WEB'

    print(df)
    return df

def clean_products(df):
    # print(df["supplier"].value_counts())
    df['supplier'] = df['supplier'].str.upper().replace({
        "SOFTWARE AMERICA, INC.": "SOFTWARE AMERICA",
        "SOFTWARE AMERICA COMPANY, INC.": "SOFTWARE AMERICA",
        "SOFTWARE AMERICA, INCORPORATED": "SOFTWARE AMERICA",
        "TOYZ, INC.": "TOYZ",
        "CHAMPION SPORTING GOODS, INC.": "CHAMPION SPORTING GOODS",
        "CHAMPION SPORTING GOODS INC.": "CHAMPION SPORTING GOODS",
        "LUV-YUR-PET, INC.": "LUV-YUR-PET",
        "FIGURINES, INC.": "FIGURINES",
        "LIL' FOLKS, CO.": "LIL' FOLKS",
        "JJ HIGGINS": "JJ HIGGINS & COMPANY",
        "JJ HIGGINS & CO.": "JJ HIGGINS & COMPANY",
        "JJ HIGGINS & CO., INC.": "JJ HIGGINS & COMPANY",
        "HARDWARE CONCEPTS, INCORPORATED": "HARDWARE CONCEPTS, INC.",
        "LANDS ALIVE!, INC.": "LANDS ALIVE!",
        "LANDS ALIVE, INC.": "LANDS ALIVE!",
        "AQUARIUMS ALIVE, INC.": "AQUARIUMS ALIVE",
        "TRINKETS AND THINGS": "TRINKETS N' THINGS",
        "R.C.I.": "RCI",
        "SCHWARTZ & CO.": "SCHWARTZ & COMPANY",
        "YARD FUN, INC.": "YARD FUN",
        "OFFICE SOLUTIONS, INC.": "OFFICE SOLUTIONS",
        "OFFICE SOLUTIONS CO.": "OFFICE SOLUTIONS",
        "PROGRAMMER'S CHOICE, INC.": "PROGRAMMER'S CHOICE",
        "PROGRAMMER'S COICE, INC.": "PROGRAMMER'S CHOICE",
        "SNIPPER, INC.": "SNIPPER",
        "SNIPPER INCORPORATED": "SNIPPER"
    })
    # print(df["supplier"].value_counts())
    
    df['PCODE'] = df['PCODE'].str.upper()
    print(df)
    return df

def clean(catalog, web, products):
    catalog = clean_catalog(catalog)
    web = clean_web(web)
    products = clean_products(products)

    df = pd.concat([catalog, web])
    print(df)
    df.to_csv("/tmp/clean.csv", index=False)

    products.to_csv("/tmp/products_clean.csv", index=False)