import os
import pygame
import subprocess
import sys
from multiprocessing import Process

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

        # Procesadores
        self.processors = [
            {"name": "No Hazard", "rect": pygame.Rect(50, 100, 300, 80), "file": "main.py", "selected": False},
            {"name": "Branch Prediction 2", "rect": pygame.Rect(50, 200, 300, 80), "file": "mainBP.py", "selected": False},
            {"name": "Forwarding 3", "rect": pygame.Rect(50, 300, 300, 80), "file": "mainF.py", "selected": False},
            {"name": "Full Hazards 4", "rect": pygame.Rect(50, 400, 300, 80), "file": "mainFH.py", "selected": False},
        ]

        # Botón de ejecutar
        self.run_button = pygame.Rect(400, 500, 200, 50)

        # Estado del bucle principal
        self.running = True
        self.selected_processors = []

    def draw(self):
        """Dibuja la interfaz gráfica."""
        self.screen.fill(self.LIGHT_GRAY)

        # Dibujar los procesadores
        for processor in self.processors:
            color = self.GREEN if processor["selected"] else self.RED
            pygame.draw.rect(self.screen, color, processor["rect"])
            text = self.font.render(processor["name"], True, self.WHITE)
            text_rect = text.get_rect(center=processor["rect"].center)
            self.screen.blit(text, text_rect)

        # Dibujar el botón de ejecutar
        pygame.draw.rect(self.screen, self.BLACK, self.run_button)
        run_text = self.font.render("Ejecutar", True, self.WHITE)
        run_text_rect = run_text.get_rect(center=self.run_button.center)
        self.screen.blit(run_text, run_text_rect)

    def handle_click(self, pos):
        """Maneja los clics en la interfaz."""
        # Verificar si se seleccionó un procesador
        for processor in self.processors:
            if processor["rect"].collidepoint(pos):
                processor["selected"] = not processor["selected"]
                if processor["selected"]:
                    self.selected_processors.append(processor["file"])
                else:
                    self.selected_processors.remove(processor["file"])
                # Asegurarse de que solo se seleccionen 2 procesadores
                if len(self.selected_processors) > 2:
                    deselected = self.selected_processors.pop(0)
                    for proc in self.processors:
                        if proc["file"] == deselected:
                            proc["selected"] = False

        # Verificar si se presionó el botón de ejecutar
        if self.run_button.collidepoint(pos):
            if len(self.selected_processors) == 2:
                self.run_selected_processors()

    def run_selected_processors(self):
        """Ejecuta las consolas y las interfaces para los procesadores seleccionados."""
        positions = [(0, 50), (850, 50)]  # Posiciones para las interfaces

        for idx, file in enumerate(self.selected_processors):
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{positions[idx][0]},{positions[idx][1]}"
            subprocess.Popen([sys.executable, file])

    def run(self):
        """Bucle principal de la interfaz."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            # Dibujar la interfaz
            self.draw()
            pygame.display.flip()

        # Finalización segura de Pygame
        pygame.quit()


# Código principal
if __name__ == "__main__":
    interface = MultiProcessorInterface()
    interface.run()
