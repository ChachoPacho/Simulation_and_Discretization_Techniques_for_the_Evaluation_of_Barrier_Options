import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# Parámetros de la opción (mismo caso que fig2a)
S0 = 100.0
K = 100.0
T = 1.0
r = 0.05
sigma = 0.2
option_type = 'put'

# Valor teórico Black-Scholes
def black_scholes_put(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

BS_value = black_scholes_put(S0, K, T, r, sigma)

# Modelo Binomial
def binomial_tree(S0, K, T, r, sigma, N, option_type='put'):
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    
    ST = np.array([S0 * (u**j) * (d**(N-j)) for j in range(N+1)])
    
    if option_type == 'put':
        V = np.maximum(K - ST, 0)
    else:
        V = np.maximum(ST - K, 0)
    
    for i in range(N-1, -1, -1):
        V = np.exp(-r * dt) * (p * V[1:] + (1-p) * V[:-1])
    
    return V[0]

# Calcular errores para rango más detallado
N_values = np.arange(10, 101, 1)  # Paso de 1 para ver bien el efecto
errors_binomial = []

print("Calculando efecto par-impar...")
for N in N_values:
    val_bin = binomial_tree(S0, K, T, r, sigma, N, option_type)
    errors_binomial.append(abs(val_bin - BS_value))

# Separar pares e impares
N_par = N_values[N_values % 2 == 0]
N_impar = N_values[N_values % 2 == 1]
error_par = [errors_binomial[i] for i in range(len(N_values)) if N_values[i] % 2 == 0]
error_impar = [errors_binomial[i] for i in range(len(N_values)) if N_values[i] % 2 == 1]

# Crear figura
fig, ax = plt.subplots(figsize=(12, 7))

# Gráfico principal
ax.plot(N_values, errors_binomial, '-', color='#e74c3c', linewidth=1.5, 
         alpha=0.5, label='Binomial (todos los N)')

# Destacar pares e impares
ax.scatter(N_par, error_par, s=100, color='blue', marker='o', 
           label='N par (menor error)', zorder=5, alpha=0.7, edgecolors='black', linewidth=1.5)
ax.scatter(N_impar, error_impar, s=100, color='red', marker='s', 
           label='N impar (mayor error)', zorder=5, alpha=0.7, edgecolors='black', linewidth=1.5)

# Líneas de tendencia (ajuste potencial)
# Para N par
log_N_par = np.log(N_par)
log_error_par = np.log(error_par)
z_par = np.polyfit(log_N_par, log_error_par, 1)
trend_par = np.exp(z_par[1]) * N_par ** z_par[0]
ax.plot(N_par, trend_par, '--', color='blue', linewidth=2.5, alpha=0.6, 
        label=f'Tendencia par: $N^{{{z_par[0]:.2f}}}$')

# Para N impar
log_N_impar = np.log(N_impar)
log_error_impar = np.log(error_impar)
z_impar = np.polyfit(log_N_impar, log_error_impar, 1)
trend_impar = np.exp(z_impar[1]) * N_impar ** z_impar[0]
ax.plot(N_impar, trend_impar, '--', color='red', linewidth=2.5, alpha=0.6, 
        label=f'Tendencia impar: $N^{{{z_impar[0]:.2f}}}$')

ax.set_xlabel('Número de pasos (N)', fontsize=13, fontweight='bold')
ax.set_ylabel('Error absoluto', fontsize=13, fontweight='bold')
ax.set_title(f'Detalle: Efecto Par-Impar en Binomial (Put: S={S0}, K={K}, σ={sigma})', 
            fontsize=14, fontweight='bold')
ax.legend(fontsize=10, loc='upper right')
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_yscale('log')

# Destacar algunas oscilaciones específicas
for i in [20, 40, 60]:
    idx = np.where(N_values == i)[0][0]
    idx_next = np.where(N_values == i+1)[0][0]
    ax.annotate('', xy=(N_values[idx_next], errors_binomial[idx_next]), 
                xytext=(N_values[idx], errors_binomial[idx]),
                arrowprops=dict(arrowstyle='<->', color='orange', lw=2, alpha=0.6))

# Anotación explicativa
ax.text(30, errors_binomial[20]*1.5, 'Oscilaciones\npar-impar', 
        fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))

# Texto explicativo
textstr = (f'Valor BS: {BS_value:.6f}\n'
          f'Error promedio (par): {np.mean(error_par):.6f}\n'
          f'Error promedio (impar): {np.mean(error_impar):.6f}\n'
          f'Ratio impar/par: {np.mean(error_impar)/np.mean(error_par):.2f}x')
props = dict(boxstyle='round', facecolor='wheat', alpha=0.9, edgecolor='black', linewidth=2)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, fontweight='bold')

plt.tight_layout()
plt.savefig('../../../code/03_metodos_valoracion/figures/par_impar_detail.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("Figura 2b guardada: par_impar_detail.png")
plt.close()
