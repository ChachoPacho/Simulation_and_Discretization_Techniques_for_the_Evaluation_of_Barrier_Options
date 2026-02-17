import numpy as np
from scipy.stats import norm

def merton_down_and_out_call(S, K, T, r, sigma, H):
    """
    Implementación de la Ecuación 8 de Figlewski & Gao (1999) / Merton (1973).
    Referencia: Fuente [2]
    """
    # Verificación básica
    if S <= H:
        return 0.0
        
    # Parámetros auxiliares
    # Nota: El paper define lambda = (r - q - sigma^2/2) / sigma^2
    # Asumiendo q (dividendos) = 0 según los parámetros del paper.
    lam = (r - 0.5 * sigma**2) / sigma**2
    x = np.log(S / H)
    
    # Función auxiliar Black-Scholes estándar
    def bs_call(S_val, K_val, T_val, r_val, sigma_val):
        d1 = (np.log(S_val / K_val) + (r_val + 0.5 * sigma_val**2) * T_val) / (sigma_val * np.sqrt(T_val))
        d2 = d1 - sigma_val * np.sqrt(T_val)
        return S_val * norm.cdf(d1) - K_val * np.exp(-r_val * T_val) * norm.cdf(d2)
    
    # Término A: Call estándar BS
    c_bs_S = bs_call(S, K, T, r, sigma)
    
    # Término B: Call BS ajustado (Reflejo en la barrera)
    # Factor de ajuste: (H/S)^(2*lambda)
    factor = (H / S)**(2 * lam)
    c_bs_H = bs_call(H**2 / S, K, T, r, sigma)
    
    return c_bs_S - factor * c_bs_H

# --- Verificación del valor 0.162 ---
S0 = 90.125
K = 100
T = 1
r = 0.10
sigma = 0.25
H = 90

valor_exacto = merton_down_and_out_call(S0, K, T, r, sigma, H)
print(f"Valor Teórico Exacto (Merton): {valor_exacto:.6f}")