import os
from dotenv import load_dotenv

def read_users_from_file(filepath):
    """Read users from a given file and return them as a set."""
    with open(filepath, 'r', encoding='utf-8') as file:
        users = {line.strip() for line in file if line.strip()}
    return users

def not_following_back(following, followers):
    """Return a set of users that you follow but who don't follow you back."""
    return following - followers

if __name__ == "__main__":
    # Carga las variables de entorno
    load_dotenv()

    # Define the paths for the input and output files using environment variables
    followers_path = os.getenv('FOLLOWERS_FILE_PATH')
    following_path = os.getenv('FOLLOWING_FILE_PATH')
    output_path = os.getenv('NOT_FOLLOWING_PATH')

    # Read the lists of followers and following from files
    followers = read_users_from_file(followers_path)
    following = read_users_from_file(following_path)

    # Calculate users who don't follow you back
    non_followers = not_following_back(following, followers)

    # Print the count of non-followers
    print(f'Usuarios que sigues y no te siguen: {len(non_followers)}')

    # Save non-followers to the output file
    if non_followers:
        with open(output_path, 'w', encoding='utf-8') as f:
            for user in non_followers:
                f.write(f'{user}\n')
        print(f'Los usuarios que no te siguen han sido guardados en {output_path}')
    else:
        print("Todos los que sigues, te siguen de vuelta.")
