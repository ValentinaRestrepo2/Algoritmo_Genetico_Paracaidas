import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Algoritmo_genetico as ag

class SimuladorParacaidista:

    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo Genético para caída de Paracaidista")
        self.root.geometry("1400x900")
        self.root.configure(bg="#F0F0F0")

        self.poblacion = []
        self.generacion = 0
        self.historico_fitness = []
        self.historico_velocidad = []
        self.historico_fuerza = []
        self.historico_tiempo = []
        self.num_generaciones = 0

        self.crear_widgets()

    def crear_widgets(self):
        
        # Panel superior (controles y simulación)
        self.panel_superior = ttk.Frame(self.root, padding="10")
        self.panel_superior.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo para controles y estado
        self.panel_izquierda = ttk.LabelFrame(self.panel_superior, text="Parámetros")
        self.panel_izquierda.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.crear_inputs_parametros(self.panel_izquierda)

        # Panel central para la simulación visual
        self.panel_central = ttk.LabelFrame(self.panel_superior, text="Simulación")
        self.panel_central.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas_animacion = tk.Canvas(self.panel_central, bg="lightblue")
        self.canvas_animacion.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas_animacion.create_line(0, 500, 1000, 500, fill="brown", width=5) # Suelo
        
        # Panel derecho para mostrar variables
        self.panel_derecha = ttk.Frame(self.panel_superior)
        self.panel_derecha.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Variables actuales
        self.panel_vars_actuales = ttk.LabelFrame(self.panel_derecha, text="Variables actuales")
        self.panel_vars_actuales.pack(fill=tk.X, pady=5)
        self.etiquetas_variables_actuales(self.panel_vars_actuales)
        
        # Variables mejor individuo
        self.panel_resultados_finales = ttk.LabelFrame(self.panel_derecha, text=" Resultado mejor individuo")
        self.panel_resultados_finales.pack(fill=tk.X, pady=5)
        self.etiquetas_mejor_individuo(self.panel_resultados_finales)

        # Panel gráficas
        self.panel_inferior = ttk.LabelFrame(self.root, text="Gráficas")
        self.panel_inferior.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.crear_multiples_graficos(self.panel_inferior)

    def crear_inputs_parametros(self, panel):
        ttk.Label(panel, text="Tamaño de la Población:").pack(pady=5, padx=10, anchor="w")
        self.entrada_poblacion = ttk.Entry(panel)
        self.entrada_poblacion.insert(0, "50")
        self.entrada_poblacion.pack(pady=5, padx=10, anchor="w")

        ttk.Label(panel, text="Probabilidad de Mutación:").pack(pady=5, padx=10, anchor="w")
        self.entrada_mutacion = ttk.Entry(panel)
        self.entrada_mutacion.insert(0, "0.1")
        self.entrada_mutacion.pack(pady=5, padx=10, anchor="w")

        ttk.Label(panel, text="Número de Generaciones:").pack(pady=5, padx=10, anchor="w")
        self.entrada_generaciones = ttk.Entry(panel)
        self.entrada_generaciones.insert(0, "100")
        self.entrada_generaciones.pack(pady=5, padx=10, anchor="w")
        
        ttk.Label(panel, text="Masa del Paracaidista (kg):").pack(pady=5, padx=10, anchor="w")
        self.entrada_masa = ttk.Entry(panel)
        self.entrada_masa.insert(0, "80")
        self.entrada_masa.pack(pady=5, padx=10, anchor="w")

        self.boton_iniciar = ttk.Button(panel, text="Iniciar Simulación", command=self.iniciar_simulacion)
        self.boton_iniciar.pack(pady=10, padx=10, anchor="center")

        self.boton_reiniciar = ttk.Button(panel, text="Reiniciar", command=self.reiniciar_simulacion, state=tk.DISABLED)
        self.boton_reiniciar.pack(pady=10, padx=10, anchor="center")
        
        # Panel de estado
        self.panel_estado = ttk.LabelFrame(panel, text="Estado")
        self.panel_estado.pack(fill=tk.X, pady=10, padx=10)
        self.label_estado_simulacion = ttk.Label(self.panel_estado, text="Listo para simular", font=("Arial", 12, "bold"))
        self.label_estado_simulacion.pack(pady=10)

    def etiquetas_variables_actuales(self, panel):
        self.label_generacion = ttk.Label(panel, text="Generación: --", font=("Arial", 12))
        self.label_generacion.pack(pady=5, padx=10, anchor="w")
        self.label_fuerza = ttk.Label(panel, text="Fuerza de Paracaídas: --", font=("Arial", 12))
        self.label_fuerza.pack(pady=5, padx=10, anchor="w")
        self.label_velocidad = ttk.Label(panel, text="Velocidad Final: --", font=("Arial", 12))
        self.label_velocidad.pack(pady=5, padx=10, anchor="w")
        self.label_tiempo = ttk.Label(panel, text="Tiempo: --", font=("Arial", 12))
        self.label_tiempo.pack(pady=5, padx=10, anchor="w")
        self.label_fitness = ttk.Label(panel, text="Fitness: --", font=("Arial", 12))
        self.label_fitness.pack(pady=5, padx=10, anchor="w")
        
    def etiquetas_mejor_individuo(self, panel):
        self.label_titulo_final = ttk.Label(panel, text="Mejor Individuo Final", font=("Arial", 12, "bold"))
        self.label_titulo_final.pack(pady=5, padx=10, anchor="w")
        self.label_fuerza_final = ttk.Label(panel, text="Fuerza de Paracaídas: --", font=("Arial", 12))
        self.label_fuerza_final.pack(pady=5, padx=10, anchor="w")
        self.label_velocidad_final = ttk.Label(panel, text="Velocidad Final: --", font=("Arial", 12))
        self.label_velocidad_final.pack(pady=5, padx=10, anchor="w")
        self.label_tiempo_final = ttk.Label(panel, text="Tiempo: --", font=("Arial", 12))
        self.label_tiempo_final.pack(pady=5, padx=10, anchor="w")
        self.label_fitness_final = ttk.Label(panel, text="Fitness: --", font=("Arial", 12))
        self.label_fitness_final.pack(pady=5, padx=10, anchor="w")

    def crear_multiples_graficos(self, panel):
        self.fig, (self.ax1, self.ax2, self.ax3, self.ax4) = plt.subplots(1, 4, figsize=(13, 3))
        
        # Configurar cada subgráfico
        self.configurar_grafico(self.ax1, 'Evolución del Fitness', 'Generación', 'Fitness')
        self.configurar_grafico(self.ax2, 'Evolución de la Velocidad', 'Generación', 'Velocidad (m/s)')
        self.configurar_grafico(self.ax3, 'Evolución de la Fuerza', 'Generación', 'Fuerza (N)')
        self.configurar_grafico(self.ax4, 'Evolución del Tiempo', 'Generación', 'Tiempo (s)')

        plt.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=panel)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def configurar_grafico(self, ax, titulo, xlabel, ylabel):
        ax.set_title(titulo, fontsize=10)
        ax.set_xlabel(xlabel, fontsize=8)
        ax.set_ylabel(ylabel, fontsize=8)
        ax.tick_params(axis='x', labelsize=7)
        ax.tick_params(axis='y', labelsize=7)
        ax.grid(True)

    def mostrar_imagen(self, nombre_imagen, x, y):
        try:
            img = Image.open(nombre_imagen)
            img = img.resize((100, 100), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            self.paracaidista_item = self.canvas_animacion.create_image(x, y, image=self.photo, anchor="center")
        except FileNotFoundError:
            messagebox.showerror("Error de Archivo", f"La imagen '{nombre_imagen}' no se encontró en la ruta especificada.")

    def animar_caida(self, individuo):
        self.canvas_animacion.delete("all")
        self.canvas_animacion.create_line(0, 500, 800, 500, fill="brown", width=5) # Suelo
        posicion_inicial = ag.ALTURA_INICIAL
        
        self.mostrar_imagen("Paracaidas.png", self.canvas_animacion.winfo_width() / 2, 50)
        
        for _ in range(100):
            if individuo.posicion <= 0:
                break
            fuerza_neta = (individuo.masa * ag.GRAVEDAD) - individuo.fuerza_paracaidas
            aceleracion = fuerza_neta / individuo.masa
            individuo.velocidad += aceleracion * 1
            individuo.posicion -= individuo.velocidad * 1
            canvas_height = 500
            y_coord = canvas_height - (individuo.posicion / posicion_inicial) * (canvas_height - 50)
            self.canvas_animacion.coords(self.paracaidista_item, self.canvas_animacion.winfo_width() / 2, y_coord)
            self.root.update_idletasks()

        self.canvas_animacion.delete(self.paracaidista_item)
        x_final = self.canvas_animacion.winfo_width() / 2
        y_final = 500 - 50
        if individuo.exito:
            self.mostrar_imagen("Celebracion.png", x_final, y_final)
            self.label_estado_simulacion.config(text="¡Aterrizaje Exitoso!", foreground="green")
        elif individuo.choque:
            self.mostrar_imagen("Choque.png", x_final, y_final)
            self.label_estado_simulacion.config(text="¡Choque!", foreground="red")
        else:
            self.label_estado_simulacion.config(text="En Simulación", foreground="blue")
            
    def actualizar_graficos(self):
        generaciones = range(len(self.historico_fitness))

        self.ax1.clear(); self.configurar_grafico(self.ax1, 'Evolución del Fitness', 'Generación', 'Fitness')
        self.ax1.plot(generaciones, self.historico_fitness, color='b')
        
        self.ax2.clear(); self.configurar_grafico(self.ax2, 'Evolución de la Velocidad', 'Generación', 'Velocidad (m/s)')
        self.ax2.plot(generaciones, self.historico_velocidad, color='r')
        
        self.ax3.clear(); self.configurar_grafico(self.ax3, 'Evolución de la Fuerza', 'Generación', 'Fuerza (N)')
        self.ax3.plot(generaciones, self.historico_fuerza, color='g')
        
        self.ax4.clear(); self.configurar_grafico(self.ax4, 'Evolución del Tiempo', 'Generación', 'Tiempo (s)')
        self.ax4.plot(generaciones, self.historico_tiempo, color='y')
        
        self.canvas.draw()
        
    def iniciar_simulacion(self):
        try:
            self.tamano_poblacion = int(self.entrada_poblacion.get())
            self.prob_mutacion = float(self.entrada_mutacion.get())
            self.num_generaciones = int(self.entrada_generaciones.get())
            self.masa_paracaidista = float(self.entrada_masa.get())

            self.poblacion = ag.getPoblacion(self.tamano_poblacion, self.masa_paracaidista)
            self.generacion = 0
            self.historico_fitness = []
            self.historico_velocidad = []
            self.historico_fuerza = []
            self.historico_tiempo = []
            self.label_estado_simulacion.config(text="Simulando...", foreground="black")

            self.boton_iniciar.config(state=tk.DISABLED)
            self.boton_reiniciar.config(state=tk.NORMAL)
            
            self.correr_simulacion()
            
        except ValueError:
            messagebox.showerror("Error de Parámetros", "Asegúrate de que los valores sean números válidos.")

    def correr_simulacion(self):
        if self.generacion < self.num_generaciones:
            self.poblacion = ag.evolucionar(self.poblacion, self.tamano_poblacion, self.prob_mutacion)
            self.generacion += 1
            mejor_individuo_actual = ag.Get_mejor_individuo(self.poblacion)
            individuo_sim = ag.AlgoritmoGenParacaidas(mejor_individuo_actual.fuerza_paracaidas, mejor_individuo_actual.masa)
            _, velocidad_final, tiempo = individuo_sim.simular_caida()
            fitness = individuo_sim.CalcularAdaptacion()

            self.historico_fitness.append(fitness)
            self.historico_velocidad.append(abs(velocidad_final))
            self.historico_fuerza.append(mejor_individuo_actual.fuerza_paracaidas)
            self.historico_tiempo.append(tiempo)

            self.label_generacion.config(text=f"Generación: {self.generacion}")
            self.label_fuerza.config(text=f"Fuerza de Paracaídas: {mejor_individuo_actual.fuerza_paracaidas:.2f} N")
            self.label_velocidad.config(text=f"Velocidad Final: {velocidad_final:.2f} m/s")
            self.label_tiempo.config(text=f"Tiempo: {tiempo:.2f} s")
            self.label_fitness.config(text=f"Fitness: {fitness:.2f}")

            self.animar_caida(individuo_sim)
            self.actualizar_graficos()
            
            self.root.after(200, self.correr_simulacion)
        else:
            self.finalizar_simulacion()

    def finalizar_simulacion(self):
        self.label_estado_simulacion.config(text="Simulación Finalizada", foreground="black")
        
        mejor_individuo_final = ag.Get_mejor_individuo(self.poblacion)
        _, velocidad_final_final, tiempo_final = mejor_individuo_final.simular_caida()
        
        self.label_fuerza_final.config(text=f"Fuerza de Paracaídas: {mejor_individuo_final.fuerza_paracaidas:.2f} N")
        self.label_velocidad_final.config(text=f"Velocidad Final: {velocidad_final_final:.2f} m/s")
        self.label_tiempo_final.config(text=f"Tiempo: {tiempo_final:.2f} s")
        self.label_fitness_final.config(text=f"Fitness: {mejor_individuo_final.CalcularAdaptacion():.2f}")
        
    def reiniciar_simulacion(self):
        self.poblacion = []
        self.generacion = 0
        self.historico_fitness = []
        self.historico_velocidad = []
        self.historico_fuerza = []
        self.historico_tiempo = []
        
        self.ax1.clear(); self.configurar_grafico(self.ax1, 'Evolución del Fitness', 'Generación', 'Fitness')
        self.ax2.clear(); self.configurar_grafico(self.ax2, 'Evolución de la Velocidad', 'Generación', 'Velocidad (m/s)')
        self.ax3.clear(); self.configurar_grafico(self.ax3, 'Evolución de la Fuerza', 'Generación', 'Fuerza (N)')
        self.ax4.clear(); self.configurar_grafico(self.ax4, 'Evolución del Tiempo', 'Generación', 'Tiempo (s)')
        self.canvas.draw()
        
        self.label_generacion.config(text="Generación: --")
        self.label_fuerza.config(text="Fuerza de Paracaídas: --")
        self.label_velocidad.config(text="Velocidad Final: --")
        self.label_tiempo.config(text="Tiempo: --")
        self.label_fitness.config(text="Fitness: --")

        self.label_fuerza_final.config(text="Fuerza de Paracaídas: --")
        self.label_velocidad_final.config(text="Velocidad Final: --")
        self.label_tiempo_final.config(text="Tiempo: --")
        self.label_fitness_final.config(text="Fitness: --")
        
        self.label_estado_simulacion.config(text="Listo para simular", foreground="black")

        self.boton_iniciar.config(state=tk.NORMAL)
        self.boton_reiniciar.config(state=tk.DISABLED)
        self.canvas_animacion.delete("all")
        self.canvas_animacion.create_line(0, 500, 1000, 500, fill="brown", width=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorParacaidista(root)
    root.mainloop()