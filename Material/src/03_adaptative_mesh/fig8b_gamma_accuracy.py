import matplotlib.pyplot as plt
import numpy as np

# Datos de la tabla extendida (Figlewski & Gao, 1999)
# AMM level: (t0, t1) donde t0 es nivel en región crítica, t1 es nivel en precio inicial
data = {
    25: {
        'Trinomial (0,0)': {'price': 0.012025, 'delta': 0.003337, 'gamma': 0.000428, 'time': 0.0090},
        'AMM (1,0)': {'price': 0.012025, 'delta': 0.001087, 'gamma': 0.000333, 'time': 0.0090},
        'AMM (2,0)': {'price': 0.011909, 'delta': 0.000810, 'gamma': 0.000400, 'time': 0.0090},
        'AMM (1,1)': {'price': 0.002812, 'delta': 0.000845, 'gamma': 0.000080, 'time': 0.0120},
        'AMM (2,2)': {'price': 0.000596, 'delta': 0.000205, 'gamma': 0.000113, 'time': 0.0131},
        'AMM (3,3)': {'price': 0.000193, 'delta': 0.000053, 'gamma': 0.000120, 'time': 0.0140},
    },
    100: {
        'Trinomial (0,0)': {'price': 0.002770, 'delta': 0.000846, 'gamma': 0.000144, 'time': 0.0931},
        'AMM (1,0)': {'price': 0.002770, 'delta': 0.000265, 'gamma': 0.000068, 'time': 0.0922},
        'AMM (2,0)': {'price': 0.002764, 'delta': 0.000188, 'gamma': 0.000077, 'time': 0.0931},
        'AMM (1,1)': {'price': 0.000600, 'delta': 0.000210, 'gamma': 0.000020, 'time': 0.0942},
        'AMM (2,2)': {'price': 0.000153, 'delta': 0.000056, 'gamma': 0.000028, 'time': 0.0971},
        'AMM (3,3)': {'price': 0.000043, 'delta': 0.000014, 'gamma': 0.000027, 'time': 0.0991},
    },
    250: {
        'Trinomial (0,0)': {'price': 0.001360, 'delta': 0.000346, 'gamma': 0.000061, 'time': 0.5358},
        'AMM (1,0)': {'price': 0.001360, 'delta': 0.000115, 'gamma': 0.000029, 'time': 0.5288},
        'AMM (2,0)': {'price': 0.001350, 'delta': 0.000085, 'gamma': 0.000031, 'time': 0.5287},
        'AMM (1,1)': {'price': 0.000245, 'delta': 0.000079, 'gamma': 0.000006, 'time': 0.5308},
        'AMM (2,2)': {'price': 0.000057, 'delta': 0.000023, 'gamma': 0.000010, 'time': 0.5878},
        'AMM (3,3)': {'price': 0.000019, 'delta': 0.000005, 'gamma': 0.000011, 'time': 0.5738},
    },
    1000: {
        'Trinomial (0,0)': {'price': 0.000244, 'delta': 0.000079, 'gamma': 0.000015, 'time': 8.5072},
        'AMM (1,0)': {'price': 0.000244, 'delta': 0.000021, 'gamma': 0.000006, 'time': 8.3711},
        'AMM (2,0)': {'price': 0.000243, 'delta': 0.000016, 'gamma': 0.000007, 'time': 8.3640},
        'AMM (1,1)': {'price': 0.000056, 'delta': 0.000023, 'gamma': 0.000002, 'time': 8.3170},
        'AMM (2,2)': {'price': 0.000016, 'delta': 0.000005, 'gamma': 0.000003, 'time': 8.3130},
        'AMM (3,3)': {'price': 0.000006, 'delta': 0.000001, 'gamma': 0.000003, 'time': 8.3751},
    }
}

# Configuración de colores y marcadores
colors = {
    'Trinomial (0,0)': '#3498db',
    'AMM (1,0)': '#95a5a6',
    'AMM (2,0)': '#7f8c8d',
    'AMM (1,1)': '#2ecc71',
    'AMM (2,2)': '#27ae60',
    'AMM (3,3)': '#16a085',
}
markers = {
    'Trinomial (0,0)': 's',
    'AMM (1,0)': 'o',
    'AMM (2,0)': 'o',
    'AMM (1,1)': '^',
    'AMM (2,2)': 'D',
    'AMM (3,3)': 'p',
}

fig, ax = plt.subplots(figsize=(14, 9))

steps = [25, 100, 250, 1000]

# Graficar cada configuración
for config_name in ['Trinomial (0,0)', 'AMM (1,1)', 'AMM (2,2)', 'AMM (3,3)']:
    gamma_rmse = [data[n][config_name]['gamma'] for n in steps]
    
    ax.plot(steps, gamma_rmse, marker=markers[config_name], markersize=14,
           linewidth=3, label=config_name, color=colors[config_name],
           alpha=0.85, markeredgecolor='black', markeredgewidth=1.5)

# Configuración del gráfico
ax.set_xlabel('Número de Pasos Temporales (N)', fontsize=15, fontweight='bold')
ax.set_ylabel('RMSE en Gamma (Γ)', fontsize=15, fontweight='bold')
ax.set_title('Precisión en el Cálculo de Gamma: Trinomial vs AMM con Ramificación Cuadrinomial', 
            fontsize=17, fontweight='bold', pad=20)

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xticks(steps)
ax.set_xticklabels(steps, fontsize=12)
ax.tick_params(axis='y', labelsize=11)
ax.grid(True, alpha=0.3, linestyle='--', which='both')
ax.legend(fontsize=13, loc='upper right', framealpha=0.95, edgecolor='black',
         title='Configuración (t₀, t₁)', title_fontsize=12)

# Anotaciones de mejora
# N=100
trinomial_gamma_100 = data[100]['Trinomial (0,0)']['gamma']
amm11_gamma_100 = data[100]['AMM (1,1)']['gamma']
improvement_100 = trinomial_gamma_100 / amm11_gamma_100

ax.annotate('', xy=(100, amm11_gamma_100), 
           xytext=(100, trinomial_gamma_100),
           arrowprops=dict(arrowstyle='<->', color='green', lw=3))
ax.text(120, 0.000050, f'Mejora\n{improvement_100:.1f}x', 
       fontsize=12, fontweight='bold', color='green',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', 
                edgecolor='darkgreen', linewidth=2, alpha=0.9))

# N=250
trinomial_gamma_250 = data[250]['Trinomial (0,0)']['gamma']
amm11_gamma_250 = data[250]['AMM (1,1)']['gamma']
improvement_250 = trinomial_gamma_250 / amm11_gamma_250

ax.text(300, 0.000030, f'Mejora {improvement_250:.1f}x\ncon AMM (1,1)', 
       fontsize=11, fontweight='bold', color='darkgreen',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', 
                edgecolor='darkgreen', linewidth=2, alpha=0.9))

plt.tight_layout()
plt.savefig('../../code/03_metodos_valoracion/figures/gamma_accuracy_comparison.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("Figura 8b guardada: gamma_accuracy_comparison.png")
plt.close()
