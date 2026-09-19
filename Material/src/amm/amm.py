import numpy as np
from scipy.stats import norm

def AMM_Barrier_Recursivo(S0, K, T, r, sigma, H, M, isCall=True, isDown=True):
    # 1. CALIBRACIÓN GLOBAL (Para la malla más profunda)
    dist_log = abs(np.log(S0) - np.log(H))
    
    # El paso grueso inicial debe ser tal que al dividirlo por 2^M lleguemos a dist_log
    h_coarse_base = (2**M) * dist_log

    # Calcular k base usando stretch parameter con la h más gruesa
    N_base = int((T * 3 * sigma**2) / (h_coarse_base**2))
    k_base = T / N_base
    
    # 2. CONSTRUIR MALLA BASE (NIVEL 0)
    # Esta es la malla A estándar
    A_grid = build_coarse_mesh(S0, K, T, r, sigma, H, h_coarse_base, k_base, N_base, isCall, isDown)
    
    # 3. BUCLE DE REFINAMIENTO (NIVEL 1 hasta M)
    # La malla anterior sirve de input para la siguiente
    current_grid = A_grid
    current_h = h_coarse_base
    current_k = k_base
    current_N = N_base
    
    for level in range(M):
        # La nueva malla fina se "injerta" en la actual
        fine_grid = build_fine_mesh(current_grid, current_h, current_k, current_N, r, sigma, H, K, isCall, isDown)
        
        # Actualizar variables para la siguiente vuelta
        current_grid = fine_grid # La fina de hoy es la gruesa de mañana
        current_h = current_h / 2
        current_k = current_k / 4
        current_N = current_N * 4
    
    # El valor está en el nodo central
    value_out = current_grid[1, 0]
    
    return value_out

def build_coarse_mesh(S0, K, T, r, sigma, H, h, k, N, isCall=True, isDown=True):
    # Calcular número de nodos necesarios en precio
    # Necesitamos cubrir desde H hasta un precio máximo razonable
    # Usamos 4 desviaciones estándar por encima de S0
    S_max = S0 * np.exp((r - 0.5*sigma**2)*T + 4*sigma*np.sqrt(T))
    max_price_nodes = int(np.log(S_max/H) / abs(h)) + 5  # +5 para margen de seguridad
    
    N_steps = N
    h_coarse = h
    k_coarse = k
  
    # Inicializar matriz A (Malla Gruesa)
    # Dimensiones: (N_steps + 1) tiempo x (Rango suficiente de precio)
    # Nota: El índice i=0 corresponde a la barrera H. i=1 es H*exp(h), etc.
    A_grid = np.zeros((max_price_nodes, N_steps + 1))
    
    # Calcular probabilidades estándar (Eq. 9) para malla gruesa
    pu_A, pm_A, pd_A = calcular_probs(k_coarse, h_coarse, r, sigma)
    direction = 1
    
    if not isDown:
        direction = -1
        pu_A, pd_A = pd_A, pu_A
    
    # Llenar valores terminales (Payoff en t=T)
    for i in range(max_price_nodes):
        price = H * np.exp(i * direction * h_coarse)
        if isCall:
            A_grid[i, N_steps] = max(price - K, 0)
        else:
            A_grid[i, N_steps] = max(K - price, 0)
        
    A_grid[0, :] = 0
        
    # Inducción hacia atrás (Standard Backward Induction)
    for j in range(N_steps - 1, -1, -1):
        # Nodos internos
        for i in range(1, max_price_nodes - 1):
            val = (pu_A * A_grid[i+1, j+1] + 
                   pm_A * A_grid[i,   j+1] + 
                   pd_A * A_grid[i-1, j+1]) * np.exp(-r * k_coarse)
            A_grid[i, j] = val
    
    return A_grid

def build_fine_mesh(coarse_grid, h_coarse, k_coarse, N_coarse, r, sigma, H, K, isCall=True, isDown=True):
    total_fine_steps = N_coarse * 4
    B_grid = np.zeros((3, total_fine_steps + 1))
    
    # 1. INYECCIÓN DE NODOS (Eq. 11)
    for j in range(N_coarse):
        t_start = j * 4
        
        val_coarse_t = coarse_grid[1, j] 
        B_grid[2, t_start] = val_coarse_t
        
        V_Au = coarse_grid[2, j+1]
        V_Am = coarse_grid[1, j+1]
        V_Ad = coarse_grid[0, j+1]
        
        # Nodos intermedios (sub-steps 1, 2, 3)
        for sub_step in range(1, 4):
          dt_eff = (4 - sub_step) * (k_coarse / 4)
          pu_adj, pm_adj, pd_adj = calcular_probs(dt_eff, h_coarse, r, sigma)
          
          if not isDown:
            pu_adj, pd_adj = pd_adj, pu_adj
          
          val_intermedio = (pu_adj * V_Au + 
                            pm_adj * V_Am + 
                            pd_adj * V_Ad) * np.exp(-r * dt_eff)
                            
          B_grid[2, t_start + sub_step] = val_intermedio

    B_grid[2, total_fine_steps] = coarse_grid[1, N_coarse]
    
    # 2. RELLENO INTERNO (Backward Induction)
    h_fine = h_coarse / 2
    k_fine = k_coarse / 4
    pu, pm, pd = calcular_probs(k_fine, h_fine, r, sigma)
    direction = 1

    if not isDown:
        direction = -1
        pu, pd = pd, pu
    
    # Payoff terminal para todas las filas
    for i in range(3):
        price_at_level = H * np.exp(i * direction * h_fine)
        if isCall:
            B_grid[i, total_fine_steps] = max(price_at_level - K, 0)
        else:
            B_grid[i, total_fine_steps] = max(K - price_at_level, 0)

    B_grid[0, :] = 0.0

    # Backward induction
    for t in range(total_fine_steps - 1, -1, -1):
        val = (pu * B_grid[2, t+1] + 
               pm * B_grid[1, t+1] + 
               pd * B_grid[0, t+1]) * np.exp(-r * k_fine)
        B_grid[1, t] = val
        
    return B_grid

def calcular_probs(dt, dx, r, sigma):
    drift = r - 0.5 * sigma**2
    
    term1 = (sigma**2 * dt) / (dx**2)
    term2 = (drift**2 * dt**2) / (dx**2)
    term3 = (drift * dt) / dx
    
    pu = 0.5 * (term1 + term2 + term3)
    pd = 0.5 * (term1 + term2 - term3)
    pm = 1.0 - pu - pd
    
    if abs(pu) < 1e-10: pu = 0.0
    if abs(pd) < 1e-10: pd = 0.0
    if abs(pm) < 1e-10: pm = 0.0
    
    return pu, pm, pd
