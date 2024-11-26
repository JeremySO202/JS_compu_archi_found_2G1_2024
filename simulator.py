import os
import pygame
import subprocess
import sys
from multiprocessing import Process

pygame.init()

import os
import pygame
import subprocess
import sys

pygame.init()

import os
import pygame
import subprocess
import sys

pygame.init()

class MultiProcessorInterface:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Selector de Procesadores")
        self.font = pygame.font.Font(None, 36)

        # Configuración de colores
        self.LIGHT_GRAY = (200, 200, 200)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.HIGHLIGHT_COLOR = (0, 100, 255)  # Color para resaltar la caja activa

        # Procesadores
        self.processors = [
            {"name": "No Hazard", "rect": pygame.Rect(50, 100, 400, 80), "file": "main.py", "interval": 1, "selected": False},
            {"name": "Branch Prediction 2", "rect": pygame.Rect(50, 200, 400, 80), "file": "mainBP.py", "interval": 1, "selected": False},
            {"name": "Forwarding 3", "rect": pygame.Rect(50, 300, 400, 80), "file": "mainF.py", "interval": 1, "selected": False},
            {"name": "Full Hazards 4", "rect": pygame.Rect(50, 400, 400, 80), "file": "mainFH.py", "interval": 1, "selected": False},
        ]

        # Botón de ejecutar
        self.run_button = pygame.Rect(160, 500, 200, 50)

        # Campo para ajustar el intervalo
        self.interval_boxes = [
            {"rect": pygame.Rect(500, 115, 100, 50), "interval": "1"},
            {"rect": pygame.Rect(500, 215, 100, 50), "interval": "1"},
            {"rect": pygame.Rect(500, 315, 100, 50), "interval": "1"},
            {"rect": pygame.Rect(500, 415, 100, 50), "interval": "1"},
        ]
        self.active_box = None  # Índice de la caja activa

        self.running = True
        self.selected_processors = []

    def draw(self):
        """Dibuja la interfaz gráfica."""
        self.screen.fill(self.LIGHT_GRAY)

        # Dibujar los procesadores
        for idx, processor in enumerate(self.processors):
            color = self.GREEN if processor["selected"] else self.RED
            pygame.draw.rect(self.screen, color, processor["rect"])
            text = self.font.render(f"{processor['name']} (Intervalo: {processor['interval']})", True, self.WHITE)
            text_rect = text.get_rect(center=processor["rect"].center)
            self.screen.blit(text, text_rect)

        # Dibujar cajas de intervalo
        for idx, box in enumerate(self.interval_boxes):
            border_color = self.HIGHLIGHT_COLOR if idx == self.active_box else self.BLACK
            pygame.draw.rect(self.screen, self.WHITE, box["rect"])
            pygame.draw.rect(self.screen, border_color, box["rect"], 2)
            interval_text = self.font.render(box["interval"], True, self.BLACK)
            interval_text_rect = interval_text.get_rect(center=box["rect"].center)
            self.screen.blit(interval_text, interval_text_rect)

        # Dibujar el botón de ejecutar
        pygame.draw.rect(self.screen, self.BLACK, self.run_button)
        run_text = self.font.render("Ejecutar", True, self.WHITE)
        run_text_rect = run_text.get_rect(center=self.run_button.center)
        self.screen.blit(run_text, run_text_rect)

    def handle_click(self, pos):
        """Maneja los clics en la interfaz."""
        # Verificar si se seleccionó un procesador
        for idx, processor in enumerate(self.processors):
            if processor["rect"].collidepoint(pos):
                processor["selected"] = not processor["selected"]
                if processor["selected"]:
                    self.selected_processors.append(processor)
                else:
                    self.selected_processors.remove(processor)
                if len(self.selected_processors) > 2:
                    deselected = self.selected_processors.pop(0)
                    deselected["selected"] = False

        # Verificar si se seleccionó una caja de intervalo
        for idx, box in enumerate(self.interval_boxes):
            if box["rect"].collidepoint(pos):
                self.active_box = idx

        # Verificar si se presionó el botón de ejecutar
        if self.run_button.collidepoint(pos):
            if len(self.selected_processors) == 2:
                self.run_selected_processors()

    def handle_keypress(self, key):
        """Maneja la entrada de texto para ajustar el intervalo."""
        if self.active_box is not None:
            box = self.interval_boxes[self.active_box]
            if key == pygame.K_BACKSPACE:
                box["interval"] = box["interval"][:-1]  # Eliminar el último carácter
            elif key == pygame.K_PERIOD and "." not in box["interval"]:
                box["interval"] += "."  # Agregar un punto decimal si no existe
            elif pygame.K_0 <= key <= pygame.K_9:
                digit = chr(key)
                box["interval"] += digit  # Agregar un dígito
            try:
                self.processors[self.active_box]["interval"] = float(box["interval"])
            except ValueError:
                pass  # Si el valor no es un número válido, no lo actualices

    def run_selected_processors(self):
        """Ejecuta los procesadores seleccionados con sus intervalos configurados."""
        positions = [(0, 50), (850, 50)]  # Posiciones para las ventanas

        for idx, processor in enumerate(self.selected_processors):
            interval = processor["interval"]
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{positions[idx][0]},{positions[idx][1]}"
            subprocess.Popen([sys.executable, processor["file"], str(interval)])

    def run(self):
        """Bucle principal de la interfaz."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_keypress(event.key)

            self.draw()
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    interface = MultiProcessorInterface()
    interface.run()
