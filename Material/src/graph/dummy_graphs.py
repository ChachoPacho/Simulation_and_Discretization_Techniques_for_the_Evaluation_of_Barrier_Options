import os
import numpy as np
import matplotlib.pyplot as plt

def create_dummy_graphs():
    # Asegurar que estamos en el directorio correcto (src/graph)
    graph_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Generando gráficos ilustrativos (Dummy Graphs)...")
    
    # =========================================================================
    # 1. Gráfico payoff CALL: zona de ganancia cuando S > K
    # =========================================================================
    S = np.linspace(60, 140, 500)
    K = 100
    premium = 8  # prima pagada
    payoff_call = np.maximum(S - K, 0)
    profit_call = payoff_call - premium
    
    plt.figure(figsize=(9, 5))
    plt.plot(S, profit_call, label='Beneficio/Pérdida (Call)', color='blue', linewidth=2.5)
    plt.axhline(0, color='black', linewidth=1.5)
    plt.axvline(K, color='gray', linestyle='--', label=f'Strike (K={K})')
    
    # Sombrear ganancia y pérdida
    plt.fill_between(S, 0, profit_call, where=(profit_call >= 0), color='green', alpha=0.3, label='Zona de Ganancia (S > K + Prima)')
    plt.fill_between(S, profit_call, 0, where=(profit_call < 0), color='red', alpha=0.3, label='Zona de Pérdida (Máxima: Prima)')
    
    plt.title('Perfil de Pagos (Payoff) - Opción CALL', fontsize=14)
    plt.xlabel('Precio del Activo Subyacente en Vencimiento (S)', fontsize=12)
    plt.ylabel('Beneficio / Pérdida', fontsize=12)
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.4, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'dummy_payoff_call.png'), dpi=300)
    plt.close()

    # =========================================================================
    # 2. Gráfico payoff PUT: zona de ganancia cuando S < K
    # =========================================================================
    payoff_put = np.maximum(K - S, 0)
    profit_put = payoff_put - premium
    
    plt.figure(figsize=(9, 5))
    plt.plot(S, profit_put, label='Beneficio/Pérdida (Put)', color='purple', linewidth=2.5)
    plt.axhline(0, color='black', linewidth=1.5)
    plt.axvline(K, color='gray', linestyle='--', label=f'Strike (K={K})')
    
    # Sombrear ganancia y pérdida
    plt.fill_between(S, 0, profit_put, where=(profit_put >= 0), color='green', alpha=0.3, label='Zona de Ganancia (S < K - Prima)')
    plt.fill_between(S, profit_put, 0, where=(profit_put < 0), color='red', alpha=0.3, label='Zona de Pérdida (Máxima: Prima)')
    
    plt.title('Perfil de Pagos (Payoff) - Opción PUT', fontsize=14)
    plt.xlabel('Precio del Activo Subyacente en Vencimiento (S)', fontsize=12)
    plt.ylabel('Beneficio / Pérdida', fontsize=12)
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(True, alpha=0.4, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'dummy_payoff_put.png'), dpi=300)
    plt.close()

    # =========================================================================
    # 3. Opción Europea: Línea de tiempo
    # =========================================================================
    plt.figure(figsize=(10, 3))
    plt.plot([0, 1], [0, 0], color='black', linewidth=3)
    
    # Puntos de tiempo
    plt.plot(0, 0, marker='o', markersize=10, color='blue', label='Suscripción (t = 0)')
    plt.plot(1, 0, marker='o', markersize=10, color='red', label='Vencimiento (T)')
    
    plt.annotate('Posibilidad ÚNICA\nde ejercicio', xy=(1, 0.05), xytext=(1, 0.5),
                 arrowprops=dict(facecolor='red', shrink=0.05, width=2, headwidth=10),
                 ha='center', fontsize=11, fontweight='bold')
                 
    plt.title('Línea de Tiempo - Opción Europea', fontsize=14)
    plt.xlim(-0.1, 1.2)
    plt.ylim(-0.5, 1)
    plt.yticks([])  # Ocultar eje Y
    plt.xticks([0, 1], ['t = 0', 'T'], fontsize=12)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.4), ncol=2, fontsize=11)
    plt.box(False) # Quitar bordes de la caja
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'dummy_timeline_european.png'), dpi=300)
    plt.close()

    # =========================================================================
    # 4. Opción Americana: Línea de tiempo
    # =========================================================================
    plt.figure(figsize=(10, 3))
    
    # Rango de ejercicio
    plt.fill_between([0, 1], -0.1, 0.1, color='green', alpha=0.2, label='Período de ejercicio permitido')
    plt.plot([0, 1], [0, 0], color='black', linewidth=3)
    
    # Puntos de tiempo
    plt.plot(0, 0, marker='o', markersize=10, color='blue', label='Suscripción (t = 0)')
    plt.plot(1, 0, marker='o', markersize=10, color='red', label='Vencimiento (T)')
    
    plt.annotate('Puede ejercerse en\nCUALQUIER momento', xy=(0.5, 0.1), xytext=(0.5, 0.5),
                 arrowprops=dict(facecolor='green', shrink=0.05, width=2, headwidth=10),
                 ha='center', fontsize=11, fontweight='bold')
                 
    plt.title('Línea de Tiempo - Opción Americana', fontsize=14)
    plt.xlim(-0.1, 1.2)
    plt.ylim(-0.5, 1)
    plt.yticks([])  # Ocultar eje Y
    plt.xticks([0, 1], ['t = 0', 'T'], fontsize=12)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.4), ncol=3, fontsize=11)
    plt.box(False) # Quitar bordes de la caja
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'dummy_timeline_american.png'), dpi=300)
    plt.close()

    # =========================================================================
    # 5. Trayectoria del precio de la Soja vs Barrera Up-and-Out (H=220)
    # =========================================================================
    np.random.seed(42) # Fijo para reproducibilidad
    N = 252 # Días de trading en el año
    T_time = np.linspace(0, 1, N)
    S0 = 200
    H = 220
    
    # Movimiento Browniano Geométrico para las trayectorias
    dt = 1.0 / N
    
    # Trayectoria 1: No toca la barrera (Sube un poco y baja)
    W1 = np.random.standard_normal(N)
    W1[0] = 0
    W1 = np.cumsum(W1) * np.sqrt(dt)
    # Ajustamos mu y sigma para que se vea bien pero no cruce 220
    path1 = S0 * np.exp((0.02 - 0.5*(0.15**2))*T_time + 0.15*W1)
    if np.max(path1) >= H:
        path1 = path1 - (np.max(path1) - H + 2) # Forzar abajo de la barrera
        
    # Trayectoria 2: Toca la barrera rápidamente y queda cancelada
    np.random.seed(10)
    W2 = np.random.standard_normal(N)
    W2[0] = 0
    W2 = np.cumsum(W2) * np.sqrt(dt)
    path2 = S0 * np.exp((0.25 - 0.5*(0.20**2))*T_time + 0.20*W2)
    
    hit_idx = np.argmax(path2 >= H) # Primer índice donde cruza
    
    plt.figure(figsize=(11, 6))
    
    # Dibujar trayectoria 1
    plt.plot(T_time, path1, color='green', linewidth=2, label='Escenario 1: Normal (Opción activa hasta T)')
    
    # Dibujar trayectoria 2 (dividida en parte activa y parte cancelada)
    plt.plot(T_time[:hit_idx+1], path2[:hit_idx+1], color='red', linewidth=2, label='Escenario 2: Sube fuerte (Cruza H)')
    plt.plot(T_time[hit_idx:], path2[hit_idx:], color='red', linewidth=1.5, linestyle=':', alpha=0.5, label='Evolución post-Knockout (No tiene valor)')
    
    # Barrera H
    plt.axhline(H, color='black', linestyle='--', linewidth=2, label=f'Barrera Up-and-Out (H = ${H})')
    
    # Marcar el evento Knock-out
    plt.plot(T_time[hit_idx], path2[hit_idx], 'rX', markersize=12)
    plt.annotate('KNOCK-OUT\n(Opción Cancelada)', 
                 xy=(T_time[hit_idx], path2[hit_idx]), 
                 xytext=(T_time[hit_idx]-0.15, H+5),
                 arrowprops=dict(facecolor='red', shrink=0.05, width=1, headwidth=8),
                 ha='center', color='red', fontweight='bold')
                 
    plt.title('Dinámica de Precio de Soja en Opción Up-and-Out', fontsize=14)
    plt.xlabel('Tiempo hasta Vencimiento (T)', fontsize=12)
    plt.ylabel('Precio de la Soja ($)', fontsize=12)
    plt.ylim(160, 240)
    plt.legend(loc='lower right', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'dummy_soja_barrera.png'), dpi=300)
    plt.close()
    
    # =========================================================================
    # 6. Árbol Trinomial con Error de Discretización en Barrera
    # =========================================================================
    plt.figure(figsize=(10, 6))
    
    H_tree = 220
    plt.axhline(H_tree, color='red', linestyle='-', linewidth=2, label=f'Barrera Continua (H=${H_tree})')
    
    steps = 3
    S0_tree = 200
    dS = 15
    for t in range(steps):
        nodes_t = [S0_tree + i*dS for i in range(-t, t+1)]
        for val in nodes_t:
            # Dibujar las 3 ramas (Up, Mid, Down)
            plt.plot([t, t+1], [val, val+dS], color='gray', alpha=0.5)
            plt.plot([t, t+1], [val, val], color='gray', alpha=0.5)
            plt.plot([t, t+1], [val, val-dS], color='gray', alpha=0.5)
            
            plt.plot(t, val, 'ko', markersize=7)
            plt.text(t - 0.05, val + 2.5, f"${val}", fontsize=10, ha='right')
            
    # Última capa de nodos
    t_end = steps
    nodes_end = [S0_tree + i*dS for i in range(-t_end, t_end+1)]
    for val in nodes_end:
        plt.plot(t_end, val, 'ko', markersize=7)
        plt.text(t_end + 0.08, val, f"${val}", fontsize=10, va='center')
        
    plt.annotate('ERROR DE DISCRETIZACIÓN:\nEl precio salta de $215 a $230.\nLa barrera de $220 nunca se evalúa\ncon precisión, sobrevaluando la opción.',
                 xy=(2.5, 222.5), xytext=(0.5, 235),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
                 bbox=dict(boxstyle="round", facecolor='yellow', alpha=0.2), fontsize=10)
                 
    plt.title('Error de Discretización en Árboles Trinomiales', fontsize=14)
    plt.xlabel('Pasos de Tiempo (t)', fontsize=12)
    plt.ylabel('Precio del Activo ($)', fontsize=12)
    plt.xticks(range(steps+1), [f't = {i}' for i in range(steps+1)], fontsize=11)
    plt.ylim(150, 250)
    plt.legend(loc='lower left', fontsize=10)
    plt.grid(True, alpha=0.2, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'dummy_trinomial_error.png'), dpi=300)
    plt.close()

    # =========================================================================
    # 7. Principio de Reflexión de Bachelier
    # =========================================================================
    plt.figure(figsize=(10, 6))
    np.random.seed(111)
    N_ref = 200
    t_ref = np.linspace(0, 1, N_ref)
    S0_ref = 100
    H_ref = 120
    
    W_ref = np.random.standard_normal(N_ref)
    W_ref[0] = 0
    W_ref = np.cumsum(W_ref)
    
    # Trayectoria que sube y cruza la barrera
    path_orig = S0_ref + W_ref * 2.5 + t_ref * 25
    hit_idx = np.argmax(path_orig >= H_ref)
    
    path_refl = path_orig.copy()
    # Reflejar los valores posteriores a tau (simétrico respecto a H)
    path_refl[hit_idx:] = H_ref - (path_orig[hit_idx:] - H_ref)
    
    plt.plot(t_ref[:hit_idx+1], path_orig[:hit_idx+1], color='blue', linewidth=2.5, label=r'Trayectoria Compartida ($t \leq \tau$)')
    plt.plot(t_ref[hit_idx:], path_orig[hit_idx:], color='blue', linewidth=2.5, alpha=0.7, label='Trayectoria Original')
    plt.plot(t_ref[hit_idx:], path_refl[hit_idx:], color='orange', linewidth=2.5, linestyle='--', label='Trayectoria Reflejada')
    
    plt.axhline(H_ref, color='red', linestyle='-', linewidth=2, label=f'Barrera ($H={H_ref}$)')
    plt.plot(t_ref[hit_idx], H_ref, 'ko', markersize=9, zorder=5, label=r'Momento de impacto ($\tau$)')
    
    # Sombreado para denotar la simetría
    plt.fill_between(t_ref[hit_idx:], path_orig[hit_idx:], path_refl[hit_idx:], color='gray', alpha=0.1)
    
    plt.annotate('Principio de Reflexión:\nAmbas trayectorias son\nigualmente probables',
                 xy=(t_ref[hit_idx + 40], H_ref),
                 xytext=(t_ref[hit_idx]-0.25, H_ref - 15),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
                 bbox=dict(boxstyle="round", facecolor='yellow', alpha=0.2), fontsize=10)
                 
    plt.title('Principio de Reflexión (Bachelier)', fontsize=14)
    plt.xlabel('Tiempo (t)', fontsize=12)
    plt.ylabel('Precio del Activo ($)', fontsize=12)
    plt.legend(loc='lower right', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'dummy_reflection.png'), dpi=300)
    plt.close()
    
    # =========================================================================
    # 8. Árbol Binomial (Cox-Ross-Rubinstein)
    # =========================================================================
    plt.figure(figsize=(9, 6))
    steps_bin = 3
    S0_bin = 100
    u = 1.15
    d = 0.85
    
    for t in range(steps_bin):
        # Iterar sobre el número de movimientos "down" (j)
        for j in range(t + 1):
            val = S0_bin * (u ** (t - j)) * (d ** j)
            
            val_u = val * u
            val_d = val * d
            
            # Dibujar líneas a los nodos hijos
            plt.plot([t, t+1], [val, val_u], color='gray', alpha=0.6, linewidth=1.5)
            plt.plot([t, t+1], [val, val_d], color='gray', alpha=0.6, linewidth=1.5)
            
            # Dibujar el nodo actual
            plt.plot(t, val, 'bo', markersize=9)
            plt.text(t - 0.05, val + 2, f"${val:.1f}", fontsize=10, ha='right', va='bottom', color='darkblue', fontweight='bold')
            
            # Anotar probabilidades p y 1-p solo en el primer paso para no saturar
            if t == 0:
                plt.text(t + 0.4, val + 4, "p", color='green', fontsize=12, fontweight='bold')
                plt.text(t + 0.4, val - 7, "1-p", color='red', fontsize=12, fontweight='bold')

    # Dibujar la capa final de nodos
    for j in range(steps_bin + 1):
        val = S0_bin * (u ** (steps_bin - j)) * (d ** j)
        plt.plot(steps_bin, val, 'bo', markersize=9)
        plt.text(steps_bin + 0.08, val, f"${val:.1f}", fontsize=10, va='center', color='darkblue', fontweight='bold')
        
    plt.title('Dinámica del Precio en un Árbol Binomial (CRR)', fontsize=14)
    plt.xlabel('Pasos de Tiempo (t)', fontsize=12)
    plt.ylabel('Precio del Activo ($)', fontsize=12)
    plt.xticks(range(steps_bin+1), [f't = {i}' for i in range(steps_bin+1)], fontsize=11)
    
    # Rango en Y dinámico pero con margen
    min_val = S0_bin * (d ** steps_bin)
    max_val = S0_bin * (u ** steps_bin)
    plt.ylim(min_val - 15, max_val + 15)
    
    plt.grid(True, alpha=0.2, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'dummy_binomial_tree.png'), dpi=300)
    plt.close()
    
    # =========================================================================
    # 9. Árbol Trinomial Estándar
    # =========================================================================
    plt.figure(figsize=(9, 6))
    steps_tri = 3
    S0_tri = 100
    
    # Fórmulas explícitas sugeridas (movimiento geométrico)
    sigma = 0.2
    dt = 0.5
    u_tri = np.exp(sigma * np.sqrt(2 * dt))
    d_tri = 1 / u_tri
    
    for t in range(steps_tri):
        for i in range(-t, t+1):
            val = S0_tri * (u_tri ** i)
            
            val_u = val * u_tri
            val_m = val
            val_d = val * d_tri
            
            # Ramas (Up, Mid, Down)
            plt.plot([t, t+1], [val, val_u], color='gray', alpha=0.6, linewidth=1.5)
            plt.plot([t, t+1], [val, val_m], color='gray', alpha=0.6, linewidth=1.5)
            plt.plot([t, t+1], [val, val_d], color='gray', alpha=0.6, linewidth=1.5)
            
            plt.plot(t, val, 'bo', markersize=9)
            plt.text(t - 0.05, val + (val*0.015), f"${val:.1f}", fontsize=10, ha='right', color='darkblue', fontweight='bold')
            
            # Anotar probabilidades teóricas en el primer paso
            if t == 0:
                plt.text(t + 0.4, val_u - (val_u*0.01), "pu", color='green', fontsize=12, fontweight='bold')
                plt.text(t + 0.4, val_m + (val_m*0.01), "pm", color='black', fontsize=12, fontweight='bold')
                plt.text(t + 0.4, val_d + (val_d*0.01), "pd", color='red', fontsize=12, fontweight='bold')

    t_end = steps_tri
    for i in range(-t_end, t_end+1):
        val = S0_tri * (u_tri ** i)
        plt.plot(t_end, val, 'bo', markersize=9)
        plt.text(t_end + 0.08, val, f"${val:.1f}", fontsize=10, va='center', color='darkblue', fontweight='bold')
        
    plt.title('Dinámica del Precio en un Árbol Trinomial Estándar', fontsize=14)
    plt.xlabel('Pasos de Tiempo (t)', fontsize=12)
    plt.ylabel('Precio del Activo ($)', fontsize=12)
    plt.xticks(range(steps_tri+1), [f't = {i}' for i in range(steps_tri+1)], fontsize=11)
    
    # Rango en Y dinámico
    min_val_tri = S0_tri * (d_tri ** steps_tri)
    max_val_tri = S0_tri * (u_tri ** steps_tri)
    plt.ylim(min_val_tri * 0.9, max_val_tri * 1.1)
    
    plt.grid(True, alpha=0.2, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'dummy_trinomial_tree.png'), dpi=300)
    plt.close()

    # =========================================================================
    # 10. Árbol Trinomial RTM (Alineado con Barrera)
    # =========================================================================
    plt.figure(figsize=(10, 6))
    steps_rtm = 3
    S0_rtm = 200
    H_rtm = 230
    
    # RTM ajusta el multiplicador u (y por tanto lambda) para que H coincida exactamente. 
    # Supongamos que llega a H en t=2 hacia arriba
    # S0 * u^2 = H => u = sqrt(H/S0)
    u_rtm = np.sqrt(H_rtm / S0_rtm)
    d_rtm = 1 / u_rtm
    
    plt.axhline(H_rtm, color='red', linestyle='-', linewidth=2, label=f'Barrera (H=${H_rtm})')
    
    for t in range(steps_rtm):
        for i in range(-t, t+1):
            val = S0_rtm * (u_rtm ** i)
            
            # Si toca la barrera (Knock-out) se cancela
            if val >= H_rtm * 0.999 and t > 0: 
                continue
                
            val_u = val * u_rtm
            val_m = val
            val_d = val * d_rtm
                
            plt.plot([t, t+1], [val, val_u], color='gray', alpha=0.6, linewidth=1.5)
            plt.plot([t, t+1], [val, val_m], color='gray', alpha=0.6, linewidth=1.5)
            plt.plot([t, t+1], [val, val_d], color='gray', alpha=0.6, linewidth=1.5)
            
            # Dibujar nodo. Si es de barrera, en rojo
            color_texto = 'darkred' if val >= H_rtm * 0.999 else 'darkblue'
            
            if val >= H_rtm * 0.999:
                plt.plot(t, val, 'ro', markersize=10, zorder=5)
            else:
                plt.plot(t, val, 'bo', markersize=9, zorder=5)
                
            plt.text(t - 0.05, val + (val*0.015), f"${val:.1f}", fontsize=10, ha='right', color=color_texto, fontweight='bold')
            
    # Última capa
    t_end = steps_rtm
    for i in range(-t_end, t_end+1):
        val = S0_rtm * (u_rtm ** i)
        
        # Solo dibujamos los que vienen de un nodo vivo. 
        # (Si en t=2 tocó H_rtm, en t=3 la rama hacia i=3 no se dibuja)
        if i <= 2:
            if val >= H_rtm * 0.999:
                plt.plot(t_end, val, 'ro', markersize=10, zorder=5)
                plt.text(t_end + 0.08, val, f"${val:.1f}", fontsize=10, va='center', color='darkred', fontweight='bold')
            else:
                plt.plot(t_end, val, 'bo', markersize=9, zorder=5)
                plt.text(t_end + 0.08, val, f"${val:.1f}", fontsize=10, va='center', color='darkblue', fontweight='bold')
                 
    plt.title('Árbol Trinomial RTM (Ritchken) Alineado con la Barrera', fontsize=14)
    plt.xlabel('Pasos de Tiempo (t)', fontsize=12)
    plt.ylabel('Precio del Activo ($)', fontsize=12)
    plt.xticks(range(steps_rtm+1), [f't = {i}' for i in range(steps_rtm+1)], fontsize=11)
    
    min_val_rtm = S0_rtm * (d_rtm ** steps_rtm)
    max_val_rtm = S0_rtm * (u_rtm ** steps_rtm)
    plt.ylim(min_val_rtm * 0.9, max_val_rtm * 1.1)
    
    plt.legend(loc='lower left', fontsize=10)
    plt.grid(True, alpha=0.2, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(graph_dir, 'dummy_trinomial_rtm.png'), dpi=300)
    plt.close()
    
    print("==================================================")
    print("10 gráficos generados correctamente en src/graph/")
    print("- dummy_payoff_call.png")
    print("- dummy_payoff_put.png")
    print("- dummy_timeline_european.png")
    print("- dummy_timeline_american.png")
    print("- dummy_soja_barrera.png")
    print("- dummy_trinomial_error.png")
    print("- dummy_reflection.png")
    print("- dummy_binomial_tree.png")
    print("- dummy_trinomial_tree.png")
    print("- dummy_trinomial_rtm.png")
    print("==================================================")

if __name__ == '__main__':
    create_dummy_graphs()
