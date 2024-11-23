import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 1300, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Componentes Resaltados con Registros Alineados")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fuentes
font = pygame.font.Font(None, 24)

# Componentes
component_height = 150
components = [
    {"name": "Instruction Memory", "rect": pygame.Rect(150, 225, 150, component_height), "highlight": False},
    {"name": "Register File", "rect": pygame.Rect(450, 225, 150, 100), "highlight": False},
    {"name": "ALU", "rect": pygame.Rect(750, 250, 100, 80), "highlight": False},
    {"name": "Data Memory", "rect": pygame.Rect(1050, 225, 150, component_height), "highlight": False},
]

# Registros alargados (alineados con componentes y expanden verticalmente)
registers = [
    pygame.Rect(50, 100, 20, 400),    # Registro inicial (entrada a Instruction Memory)
    pygame.Rect(330, 100, 20, 400),  # Entre Instruction Memory y Register File
    pygame.Rect(630, 100, 20, 400),  # Entre Register File y ALU
    pygame.Rect(870, 100, 20, 400),  # Entre ALU y Data Memory
    pygame.Rect(1220, 100, 20, 400),  # Registro final (salida de Data Memory)
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

# Función para resaltar un componente y las líneas asociadas
def highlight_component(index):
    """Resalta un componente y las líneas conectadas a él."""
    for i, component in enumerate(components):
        component["highlight"] = (i == index)

# Función para resaltar conexiones asociadas a un componente
def get_highlighted_connections(index):
    """Devuelve las conexiones a resaltar para el componente seleccionado."""
    highlighted = []
    if index == 0:  # Instruction Memory
        highlighted.append(connections[0])
        highlighted.append(connections[1])
    elif index == 1:  # Register File
        highlighted.append(connections[1])
        highlighted.append(connections[2])
    elif index == 2:  # ALU
        highlighted.append(connections[3])
        highlighted.append(connections[4])
    elif index == 3:  # Data Memory
        highlighted.append(connections[5])
        highlighted.append(connections[6])
    return highlighted

# Bucle principal
running = True
highlighted_index = -1  # Ningún componente resaltado inicialmente

while running:
    screen.fill(WHITE)  # Fondo blanco

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:  # Resaltar Instruction Memory
                highlighted_index = 0
            elif event.key == pygame.K_2:  # Resaltar Register File
                highlighted_index = 1
            elif event.key == pygame.K_3:  # Resaltar ALU
                highlighted_index = 2
            elif event.key == pygame.K_4:  # Resaltar Data Memory
                highlighted_index = 3
            elif event.key == pygame.K_0:  # Quitar resaltado
                highlighted_index = -1

    # Dibujar componentes
    for i, component in enumerate(components):
        color = RED if component["highlight"] else BLACK
        pygame.draw.rect(screen, color, component["rect"], 2)  # Rectángulo
        text = font.render(component["name"], True, color)
        text_rect = text.get_rect(center=component["rect"].center)
        screen.blit(text, text_rect)

    # Dibujar registros
    for register in registers:
        pygame.draw.rect(screen, BLACK, register, 2)

    # Dibujar conexiones
    for connection in connections:
        color = RED if connection in get_highlighted_connections(highlighted_index) else BLACK
        pygame.draw.line(screen, color, connection[0], connection[1], 2)

    # Actualizar el estado de los componentes resaltados
    highlight_component(highlighted_index)

    # Actualizar pantalla
    pygame.display.flip()

# Cerrar Pygame
pygame.quit()
sys.exit()
