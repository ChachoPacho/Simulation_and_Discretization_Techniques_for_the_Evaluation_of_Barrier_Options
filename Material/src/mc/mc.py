import numpy as np

def monte_carlo_lsm_barrier(S0, K, H, T, r, sigma, delta=0, iterations=50000, steps=100, isCall=True, isUp=True, isIn=True):
    dt = T / steps
    df = np.exp(-r * dt)
    
    rng = np.random.default_rng(seed=42)
    z = rng.standard_normal((iterations, steps))
    
    log_returns = (r - delta - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
    cumulative_log_returns = np.cumsum(log_returns, axis=1)
    s_path = S0 * np.exp(np.hstack([np.zeros((iterations, 1)), cumulative_log_returns]))
    
    if isUp:
        hit_anytime = np.any(s_path >= H, axis=1)
        first_hit_idx = np.argmax(s_path >= H, axis=1)
    else:
        hit_anytime = np.any(s_path <= H, axis=1)
        first_hit_idx = np.argmax(s_path <= H, axis=1)
    
    if isCall:
        payoff_T = np.maximum(s_path[:, -1] - K, 0)
    else:
        payoff_T = np.maximum(K - s_path[:, -1], 0)
    
    if isIn:
        cash_flow = np.where(hit_anytime, payoff_T, 0.0)
    else:
        cash_flow = np.where(~hit_anytime, payoff_T, 0.0)
    
    for t in range(steps - 1, 0, -1):
        cash_flow = cash_flow * df
        
        if isCall:
            intrinsic = np.maximum(s_path[:, t] - K, 0)
        else:
            intrinsic = np.maximum(K - s_path[:, t], 0)
            
        itm = intrinsic > 0
        
        if isIn:
            barrier_active = (hit_anytime) & (first_hit_idx <= t)
        else:
            barrier_active = ~hit_anytime | (first_hit_idx > t)
            
        active = itm & barrier_active
        
        if np.any(active):
            X = s_path[active, t]
            Y = cash_flow[active]
            
            # Regresión (Longstaff-Schwartz)
            poly = np.polyfit(X, Y, 2)
            continuation_value = np.polyval(poly, X)
            
            # Ejercicio si el valor inmediato es mayor al de continuación
            exercise = intrinsic[active] > continuation_value
            
            # Actualizar cash flows de las trayectorias donde se ejerce
            idx_active = np.where(active)[0]
            idx_exercise = idx_active[exercise]
            cash_flow[idx_exercise] = intrinsic[idx_exercise]
            
    df_cash_flow = cash_flow * df
    return np.mean(df_cash_flow), np.std(df_cash_flow)