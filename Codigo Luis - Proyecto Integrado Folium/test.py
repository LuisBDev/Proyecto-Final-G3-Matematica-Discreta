import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium

from Localizacion import *

# create the application and the main window
class display_pyqt():
    def main(area_especifica):
        app = QApplication(sys.argv)
        window = QWidget()
        window.setWindowTitle('Trayecto mínimo - Implementación Dijkstra Algorithm - Grupo 3')

        # create a QWebEngineView widget and load the HTML file
        view = QWebEngineView()

        # read the HTML file and set it as the content of the QWebEngineView
        with open(f'{area_especifica}.html', 'r') as f:
            html = f.read()

        view.setHtml(html)

        # set the size of the QWebEngineView widget
        view.setFixedSize(1340, 760)

        # create a vertical layout and add the QWebEngineView widget
        layout = QVBoxLayout(window)
        layout.addWidget(view)
        # center the QWebEngineView widget in the layout
        layout.setAlignment(view, Qt.AlignCenter)


        # show the main window
        window.show()

        # start the application event loop
        try:
            sys.exit(app.exec_())
        except SystemExit:
            print('Cerrando Folium...')

