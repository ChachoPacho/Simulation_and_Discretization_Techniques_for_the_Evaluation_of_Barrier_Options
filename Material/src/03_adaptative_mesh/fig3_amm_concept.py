import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(14, 10))

# Parámetros del árbol
S0 = 100
u = 1.15
d = 1/u
steps = 6
h_price = 1.0  # Espaciado visual en precio

# Región crítica (ejemplo: alrededor de un nivel crítico)
critical_price_center = 3  # Nivel central de la región crítica
critical_time_start = 3
critical_time_end = 6

# Función para calcular posición Y basada en el precio
def price_to_y(price_level):
    return price_level * h_price

# Construir árbol trinomial
nodes = {}  # (step, price_level) -> (x, y, price)
edges = []

# Nodo inicial
nodes[(0, 0)] = (0, price_to_y(0), S0)

# Generar árbol trinomial
for step in range(steps):
    current_nodes = [(level, data) for (s, level), data in nodes.items() if s == step]
    
    for level, (x_curr, y_curr, price_curr) in current_nodes:
        x_next = step + 1
        
        # Movimiento arriba (up)
        level_up = level + 1
        y_up = price_to_y(level_up)
        price_up = price_curr * u
        if (step + 1, level_up) not in nodes:
            nodes[(step + 1, level_up)] = (x_next, y_up, price_up)
        edges.append((x_curr, y_curr, x_next, y_up, '#2ecc71', 0.8))
        
        # Movimiento medio (middle)
        level_mid = level
        y_mid = price_to_y(level_mid)
        price_mid = price_curr
        if (step + 1, level_mid) not in nodes:
            nodes[(step + 1, level_mid)] = (x_next, y_mid, price_mid)
        edges.append((x_curr, y_curr, x_next, y_mid, '#3498db', 0.8))
        
        # Movimiento abajo (down)
        level_down = level - 1
        y_down = price_to_y(level_down)
        price_down = price_curr * d
        if (step + 1, level_down) not in nodes:
            nodes[(step + 1, level_down)] = (x_next, y_down, price_down)
        edges.append((x_curr, y_curr, x_next, y_down, '#e74c3c', 0.8))

# Dibujar aristas del árbol (malla gruesa)
for x1, y1, x2, y2, color, alpha in edges:
    ax.plot([x1, x2], [y1, y2], color='gray', linewidth=1.5, alpha=0.3, zorder=1)

# Dibujar nodos del árbol (malla gruesa)
for (step, level), (x, y, price) in nodes.items():
    # Determinar si está en región crítica
    in_critical = (critical_time_start <= step <= critical_time_end and 
                  abs(level - critical_price_center) <= 2)
    
    if in_critical:
        color = '#e74c3c'
        size = 80
        alpha = 0.6
        edgecolor = 'red'
        linewidth = 2
    else:
        color = '#95a5a6'
        size = 60
        alpha = 0.5
        edgecolor = 'black'
        linewidth = 1
    
    ax.scatter(x, y, s=size, color=color, alpha=alpha, zorder=3, 
              edgecolors=edgecolor, linewidths=linewidth)

# Dibujar malla fina en región crítica
fine_mesh_nodes = []
for t in np.arange(critical_time_start, critical_time_end + 0.25, 0.25):
    for p in np.arange(critical_price_center - 2, critical_price_center + 2 + 0.25, 0.5):
        x = t
        y = price_to_y(p)
        fine_mesh_nodes.append((x, y))
        ax.scatter(x, y, s=20, color='#2ecc71', alpha=0.9, zorder=4, 
                  marker='s', edgecolors='darkgreen', linewidths=0.5)

# Destacar región crítica con rectángulo
rect_x = critical_time_start - 0.3
rect_y = price_to_y(critical_price_center - 2.5)
rect_width = (critical_time_end - critical_time_start) + 0.6
rect_height = price_to_y(5)

rect = mpatches.Rectangle(
    (rect_x, rect_y),
    rect_width,
    rect_height,
    linewidth=3, edgecolor='#f39c12', facecolor='yellow', 
    alpha=0.15, linestyle='--', zorder=2
)
ax.add_patch(rect)

# Etiquetas y anotaciones
ax.text(1, price_to_y(6), 'Árbol Trinomial\n(Malla Gruesa)', fontsize=12, fontweight='bold', 
        bbox=dict(boxstyle='round', facecolor='#95a5a6', alpha=0.7),
        ha='center')

ax.text(4, price_to_y(critical_price_center + 2.5), 
       'Malla Fina\nInjertada\n(h/2, k/4)', fontsize=11, fontweight='bold', 
        bbox=dict(boxstyle='round', facecolor='#2ecc71', alpha=0.8),
        ha='center')

# Flechas indicando pasos
# Paso temporal grueso (k)
ax.annotate('', xy=(1, price_to_y(-3)), xytext=(0, price_to_y(-3)),
            arrowprops=dict(arrowstyle='<->', color='black', lw=2.5))
ax.text(0.5, price_to_y(-3.5), 'k', fontsize=12, fontweight='bold', ha='center')

# Paso de precio grueso (h)
ax.annotate('', xy=(-0.3, price_to_y(1)), xytext=(-0.3, price_to_y(0)),
            arrowprops=dict(arrowstyle='<->', color='black', lw=2.5))
ax.text(-0.6, price_to_y(0.5), 'h', fontsize=12, fontweight='bold', ha='center')

# Paso temporal fino (k/4)
ax.annotate('', xy=(critical_time_start + 0.25, price_to_y(0.5)), 
            xytext=(critical_time_start, price_to_y(0.5)),
            arrowprops=dict(arrowstyle='<->', color='#2ecc71', lw=2.5))
ax.text(critical_time_start + 0.125, price_to_y(0), 'k/4', fontsize=10, 
        fontweight='bold', ha='center', color='#2ecc71')

# Paso de precio fino (h/2)
ax.annotate('', xy=(critical_time_start - 0.3, price_to_y(critical_price_center + 0.5)), 
            xytext=(critical_time_start - 0.3, price_to_y(critical_price_center)),
            arrowprops=dict(arrowstyle='<->', color='#2ecc71', lw=2.5))
ax.text(critical_time_start - 0.5, price_to_y(critical_price_center + 0.25), 
        'h/2', fontsize=10, fontweight='bold', ha='center', color='#2ecc71')

# Configuración de ejes
ax.set_xlabel('Tiempo (pasos)', fontsize=13, fontweight='bold')
ax.set_ylabel('Nivel de Precio', fontsize=13, fontweight='bold')
ax.set_title('Concepto del Modelo de Malla Adaptativa (AMM)\nÁrbol Trinomial + Malla Fina', 
            fontsize=15, fontweight='bold', pad=15)

# Leyenda
legend_elements = [
    mpatches.Patch(color='#95a5a6', label='Nodos árbol grueso (h, k)', alpha=0.7),
    mpatches.Patch(color='#2ecc71', label='Nodos malla fina (h/2, k/4)'),
    mpatches.Patch(color='yellow', edgecolor='#f39c12', linewidth=2, 
                  linestyle='--', label='Región crítica (refinada)', alpha=0.5),
    mpatches.Patch(color='gray', label='Conexiones árbol trinomial', alpha=0.5)
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.9)

ax.set_xlim(-1.2, steps + 0.5)
ax.set_ylim(price_to_y(-5), price_to_y(7))
ax.grid(True, alpha=0.2, linestyle=':', zorder=0)

# Texto explicativo
textstr = ('Principio del AMM:\n'
          '• Árbol grueso para la mayoría del dominio\n'
          '• Malla fina solo en regiones críticas\n'
          '• Eficiencia: precisión sin costo excesivo')
props = dict(boxstyle='round', facecolor='wheat', alpha=0.9, edgecolor='black', linewidth=2)
ax.text(0.98, 0.98, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right', bbox=props)

plt.tight_layout()
plt.savefig('../../../code/03_metodos_valoracion/figures/amm_concept.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("Figura 3 guardada: amm_concept.png")
plt.close()
