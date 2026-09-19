import os
import sys

# Añadir el path base para poder importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from static.static import static_portfolio
from rr.rr import rubison_reiner

def analyze_static():
    S0 = 300
    K = 260
    T = 0.5
    r = 0.05
    d = 0
    sigma = 0.2
    H_down = 220
    H_up = 320
    
    # Evaluar los niveles 6, 12 y 24
    static_n_list = [6, 12, 24]
    
    barrier_cases = [
        ("Down-and-Out Call", True, True, False),
        ("Down-and-In Call", True, True, True),
        ("Up-and-Out Call", True, False, False),
        ("Up-and-In Call", True, False, True),
        ("Down-and-Out Put", False, True, False),
        ("Down-and-In Put", False, True, True),
        ("Up-and-Out Put", False, False, False),
        ("Up-and-In Put", False, False, True),
    ]

    print("\nANÁLISIS DE REPLICACIÓN ESTÁTICA vs REINER-RUBINSTEIN")
    print(f"Parámetros: S0={S0}, K={K}, H_down={H_down}, H_up={H_up}, T={T}, r={r}, sigma={sigma}")
    print("=" * 105)
    
    header = f"{'Tipo de Opción':<20} | {'N':>4} | {'# Opciones':>10} | {'Reiner-Rub.':>12} | {'Static':>12} | {'Error Rel. (%)':>15}"
    print(header)
    print("-" * 105)
    
    for case_name, isCall, isDown, isIn in barrier_cases:
        H = H_down if isDown else H_up
        
        # Valor analítico exacto de referencia
        try:
            rr_val = rubison_reiner(S0, K, H, T, r, d, sigma, 0, isCall=isCall, isDown=isDown, isIn=isIn)
        except Exception:
            rr_val = None
            
        for n in static_n_list:
            try:
                # El usuario modificó static.py para devolver (valor, portafolio)
                stat_val, portafolio = static_portfolio(S0, K, H, T, r, d, sigma, n, isCall=isCall, isDown=isDown, isIn=isIn)
                
                # Número de opciones necesarias para formar el portafolio
                # (Si es In, implícitamente hay 1 opción Vanilla extra, pero contamos las del objeto devuelto)
                num_options = len(portafolio)
            except Exception as e:
                print(e)
                stat_val = None
                num_options = "Error"
                
            # Cálculo del Error Relativo
            rel_error = "N/A"
            if rr_val is not None and stat_val is not None:
                if rr_val > 1e-6: # Evitar división por números ínfimos
                    err = abs(stat_val - rr_val) / rr_val * 100
                    rel_error = f"{err:>14.4f}%"
                else:
                    rel_error = f"{'Valor base ~0':>15}"
                    
            rr_str = f"{rr_val:>12.6f}" if rr_val is not None else f"{'Error':>12}"
            stat_str = f"{stat_val:>12.6f}" if stat_val is not None else f"{'Error':>12}"
            
            print(f"{case_name:<20} | {n:>4} | {num_options:>10} | {rr_str} | {stat_str} | {rel_error}")
        
        # Separador entre casos
        print("-" * 105)

if __name__ == '__main__':
    analyze_static()
