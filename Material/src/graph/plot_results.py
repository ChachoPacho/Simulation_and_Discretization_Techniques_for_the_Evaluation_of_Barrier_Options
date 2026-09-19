import json
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_results():
    # Ruta al archivo JSON
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'results_all.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        results = json.load(f)

    names = [r['name'] for r in results]
    
    # ==============================================================================
    # 1. Gráfico de Errores Absolutos respecto a Reiner-Rubinstein
    # ==============================================================================
    amm_err = []
    amm1_err = []
    amm2_err = []
    static6_err = []
    static12_err = []
    static24_err = []
    
    for r in results:
        rr = r['rr']
        if rr is not None:
            # Reemplazamos errores exactamente iguales a 0 por 1e-15 para poder graficar en escala logarítmica
            amm_err.append(max(abs(r['amm'][0] - rr), 1e-15))
            amm1_err.append(max(abs(r['amm'][1] - rr), 1e-15))
            amm2_err.append(max(abs(r['amm'][2] - rr), 1e-15))
            static6_err.append(max(abs(r['static'][0] - rr), 1e-15))
            static12_err.append(max(abs(r['static'][1] - rr), 1e-15))
            static24_err.append(max(abs(r['static'][2] - rr), 1e-15))
        else:
            amm_err.append(float('nan'))
            amm1_err.append(float('nan'))
            amm2_err.append(float('nan'))
            static6_err.append(float('nan'))
            static12_err.append(float('nan'))
            static24_err.append(float('nan'))

    x = np.arange(len(names))
    width = 0.12
    
    plt.figure(figsize=(16, 7))
    plt.bar(x - 2.5*width, amm_err, width, label='AMM', color='#1f77b4')
    plt.bar(x - 1.5*width, amm1_err, width, label='AMM-1', color='#ff7f0e')
    plt.bar(x - 0.5*width, amm2_err, width, label='AMM-2', color='#2ca02c')
    plt.bar(x + 0.5*width, static6_err, width, label='Static-6', color='#d62728')
    plt.bar(x + 1.5*width, static12_err, width, label='Static-12', color='#9467bd')
    plt.bar(x + 2.5*width, static24_err, width, label='Static-24', color='#8c564b')
    
    plt.yscale('log')
    plt.ylabel('Error Absoluto (Escala Logarítmica)')
    plt.title('Diferencia Absoluta respecto al método de Reiner-Rubinstein')
    plt.xticks(x, names, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), 'errores_absolutos.png'))
    plt.close()

    # ==============================================================================
    # 2. Gráfico de Tiempos de Ejecución
    # ==============================================================================
    time_rr = []
    time_amm = []
    time_amm1 = []
    time_amm2 = []
    time_static6 = []
    time_static12 = []
    time_static24 = []

    for r in results:
        time_rr.append(max(r['time_rr'], 1e-6))
        time_amm.append(max(r['time_amm'][0], 1e-6))
        time_amm1.append(max(r['time_amm'][1], 1e-6))
        time_amm2.append(max(r['time_amm'][2], 1e-6))
        time_static6.append(max(r['time_static'][0], 1e-6))
        time_static12.append(max(r['time_static'][1], 1e-6))
        time_static24.append(max(r['time_static'][2], 1e-6))

    plt.figure(figsize=(16, 7))
    width_time = 0.12
    plt.bar(x - 3*width_time, time_rr, width_time, label='Reiner-Rubinstein', color='#e377c2')
    plt.bar(x - 2*width_time, time_amm, width_time, label='AMM', color='#1f77b4')
    plt.bar(x - 1*width_time, time_amm1, width_time, label='AMM-1', color='#ff7f0e')
    plt.bar(x, time_amm2, width_time, label='AMM-2', color='#2ca02c')
    plt.bar(x + 1*width_time, time_static6, width_time, label='Static-6', color='#d62728')
    plt.bar(x + 2*width_time, time_static12, width_time, label='Static-12', color='#9467bd')
    plt.bar(x + 3*width_time, time_static24, width_time, label='Static-24', color='#8c564b')

    plt.yscale('log')
    plt.ylabel('Tiempo de Ejecución en segundos (Escala Logarítmica)')
    plt.title('Tiempos de Ejecución por Método')
    plt.xticks(x, names, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), 'tiempos_ejecucion.png'))
    plt.close()

    print("Gráficos generados correctamente en el directorio:", os.path.dirname(__file__))
    print("- errores_absolutos.png")
    print("- tiempos_ejecucion.png")

if __name__ == "__main__":
    plot_results()
