import os
import time
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Carga las variables de entorno
load_dotenv()

# Configura tu nombre de usuario y contraseña de Instagram desde el archivo .env
USERNAME = os.getenv('INSTAGRAM_USERNAME')
PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Ruta del archivo donde se guardarán los nombres de usuario
FOLLOWERS_FILE_PATH = os.getenv('FOLLOWERS_FILE_PATH')

# Configura las opciones de Chrome para el modo móvil
mobile_emulation = {
    "deviceMetrics": { "width": 400, "height": 814, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36"
}
options = webdriver.ChromeOptions()
options.add_experimental_option("mobileEmulation", mobile_emulation)

# Inicializa el navegador
service = webdriver.chrome.service.Service()
driver = webdriver.Chrome(service=service, options=options)

# Navega a la página de inicio de sesión de Instagram
driver.get('https://www.instagram.com/accounts/login/')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))

# Ingresa tu nombre de usuario y contraseña
username_input = driver.find_element(By.NAME, 'username')
password_input = driver.find_element(By.NAME, 'password')
username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)

# Presiona Enter para iniciar sesión
password_input.send_keys(Keys.RETURN)

# Espera a que se carguen los elementos necesarios post-inicio de sesión
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Ahora no')]")))
not_now_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Ahora no')]")
not_now_button.click()

# Maneja el modal de agregar a pantalla de inicio
try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Cancelar')]")))
    cancel_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Cancelar')]")
    cancel_button.click()
    print("Modal de agregar a pantalla de inicio cancelado.")
except Exception as e:
    print(f"No se encontró o no se pudo hacer clic en el botón 'Cancelar': {e}")

# Espera y luego haz clic en el div que lleva al perfil
try:
    profile_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/{USERNAME}/']")))
    profile_link.click()
    print("Navegación al perfil de usuario completada.")
except Exception as e:
    print(f"No se pudo navegar al perfil: {e}")

# Espera y luego haz clic en el enlace de seguidos
following_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/{USERNAME}/followers/') and @role='link']")))
following_link.click()
print("Navegación a la página de seguidos completada.")



#-------------------------------------------------------------------------------------------------------------
# Esperar 80 segundos para que hagas el scroll manualmente
time.sleep(80)

# Recolecta los nombres de usuario después de scrollear
followers_links = driver.find_elements(By.XPATH, ".//a[contains(@href, '/') and @role='link']")
followers_usernames = [link.get_attribute('href').split('/')[-2] for link in followers_links if '/p/' not in link.get_attribute('href')]
print(f"Se han encontrado {len(followers_usernames)} nombres de usuario.")

# Guarda los nombres de usuario en un archivo .txt
if followers_usernames:
    with open(FOLLOWERS_FILE_PATH, 'w', encoding='utf-8') as f:
        for username in followers_usernames:
            f.write(f'{username}\n')
    print(f'Se han guardado {len(followers_usernames)} seguidores en {FOLLOWERS_FILE_PATH}')


# Cierra el navegador
driver.quit()
