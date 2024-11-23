import pygame
import sys
import time

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 600, 600  # Ventana cuadrada
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Componentes Reorganizados y Escalados")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fuentes
font = pygame.font.Font(None, 20)

# Información inicial
start_time = time.time()
pc_value = 0
register_values = [0] * 8
memory_content = [0] * 16
pipeline_stages = ["Fetch", "Decode", "Execute", "Memory", "Writeback"]
pipeline_locations = [""] * len(pipeline_stages)

# Dimensiones ajustadas
component_width = 80
component_height = 50
register_width = 15
register_height = 180
vertical_spacing = 50
horizontal_spacing = 50
register_center_y = HEIGHT // 3
component_y = register_center_y - component_height // 2

# Componentes
components = [
    {"name": "Instruction Memory", "rect": pygame.Rect(50, component_y, component_width, component_height), "highlight": False},
    {"name": "Register File", "rect": pygame.Rect(50 + component_width + horizontal_spacing, component_y, component_width, component_height), "highlight": False},
    {"name": "ALU", "rect": pygame.Rect(50 + 2 * (component_width + horizontal_spacing), component_y, component_width, component_height), "highlight": False},
    {"name": "Data Memory", "rect": pygame.Rect(50 + 3 * (component_width + horizontal_spacing), component_y, component_width, component_height), "highlight": False},
]

# Registros
registers = [
    pygame.Rect(20, register_center_y - register_height // 2, register_width, register_height),  # Registro inicial
    pygame.Rect(50 + component_width, register_center_y - register_height // 2, register_width, register_height),  # Entre Instruction Memory y Register File
    pygame.Rect(50 + 2 * (component_width + horizontal_spacing) - horizontal_spacing, register_center_y - register_height // 2, register_width, register_height),  # Entre Register File y ALU
    pygame.Rect(50 + 3 * (component_width + horizontal_spacing) - horizontal_spacing, register_center_y - register_height // 2, register_width, register_height),  # Entre ALU y Data Memory
    pygame.Rect(50 + 4 * (component_width + horizontal_spacing), register_center_y - register_height // 2, register_width, register_height),  # Registro final
]

# Líneas de conexión
connections = [
    (registers[0].center, components[0]["rect"].midleft),  # Registro inicial -> Instruction Memory
    (components[0]["rect"].midright, registers[1].center),  # Instruction Memory -> Registro 1
    (registers[1].center, components[1]["rect"].midleft),  # Registro 1 -> Register File
    (components[1]["rect"].midright, registers[2].center),  # Register File -> Registro 2
    (registers[2].center, components[2]["rect"].midleft),  # Registro 2 -> ALU
    (components[2]["rect"].midright, registers[3].center),  # ALU -> Registro 3
    (registers[3].center, components[3]["rect"].midleft),  # Registro 3 -> Data Memory
    (components[3]["rect"].midright, registers[4].center),  # Data Memory -> Registro final
]

# Función para resaltar un componente
def highlight_component(index):
    for i, component in enumerate(components):
        component["highlight"] = (i == index)

# Dibujar estado
def draw_status():
    elapsed_time = time.time() - start_time
    info_x = 20
    info_y = HEIGHT // 2 + 30

    # Ciclo de ejecución
    cycle_text = font.render(f"Ciclo de ejecución: {pc_value // 4}", True, BLACK)
    screen.blit(cycle_text, (info_x, info_y))

    # Tiempo desde inicio
    time_text = font.render(f"Tiempo desde inicio: {elapsed_time:.2f} segundos", True, BLACK)
    screen.blit(time_text, (info_x, info_y + 20))

    # Valor del PC
    pc_text = font.render(f"Valor del PC: {pc_value}", True, BLACK)
    screen.blit(pc_text, (info_x, info_y + 40))

    # Valores de los registros
    reg_text = font.render(f"Valores de los registros: {register_values}", True, BLACK)
    screen.blit(reg_text, (info_x, info_y + 60))

    # Contenido de memoria
    memory_text = font.render(f"Contenido de memoria: {memory_content}", True, BLACK)
    screen.blit(memory_text, (info_x, info_y + 80))

    # Pipeline
    pipeline_text = font.render("Ubicación de instrucciones en el pipeline:", True, BLACK)
    screen.blit(pipeline_text, (info_x, info_y + 100))
    for i, stage in enumerate(pipeline_stages):
        stage_text = font.render(f"{stage}: {pipeline_locations[i]}", True, BLACK)
        screen.blit(stage_text, (info_x + 20, info_y + 120 + i * 15))

# Bucle principal
running = True
highlighted_index = -1

while running:
    screen.fill(WHITE)

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Simular avance de instrucción
                pc_value += 4
                register_values[pc_value % 8] = pc_value
                memory_content[pc_value % 16] = pc_value + 1
                pipeline_locations = [f"Instr {pc_value // 4}"] + pipeline_locations[:-1]
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_0]:
                highlighted_index = -1 if event.key == pygame.K_0 else event.key - pygame.K_1

    # Dibujar componentes
    for i, component in enumerate(components):
        color = RED if component["highlight"] else BLACK
        pygame.draw.rect(screen, color, component["rect"], 2)
        text = font.render(component["name"], True, color)
        text_rect = text.get_rect(center=component["rect"].center)
        screen.blit(text, text_rect)

    # Dibujar registros
    for register in registers:
        pygame.draw.rect(screen, BLACK, register, 2)

    # Dibujar conexiones
    for connection in connections:
        pygame.draw.line(screen, BLACK, connection[0], connection[1], 2)

    # Dibujar estado del sistema
    draw_status()

    # Actualizar el estado de los componentes resaltados
    highlight_component(highlighted_index)

    # Actualizar pantalla
    pygame.display.flip()

# Salir
pygame.quit()
sys.exit()
