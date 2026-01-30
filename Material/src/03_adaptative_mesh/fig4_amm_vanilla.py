import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(14, 10))

# Parámetros del árbol trinomial
time_steps = 10
K = 10  # Strike
h = 1.0  # Paso de precio
k = 1.0  # Paso de tiempo
T = time_steps  # Vencimiento

# Construir árbol trinomial
nodes = {}  # (step, price_level) -> (x, y)
edges = []

# Nodo inicial en nivel de precio K (para centrar alrededor del strike)
initial_level = K
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

# Dibujar aristas del árbol trinomial (malla gruesa)
for x1, y1, x2, y2 in edges:
    ax.plot([x1, x2], [y1, y2], color='gray', linewidth=1.5, alpha=0.3, zorder=1)

# Dibujar nodos del árbol trinomial (malla gruesa)
for (step, level), (x, y) in nodes.items():
    # Región crítica: último paso temporal, cerca del strike [K-2h, K+2h]
    in_critical = (step >= T - 1 and abs(y - K) <= 2.0)
    
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

# Dibujar malla fina en región crítica (T-k a T, alrededor de K en [K-2h, K+2h])
for t in np.arange(T - 1, T + 0.25, 0.25):
    for p in np.arange(K - 2.0, K + 2.0 + 0.25, 0.5):
        x = t
        y = p
        ax.scatter(x, y, s=25, color='#2ecc71', alpha=0.9, zorder=4, 
                  marker='s', edgecolors='darkgreen', linewidths=0.5)

# Línea del strike K
ax.axhline(y=K, color='#3498db', linewidth=3, linestyle='--', 
          label=f'Strike K = {K}', zorder=5)

# Rectángulo destacando región de refinamiento [K-2h, K+2h]
rect = mpatches.Rectangle(
    (T - 1 - 0.3, K - 2.0 - 0.3),
    1.6,
    4.6,
    linewidth=3, edgecolor='#f39c12', facecolor='yellow', 
    alpha=0.2, linestyle='--', zorder=2
)
ax.add_patch(rect)

# Anotaciones
ax.text(T - 0.5, K + 3.0, 'Región de\nRefinamiento', fontsize=12, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='#f39c12', alpha=0.7),
        ha='center')

# Flecha indicando T-k a T
ax.annotate('', xy=(T, K - 3.5), xytext=(T-1, K - 3.5),
            arrowprops=dict(arrowstyle='<->', color='black', lw=2.5))
ax.text(T-0.5, K - 4.3, 'k (último paso)', fontsize=11, 
        fontweight='bold', ha='center')

# Flecha indicando región espacial [K-2h, K+2h]
ax.annotate('', xy=(T + 0.5, K + 2.0), xytext=(T + 0.5, K - 2.0),
            arrowprops=dict(arrowstyle='<->', color='#f39c12', lw=2.5))
ax.text(T + 0.75, K, '[K-2h, K+2h]', fontsize=10, 
        fontweight='bold', rotation=90, va='center', color='#f39c12')

# Línea vertical indicando vencimiento T
ax.axvline(x=T, color='red', linewidth=2, linestyle=':', 
          label='Vencimiento T', alpha=0.7, zorder=5)

# Etiquetas de tiempo
for t in [0, T-1, T]:
    if t == 0:
        label = 't=0'
    elif t == T-1:
        label = 't=T-k'
    else:
        label = 't=T'
    ax.text(t, K - 5.5, label, fontsize=10, fontweight='bold', ha='center')

# Configuración de ejes
ax.set_xlabel('Tiempo (pasos)', fontsize=13, fontweight='bold')
ax.set_ylabel('Nivel de Precio', fontsize=13, fontweight='bold')
ax.set_title('AMM para Opciones Vanilla: Árbol Trinomial con Refinamiento cerca del Strike', 
            fontsize=14, fontweight='bold', pad=15)

# Leyenda
legend_elements = [
    mpatches.Patch(color='#95a5a6', label='Nodos árbol grueso (h, k)', alpha=0.7),
    mpatches.Patch(color='#2ecc71', label='Nodos malla fina (h/2, k/4)'),
    mpatches.Patch(color='yellow', edgecolor='#f39c12', linewidth=2, 
                  linestyle='--', label='Región de refinamiento', alpha=0.5),
    mpatches.Patch(color='#3498db', label=f'Strike K={K}'),
    mpatches.Patch(color='gray', label='Conexiones árbol trinomial', alpha=0.5)
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.9)

ax.set_xlim(-0.5, T + 1)
ax.set_ylim(K - 6, K + 5)
ax.grid(True, alpha=0.2, linestyle=':', zorder=0)

# Texto explicativo
textstr = 'Mayor no linealidad:\nalrededor de K al vencimiento'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.65, 0.98, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('../../code/03_metodos_valoracion/figures/amm_vanilla.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("Figura 4 guardada: amm_vanilla.png")
plt.close()
