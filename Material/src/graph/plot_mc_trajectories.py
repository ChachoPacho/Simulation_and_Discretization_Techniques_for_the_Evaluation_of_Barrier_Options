import os
import numpy as np
import matplotlib.pyplot as plt

def plot_20_trajectories():
    graph_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Parameters for Soybean Up-and-Out Call Option
    S0 = 200.0
    K = 200.0
    H = 220.0
    T = 1.0
    r = 0.05
    sigma = 0.15
    steps = 252
    iterations = 20
    
    dt = T / steps
    df = np.exp(-r * T)
    
    # Generate paths
    np.random.seed(15)  # Seed selected for a nice visual mix
    
    z = np.random.standard_normal((iterations, steps))
    log_returns = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
    cumulative_log_returns = np.cumsum(log_returns, axis=1)
    s_path = S0 * np.exp(np.hstack([np.zeros((iterations, 1)), cumulative_log_returns]))
    
    time_grid = np.linspace(0, T, steps + 1)
    
    plt.figure(figsize=(10, 6))
    
    payoffs = []
    
    red_label_added = False
    green_label_added = False
    gray_label_added = False
    
    for i in range(iterations):
        path = s_path[i]
        touches_H = np.any(path >= H)
        
        if touches_H:
            # Red: touches H
            if not red_label_added:
                plt.plot(time_grid, path, color='red', alpha=0.7, label='Toca la barrera H (Roja)')
                red_label_added = True
            else:
                plt.plot(time_grid, path, color='red', alpha=0.7)
            payoffs.append(0.0)
        else:
            payoff = max(path[-1] - K, 0)
            if payoff > 0:
                # Green: doesn't touch H and pays
                if not green_label_added:
                    plt.plot(time_grid, path, color='green', alpha=0.7, label='NO toca H y paga la opción (Verde)')
                    green_label_added = True
                else:
                    plt.plot(time_grid, path, color='green', alpha=0.7)
                payoffs.append(payoff)
            else:
                # Doesn't touch H but doesn't pay
                if not gray_label_added:
                    plt.plot(time_grid, path, color='gray', alpha=0.4, label='NO toca H pero no paga (S_T <= K)')
                    gray_label_added = True
                else:
                    plt.plot(time_grid, path, color='gray', alpha=0.4)
                payoffs.append(0.0)
                
    # Final value: average of discounted payoffs
    avg_payoff_discounted = np.mean(payoffs) * df
    
    plt.axhline(H, color='black', linestyle='--', linewidth=2, label=f'Barrera (H = ${H})')
    plt.axhline(K, color='blue', linestyle=':', linewidth=1.5, label=f'Strike (K = ${K})')
    
    plt.title(f'20 Trayectorias Simuladas del Precio de la Soja\nValor final (promedio de payoffs descontado): ${avg_payoff_discounted:.4f}', fontsize=14)
    plt.xlabel('Tiempo hasta Vencimiento (T)', fontsize=12)
    plt.ylabel('Precio de la Soja ($)', fontsize=12)
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    output_path = os.path.join(graph_dir, 'mc_20_trayectorias_soja.png')
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print(f"Gráfico guardado en: {output_path}")

if __name__ == '__main__':
    plot_20_trajectories()
