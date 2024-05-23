#Librerías necesarias
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import LineString
x = np.arange(-100, 150, 50)
y1 = (3000 - (20 * x))/ 50
y2 = 90 - x
y3 = 10 + (0 * x)
y4 = 0 * x
y5 = (-10000 * x) / 6000
y = np.arange(-100, 150, 50)
x1 = 0 * y
#Identificadores para las líneas
primera_linea = LineString(np.column_stack((x, y1)))
segunda_linea = LineString(np.column_stack((x, y2)))
tercera_linea = LineString(np.column_stack((x, y3)))
cuarta_linea = LineString(np.column_stack((x1, y)))
quinta_linea = LineString(np.column_stack((x, y4)))
sexta_linea = LineString(np.column_stack((x, y5)))
plt.plot(x, y1, '-', linewidth=2, color='b')
plt.plot(x, y2, '-', linewidth=2, color='g')
plt.plot(x, y3, '-', linewidth=2, color='r')
plt.plot(x1, y, '-', linewidth=2, color='y')
plt.plot(x, y4, '-', linewidth=2, color='k')
#plt.plot(x, z, ':', linewidth=1, color='k')
#Configuraciones adicionales del gráfico
plt.grid()
plt.xlabel('Asientos para fumadores')
plt.ylabel('Asientos para no fumadores')
plt.title('Método Gráfico')

plt.show()