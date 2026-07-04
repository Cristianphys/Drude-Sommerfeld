import numpy as np
from scipy import constants
import matplotlib.pyplot as plt

# Parametros fisicos
e = constants.e          # Carga del electrón [C]
me = constants.m_e       # Masa del electrón [kg]
hbar = constants.hbar    # Constante de Planck reducida [J·s]

# deficion de las funciones usadas
def velocidad_fermi(n):
    """
    Calcula la velocidad de Fermi para una densidad electrónica n
    v_F = (ℏ/m_e) * (3π²n)^(1/3)
    """
    k_F = (3 * np.pi**2 * n)**(1/3)
    v_F = hbar * k_F / me
    return v_F

def trayectoria_libre_media(n, rho):
    """
    Calcula la trayectoria libre media para una densidad n y resistividad ρ
    ℓ = v_F * τ = v_F * (m_e / n e² ρ)
    """
    v_F = velocidad_fermi(n)
    tau = me / (n * e**2 * rho)
    l = v_F * tau
    return l

#Tabulacion de los metales reales
# Metales con sus densidades electrónicas y resistividades a 300 K
metales = {
    'Li': {'n': 4.70e28, 'rho': 9.28e-8, 'color': '#e41a1c', 'nombre': 'Litio'},
    'Na': {'n': 2.65e28, 'rho': 4.77e-8, 'color': '#377eb8', 'nombre': 'Sodio'},
    'K':  {'n': 1.40e28, 'rho': 7.20e-8, 'color': '#4daf4a', 'nombre': 'Potasio'},
    'Cu': {'n': 8.47e28, 'rho': 1.68e-8, 'color': '#984ea3', 'nombre': 'Cobre'},
    'Ag': {'n': 5.86e28, 'rho': 1.59e-8, 'color': '#ff7f00', 'nombre': 'Plata'},
    'Au': {'n': 5.90e28, 'rho': 2.21e-8, 'color': '#f781bf', 'nombre': 'Oro'},
    'Al': {'n': 1.81e29, 'rho': 2.65e-8, 'color': '#a65628', 'nombre': 'Aluminio'},
    'Fe': {'n': 1.70e29, 'rho': 9.61e-8, 'color': '#999999', 'nombre': 'Hierro'},
    'Mg': {'n': 8.61e28, 'rho': 4.39e-8, 'color': '#66c2a5', 'nombre': 'Magnesio'},
    'Zn': {'n': 1.32e29, 'rho': 5.92e-8, 'color': '#fc8d62', 'nombre': 'Zinc'},
}

# Creacion de las figuras
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Velocidad de Fermi y Trayectoria Libre Media\npara Densidades Electrónicas Metálicas', 
             fontsize=14, fontweight='bold')

# GRÁFICO 1: Velocidad de Fermi vs Densidad Electrónica 
ax1 = axes[0]

# Curva teórica continua - extendemos el rango de densidades
n_teo = np.logspace(27, 31, 300)  # desde 10²⁷ hasta 10³¹ m⁻³ (rango ampliado)
v_F_teo = velocidad_fermi(n_teo)

ax1.plot(n_teo, v_F_teo/1e6, 'k-', linewidth=2, alpha=0.7, 
         label=r'Teoría: $v_F = \frac{\hbar}{m_e}(3\pi^2 n)^{1/3}$')

# Puntos de metales reales
for simbolo, datos in metales.items():
    n = datos['n']
    v_F = velocidad_fermi(n)
    ax1.plot(n, v_F/1e6, 'o', color=datos['color'], markersize=12, 
            markeredgecolor='black', markeredgewidth=1.5,
            label=f"{datos['nombre']} ({simbolo})")
    # Agregar etiqueta con el valor
    ax1.annotate(f'{v_F/1e6:.2f}', 
                xy=(n, v_F/1e6), 
                xytext=(5, 10), textcoords='offset points',
                fontsize=8, fontweight='bold',
                color=datos['color'])

ax1.set_xscale('log')
ax1.set_yscale('log')  # Escala logarítmica en Y para mejor visualización
ax1.set_xlabel('Densidad electrónica n [m⁻³]', fontsize=11)
ax1.set_ylabel('Velocidad de Fermi v_F [10⁶ m/s]', fontsize=11)
ax1.set_title('Velocidad de Fermi vs Densidad Electrónica', fontsize=12, fontweight='bold')
ax1.legend(fontsize=8, loc='lower right', ncol=2)
ax1.grid(True, alpha=0.3, which='both')
ax1.set_xlim(5e27, 5e29)  # Rango X ampliado

# Rango Y ampliado para ver mejor la variación
ax1.set_ylim(0.3, 10)  # Desde 0.3 hasta 10 (10⁶ m/s)

# Agregar línea de velocidad de la luz para comparación
ax1.axhline(y=300, color='red', linestyle='--', linewidth=1.5, alpha=0.6)
ax1.text(1.5e28, 250, 'c = 300×10⁶ m/s\n(~1% de c es típico en metales)', 
         fontsize=9, color='red', alpha=0.7,
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# Agregar líneas de referencia adicionales
ax1.axhline(y=1, color='gray', linestyle=':', linewidth=0.8, alpha=0.4)
ax1.axhline(y=5, color='gray', linestyle=':', linewidth=0.8, alpha=0.4)

# Anotación para el rango típico de metales
ax1.annotate('Rango típico\nde metales', xy=(3e28, 1.5), 
            fontsize=9, ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8))

# GRÁFICO 2: Trayectoria Libre Media vs Densidad Electrónica
ax2 = axes[1]

for simbolo, datos in metales.items():
    n = datos['n']
    rho = datos['rho']
    l = trayectoria_libre_media(n, rho)
    
    ax2.plot(n, l*1e9, 'o', color=datos['color'], markersize=14,
            markeredgecolor='black', markeredgewidth=1.5,
            label=f"{datos['nombre']} ({simbolo})")
    
    # Agregar etiqueta con el valor
    ax2.annotate(f'{l*1e9:.1f} nm', 
                xy=(n, l*1e9), 
                xytext=(5, 10), textcoords='offset points',
                fontsize=8, fontweight='bold',
                color=datos['color'])

# Líneas de tendencia para grupos de metales
# Metales nobles (Cu, Ag, Au) - baja resistividad
n_nobles = np.array([metales[m]['n'] for m in ['Cu', 'Ag', 'Au']])
l_nobles = np.array([trayectoria_libre_media(metales[m]['n'], metales[m]['rho'])*1e9 for m in ['Cu', 'Ag', 'Au']])

# Ajuste simple para visualizar tendencia
z_nobles = np.polyfit(n_nobles, l_nobles, 1)
p_nobles = np.poly1d(z_nobles)
n_range = np.linspace(5e28, 9e28, 50)
ax2.plot(n_range, p_nobles(n_range), '--', color='gold', linewidth=1.5, alpha=0.6,
        label='Tendencia metales nobles')

ax2.set_xscale('log')
ax2.set_yscale('log')  # También escala logarítmica en Y para mejor visualización
ax2.set_xlabel('Densidad electrónica n [m⁻³]', fontsize=11)
ax2.set_ylabel('Trayectoria libre media ℓ [nm]', fontsize=11)
ax2.set_title('Trayectoria Libre Media a 300 K vs Densidad Electrónica', fontsize=12, fontweight='bold')
ax2.legend(fontsize=8, loc='upper left', ncol=2)
ax2.grid(True, alpha=0.3, which='both')
ax2.set_xlim(8e27, 3e29)
ax2.set_ylim(1, 100)  # Rango Y ampliado para mejor visualización

# Agregar líneas de referencia para distancias interatómicas
ax2.axhline(y=0.3, color='gray', linestyle=':', linewidth=0.8, alpha=0.5)
ax2.text(2.5e29, 0.32, 'Distancia interatómica típica (~0.3 nm)', 
         fontsize=7, color='gray', alpha=0.7, rotation=0)

# Agregar líneas de referencia adicionales
ax2.axhline(y=10, color='blue', linestyle='--', linewidth=0.8, alpha=0.4)
ax2.text(1.5e28, 9, '10 nm', fontsize=8, color='blue', alpha=0.6)
ax2.axhline(y=50, color='blue', linestyle='--', linewidth=0.8, alpha=0.4)
ax2.text(1.5e28, 45, '50 nm', fontsize=8, color='blue', alpha=0.6)

plt.tight_layout()
plt.savefig('velocidad_fermi_trayectoria_libre.png', dpi=150, bbox_inches='tight')
plt.show()

# Resumen de los valores numericos

print("\n" + "="*75)
print("RESUMEN: VELOCIDAD DE FERMI Y TRAYECTORIA LIBRE MEDIA")
print("="*75)
print(f"{'Metal':<15} {'n [m⁻³]':<15} {'v_F [10⁶ m/s]':<18} {'ℓ [nm]':<12} {'% de c':<10}")
print("-"*75)

for simbolo, datos in metales.items():
    n = datos['n']
    v_F = velocidad_fermi(n)
    l = trayectoria_libre_media(n, datos['rho'])
    pct_c = (v_F / 3e8) * 100
    print(f"{datos['nombre']:<15} {n:<15.2e} {v_F/1e6:<18.3f} {l*1e9:<12.2f} {pct_c:<10.2f}%")

print("-"*75)
print(f"\n NOTAS:")
print(f"   • La trayectoria libre media a 300 K es de decenas de nanómetros")
print(f"   • Esto equivale a ~100-1000 distancias interatómicas")
print(f"   • A bajas temperaturas, ℓ puede alcanzar micras o milímetros")
print("="*75)
