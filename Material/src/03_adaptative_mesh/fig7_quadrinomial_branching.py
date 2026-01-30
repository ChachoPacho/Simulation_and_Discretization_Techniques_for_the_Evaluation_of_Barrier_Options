import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(14, 10))

# Parámetros del árbol trinomial
time_steps = 2
h = 1.0  # Paso de precio
k = 1.0  # Paso de tiempo

# Construir árbol trinomial de 2 pasos
nodes = {}  # (step, price_level) -> (x, y)
edges = []

# Nodo inicial en nivel de precio 0
initial_level = 0
nodes[(0, initial_level)] = (0, initial_level * h)

# Generar árbol trinomial
for step in range(time_steps):
    current_nodes = [(level, data) for (s, level), data in nodes.items() if s == step]
    
    for level, (x_curr, y_curr) in current_nodes:
        x_next = step + 1
        
        # Movimiento arriba (up)
        level_up = level + 1
        y_up = level_up * h
        if (step + 1, level_up) not in nodes:
            nodes[(step + 1, level_up)] = (x_next, y_up)
        edges.append((x_curr, y_curr, x_next, y_up))
        
        # Movimiento medio (middle)
        level_mid = level
        y_mid = level_mid * h
        if (step + 1, level_mid) not in nodes:
            nodes[(step + 1, level_mid)] = (x_next, y_mid)
        edges.append((x_curr, y_curr, x_next, y_mid))
        
        # Movimiento abajo (down)
        level_down = level - 1
        y_down = level_down * h
        if (step + 1, level_down) not in nodes:
            nodes[(step + 1, level_down)] = (x_next, y_down)
        edges.append((x_curr, y_curr, x_next, y_down))

# Dibujar aristas del árbol trinomial
for x1, y1, x2, y2 in edges:
    ax.plot([x1, x2], [y1, y2], color='black', linewidth=2, alpha=0.8, zorder=1)

# Dibujar nodos del árbol trinomial
for (step, level), (x, y) in nodes.items():
    color = '#95a5a6'
    size = 60
    alpha = 0.5
    edgecolor = 'black'
    linewidth = 1
    
    ax.scatter(x, y, s=size, color=color, alpha=alpha, zorder=3,
              edgecolors=edgecolor, linewidths=linewidth)

# ============ AÑADIR 3 NODOS EN t=-0.25 ============
epsilon = h/4  # Perturbación pequeña

nodes_t_minus = [
    (-0.25, epsilon, '#2ecc71'),      # S0 + ε (verde)
    (-0.25, 0, 'gold'),               # S0 (dorado)
    (-0.25, -epsilon, '#e74c3c')      # S0 - ε (rojo)
]

for x, y, color in nodes_t_minus:
    ax.scatter(x, y, s=80, color=color, alpha=0.6, zorder=4,
              edgecolors='red', linewidths=2)

# ============ AÑADIR 5 NODOS EN t=k/4 (x=0) ============
nodes_t_k4 = [
    (0, h, '#95a5a6'),       # S0 + h
    (0, h/2, '#95a5a6'),     # S0 + h/2
    (0, 0, '#95a5a6'),       # S0
    (0, -h/2, '#95a5a6'),    # S0 - h/2
    (0, -h, '#95a5a6')       # S0 - h
]

for x, y, color in nodes_t_k4:
    ax.scatter(x, y, s=60, color=color, alpha=0.5, zorder=3,
              edgecolors='black', linewidths=1)

# ============ AÑADIR 2 NODOS NUEVOS EN t=k+k/4 (x=1) ============
nodes_t_k_plus_k4 = [
    (1, 2*h, '#95a5a6'),     # S0 + 2h
    (1, -2*h, '#95a5a6')     # S0 - 2h
]

for x, y, color in nodes_t_k_plus_k4:
    ax.scatter(x, y, s=60, color=color, alpha=0.5, zorder=3,
              edgecolors='black', linewidths=1)

# ============ AÑADIR 2 NODOS NUEVOS EN t=2k+k/4 (x=2) ============
nodes_t_2k_plus_k4 = [
    (2, 3*h, '#95a5a6'),     # S0 + 3h
    (2, -3*h, '#95a5a6')     # S0 - 3h
]

for x, y, color in nodes_t_2k_plus_k4:
    ax.scatter(x, y, s=60, color=color, alpha=0.5, zorder=3,
              edgecolors='black', linewidths=1)

# ============ CONECTAR NODOS CON LÍNEAS PUNTEADAS ============

# 1. Conectar t=0 con t=k/4
# Desde S0+ε (verde): conecta a los 4 superiores de t=k/4 (cuadrinomial) - LÍNEA SÓLIDA
# NO conecta al inferior S0-h
for x_to, y_to, _ in nodes_t_k4:
    if y_to >= -h/2 - 0.01:  # Solo S0+h, S0+h/2, S0, S0-h/2 (no S0-h)
        ax.plot([-0.25, x_to], [epsilon, y_to], 
               color='gray', linewidth=2, alpha=0.6, linestyle='-', zorder=2)

# Desde S0 (dorado): conecta a los 3 nodos centrales de t=k/4 (trinomial) - LÍNEA DASHEADA
for x_to, y_to, _ in nodes_t_k4:
    if abs(y_to - h) > 0.01 and abs(y_to + h) > 0.01:  # No S0+h ni S0-h
        ax.plot([-0.25, x_to], [0, y_to], 
               color='gray', linewidth=2, alpha=0.6, linestyle='-', zorder=2)

# Desde S0-ε (rojo): conecta a los 4 inferiores de t=k/4 (cuadrinomial) - LÍNEA SÓLIDA
# NO conecta al superior S0+h
for x_to, y_to, _ in nodes_t_k4:
    if y_to <= h/2 + 0.01:  # Solo S0+h/2, S0, S0-h/2, S0-h (no S0+h)
        ax.plot([-0.25, x_to], [-epsilon, y_to], 
               color='gray', linewidth=2, alpha=0.6, linestyle='-', zorder=2)

# 2. Conectar t=k/4 con t=k+k/4
# Obtener todos los nodos en t=k+k/4 (del árbol + los 2 nuevos)
all_nodes_t1 = [(x, y) for (step, level), (x, y) in nodes.items() if step == 1]
all_nodes_t1.extend([(x, y) for x, y, _ in nodes_t_k_plus_k4])

for x_from, y_from, _ in nodes_t_k4:
    if abs(y_from - h) < 0.01:  # S0+h
        for x_to, y_to in all_nodes_t1:
            if y_to >= 0:  # Solo los 4 superiores: S0+2h, S0+h, S0, S0-h (pero hasta S0)
                y_diff = y_to - y_from
                # Conectar a los 4 nodos superiores - LÍNEA SÓLIDA
                if abs(y_diff - h) < 0.01 or abs(y_diff) < 0.01 or abs(y_diff + h) < 0.01 or abs(y_diff + 2*h) < 0.01:
                    ax.plot([x_from, x_to], [y_from, y_to], 
                           color='gray', linewidth=2, alpha=0.6, linestyle='-', zorder=2)

# Conectar S0+h/2 (segundo nodo) - conecta a todos EXCEPTO S0-2h
for x_from, y_from, _ in nodes_t_k4:
    if abs(y_from - h/2) < 0.01:  # S0+h/2
        for x_to, y_to in all_nodes_t1:
            # Conectar a todos excepto S0-2h (y=-2)
            if abs(y_to + 2*h) > 0.01:  # No es S0-2h
                ax.plot([x_from, x_to], [y_from, y_to], 
                       color='gray', linewidth=2, alpha=0.6, linestyle='--', zorder=2)

# Conectar S0-h/2 (cuarto nodo) - conecta a todos EXCEPTO S0+2h
for x_from, y_from, _ in nodes_t_k4:
    if abs(y_from + h/2) < 0.01:  # S0-h/2
        for x_to, y_to in all_nodes_t1:
            # Conectar a todos excepto S0+2h (y=2)
            if abs(y_to - 2*h) > 0.01:  # No es S0+2h
                ax.plot([x_from, x_to], [y_from, y_to], 
                       color='gray', linewidth=2, alpha=0.6, linestyle='--', zorder=2)

for x_from, y_from, _ in nodes_t_k4:
    if abs(y_from) <= epsilon + 0.01:  # S0+ε o S0-ε
        for x_to, y_to in all_nodes_t1:
            y_diff = y_to - y_from
            # Trinomial: conectar si la diferencia es aproximadamente -h, 0, o +h
            if abs(y_diff - h) < 0.01 or abs(y_diff) < 0.01 or abs(y_diff + h) < 0.01:
                ax.plot([x_from, x_to], [y_from, y_to], 
                       color='gray', linewidth=2, alpha=0.6, linestyle='--', zorder=2)

# Desde S0-h (nodo inferior solitario en t=k/4): conecta a los 4 inferiores en t=k+k/4
for x_from, y_from, _ in nodes_t_k4:
    if abs(y_from + h) < 0.01:  # S0-h
        for x_to, y_to in all_nodes_t1:
            if y_to <= 0:  # Solo los 4 inferiores
                y_diff = y_to - y_from
                # Conectar a los 4 nodos inferiores - LÍNEA SÓLIDA
                if abs(y_diff - h) < 0.01 or abs(y_diff) < 0.01 or abs(y_diff + h) < 0.01 or abs(y_diff - 2*h) < 0.01:
                    ax.plot([x_from, x_to], [y_from, y_to], 
                           color='gray', linewidth=2, alpha=0.6, linestyle='-', zorder=2)

# 3. Conectar t=k+k/4 con t=2k+k/4
# Obtener todos los nodos en t=2k+k/4 (del árbol + los 2 nuevos)
all_nodes_t2 = [(x, y) for (step, level), (x, y) in nodes.items() if step == 2]
all_nodes_t2.extend([(x, y) for x, y, _ in nodes_t_2k_plus_k4])

# Desde cada nodo en t=k+k/4, conectar trinomialmente
for x_from, y_from in all_nodes_t1:
    for x_to, y_to in all_nodes_t2:
        y_diff = y_to - y_from
        # Trinomial: conectar si la diferencia es aproximadamente -h, 0, o +h
        if abs(y_diff - h) < 0.01 or abs(y_diff) < 0.01 or abs(y_diff + h) < 0.01:
            ax.plot([x_from, x_to], [y_from, y_to], 
                   color='gray', linewidth=2, alpha=0.6, linestyle='--', zorder=2)

# ============ ETIQUETAS EN EJE X (TIEMPO) ============
time_labels = [
    (-0.25, r'$t = 0$'),
    (0, r'$t = \frac{k}{4}$'),
    (1, r'$t = k + \frac{k}{4}$'),
    (2, r'$t = 2k + \frac{k}{4}$')
]

for x_pos, label in time_labels:
    ax.text(x_pos, -2.8, label, fontsize=12, fontweight='bold', 
           ha='center', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# ============ ETIQUETAS EN EJE Y (PRECIO) ============
price_labels = [
    (3*h, r'$S_0+3h$'),
    (2*h, r'$S_0+2h$'),
    (h, r'$S_0+h$'),
    (h/2, r'$S_0+h/2$'),
    (h/4, r'$S_0+h/4$'),
    (0, r'$S_0$'),
    (-h/4, r'$S_0-h/4$'),
    (-h/2, r'$S_0-h/2$'),
    (-h, r'$S_0-h$'),
    (-2*h, r'$S_0-2h$'),
    (-3*h, r'$S_0-3h$')
]

for y_pos, label in price_labels:
    ax.text(-0.5, y_pos, label, fontsize=9, 
           ha='left', va='center', color='#333',
           bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7))

# Configuración de ejes
ax.set_xlim(-0.55, 2.25)
ax.set_ylim(-3.5, 3.25)

# Añadir cuadrícula manual en las posiciones correctas
# Líneas verticales (tiempo)
for x_pos in [-0.25, 0, 1, 2]:
    ax.axvline(x=x_pos, color='gray', alpha=0.2, linestyle=':', zorder=0, linewidth=1)

# Líneas horizontales (precio)
for y_pos in [-3*h, -2*h, -h, -epsilon, 0, epsilon, h, 2*h, 3*h]:
    ax.axhline(y=y_pos, color='gray', alpha=0.2, linestyle=':', zorder=0, linewidth=1)

ax.axis('off')

# Título
ax.text(0.8, 3.2, 'Ramificación Cuadrinomial para Cálculo de Griegas', 
       fontsize=17, fontweight='bold', ha='center',
       bbox=dict(boxstyle='round,pad=0.6', facecolor='lightblue', 
                edgecolor='navy', linewidth=2, alpha=0.9))

# Subtítulo explicativo
ax.text(0.75, 2.7, 'Método de Diferencias Finitas en Árbol Trinomial Adaptativo', 
       fontsize=11, ha='center', style='italic', color='#333')

# ============ LEYENDA ============
legend_elements = [
    mpatches.Patch(color='black', label='Árbol trinomial base (h, k)'),
    plt.Line2D([0], [0], color='gray', linewidth=2.5, linestyle='--', alpha=0.8,
               label='AMM-1 Lattice añadido'),
    plt.Line2D([0], [0], color='gray', linewidth=2.5, linestyle='-', alpha=0.8,
               label='AMM-2 Lattice añadido'),
    mpatches.Patch(color='#2ecc71', alpha=0.6, label=r'$S_0 + \varepsilon$ (perturbación +)'),
    mpatches.Patch(color='#e74c3c', alpha=0.6, label=r'$S_0 - \varepsilon$ (perturbación $-$)'),
    mpatches.Patch(color='gold', alpha=0.6, label=r'$S_0$ (precio central)')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.95,
         bbox_to_anchor=(0.75, 0.99), edgecolor='black', fancybox=True)

plt.tight_layout()
plt.savefig('../../code/03_metodos_valoracion/figures/quadrinomial_branching.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("Figura 7 guardada: quadrinomial_branching.png")
plt.close()
