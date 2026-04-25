import pandas as pd

def transform():
    df = pd.read_csv("/tmp/clean.csv")
    products = pd.read_csv("/tmp/products_clean.csv")

    df = df.merge(products, on="PCODE", how="left")

    # Metrics
    df['revenue'] = df['QTY'] * df['PRICE']
    df['profit'] = df['QTY'] * (df['PRICE'] - df['COST'])
    print(df)

    df.to_csv("/tmp/final.csv", index=False)