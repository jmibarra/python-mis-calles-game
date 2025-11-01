# 🏗️ python-mis-calles-game

¡Bienvenido al proyecto **Mi Juego de Calles**! Este es un proyecto de desarrollo de juegos en Python que combina el poder de **PyQt6** para la interfaz de usuario y **Pygame** para la lógica de juego y el renderizado gráfico. Inspirado en los juegos de pistas de madera, permite a los usuarios construir sus propios circuitos encajables de carreteras.

---

## 1. 🕹️ Acerca del Juego e Instrucciones

El objetivo de *Mi Juego de Calles* es construir una pista de carretera encajando diferentes piezas modulares.

### Características

* **Piezas Modulares:** Utiliza piezas rectas, curvas, cruces y cruces en T.
* **Sistema de Encastre (Snap):** Las piezas se "enganchan" automáticamente cuando están lo suficientemente cerca de una conexión válida.
* **Guardar/Cargar:** Permite guardar y cargar el diseño de la pista en archivos `.json`.

### Controles de Jugabilidad

| Acción | Instrucción | Tecla / Ratón |
| :--- | :--- | :--- |
| **Añadir Pieza** | Haz clic en el botón de la pieza en el panel **Catálogo** para seleccionarla. | Botón Izquierdo |
| **Mover / Arrastrar** | Mantén pulsado para arrastrar la pieza seleccionada por el tablero. | Botón Izquierdo (Mantenido) |
| **Colocar / Encastrar** | Suelta la pieza. Si está cerca de un punto de conexión, se encajará automáticamente. | Botón Izquierdo (Soltar) |
| **Rotar Pieza** | Con una pieza seleccionada (arrastrando o recién colocada), pulsa `R` para rotarla 90 grados en sentido horario. | Tecla **R** |
| **Eliminar Pieza** | Haz clic derecho sobre una pieza colocada para eliminarla del tablero. | Botón Derecho |

---

## 2. ⚙️ Descarga e Instalación

Sigue estos pasos para poner en marcha el juego en tu entorno local.

### Requisitos

El proyecto requiere **Python 3.x** y las siguientes bibliotecas, detalladas en el archivo `requirements.txt`:

* `pygame==2.6.0`
* `PyQt6`

### Pasos de Instalación

#### Paso 1: Clonar el Repositorio

Abre tu terminal o línea de comandos y descarga el proyecto:

```bash
git clone [https://github.com/jmibarra/python-mis-calles-game.git](https://github.com/jmibarra/python-mis-calles-game.git)
cd python-mis-calles-game
```

#### Paso 2: Crear y Activar el Entorno Virtual
Es fundamental trabajar en un entorno virtual para aislar las dependencias del proyecto:


```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual (Linux/macOS)
source venv/bin/activate

# Activar el entorno virtual (Windows)
# .\venv\Scripts\activate
```

## 3. ▶️ Ejecución del Juego
Una vez que el entorno virtual esté activo y las dependencias instaladas, ejecuta el juego con el siguiente comando:

```bash
python main.py
```

El juego se iniciará mostrando la ventana principal de la aplicación.

## 4. 🤝 Contribución

¡Las contribuciones son bienvenidas! Si tienes ideas para nuevas piezas, mejoras de rendimiento o correcciones de errores, me encantaría que colaboraras.

### Proceso de Colaboración (Pull Requests)

1.  **Haz un *Fork*** del repositorio.
2.  **Crea una rama** para tu funcionalidad o corrección (`git checkout -b feature/MiNuevaMejora`).
3.  **Realiza tus cambios** y haz *commit* con un mensaje descriptivo.
4.  **Sube tu rama** a tu *fork* (`git push origin feature/MiNuevaMejora`).
5.  **Abre un *Pull Request*** (PR) detallando los cambios que has realizado y por qué son necesarios.

¡Gracias por tu apoyo en este proyecto!

## 📬 Comunícate

Si tienes dudas o necesitas orientación, no dudes en contactarnos a través de los Issues o mail:  
✉️ [jmibarra86@gmail.com](mailto:jmibarra86@gmail.com)

También puedes encontrarme en LinkedIn:  
🔗 [Juan Manuel Ibarra - LinkedIn](https://www.linkedin.com/in/juan-manuel-ibarra-activity/)

**¡Gracias por contribuir a mejorar este juego!** 🌟  
Juntos podemos construir un recurso útil y abierto para la comunidad. 🙌

Si te gusta este proyecto y querés apoyar su desarrollo:

[![Invitame un café en cafecito.app](https://cdn.cafecito.app/imgs/buttons/button_1.svg)](https://cafecito.app/jmibarradev)