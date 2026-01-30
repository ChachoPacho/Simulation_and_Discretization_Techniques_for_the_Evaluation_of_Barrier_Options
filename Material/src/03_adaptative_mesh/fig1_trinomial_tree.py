import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Configuración
plt.figure(figsize=(14, 10))
ax = plt.gca()
ax.set_xlim(-0.5, 3.5)
ax.set_ylim(-1, 6.75)
ax.axis('off')

# Parámetros del árbol
S0 = 100
u = 1.15
d = 1/u
m = 1.0
steps = 3

# Colores para las ramas
color_up = '#2ecc71'    # Verde
color_mid = '#3498db'   # Azul
color_down = '#e74c3c'  # Rojo

# Probabilidades
p_u = 0.25
p_m = 0.50
p_d = 0.25

def draw_node(x, y, price, size=800):
    """Dibuja un nodo del árbol"""
    circle = plt.Circle((x, y), 0.15, color='white', ec='black', linewidth=2, zorder=3)
    ax.add_patch(circle)
    ax.text(x, y, f'${price:.1f}', ha='center', va='center', 
            fontsize=16, fontweight='bold', zorder=4)

def draw_edge(x1, y1, x2, y2, color, prob, label_offset=0.1):
    """Dibuja una arista con probabilidad"""
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=2, zorder=1)
    # Etiqueta de probabilidad
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    ax.text(mid_x + label_offset, mid_y, f'p={prob:.2f}', 
            fontsize=14, color=color, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, alpha=0.8))

# Construir el árbol completo
nodes = {}  # (step, index) -> (x, y, price)
edges = []  # Lista de aristas para dibujar después

# Paso 0 - centrado en y=3
center_y = 3
nodes[(0, 0)] = (0, center_y, S0)

# Generar todos los nodos primero
for step in range(steps):
    # Obtener todos los nodos del paso actual
    current_step_nodes = [(idx, data) for (s, idx), data in nodes.items() if s == step]
    
    for idx, (x_curr, y_curr, price_curr) in current_step_nodes:
        x_next = step + 1
        
        # Nodo superior (up)
        idx_up = idx + 1
        y_up = y_curr + 1
        price_up = price_curr * u
        if (step + 1, idx_up) not in nodes:
            nodes[(step + 1, idx_up)] = (x_next, y_up, price_up)
        edges.append((x_curr, y_curr, x_next, y_up, color_up, p_u, 0.15))
        
        # Nodo medio (middle)
        idx_mid = idx
        y_mid = y_curr
        price_mid = price_curr * m
        if (step + 1, idx_mid) not in nodes:
            nodes[(step + 1, idx_mid)] = (x_next, y_mid, price_mid)
        edges.append((x_curr, y_curr, x_next, y_mid, color_mid, p_m, -0.15))
        
        # Nodo inferior (down) - SIN restricción de idx >= 0
        idx_down = idx - 1
        y_down = y_curr - 1
        price_down = price_curr * d
        if (step + 1, idx_down) not in nodes:
            nodes[(step + 1, idx_down)] = (x_next, y_down, price_down)
        edges.append((x_curr, y_curr, x_next, y_down, color_down, p_d, 0.15))

# Dibujar todas las aristas primero
for x1, y1, x2, y2, color, prob, offset in edges:
    draw_edge(x1, y1, x2, y2, color, prob, offset)

# Dibujar todos los nodos encima
for (step, idx), (x, y, price) in nodes.items():
    draw_node(x, y, price)

# Etiquetas de tiempo
for step in range(steps + 1):
    ax.text(step, -0.5, f't={step}Δt', ha='center', fontsize=14, fontweight='bold')

# Leyenda
legend_elements = [
    mpatches.Patch(color=color_up, label='Movimiento arriba (u)'),
    mpatches.Patch(color=color_mid, label='Movimiento medio (m=1)'),
    mpatches.Patch(color=color_down, label='Movimiento abajo (d)')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=16, framealpha=0.9)

# Título
plt.title('Estructura de Árbol Trinomial', fontsize=20, fontweight='bold', pad=0)

# Anotaciones
ax.text(3.2, 6.5, f'u = {u:.3f}', fontsize=16, bbox=dict(boxstyle='round', facecolor='wheat'))
ax.text(3.2, 6, f'd = {d:.3f}', fontsize=16, bbox=dict(boxstyle='round', facecolor='wheat'))
ax.text(3.2, 5.5, f'm = {m:.3f}', fontsize=16, bbox=dict(boxstyle='round', facecolor='wheat'))

plt.tight_layout()
plt.savefig('../../../code/03_metodos_valoracion/figures/trinomial_tree_structure.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("Figura 1 guardada: trinomial_tree_structure.png")
plt.close()
