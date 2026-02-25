import numpy as np
from math import ceil

def AMM_Barrier_Recursivo(S0, K, T, r, sigma, H, M):
    # 1. CALIBRACIÓN GLOBAL (Para la malla más profunda)
    dist_log = np.log(S0) - np.log(H)
    
    # El paso grueso inicial debe ser tal que al dividirlo por 2^M lleguemos a dist_log
    h_coarse_base = (2**M) * dist_log
    
    # Calcular k base usando stretch parameter con la h más gruesa
    N_ideal = (T * 3 * sigma**2) / (h_coarse_base**2)
    N_base = int(N_ideal)
    k_base = T / N_base
    
    # 2. CONSTRUIR MALLA BASE (NIVEL 0)
    # Esta es la malla A estándar
    A_grid = build_coarse_mesh(S0, K, T, r, sigma, H, h_coarse_base, k_base, N_base)
    
    # 3. BUCLE DE REFINAMIENTO (NIVEL 1 hasta M)
    # La malla anterior sirve de input para la siguiente
    current_grid = A_grid
    current_h = h_coarse_base
    current_k = k_base
    current_N = N_base
    
    for level in range(1, M + 1):
        # La nueva malla fina se "injerta" en la actual
        fine_grid = build_fine_mesh(current_grid, current_h, current_k, current_N, r, sigma, H, K)
        
        # Actualizar variables para la siguiente vuelta
        current_grid = fine_grid # La fina de hoy es la gruesa de mañana
        current_h = current_h / 2
        current_k = current_k / 4
        current_N = current_N * 4
        
    # Retornar el valor actual (t=0) del nodo central
    return current_grid[1, 0]

def build_coarse_mesh(S0, K, T, r, sigma, H, h, k, N):
    # Calcular número de nodos necesarios en precio
    # Necesitamos cubrir desde H hasta un precio máximo razonable
    # Usamos 4 desviaciones estándar por encima de S0
    S_max = S0 * np.exp((r - 0.5*sigma**2)*T + 4*sigma*np.sqrt(T))
    max_price_nodes = int(np.log(S_max/H) / h) + 5  # +5 para margen de seguridad
    
    N_steps = N
    h_coarse = h
    k_coarse = k
  
    # Inicializar matriz A (Malla Gruesa)
    # Dimensiones: (N_steps + 1) tiempo x (Rango suficiente de precio)
    # Nota: El índice i=0 corresponde a la barrera H. i=1 es H*exp(h), etc.
    A_grid = np.zeros((max_price_nodes, N_steps + 1))
    
    # Calcular probabilidades estándar (Eq. 9) para malla gruesa
    pu_A, pm_A, pd_A = calcular_probs(k_coarse, h_coarse, r, sigma)
    
    # Llenar valores terminales (Payoff en t=T)
    for i in range(max_price_nodes):
        price = H * np.exp(i * h_coarse)
        A_grid[i, N_steps] = max(price - K, 0)
        
    # Inducción hacia atrás (Standard Backward Induction)
    for j in range(N_steps - 1, -1, -1):
        # Barrera siempre vale 0
        A_grid[0, j] = 0
        
        # Nodos internos
        for i in range(1, max_price_nodes - 1):
            val = (pu_A * A_grid[i+1, j+1] + 
                   pm_A * A_grid[i,   j+1] + 
                   pd_A * A_grid[i-1, j+1]) * np.exp(-r * k_coarse)
            A_grid[i, j] = val
    
    return A_grid

def build_fine_mesh(coarse_grid, h_coarse, k_coarse, N_coarse, r, sigma, H, K):
    total_fine_steps = N_coarse * 4
    B_grid = np.zeros((3, total_fine_steps + 1))
    
    # 1. INYECCIÓN DE NODOS (Eq. 11)
    # Lógica de interpolación (Eq. 12 y 13)
    for j in range(N_coarse):
        t_start = j * 4
        
        # Nodo entero
        # Si venimos de Malla A (grande), usamos A[3]. 
        # Si venimos de una Malla B anterior, usamos B[3].
        # Generalización: La fuente de datos es siempre la fila 1 de la malla previa.
        val_coarse_t = coarse_grid[1, j] 
        B_grid[2, t_start] = val_coarse_t
        
        # Nodos intermedios (Interpolación)
        V_Au = coarse_grid[2, j+1]
        V_Am = coarse_grid[1, j+1]
        V_Ad = coarse_grid[0, j+1] # Barrera o fila 0 previa
        
        # Nodos intermedios (sub-steps 1, 2, 3)
        for sub_step in range(1, 4):
          # Calcular tiempo efectivo restante hasta el próximo nodo A
          # Si estoy en sub_step 1 (k/4), me faltan 3k/4 para llegar a j+1
          dt_eff = (4 - sub_step) * (k_coarse / 4)
          
          # IMPORTANTE: Usar h_coarse (no h_fine) porque estamos interpolando
          # entre nodos de la malla gruesa que están separados por h_coarse
          pu_adj, pm_adj, pd_adj = calcular_probs(dt_eff, h_coarse, r, sigma)
          
          # Valorar usando los nodos A del FUTURO
          val_intermedio = (pu_adj * V_Au + 
                            pm_adj * V_Am + 
                            pd_adj * V_Ad) * np.exp(-r * dt_eff)
                            
          B_grid[2, t_start + sub_step] = val_intermedio

    B_grid[2, total_fine_steps] = coarse_grid[1, N_coarse]
    
    # 2. RELLENO INTERNO (Backward Induction)
    h_fine = h_coarse / 2
    k_fine = k_coarse / 4
    pu, pm, pd = calcular_probs(k_fine, h_fine, r, sigma)
    
    # Payoff terminal para todas las filas
    for i in range(3):
        price_at_level = H * np.exp(i * h_fine)
        B_grid[i, total_fine_steps] = max(price_at_level - K, 0)

    # Backward induction
    for t in range(total_fine_steps - 1, -1, -1):
        # Barrera siempre vale 0
        B_grid[0, t] = 0
        
        # Fila central (i=1)
        val = (pu * B_grid[2, t+1] + 
               pm * B_grid[1, t+1] + 
               pd * B_grid[0, t+1]) * np.exp(-r * k_fine)
        B_grid[1, t] = val
        
    return B_grid

def calcular_probs(dt, dx, r, sigma):
    """Implementa Eq. 9 o Eq. 12 dependiendo de los inputs"""
    drift = r - 0.5 * sigma**2 # Asumiendo q=0
    
    # Términos comunes
    term1 = (sigma**2 * dt) / (dx**2)
    term2 = (drift**2 * dt**2) / (dx**2)
    term3 = (drift * dt) / dx
    
    pu = 0.5 * (term1 + term2 + term3)
    pd = 0.5 * (term1 + term2 - term3)
    pm = 1.0 - pu - pd
    
    # Validar que las probabilidades sean válidas
    if pu < 0 or pd < 0 or pm < 0:
        raise ValueError(f"Probabilidades negativas detectadas: pu={pu:.6f}, pm={pm:.6f}, pd={pd:.6f}\n"
                        f"Parámetros: dt={dt}, dx={dx}, r={r}, sigma={sigma}")
    if abs(pu + pm + pd - 1.0) > 1e-10:
        raise ValueError(f"Las probabilidades no suman 1: {pu + pm + pd}")
    
    return pu, pm, pd
  
if __name__ == "__main__":
    # Ejemplo de uso
    S0 = 90.125
    K = 100
    T = 1
    r = 0.1
    sigma = 0.25
    H = 90
    M = 4

    print(f"S0: {S0}\nK: {K}\nT: {T}\nr: {r}\nsigma: {sigma}\nH: {H}\nM: {M}\n")    

    # Calcular con AMM
    value_amm = AMM_Barrier_Recursivo(S0, K, T, r, sigma, H, M)
    print(f"\nValor AMM: {value_amm}")
