# Resumen del Proyecto: Conversor de Video a ASCII Art


![image](https://github.com/user-attachments/assets/ec3f49c0-781e-4ea8-beb9-484224ac814b)


Este proyecto es una aplicación web desarrollada con Python y Flask, diseñada para convertir videos subidos por el usuario a arte ASCII. El proceso implica la extracción de fotogramas del video, su conversión a caracteres ASCII, y la posterior reconstrucción en un nuevo video con audio.

**Características Principales:**

1.  **Subida de Videos:**
    *   **Formulario de Subida:** Los usuarios pueden subir archivos de video a través de un formulario HTML.
    *   **Almacenamiento Temporal:** Los videos subidos se almacenan temporalmente en el servidor.

2.  **Procesamiento de Video a ASCII:**
    *   **Extracción de Fotogramas:** El video subido se procesa para extraer cada uno de sus fotogramas.
    *   **Redimensionado y Escala de Grises:** Los fotogramas se redimensionan y se convierten a escala de grises para facilitar la conversión a ASCII.
    *   **Conversión a ASCII:** Cada fotograma se convierte a una representación de texto ASCII utilizando una serie de caracteres que simulan diferentes niveles de luminosidad.
    *   **Generación de Frames ASCII como Imágenes:** Los frames ASCII se guardan en formato imagen para luego generar un video.
    *   **Procesamiento en Hilo:** La conversión de video a ASCII se ejecuta en un hilo separado para evitar bloquear la interfaz web.

3.  **Generación de Video ASCII:**
    *   **Reconstrucción de Video:** Los fotogramas ASCII se combinan para generar un nuevo video.
    *   **Adición de Audio:** El audio original del video subido se extrae y se combina con el video ASCII generado.
    *   **Formato de Salida:** El video ASCII resultante se genera en formato MP4.
  
4.  **Interfaz de Usuario (UI):**
    *   **Barra de Progreso:** Se muestra una barra de progreso en la interfaz web para indicar el avance del procesamiento.
    *   **Reproductor de Audio:** Se integra un reproductor de audio HTML para reproducir el audio original del video subido.
    *   **Visualización de ASCII:** Los fotogramas ASCII se muestran en un contenedor preformateado en la interfaz web, simulando un video ASCII.
    *   **Controles de Reproducción:** Se proporcionan controles para pausar, reanudar y reiniciar la reproducción del video ASCII.
    *   **Actualización Dinámica:** La interfaz se actualiza dinámicamente con los fotogramas ASCII conforme se van generando.
 

5.  **Manejo de Archivos:**
    *   **Creación de Directorios:** Se crean dinámicamente directorios para almacenar los archivos subidos, los frames ASCII y el video generado.
    *   **Eliminación de Archivos Previos:** Antes de procesar un nuevo video, la aplicación elimina los archivos de procesamiento previos.
    *   **Limpieza de Recursos:** Una vez finalizado el proceso, los archivos temporales se eliminan.

6. **Manejo de Errores:**
   *  **Manejo de Excepciones:** Se implementa un manejo de excepciones para capturar errores durante la conversión y el procesamiento de video.
   *  **Feedback al Usuario:** La aplicación proporciona feedback al usuario en caso de errores o fallos durante el proceso.

**Tecnologías Utilizadas:**

*   **Python:** Lenguaje de programación principal.
*   **Flask:** Framework web para construir la aplicación.
*   **OpenCV (cv2):** Para el procesamiento de video y la extracción de fotogramas.
*   **NumPy:** Para manipulación de matrices (utilizado en la conversion de frames a ascii).
*   **FFmpeg:** Para la extracción de audio del video y la generación de videos (incluyendo el ascii).
*   **threading:** Para ejecutar la conversión de video a ASCII en un hilo separado.
*  **Pillow (PIL):** Para dibujar texto ASCII en imagenes.
*   **HTML, CSS, JavaScript:** Para la interfaz de usuario.

**Propósito:**

Este proyecto tiene como objetivo principal explorar y demostrar la conversión de videos a representaciones en arte ASCII. Sirve como ejemplo de manipulación de video, procesamiento de imágenes y generación de contenido con Python y Flask.

**Para un Trabajo/Experimento:**

Este proyecto está principalmente enfocado en la demostración de la conversión de video a ASCII y puede ser usado para explorar conceptos de procesamiento de video, manipulación de imágenes y programación web. La aplicación es una prueba de concepto y demuestra el uso de varias librerías de Python para lograr una tarea específica.



Resumen:
Mayor resolución del video (new_width más grande): Más detalles, mayor calidad.
Ajuste del tamaño de la fuente en CSS: Fuente más pequeña (font-size más pequeño) para mantener detalles sin aumentar el tamaño del contenedor.




| Frame Interval (ms) | Frames per Second (FPS) |
|---------------------|-------------------------|
| 1000                | 1                       |
| 500                 | 2                       |
| 250                 | 4                       |
| 200                 | 5                       |
| 100                 | 10                      |
| 66                  | 15                      |
| 50                  | 20                      |
| 40                  | 25                      |
| 33                  | 30                      |
| 25                  | 40                      |
| 20                  | 50                      |
| 16                  | 60                      |

Para calcular el FPS a partir del `frameInterval`, puedes usar la fórmula:
\[ \text{FPS} = \frac{1000}{\text{frameInterval (ms)}} \]

Por ejemplo, si el `frameInterval` es 25 ms:
\[ \text{FPS} = \frac{1000}{25} = 40 \]

Utiliza esta tabla para ajustar el `frameInterval` a la velocidad de reproducción que prefieras.




| Relación de Aspecto | Ancho (new_width) | Alto (new_height) |
|----------------------|-------------------|-------------------|
| 4:3                  | 100               | 75                |
| 16:9                 | 100               | 56.25             |
| 3:2                  | 100               | 66.67             |
| 4:5                  | 100               | 125               |
| 1:1 (Cuadrado)       | 100               | 100               |
| 9:16                 | 100               | 177.78            |
| 2:1                  | 100               | 50                |
| 5:4                  | 100               | 80                |



https://github.com/user-attachments/assets/03407229-2113-4298-9c65-197268eaebf8



