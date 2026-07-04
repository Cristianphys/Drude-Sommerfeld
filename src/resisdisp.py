import numpy as np
from scipy.optimize import curve_fit
from scipy import constants
import matplotlib.pyplot as plt
from scipy.stats import norm
#parametros fisicos
e = constants.e          # Carga del electrón [C]
me = constants.m_e       # Masa del electrón [kg]
hbar = constants.hbar    # Constante de Planck reducida [J·s]
kB = constants.k         # Constante de Boltzmann [J/K]

def rho_model(T, rho0, B, p):

    return rho0 + B * T**p


# Parámetros verdaderos que queremos recuperar
rho0_true = 1.5e-8     # Resistividad residual [Ω·m] (típica de cobre puro)
B_true = 2.5e-15        # Coeficiente [Ω·m/K^5]
p_true = 5              # Exponente de Bloch-Grüneisen

print("="*70)
print("AJUSTE POR MÍNIMOS CUADRADOS NO LINEALES")
print("Modelo: ρ(T) = ρ₀ + B·T^p")
print("="*70)
print(f"\nParámetros verdaderos (DESCONOCIDOS):")
print(f"  ρ₀ = {rho0_true:.4e} Ω·m")
print(f"  B  = {B_true:.4e} Ω·m/K^{p_true}")
print(f"  p  = {p_true}")
print(f"  σ₀ = {1/rho0_true:.2e} S/m (conductividad residual)")

# Rango de temperatura [K]
T = np.linspace(5, 300, 150)

# Semilla para reproducibilidad
rng = np.random.default_rng(42)

# Ruido experimental relativo (3% como en experimentos típicos)
ruido_relativo = 0.03

# Generar datos "verdaderos" y añadir ruido
rho_true = rho_model(T, rho0_true, B_true, p_true)
noise = rng.normal(0, ruido_relativo * rho_true)
rho_obs = rho_true + noise

# Incertidumbre estimada para cada punto
sigma_rho = ruido_relativo * rho_obs

print(f"\nDatos generados:")
print(f"  Número de puntos: {len(T)}")
print(f"  Rango T: [{T[0]:.1f}, {T[-1]:.1f}] K")
print(f"  Ruido relativo: {ruido_relativo*100:.1f}%")
print(f"  ρ(5K)  = {rho_obs[0]:.4e} Ω·m")
print(f"  ρ(300K)= {rho_obs[-1]:.4e} Ω·m")

#ajustes por minimo cuadrados lineales
print("\n" + "="*70)
print("PROCESO DE AJUSTE (curve_fit)")
print("="*70)

# Definir función para curve_fit
def fit_function(T, rho0, B):
    """Función de ajuste con p fijo = 5 (Bloch-Grüneisen)"""
    return rho_model(T, rho0, B, p_true)

# Valores iniciales (estimaciones razonables)
p0 = [1e-8, 1e-15]

print(f"\nValores iniciales para el ajuste:")
print(f"  ρ₀ inicial = {p0[0]:.2e} Ω·m")
print(f"  B inicial  = {p0[1]:.2e} Ω·m/K^{p_true}")

# Realizar el ajuste con incertidumbres (ajuste ponderado)
popt, pcov = curve_fit(
    fit_function,     # Función modelo
    T,                # temperatura
    rho_obs,          # resistividad observada
    p0=p0,            # Valores iniciales
    sigma=sigma_rho,  # Incertidumbres
    absolute_sigma=False  # Solo pesos relativos
)

# Extraer parámetros ajustados e incertidumbres
rho0_fit, B_fit = popt
rho0_err, B_err = np.sqrt(np.diag(pcov))

print(f"\nResultados del ajuste:")
print(f"  ρ₀ = ({rho0_fit:.4e} ± {rho0_err:.4e}) Ω·m")
print(f"  B  = ({B_fit:.4e} ± {B_err:.4e}) Ω·m/K^{p_true}")

# Valores predichos por el modelo ajustado
rho_pred = fit_function(T, rho0_fit, B_fit)

# Residuos
residuos = rho_obs - rho_pred
residuos_normalizados = residuos / sigma_rho

# Estadísticos de bondad del ajuste
# R² (coeficiente de determinación)
ss_res = np.sum(residuos**2)
ss_tot = np.sum((rho_obs - np.mean(rho_obs))**2)
R2 = 1 - ss_res/ss_tot

# Chi-cuadrado reducido
chi2 = np.sum(residuos_normalizados**2)
dof = len(T) - 2  # grados de libertad (N - número de parámetros)
chi2_red = chi2 / dof

print(f"\nEstadísticos de bondad del ajuste:")
print(f"  R² = {R2:.6f}")
print(f"  χ² = {chi2:.2f}")
print(f"  χ²/dof = {chi2_red:.4f}")
print(f"  Grados de libertad = {dof}")

# Interpretación del χ² reducido
if 0.5 < chi2_red < 1.5:
    print(f" χ²/dof ≈ 1 → El ajuste es EXCELENTE")
elif chi2_red < 2.0:
    print(f"  χ²/dof > 1.5 → Ajuste aceptable pero con dispersión")
else:
    print(f" χ²/dof > 2 → Posible subestimación de errores o modelo inadecuado")

print("\n" + "="*70)
print("COMPARACIÓN: VALORES VERDADEROS vs AJUSTADOS")
print("="*70)

# Diferencia en unidades de incertidumbre (significancia estadística)
rho0_dif = (rho0_fit - rho0_true) / rho0_err
B_dif = (B_fit - B_true) / B_err

print(f"\n  ρ₀:")
print(f"    Verdadero: {rho0_true:.4e} Ω·m")
print(f"    Ajustado:  {rho0_fit:.4e} ± {rho0_err:.4e} Ω·m")
print(f"    Diferencia: {abs(rho0_fit - rho0_true):.4e} Ω·m ({rho0_dif:.2f}σ)")

print(f"\n  B:")
print(f"    Verdadero: {B_true:.4e} Ω·m/K^{p_true}")
print(f"    Ajustado:  {B_fit:.4e} ± {B_err:.4e} Ω·m/K^{p_true}")
print(f"    Diferencia: {abs(B_fit - B_true):.4e} Ω·m/K^{p_true} ({B_dif:.2f}σ)")

# Verificar si los parámetros verdaderos están dentro del intervalo de confianza
if abs(rho0_dif) < 2:
    print(f"\n ρ₀ está dentro del intervalo de confianza del 95%")
else:
    print(f"\n ρ₀ FUERA del intervalo de confianza")

if abs(B_dif) < 2:
    print(f" B está dentro del intervalo de confianza del 95%")
else:
    print(f" B FUERA del intervalo de confianza")

# apartado de las graficas
fig, axes = plt.subplots(1, 2, figsize=(14, 6))  # Cambiado a 1x2
fig.suptitle('Ajuste de Resistividad por Mínimos Cuadrados No Lineales\n' +
             f'Modelo: ρ(T) = ρ₀ + B·T^{p_true} (Bloch-Grüneisen)', 
             fontsize=14, fontweight='bold')

#  Gráfico 1: Datos y ajuste
ax1 = axes[0]
# Datos experimentales con barras de error
ax1.errorbar(T, rho_obs*1e8, yerr=sigma_rho*1e8, 
             fmt='o', color='#377eb8', markersize=4, alpha=0.6,
             capsize=2, label='Datos experimentales')
# Curva verdadera
ax1.plot(T, rho_true*1e8, '-', color='black', linewidth=2, 
         label='Modelo real (desconocido)')
# Curva ajustada
ax1.plot(T, rho_pred*1e8, '--', color='red', linewidth=2.5,
         label='Ajuste por mínimos cuadrados')
ax1.set_xlabel('Temperatura [K]', fontsize=11)
ax1.set_ylabel(r'$\rho(T)$ [10$^{-8}$ Ω·m]', fontsize=11)
ax1.set_title('Datos experimentales y ajuste', fontsize=12)
ax1.legend(fontsize=9, loc='upper left')
ax1.grid(True, alpha=0.3)
# Agregar caja con parámetros
textstr = f'Ajuste:\nρ₀ = ({rho0_fit:.2e}±{rho0_err:.2e}) Ω·m\nB = ({B_fit:.2e}±{B_err:.2e}) Ω·m/K$^{p_true}$\nR² = {R2:.4f}'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax1.text(0.05, 0.95, textstr, transform=ax1.transAxes, fontsize=9,
         verticalalignment='top', bbox=props)

# Gráfico de residuos 
ax2 = axes[1]
ax2.plot(T, residuos*1e8, 'o', color='#e41a1c', markersize=4, alpha=0.6)
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
ax2.fill_between(T, -2*sigma_rho*1e8, 2*sigma_rho*1e8, 
                  alpha=0.2, color='gray', label='Banda ±2σ')
ax2.set_xlabel('Temperatura [K]', fontsize=11)
ax2.set_ylabel('Residuos [10$^{-8}$ Ω·m]', fontsize=11)
ax2.set_title('Residuos del ajuste', fontsize=12)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
#ejecutar resultados numericos
print("\n" + "="*70)
print("RESUMEN DEL AJUSTE POR MÍNIMOS CUADRADOS NO LINEALES")
print("="*70)
print(f"\n Parámetros recuperados exitosamente:")
print(f" ρ₀ = {rho0_fit:.4e} ± {rho0_err:.4e} Ω·m  (diferencia: {rho0_dif:.1f}σ)")
print(f" B  = {B_fit:.4e} ± {B_err:.4e} Ω·m/K^{p_true}  (diferencia: {B_dif:.1f}σ)")
print(f"\n Calidad del ajuste:")
print(f" R² = {R2:.6f}  (1 = ajuste perfecto)")
print(f" χ²/dof = {chi2_red:.3f}  (≈1 = errores bien estimados)")
print(f"\n Interpretación física:")
print(f" - ρ₀ representa dispersión por impurezas (independiente de T)")
print(f" - B cuantifica la intensidad de interacción electrón-fonón")
print(f" - El ajuste valida la Regla de Matthiessen")
