import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(14, 10))

# Parámetros del árbol trinomial
time_steps = 10
H = 10  # Barrera
S0 = 10.5  # Precio inicial cerca de la barrera
h = 1.0  # Paso de precio
k = 1.0  # Paso de tiempo

# Construir árbol trinomial
nodes = {}  # (step, price_level) -> (x, y)
edges = []

# Nodo inicial en nivel de precio cercano a la barrera
initial_level = S0
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
    # Región crítica: banda alrededor de H en todo el tiempo [H-2h, H+2h]
    in_critical = abs(y - H) <= 2.0
    
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

# Dibujar malla fina en región crítica (banda alrededor de H [H-2h, H+2h], todo el tiempo)
for t in np.arange(0, time_steps + 0.25, 0.25):
    for p in np.arange(H - 2.0, H + 2.0 + 0.25, 0.5):
        x = t
        y = p
        ax.scatter(x, y, s=25, color='#2ecc71', alpha=0.9, zorder=4, 
                  marker='s', edgecolors='darkgreen', linewidths=0.5)

# Línea de la barrera H
ax.axhline(y=H, color='#3498db', linewidth=4, linestyle='-', 
          label=f'Barrera H = {H}', zorder=5)

# Precio inicial S0
ax.scatter(0, S0, s=300, color='gold', marker='*', edgecolors='black', 
          linewidth=2, label=f'S₀ = {S0} (cerca de H)', zorder=6)

# Rectángulo destacando banda de refinamiento [H-2h, H+2h]
rect = mpatches.Rectangle(
    (-0.3, H - 2.0 - 0.3),
    time_steps + 0.6,
    4.6,
    linewidth=3, edgecolor='#f39c12', facecolor='yellow', 
    alpha=0.15, linestyle='--', zorder=2
)
ax.add_patch(rect)

# Flechas mostrando flujo de información
# De malla gruesa a malla fina
for t in [2, 5, 8]:
    # Desde arriba
    ax.annotate('', xy=(t, H + 1.5), xytext=(t + 1.5, H + 3),
                arrowprops=dict(arrowstyle='->', color='purple', lw=2.5, 
                              linestyle='--', alpha=0.7))
    # Desde abajo
    ax.annotate('', xy=(t, H - 1.5), xytext=(t + 1.5, H - 3),
                arrowprops=dict(arrowstyle='->', color='purple', lw=2.5, 
                              linestyle='--', alpha=0.7))

# Etiqueta de flujo
ax.text(6.5, H + 3, 'Flujo de información:\nMalla gruesa → Malla fina', 
       fontsize=11, fontweight='bold', ha='center',
       bbox=dict(boxstyle='round', facecolor='purple', alpha=0.3))

# Anotaciones
ax.text(0.75, H - 2.5, 'Banda de Refinamiento\n[H-2h, H+2h]', 
       fontsize=12, fontweight='bold',
       bbox=dict(boxstyle='round', facecolor='#f39c12', alpha=0.7),
       ha='center')

# Flecha indicando ancho de banda [H-2h, H+2h]
ax.annotate('', xy=(time_steps + 0.5, H + 2.0), 
           xytext=(time_steps + 0.5, H - 2.0),
           arrowprops=dict(arrowstyle='<->', color='#f39c12', lw=3))
ax.text(time_steps, H + 2.25, '[H-2h,H+2h]', fontsize=10, 
       fontweight='bold', rotation=0, va='center', color='#f39c12')

# Configuración de ejes
ax.set_xlabel('Tiempo (pasos)', fontsize=13, fontweight='bold')
ax.set_ylabel('Nivel de Precio', fontsize=13, fontweight='bold')
ax.set_title('AMM para Opciones Barrera: Árbol Trinomial con Banda de Refinamiento', 
            fontsize=14, fontweight='bold', pad=15)

# Leyenda
legend_elements = [
    mpatches.Patch(color='#95a5a6', label='Nodos árbol grueso (h, k)', alpha=0.7),
    mpatches.Patch(color='#2ecc71', label='Nodos malla fina (h/2, k/4)'),
    mpatches.Patch(color='yellow', edgecolor='#f39c12', linewidth=2, 
                  linestyle='--', label='Banda de refinamiento', alpha=0.4),
    mpatches.Patch(color='#3498db', label=f'Barrera H={H}'),
    mpatches.Patch(color='gold', label=f'Precio inicial S₀={S0}'),
    mpatches.Patch(color='gray', label='Conexiones árbol trinomial', alpha=0.5)
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.9)

ax.set_xlim(-1, 11)
ax.set_ylim(H - 3.5, H + 3.5)
ax.grid(True, alpha=0.2, linestyle=':', zorder=0)

# Texto explicativo
textstr = ('Diferencia clave vs vanilla:\n'
          '• Refinamiento en TODO el tiempo\n'
          '• Banda vertical (no solo al vencimiento)\n'
          '• Flujo: gruesa → fina')
props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
ax.text(0.75, 0.1, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('../../code/03_metodos_valoracion/figures/amm_barrier.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("Figura 6 guardada: amm_barrier.png")
plt.close()
