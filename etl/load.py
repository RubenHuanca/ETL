import pandas as pd
from sqlalchemy import create_engine, text
from config import DB_URI


def load():
    engine = create_engine(DB_URI)    
    df = pd.read_csv("/tmp/final.csv")
    # IMPORTANT:
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce').dt.date

    # ---------------- CLEAN DB ----------------
    with engine.connect() as conn:
        conn.execute(text("""
            TRUNCATE TABLE fact_sales, dim_product, dim_date RESTART IDENTITY CASCADE;
        """))
        conn.commit()

    # ---------------- DIM PRODUCT ----------------
    dim_product = df[['PCODE','DESCRIP','TYPE','supplier','PRICE','COST']].drop_duplicates()
    dim_product.columns = dim_product.columns.str.lower()

    dim_product.to_sql("dim_product", engine, if_exists="append", index=False)

    # ---------------- DIM DATE ----------------
    dim_date = df[['DATE']].drop_duplicates()
    dim_date['year'] = pd.to_datetime(dim_date['DATE']).dt.year
    dim_date['month'] = pd.to_datetime(dim_date['DATE']).dt.month
    dim_date['day'] = pd.to_datetime(dim_date['DATE']).dt.day
    dim_date.columns = dim_date.columns.str.lower()

    dim_date.to_sql("dim_date", engine, if_exists="append", index=False)

    # ---------------- READ IDS FROM DB ----------------
    dim_product_db = pd.read_sql("SELECT product_id, pcode FROM dim_product", engine)
    dim_date_db = pd.read_sql("SELECT date_id, date FROM dim_date", engine)

    # Ensure same type before merge
    dim_date_db['date'] = pd.to_datetime(dim_date_db['date']).dt.date

    # ---------------- MAP KEYS ----------------
    df = df.merge(dim_product_db, left_on="PCODE", right_on="pcode", how="left")
    df = df.merge(dim_date_db, left_on="DATE", right_on="date", how="left")

    # ---------------- VALIDATION ----------------
    if df['product_id'].isna().any():
        raise Exception("Some product_id are NULL (mapping failed)")

    if df['date_id'].isna().any():
        raise Exception("Some date_id are NULL (mapping failed)")

    # ---------------- FACT TABLE ----------------
    fact_sales = df[['product_id','date_id','custnum','channel','QTY','revenue','profit']]
    fact_sales.columns = fact_sales.columns.str.lower()

    fact_sales.to_sql("fact_sales", engine, if_exists="append", index=False)

    print("LOADED")