import os
from dotenv import load_dotenv

def count_users(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            users = file.readlines()
            print(f'Hay {len(users)} usuarios en el archivo {os.path.basename(file_path)}.')
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
        count_users(followers_path)
        count_users(following_path)
    else:
        print("Verifique que las rutas de los archivos estén definidas en el archivo .env.")
