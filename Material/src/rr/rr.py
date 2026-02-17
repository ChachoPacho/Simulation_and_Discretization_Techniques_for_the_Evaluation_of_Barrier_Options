import numpy as np
from scipy.stats import norm

def reiner_rubinstein_down_out_call(S, K, T, r, sigma, H, option_type='call', barrier_type='down-and-out', q=0):
    """
    Calcula el precio de una opción barrera usando fórmulas cerradas (Reiner-Rubinstein).
    S: Precio actual, K: Strike, H: Barrera, T: Tiempo, r: Tasa, sigma: Volatilidad, q: Dividendos.
    """
    
    # Parámetros auxiliares
    mu = (r - q - (sigma**2) / 2) / (sigma**2)
    lam = np.sqrt(mu**2 + 2 * r / (sigma**2))
    
    def d(s_val, k_val, t_val, sigma_val, mu_val):
        return (np.log(s_val / k_val) + (mu_val + 1) * (sigma_val**2) * t_val) / (sigma_val * np.sqrt(t_val))

    # d1 y d2 estándar para Black-Scholes
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # d-términos con la barrera H
    y = np.log((H**2) / (S * K)) / (sigma * np.sqrt(T)) + (mu + 1) * sigma * np.sqrt(T)
    x1 = np.log(S / H) / (sigma * np.sqrt(T)) + (mu + 1) * sigma * np.sqrt(T)
    y1 = np.log(H / S) / (sigma * np.sqrt(T)) + (mu + 1) * sigma * np.sqrt(T)

    # Cálculo de componentes (A, B, C, D, E, F según la literatura)
    # Aquí implementamos la lógica simplificada para 'down-and-out call' como ejemplo:
    if option_type == 'call' and barrier_type == 'down-and-out':
        if S <= H: return 0.0
        
        phi = 1
        eta = 1
        
        A = phi * S * np.exp(-q * T) * norm.cdf(phi * d1) - phi * K * np.exp(-r * T) * norm.cdf(phi * d2)
        B = phi * S * np.exp(-q * T) * norm.cdf(phi * x1) - phi * K * np.exp(-r * T) * norm.cdf(phi * (x1 - sigma * np.sqrt(T)))
        C = phi * S * np.exp(-q * T) * (H / S)**(2 * (mu + 1)) * norm.cdf(eta * y1) - \
            phi * K * np.exp(-r * T) * (H / S)**(2 * mu) * norm.cdf(eta * (y1 - sigma * np.sqrt(T)))
        D = phi * S * np.exp(-q * T) * (H / S)**(2 * (mu + 1)) * norm.cdf(eta * y) - \
            phi * K * np.exp(-r * T) * (H / S)**(2 * mu) * norm.cdf(eta * (y - sigma * np.sqrt(T)))
        
        # Para Down-and-out Call con K > H:
        if K >= H:
            return A - C
        else:
            return B - D
            
    return "Tipo de barrera no implementado en este snippet"
