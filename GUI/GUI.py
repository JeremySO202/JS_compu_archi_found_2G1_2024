import pygame
#import time

pygame.init()

class PygameInterface:
    def __init__(self, width=700, height=800):
        # Configuración de la ventana
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Componentes Interactivos con Inicializador")
        self.font = pygame.font.Font(None, 20)

        # Configuración de colores
        self.LIGHT_GRAY = (230, 230, 230)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 255, 0)
        

        # Estado inicial
        self.time = 0
        self.pc_value = 0
        self.register_values = [0] * 16
        self.memory_content = [0] * 32
        self.pipeline_stages = ["Fetch", "Decode", "Execute", "Memory", "Writeback"]
        self.pipeline_locations = [""] * len(self.pipeline_stages)

        # Cuadros de la interfaz
        self.components_rect = pygame.Rect(30, 30, 640, 300)
        self.status_left_rect = pygame.Rect(30, 350, 320, 420)
        self.status_right_rect = pygame.Rect(360, 350, 320, 420)

        # Configuración de componentes
        self.component_width = 120
        self.component_height = 40
        self.register_width = 15
        self.register_height = 120
        self.horizontal_spacing = (self.components_rect.width - 4 * self.component_width) // 5
        self.component_y = self.components_rect.y + (self.components_rect.height - self.component_height) // 2

        self.components = self._initialize_components()
        self.registers = self._initialize_registers()
        self.connections = self._initialize_connections()

        # Estado del bucle principal
        self.running = True

    def _initialize_components(self):
        """Inicializa los rectángulos de los componentes."""
        return [
            {"name": "Instruction\nMemory", "rect": pygame.Rect(self.components_rect.x + self.horizontal_spacing, self.component_y, self.component_width, self.component_height), "highlight": False, "color": self.BLACK},
            {"name": "Register File", "rect": pygame.Rect(self.components_rect.x + 2 * self.horizontal_spacing + self.component_width, self.component_y, self.component_width, self.component_height), "highlight": False, "color": self.BLACK},
            {"name": "ALU", "rect": pygame.Rect(self.components_rect.x + 3 * self.horizontal_spacing + 2 * self.component_width, self.component_y, self.component_width, self.component_height), "highlight": False, "color": self.BLACK},
            {"name": "Data Memory", "rect": pygame.Rect(self.components_rect.x + 4 * self.horizontal_spacing + 3 * self.component_width, self.component_y, self.component_width, self.component_height), "highlight": False, "color": self.BLACK},
        ]

    def _initialize_registers(self):
        """Inicializa los rectángulos de los registros."""
        return [
            pygame.Rect(self.components_rect.x + self.horizontal_spacing // 2, self.component_y + self.component_height // 2 - self.register_height // 2, self.register_width, self.register_height),
            pygame.Rect(self.components[0]["rect"].x + self.component_width, self.component_y + self.component_height // 2 - self.register_height // 2, self.register_width, self.register_height),
            pygame.Rect(self.components[1]["rect"].x + self.component_width, self.component_y + self.component_height // 2 - self.register_height // 2, self.register_width, self.register_height),
            pygame.Rect(self.components[2]["rect"].x + self.component_width, self.component_y + self.component_height // 2 - self.register_height // 2, self.register_width, self.register_height),
            pygame.Rect(self.components[3]["rect"].x + self.component_width + self.horizontal_spacing // 2, self.component_y + self.component_height // 2 - self.register_height // 2, self.register_width, self.register_height),
        ]

    def _initialize_connections(self):
        """Inicializa las conexiones entre registros y componentes."""
        return [
            (self.registers[0].center, self.components[0]["rect"].midleft),
            (self.components[0]["rect"].midright, self.registers[1].center),
            (self.registers[1].center, self.components[1]["rect"].midleft),
            (self.components[1]["rect"].midright, self.registers[2].center),
            (self.registers[2].center, self.components[2]["rect"].midleft),
            (self.components[2]["rect"].midright, self.registers[3].center),
            (self.registers[3].center, self.components[3]["rect"].midleft),
            (self.components[3]["rect"].midright, self.registers[4].center),
        ]

    def highlight_component(self, component_indices, color):
        """Permite resaltar múltiples componentes con un color."""
        for index in component_indices:
            if 0 <= index < len(self.components):
                self.components[index]["highlight"] = True
                self.components[index]["color"] = color


    def update_time_value(self, value):
        """Actualiza el valor del PC."""
        self.time = value

    def update_pc_value(self, value):
        """Actualiza el valor del PC."""
        self.pc_value = value

    
    def update_register_values(self, values):
        """Actualiza los valores de los registros."""
        if len(values) == len(self.register_values):
            self.register_values = values

    def update_memory_content(self, values):
        """Actualiza el contenido de la memoria."""
        if len(values) == len(self.memory_content):
            self.memory_content = values

    def draw(self):
        """Dibuja la interfaz en pantalla."""
        self.screen.fill(self.LIGHT_GRAY)

        # Cuadro de componentes
        pygame.draw.rect(self.screen, self.WHITE, self.components_rect)

        # Dibujar componentes
        for component in self.components:
            color = component["color"] if component["highlight"] else self.BLACK
            pygame.draw.rect(self.screen, self.WHITE, component["rect"])  # Fondo blanco
            pygame.draw.rect(self.screen, color, component["rect"], 2)  # Contorno
            lines = component["name"].split("\n")
            for idx, line in enumerate(lines):
                text = self.font.render(line, True, color)
                text_rect = text.get_rect(center=(component["rect"].centerx, component["rect"].centery - 10 + idx * 10))
                self.screen.blit(text, text_rect)

        # Dibujar registros
        for register in self.registers:
            pygame.draw.rect(self.screen, self.BLACK, register, 2)

        # Dibujar conexiones
        for connection in self.connections:
            pygame.draw.line(self.screen, self.BLACK, connection[0], connection[1], 2)

        # Dibujar estado
        self.draw_status_left()
        self.draw_status_right()


    def draw_status_left(self):
        #"""Dibuja el estado del lado izquierdo con registros en dos columnas."""
        elapsed_time = self.time
        info_x = self.status_left_rect.x + 10
        info_y = self.status_left_rect.y + 10

        pygame.draw.rect(self.screen, self.WHITE, self.status_left_rect)

        # Ciclo y tiempo
        cycle_text = self.font.render(f"Ciclo de ejecución: {self.pc_value // 4}", True, self.BLACK)
        self.screen.blit(cycle_text, (info_x, info_y))

        time_text = self.font.render(f"Tiempo desde inicio: {elapsed_time:.2f} segundos", True, self.BLACK)
        self.screen.blit(time_text, (info_x, info_y + 20))

        pc_text = self.font.render(f"Valor del PC: {self.pc_value}", True, self.BLACK)
        self.screen.blit(pc_text, (info_x, info_y + 40))

        # Dibujar registros en dos columnas
        reg_text = self.font.render("Registros:", True, self.BLACK)
        self.screen.blit(reg_text, (info_x, info_y + 70))

        column1_x = info_x + 10
        column2_x = info_x + 160
        for i in range(len(self.register_values) // 2):
            reg_1 = self.font.render(f"R{i}: {self.register_values[i]}", True, self.BLACK)
            reg_2 = self.font.render(f"R{i + 8}: {self.register_values[i + 8]}", True, self.BLACK)
            self.screen.blit(reg_1, (column1_x, info_y + 90 + i * 20))
            self.screen.blit(reg_2, (column2_x, info_y + 90 + i * 20))


        # Pipeline
        pipeline_text = self.font.render("Ubicación de instrucciones en el pipeline:", True, self.BLACK)
        self.screen.blit(pipeline_text, (info_x, info_y + 250))
        for i, stage in enumerate(self.pipeline_stages):
            stage_text = self.font.render(f"{stage}: {self.pipeline_locations[i]}", True, self.BLACK)
            self.screen.blit(stage_text, (info_x, info_y + 270 + i * 20))

    def draw_status_right(self):
        """Dibuja el estado del lado derecho con memoria en dos columnas."""
        info_x = self.status_right_rect.x + 10
        info_y = self.status_right_rect.y + 10

        pygame.draw.rect(self.screen, self.WHITE, self.status_right_rect)

        # Título de memoria
        memory_text = self.font.render("Memoria:", True, self.BLACK)
        self.screen.blit(memory_text, (info_x, info_y))

        # Dibujar memoria en dos columnas
        column1_x = info_x + 10
        column2_x = info_x + 160
        for i in range(len(self.memory_content) // 2):
            mem_1 = self.font.render(f"M{i}: {self.memory_content[i]}", True, self.BLACK)
            mem_2 = self.font.render(f"M{i + 16}: {self.memory_content[i + 16]}", True, self.BLACK)
            self.screen.blit(mem_1, (column1_x, info_y + 20 + i * 20))
            self.screen.blit(mem_2, (column2_x, info_y + 20 + i * 20))

        

    def run(self):
        """Bucle principal de la interfaz gráfica."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Dibuja la interfaz y actualiza la pantalla
            self.draw()
            pygame.display.flip()

        # Finalización segura de Pygame
        pygame.quit()
