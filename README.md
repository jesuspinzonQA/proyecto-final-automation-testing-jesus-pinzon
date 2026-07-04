# Proyecto Final Automation Testing - Jesus Pinzon

Framework de automatizacion de pruebas UI y API desarrollado como entrega final del curso de QA Automation.

El proyecto valida flujos completos sobre [SauceDemo](https://www.saucedemo.com/) con Selenium WebDriver y prueba endpoints publicos de [JSONPlaceholder](https://jsonplaceholder.typicode.com/) con Requests.

## Tecnologias utilizadas

- Python 3.11+
- Pytest
- Selenium WebDriver
- Requests
- Pytest HTML
- GitHub Actions

## Alcance de pruebas

### UI - SauceDemo

La suite UI implementa Page Object Model y cubre:

1. Login exitoso con usuarios validos parametrizados desde JSON.
2. Login negativo con credenciales invalidas.
3. Validacion de inventario, productos visibles y controles principales.
4. Ordenamiento de productos por nombre descendente.
5. Agregado de productos al carrito.
6. Checkout completo de un producto.

Los datos de prueba se leen desde `data/ui_test_data.json`.

### API - JSONPlaceholder

La suite API cubre:

1. `GET /posts/1` con validacion de codigo de estado, estructura y contenido.
2. `GET /invalid-endpoint` para validar escenario de error 404.
3. `POST /posts` con validacion del recurso creado.
4. `DELETE /posts/1` con validacion de respuesta exitosa.

## Estructura del proyecto

```text
.
├── .github/workflows/automation-tests.yml
├── data/
│   └── ui_test_data.json
├── logs/
├── pages/
│   ├── base_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   ├── inventory_page.py
│   └── login_page.py
├── Reports/
├── screenshots/
├── tests/
│   ├── test_api_jsonplaceholder.py
│   └── test_ui_saucedemo.py
├── utils/
│   └── data_loader.py
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Instalacion

Clonar el repositorio:

```bash
git clone https://github.com/jesuspinzonQA/proyecto-final-automation-testing-jesus-pinzon.git
cd proyecto-final-automation-testing-jesus-pinzon
```

Crear y activar un entorno virtual:

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
```

En macOS/Linux:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecucion de pruebas

Ejecutar toda la suite:

```bash
pytest
```

Ejecutar solo pruebas UI:

```bash
pytest -m ui
```

Ejecutar solo pruebas API:

```bash
pytest -m api
```

Ejecutar UI en modo headless:

```bash
pytest -m ui --headless
```

## Reportes y evidencias

La configuracion de `pytest.ini` genera automaticamente un reporte HTML en:

```text
Reports/reporte.html
```

El reporte muestra:

- Tests ejecutados.
- Estado de cada test.
- Duracion.
- Detalle de errores.
- Screenshots embebidos cuando falla una prueba UI.

Las capturas de pantalla tambien se guardan en:

```text
screenshots/
```

El nombre de cada captura incluye el nombre del test y fecha/hora de ejecucion.

## Logging

La ejecucion registra pasos clave en:

```text
logs/automation.log
logs/pytest.log
```

Estos logs ayudan a depurar flujos, datos usados y errores durante la ejecucion.

## CI/CD

El workflow `.github/workflows/automation-tests.yml` ejecuta las pruebas automaticamente en GitHub Actions cuando se realiza un push o pull request hacia `main` o `master`.

Al finalizar, publica como artefactos:

- `Reports/`
- `screenshots/`
- `logs/`

## Notas de mantenimiento

- Los Page Objects viven en `pages/`.
- Los tests no contienen selectores directos de Selenium.
- Los datos variables se ubican en `data/`.
- Cada prueba usa una instancia independiente del navegador para evitar dependencias entre tests.
