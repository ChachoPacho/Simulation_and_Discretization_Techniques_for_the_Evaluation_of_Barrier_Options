import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

# Añadir el path base para poder importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mc.mc import monte_carlo_lsm_barrier

def plot_mc_convergence():
    graph_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Parámetros
    S0 = 300
    K = 260
    T = 0.5
    r = 0.05
    d = 0
    sigma = 0.2
    H = 220
    
    # Down-and-Out Call
    isCall = False
    isDown = True
    isIn = True
    
    # Iteraciones a evaluar (en escala logarítmica)
    # Desde 1,000 hasta 200,000 iteraciones
    iterations_list = np.logspace(3, 6, 30).astype(int)
    
    mc_values = []
    mc_errors = []
    mc_times = []
    
    print("Simulando Monte Carlo (Longstaff-Schwartz) para medir convergencia...")
    for iters in iterations_list:
        print(f"  - Simulando {iters:>7,} iteraciones...")
        # Nota: isUp es lo opuesto a isDown
        t0 = time.time()
        val, std = monte_carlo_lsm_barrier(S0, K, H, T, r, sigma, delta=d, 
                                           iterations=iters, steps=100, 
                                           isCall=isCall, isUp=(not isDown), isIn=isIn)
        t1 = time.time()
        
        # Error estándar de la media (SE = Desviación Estándar / sqrt(N))
        se = std / np.sqrt(iters) 
        mc_values.append(val)
        mc_errors.append(se)
        mc_times.append(t1 - t0)

    mc_values = np.array(mc_values)
    mc_errors = np.array(mc_errors)
    
    # Crear gráfico
    plt.figure(figsize=(11, 6))
    
    # 2. Línea de Monte Carlo
    plt.plot(iterations_list, mc_values, color='#1f77b4', linewidth=2, marker='o', markersize=6, label='Valor Monte Carlo (Media)')
    
    # 3. Intervalo de Confianza del 95% (+/- 1.96 SE)
    ci_upper = mc_values + 1.96 * mc_errors
    ci_lower = mc_values - 1.96 * mc_errors
    
    plt.fill_between(iterations_list, ci_lower, ci_upper, color='#1f77b4', alpha=0.2, label='Intervalo de Confianza 95%')
    
    plt.xscale('log')
    plt.title(f"Convergencia del Método de Monte Carlo\n(Opción {'Down' if isDown else 'Up'}-and-{'In' if isIn else 'Out'} {'Call' if isCall else 'Put'})", fontsize=14)
    plt.xlabel('Número de Iteraciones o Trayectorias (N) - Escala Logarítmica', fontsize=12)
    plt.ylabel('Precio Estimado de la Opción ($)', fontsize=12)
    
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend(loc='best', fontsize=11)
    plt.tight_layout()
    
    output_path = os.path.join(graph_dir, 'mc_convergence.png')
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    # --- Gráfico de Error de Monte Carlo ---
    plt.figure(figsize=(11, 6))
    
    plt.plot(iterations_list, mc_errors, color='#d62728', linewidth=2, marker='s', markersize=5, label='Error Estándar (SE)')
    
    # Línea de referencia O(1/sqrt(N)) ajustada al primer punto para visualizar convergencia teórica
    ref_errors = mc_errors[0] * np.sqrt(iterations_list[0]) / np.sqrt(iterations_list)
    plt.plot(iterations_list, ref_errors, color='black', linestyle=':', linewidth=2, label='Referencia $O(1/\sqrt{N})$')
    
    plt.xscale('log')
    plt.yscale('log')
    plt.title(f"Convergencia del Error de Monte Carlo\n(Opción {'Down' if isDown else 'Up'}-and-{'In' if isIn else 'Out'} {'Call' if isCall else 'Put'})", fontsize=14)
    plt.xlabel('Número de Iteraciones o Trayectorias (N) - Escala Logarítmica', fontsize=12)
    plt.ylabel('Error Estándar (SE) - Escala Logarítmica', fontsize=12)
    
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend(loc='best', fontsize=11)
    plt.tight_layout()
    
    output_error_path = os.path.join(graph_dir, 'mc_convergence_error.png')
    plt.savefig(output_error_path, dpi=300)
    plt.close()
    
    print("=" * 70)
    print(f"Gráfico de convergencia MC generado correctamente en:\n{output_path}")
    print(f"Gráfico de error MC generado correctamente en:\n{output_error_path}")
    print("=" * 70)
    
    # --- Gráfico de Tiempo de Procesamiento ---
    plt.figure(figsize=(11, 6))
    
    plt.plot(iterations_list, mc_times, color='#2ca02c', linewidth=2, marker='^', markersize=6, label='Tiempo de Ejecución')
    
    plt.xscale('log')
    plt.yscale('log')
    plt.title(f"Tiempo de Procesamiento de Monte Carlo\n(Opción {'Down' if isDown else 'Up'}-and-{'In' if isIn else 'Out'} {'Call' if isCall else 'Put'})", fontsize=14)
    plt.xlabel('Número de Iteraciones o Trayectorias (N) - Escala Logarítmica', fontsize=12)
    plt.ylabel('Tiempo de Procesamiento (Segundos) - Escala Logarítmica', fontsize=12)
    
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend(loc='best', fontsize=11)
    plt.tight_layout()
    
    output_time_path = os.path.join(graph_dir, 'mc_convergence_time.png')
    plt.savefig(output_time_path, dpi=300)
    plt.close()
    
    print("=" * 70)
    print(f"Gráfico de tiempo MC generado correctamente en:\n{output_time_path}")
    print("=" * 70)

if __name__ == '__main__':
    plot_mc_convergence()
