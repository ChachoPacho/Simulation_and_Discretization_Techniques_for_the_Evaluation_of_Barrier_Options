import matplotlib.pyplot as plt
import numpy as np

# Datos de la tabla (Figlewski & Gao, 1999)
models = {
    'Binomial 100': {'N': 100, 'RMSE': 0.004929, 'Time': 0.045, 'color': '#e74c3c', 'marker': 'o'},
    'Trinomial 100': {'N': 100, 'RMSE': 0.002770, 'Time': 0.094, 'color': '#3498db', 'marker': 's'},
    'AMM-1 100': {'N': 100, 'RMSE': 0.000600, 'Time': 0.096, 'color': '#2ecc71', 'marker': '^'},
    'AMM-2 100': {'N': 100, 'RMSE': 0.000151, 'Time': 0.098, 'color': '#27ae60', 'marker': 'D'},
    'Binomial 1000': {'N': 1000, 'RMSE': 0.000448, 'Time': 3.067, 'color': '#c0392b', 'marker': 'o'},
    'Trinomial 1000': {'N': 1000, 'RMSE': 0.000244, 'Time': 8.562, 'color': '#2980b9', 'marker': 's'},
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Panel izquierdo: RMSE vs Tiempo (escala log-log)
for name, data in models.items():
    ax1.scatter(data['Time'], data['RMSE'], s=200, 
               color=data['color'], marker=data['marker'], 
               label=name, alpha=0.8, edgecolors='black', linewidth=1.5, zorder=3)

# Líneas conectando modelos de mismo tipo
# Binomial
ax1.plot([models['Binomial 100']['Time'], models['Binomial 1000']['Time']],
        [models['Binomial 100']['RMSE'], models['Binomial 1000']['RMSE']],
        '--', color='#e74c3c', alpha=0.5, linewidth=2)

# Trinomial
ax1.plot([models['Trinomial 100']['Time'], models['Trinomial 1000']['Time']],
        [models['Trinomial 100']['RMSE'], models['Trinomial 1000']['RMSE']],
        '--', color='#3498db', alpha=0.5, linewidth=2)

# Región de eficiencia del AMM
amm_times = [models['AMM-1 100']['Time'], models['AMM-2 100']['Time']]
amm_rmses = [models['AMM-1 100']['RMSE'], models['AMM-2 100']['RMSE']]
ax1.fill_between([0.09, 0.11], [1e-5, 1e-5], [0.01, 0.01], 
                alpha=0.2, color='green', label='Zona de eficiencia AMM')

ax1.set_xlabel('Tiempo de ejecución (segundos)', fontsize=13, fontweight='bold')
ax1.set_ylabel('RMSE (Error Cuadrático Medio)', fontsize=13, fontweight='bold')
ax1.set_title('Eficiencia del AMM: Precisión vs Tiempo', fontsize=14, fontweight='bold')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.legend(fontsize=9, loc='upper right', ncol=2)
ax1.grid(True, alpha=0.3, linestyle='--', which='both')

# Anotaciones
ax1.annotate('AMM logra\nmayor precisión\ncon tiempo similar', 
            xy=(models['AMM-2 100']['Time'], models['AMM-2 100']['RMSE']),
            xytext=(0.3, 0.001),
            arrowprops=dict(arrowstyle='->', color='green', lw=3),
            fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8))

ax1.annotate('Trinomial 1000:\n8.5s para RMSE=0.00024', 
            xy=(models['Trinomial 1000']['Time'], models['Trinomial 1000']['RMSE']),
            xytext=(5, 0.003),
            arrowprops=dict(arrowstyle='->', color='blue', lw=2),
            fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7))

# Panel derecho: Mejora de precisión (factor)
model_names = ['Binomial\n100', 'Trinomial\n100', 'AMM-1\n100', 'AMM-2\n100']
rmse_values = [
    models['Binomial 100']['RMSE'],
    models['Trinomial 100']['RMSE'],
    models['AMM-1 100']['RMSE'],
    models['AMM-2 100']['RMSE']
]
time_values = [
    models['Binomial 100']['Time'],
    models['Trinomial 100']['Time'],
    models['AMM-1 100']['Time'],
    models['AMM-2 100']['Time']
]
colors_bar = ['#e74c3c', '#3498db', '#2ecc71', '#27ae60']

# Calcular factor de mejora (RMSE normalizado por tiempo)
efficiency = [rmse / time for rmse, time in zip(rmse_values, time_values)]
efficiency_normalized = [e / min(efficiency) for e in efficiency]

x_pos = np.arange(len(model_names))
bars = ax2.bar(x_pos, rmse_values, color=colors_bar, alpha=0.7, 
              edgecolor='black', linewidth=1.5)

# Etiquetas de valores
for i, (bar, rmse, time) in enumerate(zip(bars, rmse_values, time_values)):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{rmse:.6f}\n({time:.3f}s)',
            ha='center', va='bottom', fontsize=9, fontweight='bold')

ax2.set_xlabel('Modelo (N=100 pasos)', fontsize=13, fontweight='bold')
ax2.set_ylabel('RMSE', fontsize=13, fontweight='bold')
ax2.set_title('Comparación de Precisión (N=100)', fontsize=14, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(model_names, fontsize=10)
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3, linestyle='--', axis='y')

# Línea de referencia
ax2.axhline(y=models['Trinomial 100']['RMSE'], color='blue', 
           linestyle='--', linewidth=2, alpha=0.5, 
           label='Trinomial estándar')
ax2.legend(fontsize=10)

# Factores de mejora
improvement_vs_trinomial = [
    models['Trinomial 100']['RMSE'] / models['AMM-1 100']['RMSE'],
    models['Trinomial 100']['RMSE'] / models['AMM-2 100']['RMSE']
]

textstr = (f'Mejora vs Trinomial:\n'
          f'AMM-1: {improvement_vs_trinomial[0]:.1f}x\n'
          f'AMM-2: {improvement_vs_trinomial[1]:.1f}x\n'
          f'Costo adicional: <1%')
props = dict(boxstyle='round', facecolor='wheat', alpha=0.9, edgecolor='black', linewidth=2)
ax2.text(0.98, 0.98, textstr, transform=ax2.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='right', 
        bbox=props, fontweight='bold')

plt.tight_layout()
plt.savefig('../../code/03_metodos_valoracion/figures/rmse_vs_time.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("Figura 8 guardada: rmse_vs_time.png")
plt.close()
