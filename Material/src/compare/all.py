from rr.rr import rubison_reiner
from amm.amm import AMM_Barrier_Recursivo
from static.static import static_portfolio
from bs.bs import black_scholes
import time
# ============================================================================
# PARÁMETROS - EDITAR MANUALMENTE
# ============================================================================
S0 = 300      # Precio inicial del activo
K = 260       # Precio de ejercicio (strike)
T = 0.5         # Tiempo hasta vencimiento (años)
r = 0.05      # Tasa libre de riesgo
d = 0         # Tasa de dividendos
sigma = 0.2  # Volatilidad
H_down = 220   # Nivel de la barrera para opciones Down
H_up = 320    # Nivel de la barrera para opciones Up

# Parámetros para métodos numéricos
static_n_list = [12, 24, 48]  # Número de opciones en replicación estática
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

print(f"\nParámetros: S0={S0}, K={K}, H_down={H_down}, H_up={H_up}, T={T}, r={r}, d={d}, σ={sigma}")
print()

# Almacenar resultados en una estructura de datos
results = []

value_amm = []
time_amm = []

last_type = None
value_vanilla = 0
# Iterar por los 8 casos
for case_name, isCall, isDown, isIn in barrier_cases:
    H = H_down if isDown else H_up
    
    # Calcular valor vanilla de referencia
    value_vanilla = value_vanilla if last_type == isCall else black_scholes(S0, K, T, r, d, sigma, option_type=('call' if isCall else 'put'))
    last_type = isCall
    
    # Calcular con cada método
    t0 = time.perf_counter()
    try:
        value_rr = rubison_reiner(S0, K, H, T, r, d, sigma, 0, 
                                  isCall=isCall, isDown=isDown, isIn=isIn)
    except Exception as e:
        value_rr = None
    time_rr = time.perf_counter() - t0
    
    if not isIn:
        time_amm = []
        value_amm = []
        for amm_levels in range(3):
            t0 = time.perf_counter()
            try:
                value_amm.append(AMM_Barrier_Recursivo(S0, K, T, r, sigma, H, amm_levels, isCall=isCall, isDown=isDown))
            except Exception as e:
                value_amm.append(None)
            time_amm.append(time.perf_counter() - t0)
    else:
        value_amm = value_amm.copy()
        for amm_levels in range(3):
            if value_amm[amm_levels] is not None:
                value_amm[amm_levels] = value_vanilla - value_amm[amm_levels]
    
    time_static = []
    value_static = []
    for n in static_n_list:
        t0 = time.perf_counter()
        try:
            val, _ = static_portfolio(S0, K, H, T, r, d, sigma, n, 
                                   isCall=isCall, isDown=isDown, isIn=isIn)
            value_static.append(val)
        except Exception as e:
            value_static.append(None)
        time_static.append(time.perf_counter() - t0)
    
    results.append({
        'name': case_name,
        'vanilla': value_vanilla,
        'rr': value_rr,
        'time_rr': time_rr,
        'amm': value_amm,
        'time_amm': time_amm,
        'static': value_static,
        'time_static': time_static,
    })
    
print("TABLA DE RESULTADOS")
print("=" * 155)

header = f"{'Tipo de Opción':<22} | {'Vanilla':>12} | {'Reiner-Rub.':>12} | {'AMM':>12} | {'AMM-1':>12} | {'AMM-2':>12} | {'Static-6':>12} | {'Static-12':>12} | {'Static-24':>12}"
print(header)
print("-" * 155)

# Filas de datos
for result in results:
    name = result['name']
    vanilla = f"{result['vanilla']:>12.6f}" if result['vanilla'] is not None else f"{'N/A':>12}"
    rr = f"{result['rr']:>12.6f}" if result['rr'] is not None else f"{'Error':>12}"
    amm1 = f"{result['amm'][0]:>12.6f}" if result['amm'][0] is not None else f"{'Error':>12}"
    amm2 = f"{result['amm'][1]:>12.6f}" if result['amm'][1] is not None else f"{'Error':>12}"
    amm3 = f"{result['amm'][2]:>12.6f}" if result['amm'][2] is not None else f"{'Error':>12}"
    stat1 = f"{result['static'][0]:>12.6f}" if result['static'][0] is not None else f"{'Error':>12}"
    stat2 = f"{result['static'][1]:>12.6f}" if result['static'][1] is not None else f"{'Error':>12}"
    stat3 = f"{result['static'][2]:>12.6f}" if result['static'][2] is not None else f"{'Error':>12}"
    
    print(f"{name:<22} | {vanilla} | {rr} | {amm1} | {amm2} | {amm3} | {stat1} | {stat2} | {stat3}")


print("\nDIFERENCIAS ABSOLUTAS RESPECTO A REINER-RUBINSTEIN")
print("=" * 125)

header_diff = f"{'Tipo de Opción':<22} | {'AMM':>12} | {'AMM-1':>12} | {'AMM-2':>12} | {'Static-6':>12} | {'Static-12':>12} | {'Static-24':>12}"
print(header_diff)
print("-" * 125)

for result in results:
    name = result['name']
    rr_val = result['rr']
    
    if rr_val is not None:
        diff_amm1 = f"{abs(result['amm'][0] - rr_val):>12.6f}" if result['amm'][0] is not None else f"{'N/A':>12}"
        diff_amm2 = f"{abs(result['amm'][1] - rr_val):>12.6f}" if result['amm'][1] is not None else f"{'N/A':>12}"
        diff_amm3 = f"{abs(result['amm'][2] - rr_val):>12.6f}" if result['amm'][2] is not None else f"{'N/A':>12}"
        diff_stat1 = f"{abs(result['static'][0] - rr_val):>12.6f}" if result['static'][0] is not None else f"{'N/A':>12}"
        diff_stat2 = f"{abs(result['static'][1] - rr_val):>12.6f}" if result['static'][1] is not None else f"{'N/A':>12}"
        diff_stat3 = f"{abs(result['static'][2] - rr_val):>12.6f}" if result['static'][2] is not None else f"{'N/A':>12}"
    else:
        diff_amm1 = diff_amm2 = diff_amm3 = diff_stat1 = diff_stat2 = diff_stat3 = f"{'N/A':>12}"
    
    print(f"{name:<22} | {diff_amm1} | {diff_amm2} | {diff_amm3} | {diff_stat1} | {diff_stat2} | {diff_stat3}")

print("\nTIEMPOS DE EJECUCIÓN (segundos)")
print("=" * 140)

header_time = f"{'Tipo de Opción':<22} | {'Reiner-Rub.':>12} | {'AMM':>12} | {'AMM-1':>12} | {'AMM-2':>12} | {'Static-6':>12} | {'Static-12':>12} | {'Static-24':>12}"
print(header_time)
print("-" * 140)

for result in results:
    name = result['name']
    
    time_rr = f"{result['time_rr']:>12.6f}" if result['rr'] is not None else f"{'N/A':>12}"
    time_amm1 = f"{result['time_amm'][0]:>12.6f}" if result['amm'][0] is not None else f"{'N/A':>12}"
    time_amm2 = f"{result['time_amm'][1]:>12.6f}" if result['amm'][1] is not None else f"{'N/A':>12}"
    time_amm3 = f"{result['time_amm'][2]:>12.6f}" if result['amm'][2] is not None else f"{'N/A':>12}"
    time_stat1 = f"{result['time_static'][0]:>12.6f}" if result['static'][0] is not None else f"{'N/A':>12}"
    time_stat2 = f"{result['time_static'][1]:>12.6f}" if result['static'][1] is not None else f"{'N/A':>12}"
    time_stat3 = f"{result['time_static'][2]:>12.6f}" if result['static'][2] is not None else f"{'N/A':>12}"
    
    print(f"{name:<22} | {time_rr} | {time_amm1} | {time_amm2} | {time_amm3} | {time_stat1} | {time_stat2} | {time_stat3}")
