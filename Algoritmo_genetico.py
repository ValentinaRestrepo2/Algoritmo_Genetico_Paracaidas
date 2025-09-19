import random as rd

# Parametros por defecto
ALTURA_INICIAL = 1000  # metros
GRAVEDAD = 9.8  # m/s^2

class AlgoritmoGenParacaidas:
  
    def __init__(self, fuerza_paracaidas, masa):
        self.fuerza_paracaidas = fuerza_paracaidas
        self.masa = masa
        self.velocidad = 0
        self.posicion = ALTURA_INICIAL
        self.tiempo = 0
        self.exito = False
        self.choque = False

    def simular_caida(self, pasos=1000): # Se aumenta el número de pasos para una simulación más detallada
        delta_t = 1  # Son los segundos por paso
        posiciones = []
        
        for _ in range(pasos):
            if self.posicion <= 0:
                self.posicion = 0
                if abs(self.velocidad) < 2:  # Rango de velocidad para un aterrizaje exitoso
                    self.exito = True
                else:
                    self.choque = True
                break
            
            fuerza_neta = (self.masa * GRAVEDAD) - self.fuerza_paracaidas
            aceleracion = fuerza_neta / self.masa
            
            self.velocidad += aceleracion * delta_t
            self.posicion -= self.velocidad * delta_t
            self.tiempo += delta_t
            
            posiciones.append(self.posicion)
            
        return self.posicion, self.velocidad, self.tiempo, posiciones

    def CalcularAdaptacion(self):
        #Cuanto más cerca esté la velocidad final de 0 es mejor.
        _, velocidad_final, tiempo, _ = self.simular_caida()
        # El fitness es inversamente proporcional al valor absoluto de la velocidad final
        fitness = 1 / (abs(velocidad_final) + 0.001)
        return fitness

def getPoblacion(tamano_poblacion, masa):
    # Población inicial de paracaidistas con fuerzas de paracaídas aleatorias
    rango_FuerzaMax = masa * GRAVEDAD * 1.5  # La fuerza máxima puede ser un 50% mayor a la gravedad
    return [AlgoritmoGenParacaidas(rd.uniform(0, rango_FuerzaMax), masa) for _ in range(tamano_poblacion)]

def seleccion(poblacion, num_mejores):
    poblacion_valorada = [(p.CalcularAdaptacion(), p) for p in poblacion]
    poblacion_ordenada = sorted(poblacion_valorada, key=lambda x: x[0], reverse=True)
    mejores_individuos = [p[1] for p in poblacion_ordenada[:num_mejores]]
    return mejores_individuos

def cruce(padre1, padre2, masa):
    fuerza_hijo = (padre1.fuerza_paracaidas + padre2.fuerza_paracaidas) / 2
    return AlgoritmoGenParacaidas(fuerza_hijo, masa)

def mutacion(individuo, prob_mutacion):
    if rd.random() < prob_mutacion:
        rango_fuerza_max = individuo.masa * GRAVEDAD * 1.5
        variacion = rd.uniform(-1, 1) * rango_fuerza_max * 0.1
        nueva_fuerza = individuo.fuerza_paracaidas + variacion
        nueva_fuerza = max(0, min(rango_fuerza_max, nueva_fuerza))
        individuo.fuerza_paracaidas = nueva_fuerza
    return individuo

def evolucionar(poblacion, tamano_poblacion, prob_mutacion):
    poblacion_nueva = []
    num_mejores_a_seleccionar = min(2, len(poblacion))
    mejores = seleccion(poblacion,num_mejores_a_seleccionar ) # 2 o 1
    poblacion_nueva.extend(mejores)

    while len(poblacion_nueva) < tamano_poblacion:
        padre1, padre2 = rd.sample(mejores, 2)
        hijo = cruce(padre1, padre2, padre1.masa)
        hijo = mutacion(hijo, prob_mutacion)
        poblacion_nueva.append(hijo)
        
    return poblacion_nueva

def Get_mejor_individuo(poblacion):
    mejor_individuo = max(poblacion, key=lambda p: p.CalcularAdaptacion())
    return mejor_individuo

if __name__ == "__main__":
    #Prueba
    # Parámetros iniciales de prueba
    TAMANO_POBLACION = 50
    PROB_MUTACION = 0.1
    NUM_GENERACIONES = 100
    MASA_PARACAIDISTA = 80 # kg

    print(f"Parámetros: Población={TAMANO_POBLACION}, Mutación={PROB_MUTACION}, Generaciones={NUM_GENERACIONES}, Masa={MASA_PARACAIDISTA} kg")
    poblacion = getPoblacion(TAMANO_POBLACION, MASA_PARACAIDISTA)

    # Generaciones
    for generacion in range(NUM_GENERACIONES):
        poblacion = evolucionar(poblacion, TAMANO_POBLACION, PROB_MUTACION)
        
        # Ver el mejor individuo cada 10 generaciones
        if (generacion + 1) % 10 == 0 or generacion == 0 or generacion == NUM_GENERACIONES - 1:
            mejor_individuo = Get_mejor_individuo(poblacion)
            _, velocidad_final,tiempo, _ = mejor_individuo.simular_caida()
            fitness = mejor_individuo.CalcularAdaptacion()
            print(f"\n--- Generación {generacion + 1} ---")
            print(f"  Mejor individuo: Fuerza de Paracaídas = {mejor_individuo.fuerza_paracaidas:.2f} N")
            print(f"  Velocidad Final al Aterrizar = {velocidad_final:.2f} m/s")
            print(f"  Tiempo = {tiempo:.2f}")
            print(f"  Fitness (Adaptación) = {fitness:.2f}")

    # Mostrar el mejor individuo
    print("\n--- Simulación finalizada ---")
    mejor_individuo_final = Get_mejor_individuo(poblacion)
    _, velocidad_final_final,tiempo_final, _ = mejor_individuo_final.simular_caida()

    print(f"\nEl mejor individuo encontrado después de {NUM_GENERACIONES} generaciones es:")
    print(f"  Fuerza de Paracaídas: {mejor_individuo_final.fuerza_paracaidas:.2f} N")
    print(f"  Velocidad de Aterrizaje: {velocidad_final_final:.2f} m/s")
    print(f"  Tiempo = {tiempo_final:.2f} s")
    print(f"  Fitness (Adaptación): {mejor_individuo_final.CalcularAdaptacion():.2f}")

    if abs(velocidad_final_final) < 2:
        print("\n¡Aterrizaje exitoso!")
    else:
        print("\nEl paracaidista chocó.")