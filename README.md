# Flask

A Flask starter template as per the docs: https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application


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
