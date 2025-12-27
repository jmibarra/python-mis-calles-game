# main_window.py

from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QFrame, 
                             QFileDialog, QApplication)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QTimer

from mis_calles_game.ui.game_widget import GameWidget
from mis_calles_game.ui.catalog import CatalogWidget
from mis_calles_game.file_manager import save_track, load_track

class MainWindow(QMainWindow):
    """La ventana principal de nuestra aplicación."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Juego de Calles (PyQt + Pygame)")
        self.current_track_path = None
        
        self.setup_ui()
        self.setup_menu()
        self.setup_timer()

    def setup_ui(self):
        main_layout = QHBoxLayout()
        
        self.game_widget = GameWidget()
        main_layout.addWidget(self.game_widget)
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        self.catalog_widget = CatalogWidget(self.game_widget)
        main_layout.addWidget(self.catalog_widget)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def setup_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Archivo")

        actions = [
            ("Nuevo", self.nuevo_juego),
            ("Abrir", self.abrir_juego),
            ("Guardar", self.guardar_juego),
            ("Guardar Como...", self.guardar_juego_como),
            ("Cerrar", QApplication.instance().quit)
        ]

        for label, callback in actions:
            action = QAction(label, self)
            action.triggered.connect(callback)
            file_menu.addAction(action)
            if label == "Guardar Como...":
                file_menu.addSeparator()

        # Menú Opciones
        options_menu = menubar.addMenu("Opciones")
        
        self.traffic_action = QAction("Activar Tráfico", self)
        self.traffic_action.setCheckable(True)
        self.traffic_action.setChecked(True) # Activado por defecto
        self.traffic_action.triggered.connect(self.toggle_traffic)
        options_menu.addAction(self.traffic_action)

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.setInterval(33) # ~30 FPS
        self.timer.timeout.connect(self.game_widget.run_game_frame)
        self.timer.start()

    def nuevo_juego(self):
        self.game_widget.placed_pieces.clear()
        self.current_track_path = None
        self.game_widget.run_game_frame()

    def abrir_juego(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Abrir Pista", "", "Archivos de Pista (*.json)")
        if filepath:
            loaded_pieces = load_track(filepath)
            if loaded_pieces is not None:
                self.game_widget.placed_pieces = loaded_pieces
                self.current_track_path = filepath
                self.game_widget.run_game_frame()

    def guardar_juego(self):
        if self.current_track_path:
            save_track(self.game_widget.placed_pieces, self.current_track_path)
        else:
            self.guardar_juego_como()

    def guardar_juego_como(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Guardar Pista", "", "Archivos de Pista (*.json)")
        if filepath:
            if not filepath.endswith('.json'):
                filepath += '.json'
            save_track(self.game_widget.placed_pieces, filepath)
            self.current_track_path = filepath

    def toggle_traffic(self, checked):
        """Activa o desactiva el tráfico."""
        if self.game_widget:
            self.game_widget.set_traffic_enabled(checked)