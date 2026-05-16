# Proyecto de Automatización - SauceDemo

## Descripción

Este proyecto automatiza pruebas funcionales sobre el sitio web:

https://www.saucedemo.com/

Se utiliza Selenium WebDriver con Python y Pytest para validar el flujo de login, navegación por inventario y agregado de productos al carrito.

## Tecnologías utilizadas

- Python
- Pytest
- Selenium WebDriver
- WebDriver Manager
- Google Chrome

## Estructura del proyecto

proyecto_saucedemo/
│
├── utils/
│   └── helpers.py
│
├── tests/
│   └── test_saucedemo.py
│
├── conftest.py
├── requirements.txt
└── README.md

## Archivos principales

### conftest.py

Contiene la fixture `driver`, encargada de iniciar y cerrar el navegador.

### utils/helpers.py

Contiene funciones auxiliares reutilizables:

- `login()`: realiza el inicio de sesión.
- `obtener_primer_producto()`: obtiene datos del primer producto visible.

### tests/test_saucedemo.py

Contiene los casos de prueba automatizados:

1. Login exitoso.
2. Validación de la página de inventario.
3. Agregado de producto al carrito.

## Credenciales utilizadas

Usuario:

standard_user

Contraseña:

secret_sauce

## Casos de prueba cubiertos

### Login

- Navega a la página de login.
- Ingresa usuario y contraseña válidos.
- Valida redirección a `/inventory.html`.
- Valida título `Products`.
- Valida logo `Swag Labs`.

### Inventario

- Verifica que el título sea correcto.
- Valida que existan productos visibles.
- Lista nombre y precio del primer producto.
- Valida presencia de menú, filtro y carrito.

### Carrito

- Agrega el primer producto visible.
- Verifica que el contador del carrito sea `1`.
- Navega al carrito.
- Comprueba que el producto agregado esté presente.

## Instalación

Instalar dependencias:

```bash
pip install -r requirements.txt