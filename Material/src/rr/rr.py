import numpy as np
from scipy.stats import norm

def calcular_terminos_rr(S, K, H, t, r_rate, d_rate, sigma, phi, eta, R=0):
    """
    Calcula los 6 términos analíticos de Reiner y Rubinstein.
    Permite el uso de arreglos (numpy arrays) para evaluar miles de precios a la vez.
    """
    # Conversión a las variables de Reiner y Rubinstein (1 + tasa) [3, 4]
    # Asumiendo que recibimos tasas continuas estándar:
    r = np.exp(r_rate)
    d = np.exp(d_rate)
    
    # Variables auxiliares de la tesis [1, 4]
    mu = np.log(r/d) - 0.5 * sigma**2
    lambda_ = 1 + (mu / sigma**2)
    a = mu / sigma**2  # Derivado del paper original de R&R [5]
    b = np.sqrt(mu**2 + 2 * np.log(r) * sigma**2) / sigma**2
    
    # Parámetros d1, d2 adaptados a x, x1, y, y1, z [1]
    denominador = sigma * np.sqrt(t)
    x  = (np.log(S/K) / denominador) + lambda_ * denominador
    x1 = (np.log(S/H) / denominador) + lambda_ * denominador
    y  = (np.log(H**2 / (S*K)) / denominador) + lambda_ * denominador
    y1 = (np.log(H/S) / denominador) + lambda_ * denominador
    z  = (np.log(H/S) / denominador) + b * denominador
    
    # Evaluaciones de la Normal estándar vectorizadas
    N = norm.cdf
    
    # Factores de descuento [1]
    S_d_t = S * (d ** -t)
    K_r_t = K * (r ** -t)
    R_r_t = R * (r ** -t)
    H_S = H / S
    
    # Términos de Valoración [6] al [3] basados en la Ecuaciones 3.1 a 3.6 de la tesis [1, 7]
    term1 = phi * S_d_t * N(phi * x) - phi * K_r_t * N(phi * x - phi * denominador)
    
    term2 = phi * S_d_t * N(phi * x1) - phi * K_r_t * N(phi * x1 - phi * denominador)
    
    term3 = phi * S_d_t * (H_S ** (2 * lambda_)) * N(eta * y) \
            - phi * K_r_t * (H_S ** (2 * lambda_ - 2)) * N(eta * y - eta * denominador)
            
    term4 = phi * S_d_t * (H_S ** (2 * lambda_)) * N(eta * y1) \
            - phi * K_r_t * (H_S ** (2 * lambda_ - 2)) * N(eta * y1 - eta * denominador)
            
    term5 = R_r_t * (N(eta * x1 - eta * denominador) \
            - (H_S ** (2 * lambda_ - 2)) * N(eta * y1 - eta * denominador))
            
    term6 = R * ((H_S ** (a + b)) * N(eta * z) \
            + (H_S ** (a - b)) * N(eta * z - 2 * eta * b * denominador))
            
    return term1, term2, term3, term4, term5, term6

def rubison_reiner(S, K, H, t, r_rate, d_rate, sigma, R=0, isCall=True, isDown=True, isIn=True):
    phi = 1 if isCall else -1
    eta = 1 if isDown else -1
    
    t1, t2, t3, t4, t5, t6 = calcular_terminos_rr(S, K, H, t, r_rate, d_rate, sigma, phi, eta, R)
    
    if isIn:
        if (isDown and isCall and K > H) or (not isDown and not isCall and K < H):
            return t3 + t5
        
        if (isDown and isCall and K < H) or (not isDown and not isCall and K > H):
            return t1 - t2 + t4 + t5
        
        if (not isDown and isCall and K > H) or (isDown and not isCall and K < H):
            return t1 + t5
        
        if (not isDown and isCall and K < H) or (isDown and not isCall and K > H):
            return t2 - t3 + t4 + t5
    else:
        if (isDown and isCall and K > H) or (not isDown and not isCall and K < H):
            return t1 - t3 + t6
        
        if (isDown and isCall and K < H) or (not isDown and not isCall and K > H):
            return t2 - t4 + t6
        
        if (not isDown and isCall and K > H) or (isDown and not isCall and K < H):
            return t6
        
        if (not isDown and isCall and K < H) or (isDown and not isCall and K > H):
            return t1 - t2 + t3 - t4 + t6
    
    return 0

    
if __name__ == "__main__":
    S0 = 100
    K = 100
    T = 1
    r = 0.10
    d = 0.05
    sigma = 0.25
    H = 120

    precio = rubison_reiner(S0, K, H, T, r, d, sigma, isCall=True, isDown=False, isIn=False)
    print(f"Precio de la opción: {precio}")
