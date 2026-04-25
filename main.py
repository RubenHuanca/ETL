from etl.extract import extract
from etl.clean import clean
from etl.transform import transform
from etl.load import load

catalog, web, products = extract()
clean(catalog, web, products)
transform()
load()