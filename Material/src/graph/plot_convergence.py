import matplotlib.pyplot as plt
import numpy as np
import os

def plot_convergence():
    # Asegurar que guardamos en src/graph
    graph_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Datos extraídos de la tabla LaTeX
    N = [25, 100, 250, 1000]
    
    # RMSE para el Precio
    rmse_binomial = [0.020841, 0.004929, 0.002214, 0.000448]
    rmse_trinomial = [0.012025, 0.002770, 0.001360, 0.000244]
    rmse_amm1 = [0.002812, 0.000600, 0.000245, 0.000056]
    rmse_amm2 = [0.000615, 0.000151, 0.000057, 0.000016]
    
    # Tiempos de ejecución (segundos)
    time_binomial = [0.0060, 0.0451, 0.2163, 3.0674]
    time_trinomial = [0.0090, 0.0941, 0.5407, 8.5623]
    time_amm1 = [0.0117, 0.0961, 0.5418, 8.5954]
    time_amm2 = [0.0121, 0.0982, 0.5428, 8.5854]

    # =========================================================================
    # Gráfico 1: Convergencia de Error (RMSE) vs Pasos (N)
    # =========================================================================
    plt.figure(figsize=(10, 6))
    plt.plot(N, rmse_binomial, marker='o', label='Binomial', linewidth=2.5, markersize=8, color='#1f77b4')
    plt.plot(N, rmse_trinomial, marker='s', label='Trinomial', linewidth=2.5, markersize=8, color='#ff7f0e')
    plt.plot(N, rmse_amm1, marker='^', label='AMM-1', linewidth=2.5, markersize=8, color='#2ca02c')
    plt.plot(N, rmse_amm2, marker='d', label='AMM-2', linewidth=2.5, markersize=8, color='#d62728')
    
    plt.xscale('log')
    plt.yscale('log')
    
    plt.title('Convergencia del Error (RMSE) según Número de Pasos (N)', fontsize=14)
    plt.xlabel('Número de Pasos (N) - Escala Logarítmica', fontsize=12)
    plt.ylabel('RMSE de Precio - Escala Logarítmica', fontsize=12)
    
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'convergence_rmse_vs_N.png'), dpi=300)
    plt.close()
    
    # =========================================================================
    # Gráfico 2: Eficiencia Computacional (RMSE vs Tiempo)
    # =========================================================================
    # Este gráfico es vital para mostrar que AMM-2 es mejor no solo en pasos, 
    # sino también que vale la pena el pequeño overhead de tiempo.
    plt.figure(figsize=(10, 6))
    plt.plot(time_binomial, rmse_binomial, marker='o', label='Binomial', linewidth=2.5, markersize=8, color='#1f77b4')
    plt.plot(time_trinomial, rmse_trinomial, marker='s', label='Trinomial', linewidth=2.5, markersize=8, color='#ff7f0e')
    plt.plot(time_amm1, rmse_amm1, marker='^', label='AMM-1', linewidth=2.5, markersize=8, color='#2ca02c')
    plt.plot(time_amm2, rmse_amm2, marker='d', label='AMM-2', linewidth=2.5, markersize=8, color='#d62728')
    
    plt.xscale('log')
    plt.yscale('log')
    
    plt.title('Eficiencia Computacional: RMSE vs Tiempo de Ejecución', fontsize=14)
    plt.xlabel('Tiempo de Ejecución en segundos (s) - Escala Logarítmica', fontsize=12)
    plt.ylabel('RMSE de Precio - Escala Logarítmica', fontsize=12)
    
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(fontsize=11)
    
    # Anotar algunos puntos de N para dar contexto visual de en qué momento de la curva estamos
    for i, n in enumerate(N):
        if i == 0 or i == len(N) - 1: # Anotar solo extremos para no saturar
            plt.annotate(f'N={n}', (time_binomial[i], rmse_binomial[i]), textcoords="offset points", xytext=(-15,-10), ha='center', fontsize=10, color='#1f77b4')
            plt.annotate(f'N={n}', (time_amm2[i], rmse_amm2[i]), textcoords="offset points", xytext=(15,-10), ha='center', fontsize=10, color='#d62728')

    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'convergence_efficiency.png'), dpi=300)
    plt.close()
    
    print("==================================================")
    print("Gráficos de convergencia generados en src/graph/")
    print("- convergence_rmse_vs_N.png")
    print("- convergence_efficiency.png")
    print("==================================================")

if __name__ == '__main__':
    plot_convergence()
