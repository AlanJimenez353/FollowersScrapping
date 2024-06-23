import os
from dotenv import load_dotenv

def read_users_from_file(filepath):
    """Read users from a given file and return them as a set."""
    with open(filepath, 'r', encoding='utf-8') as file:
        users = {line.strip() for line in file if line.strip()}
    return users

def remove_exceptions(non_followers, exceptions):
    """Return a set of non-followers excluding the exceptions."""
    return non_followers - exceptions

if __name__ == "__main__":
    # Carga las variables de entorno
    load_dotenv()

    # Define the paths for the input files and the exception file using environment variables
    not_following_path = os.getenv('NOT_FOLLOWING_PATH')
    exceptions_path = os.getenv('EXCEPTIONS_PATH')

    # Read the list of users who don't follow you back and exceptions
    non_followers = read_users_from_file(not_following_path)
    exceptions = read_users_from_file(exceptions_path)

    # Calculate non-followers excluding the exceptions
    updated_non_followers = remove_exceptions(non_followers, exceptions)

    # Save the updated list of non-followers to the same file
    with open(not_following_path, 'w', encoding='utf-8') as file:
        for user in updated_non_followers:
            file.write(f'{user}\n')

    print(f'La lista actualizada de usuarios que no te siguen ha sido guardada, excluyendo {len(exceptions)} excepciones.')
