import os
from dotenv import load_dotenv

def remove_duplicates(file_path):
    unwanted_words = {'inbox', 'explore', 'www.instagram.com', 'reels'}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Filtra las líneas que no contienen palabras no deseadas y elimina duplicados
            unique_lines = set(line for line in file if not any(word in line for word in unwanted_words))

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(unique_lines)
        print(f'Se han eliminado duplicados y filtrado palabras no deseadas en {os.path.basename(file_path)}. Quedan {len(unique_lines)} únicos.')
    except FileNotFoundError:
        print(f'El archivo no se encontró: {file_path}')

if __name__ == "__main__":
    # Carga las variables de entorno del archivo .env
    load_dotenv()

    # Obtiene las rutas de los archivos desde las variables de entorno
    followers_path = os.getenv('FOLLOWERS_FILE_PATH')
    following_path = os.getenv('FOLLOWING_FILE_PATH')

    # Llama a la función para cada archivo
    if followers_path and following_path:
        remove_duplicates(followers_path)
        remove_duplicates(following_path)
    else:
        print("Verifique que las rutas de los archivos estén definidas en el archivo .env.")
