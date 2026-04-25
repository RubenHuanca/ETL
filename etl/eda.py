import pandas as pd
import matplotlib.pyplot as plt
from extract import extract

def eda_catalog(df):
    print(df.describe())
    # print(df["CATALOG"].value_counts())
    df["CATALOG"].value_counts().plot(kind="bar")
    plt.title("Catalog Distribution")
    plt.show()
    # return df

def eda_web(df):
    print(df.describe())
    # print(df["CATALOG"].value_counts())
    df["CATALOG"].value_counts().plot(kind="bar")
    plt.title("Web Distribution")
    plt.show()
    # return df

def eda_products(df):
    print(df.describe())
    # print(df["supplier"].value_counts())
    df["supplier"].value_counts().plot(kind="bar")
    plt.title("Products Distribution")
    plt.show()
    # return df

def eda(catalog, web, products):
    catalog = eda_catalog(catalog)
    web = eda_web(web)
    products = eda_products(products)

# EDA
catalog, web, products = extract()
eda(catalog, web, products)