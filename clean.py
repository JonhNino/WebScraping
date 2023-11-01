import pandas as pd

# Diccionario para mapear números escritos en letras a números enteros
number_mapping = {
    "One": "1",
    "Two": "2",
    "Three": "3",
    "Four": "4",
    "Five": "5"
}

# Leer el archivo CSV
file_path = "books4.csv"
df = pd.read_csv(file_path, sep=";")

# Reemplazar el carácter '£' en todo el DataFrame
df.replace("£", "", regex=True, inplace=True)

# Reemplazar números escritos en letras por números enteros en la columna 'star_rating'
df['star_rating'] = df['star_rating'].replace(number_mapping)

# Guardar el archivo modificado
df.to_csv(file_path, sep=";", index=False)

print("Modificaciones realizadas con éxito.")
