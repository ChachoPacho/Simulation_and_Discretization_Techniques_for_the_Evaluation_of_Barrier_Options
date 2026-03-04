import numpy as np
from bs.bs import black_scholes

def replication_dek_barrier(S0, K, B, T, r, d, sigma, N=10, is_up=True, option_type='call'):
    dt = T / N
    time_steps = np.linspace(0, T, N + 1)
    
    # 1. Inicialización (t = T)
    # El portafolio comienza con 1 opción vanilla original
    # Portafolio: Lista de diccionarios {tipo, strike, vencimiento, peso}
    portfolio = [{'type': option_type, 
                  'K': K, 'T': T, 'w': 1.0}]
    
    # Determinamos el instrumento de ajuste según las reglas de frontera DEK:
    # - Fronteras superiores (up barriers): usar CALLS con K >= B
    # - Fronteras inferiores (down barriers): usar PUTS con K <= B
    adj_type = 'call' if is_up else 'put'
    adj_strike = B
    
    # 2. Bucle Recursivo (Backward Induction)
    # Iteramos desde el penúltimo paso de tiempo hasta el presente
    for i in range(N, 0, -1):
        t_exp = time_steps[i] # Tiempo actual de evaluación en la barrera
        t_eval = time_steps[i - 1]
        
        # Calcular valor del portafolio acumulado en (S=B, t=t_exp)
        v_port = 0
        for opt in portfolio:
            bs_value = black_scholes(B, opt['K'], opt['T'] - t_eval, r, d, sigma, opt['type'])
            v_port += opt['w'] * bs_value
        
        # Vtarget suele ser 0 para Knock-out (sin rebate)
        v_target = 0 
        
        # Valor de la opción de ajuste en el punto de la barrera (B, t_exp)
        # La opción de ajuste vence en T (el vencimiento final)
        v_adj = black_scholes(B, adj_strike, t_exp - t_eval, r, d, sigma, adj_type)
        
        # Cálculo del peso alpha_i (Ecuación 4.15)
        alpha_i = (v_target - v_port) / v_adj
        
        # Añadir la nueva opción al portafolio
        # La opción vence en T (vencimiento final), pero se añade en tiempo t_exp
        portfolio.append({'type': adj_type, 'K': adj_strike, 'T': t_exp, 'w': alpha_i})
        
    return portfolio

def static_portfolio(S0, K, B, T, r, d, sigma, N_ajustes, isCall=True, isIn=True, isDown=True):
    option_type = 'call' if isCall else 'put'
    
    # Verificar si la barrera ya fue cruzada en t=0
    barrier_crossed = (isDown and S0 <= B) or (not isDown and S0 >= B)
    
    if barrier_crossed:
        # Si la barrera ya fue cruzada:
        # - Out options valen 0 (ya fueron knocked out)
        # - In options valen lo mismo que vanilla (ya fueron knocked in)
        if isIn:
            return black_scholes(S0, K, T, r, d, sigma, option_type)
        else:
            return 0.0
    
    # Proceder con la replicación DEK
    portafolio = replication_dek_barrier(S0, K, B, T, r, d, sigma, N_ajustes, is_up=(not isDown), option_type=option_type)
    
    value = 0
    for opt in portafolio:
        bs_value = black_scholes(S0, opt['K'], opt['T'], r, d, sigma, opt['type'])
        value += opt['w'] * bs_value
        
    if isIn:
        vanilla = black_scholes(S0, K, T, r, d, sigma, option_type)
        value = vanilla - value
        
    return max(value, 0.0)
