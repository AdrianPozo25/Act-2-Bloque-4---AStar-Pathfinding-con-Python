# A* Pathfinding - Sistema de Navegacion Autonomo

Prototipo de busqueda de rutas optimas desarrollado para el departamento de Inteligencia Artificial de una empresa de tecnologia automovilistica. El programa simula como un vehiculo autonomo encontraria la ruta mas eficiente entre dos puntos dentro de una ciudad.

---

## Descripcion del proyecto

El programa genera un mapa en forma de cuadricula que representa una ciudad. Cada celda del mapa puede ser una calle normal, un edificio bloqueado, una zona de trafico lento o una autovia rapida. El usuario configura el mapa a su gusto, elige donde empieza y donde termina el recorrido, y el algoritmo calcula y dibuja la ruta optima.

El algoritmo principal es A*, que combina el coste real del camino recorrido con una estimacion de lo que queda hasta el destino. Esto le permite encontrar siempre la ruta de menor coste explorando el minimo numero de celdas posible. El programa tambien incluye Dijkstra y BFS para poder comparar como se comporta cada uno ante el mismo mapa.

---

## Como ejecutarlo

No necesita instalacion ni dependencias. Solo hay que descargar el archivo A-Star.html y abrirlo en cualquier navegador moderno haciendo doble clic. Tambien se puede abrir desde Visual Studio Code usando la extension Live Server.

---

## Como usar el programa

Al abrir el archivo aparece directamente el mapa con una ciudad de ejemplo ya cargada. Desde la interfaz el usuario puede hacer lo siguiente.

Primero se elige la herramienta con la que se quiere pintar: calle libre, bloqueado, trafico lento, autovia, origen o destino. Luego se hace clic sobre las celdas del mapa para cambiarlas. Se puede mantener el clic y arrastrar para pintar varias celdas seguidas. Con el clic derecho se borra cualquier celda.

Tambien se puede escribir directamente las coordenadas del origen y el destino en los campos de texto, con el formato fila,columna. Por ejemplo: 0,0 para la esquina superior izquierda.

Una vez configurado el mapa se pulsa el boton Ejecutar para calcular la ruta con el algoritmo seleccionado. La ruta aparece marcada sobre el mapa. En la parte inferior se muestran los resultados: cuantos pasos tiene la ruta, cual es el coste total, cuantos nodos se han explorado y cuanto tiempo ha tardado el calculo.

Si se quiere comparar todos los algoritmos a la vez, se pulsa el boton Comparar todos. El programa ejecuta A-STAR, Dijkstra y BFS sobre el mismo mapa y muestra los resultados de cada uno en el log.

---

## Tipos de celda y sus costes

El mapa tiene cuatro tipos de celda. Las calles libres tienen un coste de 1 y representan vias normales de la ciudad. Las celdas bloqueadas son edificios o calles cortadas por las que no se puede pasar. Las zonas de trafico lento tienen un coste de 3, lo que hace que el algoritmo prefiera evitarlas si hay un camino mejor. Las autovias tienen un coste de 0.5, por lo que el algoritmo las utilizara siempre que pueda para reducir el coste total de la ruta.

---

## Movimiento diagonal

El programa no se limita al movimiento en cuatro direcciones como hace el formato Manhattan clasico. Admite las ocho direcciones posibles, incluyendo las cuatro diagonales. Los movimientos en diagonal tienen un coste ligeramente mayor que los ortogonales porque la distancia real es mayor. Esto permite generar rutas mas naturales y realistas, similares a las que seguiria un vehiculo real.

---

## Algoritmos incluidos

A* con heuristica Euclidea es el algoritmo principal del proyecto. Usa la distancia en linea recta como estimacion de lo que queda hasta el destino. Es la opcion mas eficiente y la que recomienda el proyecto.

A* con heuristica Manhattan usa la suma de diferencias absolutas en lugar de la distancia en linea recta. Es menos preciso con movimiento diagonal pero sirve para comparar.

Dijkstra calcula la ruta de minimo coste pero sin ninguna estimacion del destino. Explora mas nodos que A* pero siempre encuentra la solucion optima.

BFS busca el camino con menos pasos sin tener en cuenta los costes de las celdas. Es el mas simple de los tres y el menos adecuado para este tipo de mapa.

---

## Tecnologias utilizadas

El proyecto esta desarrollado completamente en HTML y CSS sin ninguna libreria externa. Todo el codigo esta en un unico archivo. La visualizacion del mapa se hace con el elemento Canvas de HTML5. La cola de prioridad que necesita A* esta implementada desde cero como una clase MinHeap en JavaScript.

---

## Estructura del archivo

Todo el proyecto esta contenido en un unico archivo HTML. El codigo esta dividido en tres partes: el HTML con la estructura de la interfaz, el CSS con los estilos visuales y el JavaScript con toda la logica del algoritmo, el renderizado del mapa y la gestion de eventos del usuario.

---

## Contexto academico

Este proyecto fue desarrollado como practica de la asignatura de Inteligencia Artificial. El objetivo era prototipar un algoritmo de busqueda de rutas optimas simulando el trabajo de un programador junior en una empresa de tecnologia automovilistica. El entregable consiste en el archivo HTML del proyecto y esta memoria publicada en GitHub.