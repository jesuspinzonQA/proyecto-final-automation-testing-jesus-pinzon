import logging
import base64
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


ROOT_DIR = Path(__file__).resolve().parent
SCREENSHOTS_DIR = ROOT_DIR / "screenshots"
LOGS_DIR = ROOT_DIR / "logs"

SCREENSHOTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOGS_DIR / "automation.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Ejecuta las pruebas UI sin abrir la ventana del navegador.",
    )


@pytest.fixture
def driver(request):
    """Inicializa y cierra Chrome para cada prueba UI."""
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,768")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    logging.info("Navegador iniciado para %s", request.node.name)

    yield browser

    logging.info("Navegador cerrado para %s", request.node.name)
    browser.quit()


def _safe_test_name(test_name):
    return "".join(char if char.isalnum() or char in ("-", "_") else "_" for char in test_name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    browser = item.funcargs.get("driver")
    if browser is None:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"{_safe_test_name(item.name)}_{timestamp}.png"
    screenshot_path = SCREENSHOTS_DIR / screenshot_name
    browser.save_screenshot(str(screenshot_path))
    logging.error("Prueba fallida: %s. Screenshot: %s", item.name, screenshot_path)

    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html:
        extras = getattr(report, "extras", [])
        encoded_image = base64.b64encode(screenshot_path.read_bytes()).decode("utf-8")
        html = (
            '<div>'
            f'<img src="data:image/png;base64,{encoded_image}" alt="screenshot" '
            'style="width:320px;border:1px solid #ddd;" />'
            "</div>"
        )
        extras.append(pytest_html.extras.html(html))
        report.extras = extras
