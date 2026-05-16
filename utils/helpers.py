from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL_BASE = "https://www.saucedemo.com/"
USUARIO_VALIDO = "standard_user"
PASSWORD_VALIDO = "secret_sauce"


def login(driver, usuario=USUARIO_VALIDO, password=PASSWORD_VALIDO):
    """Realiza el login en SauceDemo con espera explícita."""
    wait = WebDriverWait(driver, 10)

    driver.get(URL_BASE)

    campo_usuario = wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    campo_password = driver.find_element(By.ID, "password")
    boton_login = driver.find_element(By.ID, "login-button")

    campo_usuario.send_keys(usuario)
    campo_password.send_keys(password)
    boton_login.click()

    wait.until(EC.url_contains("/inventory.html"))


def obtener_primer_producto(driver):
    """Obtiene el primer producto visible del inventario."""
    wait = WebDriverWait(driver, 10)

    producto = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item"))
    )

    nombre = producto.find_element(By.CLASS_NAME, "inventory_item_name").text
    precio = producto.find_element(By.CLASS_NAME, "inventory_item_price").text
    boton_agregar = producto.find_element(By.TAG_NAME, "button")

    return producto, nombre, precio, boton_agregar