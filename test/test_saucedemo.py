from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import login, obtener_primer_producto


def test_login_exitoso(driver):
    """Valida que el usuario pueda iniciar sesión correctamente."""
    login(driver)

    assert "/inventory.html" in driver.current_url

    titulo = driver.find_element(By.CLASS_NAME, "title").text
    assert titulo == "Products"

    logo = driver.find_element(By.CLASS_NAME, "app_logo").text
    assert logo == "Swag Labs"


def test_pagina_inventario(driver):
    """Valida título, productos visibles y elementos principales."""
    login(driver)

    titulo = driver.find_element(By.CLASS_NAME, "title").text
    assert titulo == "Products"

    productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(productos) > 0

    primer_producto, nombre, precio, _ = obtener_primer_producto(driver)

    print(f"Primer producto: {nombre}")
    print(f"Precio: {precio}")

    assert nombre != ""
    assert precio != ""

    menu = driver.find_element(By.ID, "react-burger-menu-btn")
    filtro = driver.find_element(By.CLASS_NAME, "product_sort_container")
    carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_link")

    assert menu.is_displayed()
    assert filtro.is_displayed()
    assert carrito.is_displayed()


def test_agregar_producto_al_carrito(driver):
    """Valida que se pueda agregar el primer producto al carrito."""
    wait = WebDriverWait(driver, 10)

    login(driver)

    _, nombre_producto, _, boton_agregar = obtener_primer_producto(driver)
    boton_agregar.click()

    contador_carrito = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )

    assert contador_carrito.text == "1"

    carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    carrito.click()

    wait.until(EC.url_contains("/cart.html"))

    producto_en_carrito = driver.find_element(By.CLASS_NAME, "inventory_item_name").text

    assert producto_en_carrito == nombre_producto