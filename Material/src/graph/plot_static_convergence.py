import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Añadir el path base para poder importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from static.static import static_portfolio
from rr.rr import rubison_reiner

def plot_static_convergence():
    graph_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Parámetros del caso solicitado
    S0 = 300
    K = 260
    T = 0.5
    r = 0.05
    d = 0
    sigma = 0.2
    H = 220
    
    # Down-and-In Put
    isCall = True
    isDown = True
    isIn = False
    
    print("Calculando valor base con Reiner-Rubinstein...")
    try:
        rr_val = rubison_reiner(S0, K, H, T, r, d, sigma, 0, isCall=isCall, isDown=isDown, isIn=isIn)
        print(f"Valor RR (Down-and-In Put): {rr_val:.6f}")
    except Exception as e:
        print(f"Error calculando RR: {e}")
        return
        
    N_start = 6
    step = 3
    iterations = 12
    N_end = N_start + step * iterations
    
    # Rango de N (desde N_start hasta N_end)
    N_list = list(range(N_start, N_end + 1, step))
    errors = []
    valid_N = []
    
    print(f"Simulando portafolios estáticos para N={N_start} hasta N={N_end}...")
    for n in N_list:
        print(n)
        try:
            stat_val, _ = static_portfolio(S0, K, H, T, r, d, sigma, n, isCall=isCall, isDown=isDown, isIn=isIn)
            
            if rr_val > 1e-6:
                err = abs(stat_val - rr_val) / rr_val * 100
                errors.append(err)
                valid_N.append(n)
        except Exception:
            # Si para algún N falla la matemática (ej. division by zero), lo omitimos del gráfico
            pass

    # Crear el gráfico
    plt.figure(figsize=(11, 6))
    
    # Dibujar la línea de error
    plt.plot(valid_N, errors, color='darkmagenta', linewidth=2, marker='.', markersize=6, alpha=0.8, label='Error Relativo (%)')
    
    plt.title(f"Evolución del Error: Replicación Estática vs Reiner-Rubinstein\n(Opción {'Down' if isDown else 'Up'}-and-{'In' if isIn else 'Out'} {'Call' if isCall else 'Put'})", fontsize=14)
    plt.xlabel('Cantidad de Opciones de Ajuste (N)', fontsize=12)
    plt.ylabel('Error Relativo (%)', fontsize=12)
    
    # Decoración
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.3)
    
    # Ajustar vista para ver por encima de y=0
    plt.ylim(bottom=0)
    
    # Escala logarítmica si el error oscila masivamente, pero en porcentaje lineal a veces se aprecia mejor la convergencia.
    # Si detectamos valores enormes, aplicamos escala logarítmica
    # if max(errors) > 50:
    #     plt.yscale('symlog')
    #     plt.ylabel('Error Relativo (%) - Escala Logarítmica', fontsize=12)
    
    plt.legend(fontsize=11)
    plt.tight_layout()
    
    # Guardar
    output_path = os.path.join(graph_dir, 'static_convergence_dip.png')
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print("=" * 60)
    print(f"Gráfico generado correctamente en:\n{output_path}")
    print("=" * 60)

if __name__ == '__main__':
    plot_static_convergence()
