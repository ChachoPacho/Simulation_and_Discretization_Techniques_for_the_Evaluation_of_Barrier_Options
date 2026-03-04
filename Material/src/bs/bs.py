import numpy as np
from scipy.stats import norm


def black_scholes(S, K, T, r, d, sigma, option_type='call'):
    if T <= 0:
        if option_type.lower() == 'call':
            return max(S - K, 0)
        else:
            return max(K - S, 0)

    # Cálculo de d1 y d2
    d1 = (np.log(S / K) + (r - d + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type.lower() == 'call':
        return (
            S * np.exp(-d * T) * norm.cdf(d1) - norm.cdf(d2) * np.exp(-r * T) * K
        )
    elif option_type.lower() == 'put':
        return (
          norm.cdf(-d2) * K * np.exp(-r * T) - S * np.exp(-d * T) * norm.cdf(-d1)
        )
    else:
        raise ValueError("El tipo de opción debe ser 'call' o 'put'")