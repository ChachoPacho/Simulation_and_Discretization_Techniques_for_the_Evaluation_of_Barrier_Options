import numpy as np
import scipy.stats as si 

from rr.rr import rubison_reiner
from amm.amm import AMM_Barrier_Recursivo
from static.static import static_portfolio
from bs.bs import black_scholes

# ============================================================================
# PARÁMETROS - EDITAR MANUALMENTE
# ============================================================================
S0 = 100      # Precio inicial del activo
K = 100       # Precio de ejercicio (strike)
T = 1         # Tiempo hasta vencimiento (años)
r = 0.10      # Tasa libre de riesgo
d = 0.05         # Tasa de dividendos
sigma = 0.25  # Volatilidad
H = 120        # Nivel de la barrera

# Parámetros para métodos numéricos
amm_levels = 2      # Niveles de refinamiento AMM
static_n = 6        # Número de opciones en replicación estática
# ============================================================================

# Definir los 8 casos de opciones barrera
barrier_cases = [
    # (nombre, isCall, isDown, isIn)
    ("Down-and-Out Call", True, True, False),
    ("Down-and-In Call", True, True, True),
    ("Up-and-Out Call", True, False, False),
    ("Up-and-In Call", True, False, True),
    ("Down-and-Out Put", False, True, False),
    ("Down-and-In Put", False, True, True),
    ("Up-and-Out Put", False, False, False),
    ("Up-and-In Put", False, False, True),
]

print(f"\nParámetros: S0={S0}, K={K}, H={H}, T={T}, r={r}, d={d}, σ={sigma}")
print()

# Almacenar resultados en una estructura de datos
results = []

# Iterar por los 8 casos
for case_name, isCall, isDown, isIn in barrier_cases:
    # Calcular valor vanilla de referencia
    value_vanilla = black_scholes(S0, K, T, r, d, sigma, option_type=('call' if isCall else 'put'))
    
    # Calcular con cada método
    try:
        value_rr = rubison_reiner(S0, K, H, T, r, d, sigma, 0, 
                                  isCall=isCall, isDown=isDown, isIn=isIn)
    except Exception as e:
        value_rr = None
    
    try:
        value_amm = AMM_Barrier_Recursivo(S0, K, T, r, sigma, H, amm_levels,
                                         isCall=isCall, isDown=isDown, isIn=isIn)
    except Exception as e:
        value_amm = None
    
    try:
        value_static = static_portfolio(S0, K, H, T, r, d, sigma, static_n, 
                                       isCall=isCall, isDown=isDown, isIn=isIn)
    except Exception as e:
        value_static = None
    
    results.append({
        'name': case_name,
        'vanilla': value_vanilla,
        'rr': value_rr,
        'amm': value_amm,
        'static': value_static,
    })

print("TABLA DE RESULTADOS")
print("=" * 85)

header = f"{'Tipo de Opción':<22} | {'Vanilla':>12} | {'Reiner-Rub.':>12} | {'AMM':>12} | {'Static-1':>12}"
print(header)
print("-" * 85)

# Filas de datos
for result in results:
    name = result['name']
    vanilla = f"{result['vanilla']:>12.6f}" if result['vanilla'] is not None else f"{'N/A':>12}"
    rr = f"{result['rr']:>12.6f}" if result['rr'] is not None else f"{'Error':>12}"
    amm = f"{result['amm']:>12.6f}" if result['amm'] is not None else f"{'Error':>12}"
    static = f"{result['static']:>12.6f}" if result['static'] is not None else f"{'Error':>12}"
    
    print(f"{name:<22} | {vanilla} | {rr} | {amm} | {static}")


print("\nDIFERENCIAS ABSOLUTAS RESPECTO A REINER-RUBINSTEIN")
print("=" * 55)

header_diff = f"{'Tipo de Opción':<22} | {'AMM':>12} | {'Static-1':>12}"
print(header_diff)
print("-" * 55)

for result in results:
    name = result['name']
    rr_val = result['rr']
    
    if rr_val is not None:
        diff_amm = f"{abs(result['amm'] - rr_val):>12.6f}" if result['amm'] is not None else f"{'N/A':>12}"
        diff_static = f"{abs(result['static'] - rr_val):>12.6f}" if result['static'] is not None else f"{'N/A':>12}"
    else:
        diff_amm = diff_static = f"{'N/A':>12}"
    
    print(f"{name:<22} | {diff_amm} | {diff_static}")

