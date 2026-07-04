import logging

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import load_json


logger = logging.getLogger(__name__)
ui_data = load_json("data/ui_test_data.json")


def login_successfully(driver, username="standard_user", password="secret_sauce"):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.load()
    login_page.login(username, password)
    inventory_page.wait_until_loaded()
    return inventory_page


@pytest.mark.ui
@pytest.mark.parametrize(
    "user_data",
    ui_data["valid_users"],
    ids=[user["case_id"] for user in ui_data["valid_users"]],
)
def test_login_exitoso_con_usuarios_validos(driver, user_data):
    logger.info("Validando login exitoso para %s", user_data["username"])

    inventory_page = login_successfully(
        driver,
        username=user_data["username"],
        password=user_data["password"],
    )

    assert "/inventory.html" in driver.current_url
    assert inventory_page.get_title() == "Products"
    assert inventory_page.get_logo() == "Swag Labs"


@pytest.mark.ui
@pytest.mark.parametrize(
    "user_data",
    ui_data["invalid_users"],
    ids=[user["case_id"] for user in ui_data["invalid_users"]],
)
def test_login_fallido_muestra_mensaje_de_error(driver, user_data):
    logger.info("Validando login negativo para %s", user_data["username"])
    login_page = LoginPage(driver)

    login_page.load()
    login_page.login(user_data["username"], user_data["password"])

    assert user_data["expected_error"] in login_page.get_error_message()
    assert "inventory.html" not in driver.current_url


@pytest.mark.ui
def test_inventario_muestra_productos_y_controles_principales(driver):
    logger.info("Validando productos y controles principales del inventario")
    inventory_page = login_successfully(driver)

    assert inventory_page.get_product_count() >= 6
    assert inventory_page.has_main_controls()


@pytest.mark.ui
def test_ordenar_productos_por_nombre_descendente(driver):
    logger.info("Validando ordenamiento de productos Z to A")
    inventory_page = login_successfully(driver)

    inventory_page.sort_by("Name (Z to A)")
    product_names = inventory_page.get_product_names()

    assert product_names == sorted(product_names, reverse=True)


@pytest.mark.ui
@pytest.mark.parametrize("product_name", ui_data["products"])
def test_agregar_producto_al_carrito(driver, product_name):
    logger.info("Validando agregado al carrito para %s", product_name)
    inventory_page = login_successfully(driver)
    cart_page = CartPage(driver)

    inventory_page.add_product_by_name(product_name)
    assert inventory_page.get_cart_badge_count() == "1"

    inventory_page.open_cart()
    cart_page.wait_until_loaded()

    assert cart_page.get_item_count() == 1
    assert product_name in cart_page.get_item_names()


@pytest.mark.ui
def test_checkout_completo_de_un_producto(driver):
    logger.info("Validando flujo completo de checkout")
    checkout_data = ui_data["checkout"]
    product_name = ui_data["products"][0]
    inventory_page = login_successfully(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    inventory_page.add_product_by_name(product_name)
    inventory_page.open_cart()
    cart_page.wait_until_loaded()
    cart_page.start_checkout()
    checkout_page.fill_customer_information(
        checkout_data["first_name"],
        checkout_data["last_name"],
        checkout_data["postal_code"],
    )
    checkout_page.finish_purchase()

    assert checkout_page.get_confirmation_message() == "Thank you for your order!"
