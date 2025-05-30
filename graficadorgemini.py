import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button # Importar Slider y Button

# 1. Definir el sistema de ecuaciones diferenciales (igual que antes)
def sir_model(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

# 2. Definir parámetros iniciales y condiciones
N = 10000
I0 = 3000
R0 = 0
S0 = N - I0 - R0
y0 = [S0, I0, R0]

# Rango de tiempo
t = np.linspace(0, 160, 160)

# Valores iniciales para los deslizadores
initial_beta = 0.2
initial_gamma = 0.1

# 3. Configurar la figura y los ejes para el gráfico y los deslizadores
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(left=0.1, bottom=0.45) # Ajustar para dejar espacio para los deslizadores

# Líneas iniciales del gráfico
# Ahora pasamos datos dummy (o los datos iniciales) para evitar el error
# La función update() luego actualizará estos datos.
# Podemos pasar 't' y un array de ceros con la misma forma que 't'
line_S, = ax.plot(t, np.zeros_like(t), 'g', alpha=0.7, lw=2, label='Susceptibles (S)')
line_I, = ax.plot(t, np.zeros_like(t), 'r', alpha=0.7, lw=2, label='Infectados (I)')
line_R, = ax.plot(t, np.zeros_like(t), 'k', alpha=0.7, lw=2, label='Recuperados (R)')
ax.set_xlabel('Tiempo (días)')
ax.set_ylabel('Número de individuos')
ax.set_title('Modelo SIR Interactivo')
ax.legend()
ax.grid(True)

# Establecer límites iniciales del eje Y (pueden ser dinámicos si lo deseas)



# 4. Crear los ejes para los deslizadores
axcolor = 'lightgoldenrodyellow'
ax_N = plt.axes([0.1, 0.3, 0.8, 0.03], facecolor=axcolor)
ax_I0 = plt.axes([0.1, 0.25, 0.8, 0.03], facecolor=axcolor)
ax_beta = plt.axes([0.1, 0.2, 0.8, 0.03], facecolor=axcolor) # [izquierda, abajo, ancho, alto]
ax_gamma = plt.axes([0.1, 0.15, 0.8, 0.03], facecolor=axcolor)
ax_R0 = plt.axes([0.1, 0.1, 0.8, 0.03], facecolor=axcolor) # Para mostrar R0 (solo lectura)


# Crear los deslizadores
slider_N = Slider(ax_N, 'Poblacion\ntotal', 500, 50000, valinit=N, valstep=100)
slider_I0 = Slider(ax_I0, 'Infectados\niniciales', 10, 25000, valinit=I0, valstep=10)
slider_beta = Slider(ax_beta, 'Beta (β)', 0.01, 1.0, valinit=initial_beta, valstep=0.01)
slider_gamma = Slider(ax_gamma, 'Gamma (γ)', 0.01, 0.5, valinit=initial_gamma, valstep=0.01)

# Texto para mostrar R0 (no es un slider, es solo un texto que se actualiza)
# Inicialmente lo dejamos vacío o con un valor temporal
R0_text = ax_R0.text(0.5, 0.5, '', transform=ax_R0.transAxes, ha='center', va='center', fontsize=10)
ax_R0.set_xticks([]) # Ocultar ticks del eje x
ax_R0.set_yticks([]) # Ocultar ticks del eje y
ax_R0.set_facecolor(axcolor) # Fondo para que parezca parte de los controles


# 5. Función de actualización para los deslizadores
def update(val=None): # val es el valor del slider, lo hacemos opcional
    N_val = slider_N.val
    y0 = [slider_N.val - slider_I0.val, slider_I0.val, R0]
    beta_val = slider_beta.val
    gamma_val = slider_gamma.val

    ax.set_ylim(0, N_val * 1.05)

    # Resolver el modelo SIR con los nuevos parámetros
    sol = odeint(sir_model, y0, t, args=(N_val, beta_val, gamma_val))
    S_t, I_t, R_t = sol[:, 0], sol[:, 1], sol[:, 2]

    # Actualizar los datos de las líneas
    line_S.set_ydata(S_t)
    line_I.set_ydata(I_t)
    line_R.set_ydata(R_t)

    # Actualizar el texto de R0
    R0_calc = beta_val / gamma_val
    R0_text.set_text(f'R0 (β/γ): {R0_calc:.2f}')

    # Redibujar el canvas
    fig.canvas.draw_idle()

# 6. Conectar los deslizadores a la función de actualización
slider_N.on_changed(update)
slider_I0.on_changed(update)
slider_beta.on_changed(update)
slider_gamma.on_changed(update)

# !!! CORRECCIÓN CRÍTICA: Llamar a update() una vez al principio
update() # Esto inicializa las líneas con datos reales antes de mostrar el gráfico

# Opcional: Botón de reset
resetax = plt.axes([0.8, 0.02, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    slider_N.reset()
    slider_I0.reset()
    slider_beta.reset()
    slider_gamma.reset()
    # update() se llamará automáticamente porque los sliders se resetearán

button.on_clicked(reset)

plt.show()

