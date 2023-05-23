# Importar las librerias de trabajo
import sys # Interactua con el sistema operativo
import csv # Libreria para trabajar con archivos CSV
import serial # Establecer comunicación con el puerto serial
from datetime import datetime # Trabaja con las fechas y horas
from PyQt5.QtWidgets import * # Crea la interfaz gráfica del usuario
from PyQt5.QtCore import * # Módulos principales de PyQt5
from PyQt5.QtGui import * # Módulos para la interfaz gráfica
import numpy as np # Módulo para trabajar con arreglos numéricos
import pyqtgraph as pg # Biblioteca para graficar en PyQt5

class SerialPlot(QWidget): #Define la clase SerialPlot que hereda QWidget
    def __init__(self, parent=None):
        super(SerialPlot, self).__init__(parent)

        # Configuración de la ventana principal
        self.setWindowTitle("Datos del cohete")
        self.setGeometry(0, 0, 800, 600) #Posición y tamaño de la ventana 

        # Configuración del gráfico de la Altura
        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.setGeometry(50, 550, 600, 200)
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setLabel('left', 'Altitud')
        self.graphWidget.setLabel('bottom', 'Tiempo (s)')
        self.graphWidget.setTitle('<b><font size=6 color="black">Altitud</font></b>')

        # Configuración del gráfico de la aceleración
        self.graphWidget1 = pg.PlotWidget(self)
        self.graphWidget1.setGeometry(50, 50, 600, 200)
        self.graphWidget1.setBackground('w')
        self.graphWidget1.showGrid(x=True, y=True)
        self.graphWidget1.setLabel('left', 'Aceleración')
        self.graphWidget1.setLabel('bottom', 'Tiempo (s)')
        self.graphWidget1.setTitle('<b><font size=6 color="black">Acelerómetro</font></b>')

        # Configuración del gráfico del giroscopio
        self.graphWidget2 = pg.PlotWidget(self)
        self.graphWidget2.setGeometry(50, 300, 600, 200)
        self.graphWidget2.setBackground('w')
        self.graphWidget2.showGrid(x=True, y=True)
        self.graphWidget2.setLabel('left', 'Giroscopio')
        self.graphWidget2.setLabel('bottom', 'Tiempo (s)')
        self.graphWidget2.setTitle('<b><font size=6 color="black">Giroscopio</font></b>')

        # Configuración del puerto serial
        self.ser = serial.Serial('COM3', 9600)
        self.ser.flush()

        # Variables para almacenar los datos
        num_points = 1000  # Número de puntos a mostrar en la gráfica
        self.x_data = np.zeros(num_points)  # Tiempo
        self.y_data_1 = np.zeros(num_points)  # Altura
        self.y_data_2 = np.zeros(num_points)  # AcX
        self.y_data_3 = np.zeros(num_points)  # AcY
        self.y_data_4 = np.zeros(num_points)  # AcZ
        self.y_data_5 = np.zeros(num_points)  # GyX
        self.y_data_6 = np.zeros(num_points)  # GyY
        self.y_data_7 = np.zeros(num_points)  # GyZ
        


        # Crear las líneas para cada valor a graficar
        self.curve1 = self.graphWidget.plot(self.x_data, self.y_data_1, pen='red', name='Altura')
        # Crear las líneas para cada valor a graficar
        self.curve2 = self.graphWidget1.plot(self.x_data, self.y_data_2, pen='g', name='AcX')
        self.curve3 = self.graphWidget1.plot(self.x_data, self.y_data_3, pen='b', name='AcY')
        self.curve4 = self.graphWidget1.plot(self.x_data, self.y_data_4, pen='r', name='AcZ')
        # Crear las líneas para cada valor a graficar
        self.curve5 = self.graphWidget2.plot(self.x_data, self.y_data_5, pen='g', name='GyX')
        self.curve6 = self.graphWidget2.plot(self.x_data, self.y_data_6, pen='b', name='GyY')
        self.curve7 = self.graphWidget2.plot(self.x_data, self.y_data_7, pen='r', name='GyZ')
        

        # Etiqueta para la temperatura
        self.temp_label = QLabel(self)
        self.temp_label.setGeometry(700, 550, 100, 30)

        layout = QHBoxLayout()
        layout.addWidget(self.graphWidget)
        layout.addWidget(self.graphWidget1)
        layout.addWidget(self.graphWidget2)
        self.setLayout(layout)
        self.showFullScreen()

        # Configuración del temporizador para actualizar los datos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(10)

        # Variable para almacenar el tiempo inicial
        self.start_time = datetime.now()

    def update_data(self):
        # Leer los datos del puerto serie
        line = self.ser.readline().decode().strip()
        values = line.split(',')

        # Calcular el tiempo transcurrido en segundos
        current_time = datetime.now()
        elapsed_time = (current_time - self.start_time).total_seconds()

        # Obtener la self.start_timetura de Arduino
        temperature = float(values[7])

        # Mostrar la temperatura en la etiqueta
        self.temp_label.setText(f'Temperatura: {temperature} °C')

        # Añadir los nuevos valores a los datos de la altura
        self.y_data_1[:-1] = self.y_data_1[1:]
        self.y_data_1[-1] = float(values[0])
        # Añadir los nuevos valores a los datos de la aceleración
        self.y_data_2[:-1] = self.y_data_2[1:]
        self.y_data_2[-1] = float(values[1])
        self.y_data_3[:-1] = self.y_data_3[1:]
        self.y_data_3[-1] = float(values[2])
        self.y_data_4[:-1] = self.y_data_4[1:]
        self.y_data_4[-1] = float(values[3])
        # Añadir los nuevos valores a los datos del giroscopio
        self.y_data_5[:-1] = self.y_data_5[1:]
        self.y_data_5[-1] = float(values[4])
        self.y_data_6[:-1] = self.y_data_6[1:]
        self.y_data_6[-1] = float(values[5])
        self.y_data_7[:-1] = self.y_data_7[1:]
        self.y_data_7[-1] = float(values[6])
        # Crear valores para el tiempo
        self.x_data[:-1] = self.x_data[1:]
        self.x_data[-1] = elapsed_time

        
        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Altura)
        self.curve1.setData(self.x_data, self.y_data_1)
        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Aceleración)
        self.curve2.setData(self.x_data, self.y_data_2)
        self.curve3.setData(self.x_data, self.y_data_3)
        self.curve4.setData(self.x_data, self.y_data_4)
        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Giroscopio)
        self.curve5.setData(self.x_data, self.y_data_5)
        self.curve6.setData(self.x_data, self.y_data_6)
        self.curve7.setData(self.x_data, self.y_data_7)
      

        with open('datos.csv', 'a', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            if archivo_csv.tell() == 0:  # Verificar si el archivo está vacío
                escritor_csv.writerow(['Tiempo', 'Altitud','Acel X', 'Acel Y', 'Acel Z', 'Gyr X', 'Gyr Y', 'Gyr Z', 'Temperatura'])
            escritor_csv.writerow([elapsed_time, values[0], values[1], values[2], values[3], values[4], values[5], values[6], temperature])



    def resizeEvent(self, event):
        # Actualizar el tamaño del gráfico al cambiar el tamaño de la ventana
        self.graphWidget.setGeometry(50, 50, self.width() - 100, self.height() // 3 - 50)
        self.graphWidget2.setGeometry(50, self.height() // 3 + 10, self.width() - 100, self.height() // 3 - 50)
        self.graphWidget3.setGeometry(50, (self.height() // 3) * 2 + 10, self.width() - 100, self.height() // 3 - 50)

    def closeEvent(self, event):
        # Detener el temporizador y cerrar el puerto serial antes de cerrar la aplicación
        self.timer.stop()
        self.ser.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Configuración de estilos de la aplicación
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    app.setPalette(palette)
    ex = SerialPlot()
    ex.show()
    sys.exit(app.exec_())



