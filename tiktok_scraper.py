import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import glob
import shutil

# Carpeta donde se guardarán las descargas (videos)
download_dir = os.path.abspath("downloads")
os.makedirs(download_dir, exist_ok=True)  # Crear carpeta si no existe

# Configuración de opciones para Chrome
options = Options()
options.add_argument("--start-maximized")  # Iniciar maximizado
options.add_argument("--disable-blink-features=AutomationControlled")  # Evitar detección de automatización
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Quitar el banner "Chrome is being controlled..."
options.add_experimental_option('useAutomationExtension', False)  # Deshabilitar extensión de automatización
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0.0.0 Safari/537.36"
)  # User-Agent personalizado para parecer un navegador normal

# Preferencias para las descargas automáticas
prefs = {
    "download.default_directory": download_dir,  # Carpeta destino
    "download.prompt_for_download": False,       # Sin preguntar donde guardar
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)

# Inicialización del driver de Chrome con las opciones configuradas
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)  # Esperas explícitas de hasta 20 segundos

def wait_for_new_file(old_files, timeout=30):
    """Espera hasta que aparezca un archivo nuevo en download_dir distinto a los old_files"""
    start = time.time()
    while time.time() - start < timeout:
        files = set(glob.glob(os.path.join(download_dir, '*')))  # Lista archivos actuales
        new_files = files - old_files  # Detectar archivos nuevos
        if new_files:
            return new_files.pop()  # Retorna el nuevo archivo detectado
        time.sleep(1)
    return None  # Retorna None si no detectó archivo nuevo en el timeout

def extraer_comentarios(driver, wait, scrolls=10, pause=2):
    """Extrae comentarios del video actual y devuelve una lista de diccionarios con Usuario, Comentario"""
    try:
        # Esperar que cargue el contenedor de comentarios
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-1i7ohvi-DivCommentItemContainer')))
    except:
        print("No se encontró la sección de comentarios.")
        return []

    # Hacer scroll para cargar más comentarios
    for _ in range(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)  # Espera a que carguen comentarios nuevos

    comentarios = driver.find_elements(By.CSS_SELECTOR, 'div.css-1i7ohvi-DivCommentItemContainer')
    data = []
    for comentario in comentarios:
        try:
            usuario = comentario.find_element(By.CSS_SELECTOR, 'a.css-xvxjh0-StyledUserLinkName span').text.strip()
        except:
            usuario = "No encontrado"
        try:
            texto = comentario.find_element(By.CSS_SELECTOR, 'p.css-xm2h10-PCommentText span').text.strip()
        except:
            texto = "No encontrado"
        data.append({'Usuario': usuario, 'Comentario': texto})
    return data

try:
    # Abre la URL con los resultados de búsqueda en TikTok
    driver.get("https://www.tiktok.com/search?q=petro&t=1748979881914")

    # Espera y clickea en el primer resultado de la búsqueda
    first_result = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[class*="DivItemContainerForSearch"]'))
    )
    first_result.click()
    todos_los_comentarios = []
    # Descargar hasta 3 videos (puedes ajustar el rango)
    for i in range(1, 4):
        # Esperar que cargue el video en la página
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
        time.sleep(3)  # Espera adicional para que el video cargue bien

        # Localizar el elemento video
        video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))

        # Obtener lista de archivos actuales antes de descargar
        old_files = set(glob.glob(os.path.join(download_dir, '*')))

        # Simular click derecho sobre el video para abrir menú contextual
        actions = ActionChains(driver)
        actions.context_click(video_element).perform()

        # Esperar y clicar en la opción "Descargar video" del menú contextual
        download_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-e2e="right-click-menu-popover_download-video"]'))
        )
        download_button.click()

        # Esperar a que aparezca el archivo nuevo descargado
        downloaded_file = wait_for_new_file(old_files)
        if downloaded_file:
            # Mover y renombrar el archivo descargado a video{i}.mp4
            new_name = os.path.join(download_dir, f"video{i}.mp4")
            shutil.move(downloaded_file, new_name)
            print(f"Video {i} descargado y renombrado a {new_name}")
        else:
            print(f"No se detectó archivo descargado para video {i}")

        comentarios = extraer_comentarios(driver, wait)
        if comentarios:
            # Agregar columna con nombre del video como video1.mp4, video2.mp4, etc.
            nombre_video = f"video{i}.mp4"
            for item in comentarios:
                item['Video'] = nombre_video

            # Acumular comentarios
            todos_los_comentarios.extend(comentarios)

            print(f"Extraídos {len(comentarios)} comentarios del {nombre_video}")
        else:
            print(f"No se encontraron comentarios para el video {i}")

        # Clic en el botón para ir al siguiente video
        next_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-e2e="arrow-right"]'))
        )
        next_button.click()

        # Esperar unos segundos para que cargue el siguiente video antes de continuar
        time.sleep(5)

finally:
    print("Proceso finalizado.")
    input("Presiona ENTER para cerrar el navegador y terminar...")  # Pausa para revisar resultados
    driver.quit()  # Cierra el navegador


if todos_los_comentarios:
    df_final = pd.DataFrame(todos_los_comentarios)
    archivo_excel = os.path.join(download_dir, "comentarios_tiktok.xlsx")
    df_final.to_excel(archivo_excel, index=False)
    print(f"Guardados todos los comentarios en {archivo_excel}")
else:
    print("No se extrajeron comentarios de ningún video.")