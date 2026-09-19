import os
import sys
import json
import random
import numpy as np
import matplotlib.pyplot as plt

# Añadir el path base para poder importar los módulos (bs y rr)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bs.bs import black_scholes
from rr.rr import rubison_reiner

def generate_random_params(is_down):
    """
    Genera un conjunto de parámetros aleatorios para el testeo
    """
    S0 = 100.0
    K = random.uniform(80.0, 120.0)
    T = random.uniform(0.25, 2.0)
    r = random.uniform(0.01, 0.10)
    sigma = random.uniform(0.10, 0.50)
    d = 0.0 # Tasa de dividendos en 0 para simplificar
    
    if is_down:
        H = random.uniform(70.0, 99.0)
    else:
        H = random.uniform(101.0, 130.0)
        
    is_call = random.choice([True, False])
    is_in = random.choice([True, False])
    
    return S0, K, T, r, sigma, d, H, is_call, is_in

def run_simulations(n_samples=1000):
    print(f"Generando {n_samples} muestras para opciones Down y {n_samples} para opciones Up...")
    
    results = {'Down': [], 'Up': []}
    
    for group, is_down in [('Down', True), ('Up', False)]:
        samples_collected = 0
        while samples_collected < n_samples:
            S0, K, T, r, sigma, d, H, is_call, is_in = generate_random_params(is_down)
            
            # Calcular valor Vanilla (referencia)
            option_type = 'call' if is_call else 'put'
            try:
                vanilla = black_scholes(S0, K, T, r, d, sigma, option_type=option_type)
            except Exception:
                continue
                
            # Calcular valor con modelo de Reiner-Rubinstein
            try:
                rr = rubison_reiner(S0, K, H, T, r, d, sigma, 0, isCall=is_call, isDown=is_down, isIn=is_in)
            except Exception:
                continue
                
            if rr is None or vanilla is None or np.isnan(vanilla) or np.isnan(rr):
                continue
                
            # Calcular el ahorro porcentual de comprar la opción barrera en lugar de la regular
            if vanilla > 1e-6:
                saving = (vanilla - rr) / vanilla * 100.0
                # Limitar por seguridad a evitar pequeños errores flotantes (e.g. 100.000000002)
                saving = max(0.0, min(100.0, saving))
            else:
                saving = 0.0
                
            # Distancia de barrera relativa al precio actual (como porcentaje)
            dist = abs(S0 - H) / S0 * 100.0
            
            name = f"{group}-and-{'In' if is_in else 'Out'} {'Call' if is_call else 'Put'}"
            
            results[group].append({
                'name': name,
                'S0': S0, 'K': K, 'T': T, 'r': r, 'sigma': sigma, 'H': H,
                'isCall': is_call, 'isIn': is_in, 'isDown': is_down,
                'vanilla': float(vanilla), 'rr': float(rr), 'saving': float(saving), 'barrier_dist': float(dist)
            })
            
            samples_collected += 1
            
            # Progreso simple
            if samples_collected % 250 == 0:
                print(f"Procesadas {samples_collected}/{n_samples} opciones {group}...")
                
    return results

def plot_and_analyze(results):
    graph_dir = os.path.join(os.path.dirname(__file__), '..', 'graph')
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(graph_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    
    # 1. Guardar resultados en JSON
    json_path = os.path.join(data_dir, 'random_savings_samples.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
    print(f"\nDatos de las {sum(len(v) for v in results.values())} simulaciones guardados en {json_path}")
        
    all_savings = []
    
    for group in ['Down', 'Up']:
        group_results = results[group]
        all_savings.extend([r['saving'] for r in group_results])
        
    if not all_savings:
        print("No hay muestras válidas para graficar.")
        return
        
    avg_sav = np.mean(all_savings)
    min_sav = np.min(all_savings)
    max_sav = np.max(all_savings)
    
    print(f"\n==========================================")
    print(f"Análisis Global ({len(all_savings)} muestras válidas)")
    print(f"==========================================")
    print(f"Ahorro Promedio: {avg_sav:.2f}%")
    print(f"Ahorro Mínimo:   {min_sav:.2f}%")
    print(f"Ahorro Máximo:   {max_sav:.2f}%")
    
    # 2. Generar Histograma de ahorros unificado
    plt.figure(figsize=(10, 6))
    plt.hist(all_savings, bins=80, color='#9467bd', edgecolor='black', alpha=0.75, label='Frecuencia')
    plt.yscale('log')
    plt.axvline(avg_sav, color='red', linestyle='dashed', linewidth=2, label=f'Media ({avg_sav:.2f}%)')
    plt.title(f'Distribución Global de Ahorro Porcentual\n(Muestras={len(all_savings)})')
    plt.xlabel('Ahorro Porcentual al usar Opción Barrera (%)')
    plt.legend()
    plt.ylabel('Frecuencia (Escala Logarítmica)')
    plt.grid(True, axis='y', ls='--', alpha=0.5)
    plt.tight_layout()
    hist_path = os.path.join(graph_dir, f'histograma_ahorro_global.png')
    plt.savefig(hist_path)
    plt.close()
    print(f"-> Histograma unificado generado: {hist_path}")

if __name__ == '__main__':
    # Usar una semilla fija es opcional, pero ayuda a la reproducibilidad. 
    # random.seed(42)
    final_results = run_simulations(n_samples=100000)
    plot_and_analyze(final_results)
