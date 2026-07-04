import numpy as np
from scipy.optimize import curve_fit
from scipy import constants
import matplotlib.pyplot as plt

# Constantes físicas
e = constants.e
me = constants.m_e
hbar = constants.hbar

# 1. DEFINICIÓN DEL MODELO
def rho_model(T, rho0, B, p):
    return rho0 + B * T**p

def sigma_model(T, rho0, B, p):
    return 1.0 / rho_model(T, rho0, B, p)

# 2. GENERACIÓN DE DATOS SINTÉTICOS
T = np.linspace(5, 300, 150)
rho0_base = 1.5e-8
B_base = 2.0e-16

exponentes = [1, 2, 3, 5]
nombres_exponentes = {
    1: 'p=1 (lineal)',
    2: 'p=2 (bajas T)',
    3: 'p=3 (especial)',
    5: 'p=5 (altas T)'
}

rho_true_dict = {}
rho_obs_dict = {}
sigma_true_dict = {}
sigma_obs_dict = {}

rng = np.random.default_rng(42)
ruido_relativo = 0.03

for p in exponentes:
    B = B_base * (300**5) / (300**p)
    rho_true_dict[p] = rho_model(T, rho0_base, B, p)
    noise = rng.normal(0, ruido_relativo * rho_true_dict[p])
    rho_obs_dict[p] = rho_true_dict[p] + noise
    sigma_true_dict[p] = sigma_model(T, rho0_base, B, p)
    sigma_obs_dict[p] = 1.0 / rho_obs_dict[p]

# 3. AJUSTE DE CURVAS
def fit_rho_model(T, rho0, B, p):
    return rho_model(T, rho0, B, p)

resultados_ajuste = {}

for p in exponentes:
    popt, pcov = curve_fit(
        lambda T, rho0, B: fit_rho_model(T, rho0, B, p),
        T,
        rho_obs_dict[p],
        p0=[1e-8, 1e-16]
    )
    rho0_fit, B_fit = popt
    resultados_ajuste[p] = {
        'rho0_fit': rho0_fit,
        'B_fit': B_fit
    }

# 4. VISUALIZACIÓN - SOLO DOS GRÁFICAS
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Modelo Drude-Sommerfeld', fontsize=14, fontweight='bold')

colores = {1: '#e41a1c', 2: '#377eb8', 3: '#4daf4a', 5: '#984ea3'}

# Gráfico 1: Resistividad vs Temperatura
for p in exponentes:
    ax1.plot(T, rho_true_dict[p], '-', color=colores[p], linewidth=2,
            label=nombres_exponentes[p])
    ax1.plot(T, rho_obs_dict[p], '.', color=colores[p], markersize=3, alpha=0.5)
ax1.set_xlabel('Temperatura [K]')
ax1.set_ylabel(r'$\rho(T)$ [$\Omega\cdot$m]')
ax1.set_title('Resistividad')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_yscale('log')

# Gráfico 2: Conductividad vs Temperatura
for p in exponentes:
    ax2.plot(T, sigma_true_dict[p]/1e7, '-', color=colores[p], linewidth=2,
            label=nombres_exponentes[p])
ax2.set_xlabel('Temperatura [K]')
ax2.set_ylabel(r'$\sigma(T)$ [10$^7$ S/m]')
ax2.set_title('Conductividad')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
