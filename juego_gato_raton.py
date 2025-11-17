import random

# Tamaño del tablero
N = 5

# Crear la matriz
tablero = [['[ ]' for j in range(N)] for i in range(N)]

# Definir movimientos
movimientos = {
    '8': (-1, 0),  # arriba
    '2': (1, 0),   # abajo
    '4': (0, -1),  # izquierda
    '6': (0, 1)    # derecha
}
#mostrar tablero
def mostrar_tablero():
    for fila in tablero:
        fila_formateada = []
        for celda in fila:
            contenido = celda.strip('[]') or ' '
            fila_formateada.append(f"[{contenido:^3}]")
        print(" ".join(fila_formateada))
    print()

# Movimiento válido
def mover(pos, mov, pasos=1, evitar_obstaculo=True, es_raton=False):
    nueva = pos[:]
    for _ in range(pasos):
        temp = [nueva[0] + mov[0], nueva[1] + mov[1]]
        if 0 <= temp[0] < N and 0 <= temp[1] < N:
            if evitar_obstaculo:
                if tablero[temp[0]][temp[1]] == 'T':
                    break
                if tablero[temp[0]][temp[1]] == 'Q' and not es_raton:
                    break
            nueva = temp
        else:
            break
    return nueva

# Movimiento manual del gato
def jugador_mueve_gato(pasos=1):
    print("Tu turno (8=arriba, 2=abajo, 4=izquierda, 6=derecha): ")
    tecla = input('---> movimiento: ').lower()
    if tecla in movimientos:
        return mover(gato, movimientos[tecla], pasos, evitar_obstaculo=False)
    print('Movimiento invalido')
    return gato

# Distancia Manhattan
def distancia(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Movimiento del ratón
def minimax_raton(raton, gato):
    mejor_movimiento = raton
    mejor_valor = -1
    for mov in movimientos.values():
        nueva_pos = mover(raton, mov, pasos=1, evitar_obstaculo=True, es_raton=True)
        if nueva_pos != raton:
            valor = distancia(nueva_pos, gato)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = nueva_pos
    return mejor_movimiento

# Verificar si el ratón está rodeado
def raton_esta_rodeado():
    for mov in movimientos.values():
        nueva = mover(raton, mov, pasos=1, evitar_obstaculo=True, es_raton=True)
        if nueva != raton:
            return False
    return True

# Colocar trampa manual
def colocar_trampa_manual():
    print("Puedes colocar una trampa cerca del raton")
    print("Elige dirección (8=arriba, 2=abajo, 4=izquierda, 6=derecha): ")
    tecla = input('---> dirección: ').lower()
    if tecla in movimientos:
        dx, dy = movimientos[tecla]
        pos = [raton[0] + dx, raton[1] + dy]
        if 0 <= pos[0] < N and 0 <= pos[1] < N and tablero[pos[0]][pos[1]] == '[ ]':
            tablero[pos[0]][pos[1]] = 'T'
            trampas.append(pos)
            print("Trampa colocada en", pos)
        else:
            print("No se puede colocar trampa ahi.")
    else:
        print("Direccion invalida.")

# Generar 5 quesos estáticos
def generar_quesos_estaticos(cantidad):
    quesos = []
    while len(quesos) < cantidad:
        x = random.randint(0, N-1)
        y = random.randint(0, N-1)
        if [x, y] not in quesos and [x, y] != gato and [x, y] != raton:
            quesos.append([x, y])
            tablero[x][y] = 'Q'
    return quesos

# Posiciones iniciales
gato = [0, 0]
raton = [2, 2]
tablero[gato[0]][gato[1]] = 'G'
tablero[raton[0]][raton[1]] = 'R'

# Generar quesos y trampas
quesos = generar_quesos_estaticos(5)
trampas = []

# Estado del juego
raton_pierde_turno = False

# Mostrar tablero inicial
mostrar_tablero()

# Bucle de juego
for turno in range(1, 16):
    print(f"\n Turno {turno}")

    # Verificar si el ratón está rodeado
    if raton_esta_rodeado():
        print("El raton esta rodeado y no puede moverse")
        print("El gato atrapo al raton")
        break

    # Limpiar posición anterior del gato
    tablero[gato[0]][gato[1]] = '[ ]'

    # Mover el gato
    gato = jugador_mueve_gato(1)
    tablero[gato[0]][gato[1]] = 'G'
    mostrar_tablero()

    # Verificar si el gato atrapó al ratón
    if gato == raton:
        print("El gato atrapo al raton")
        break

    # Opción de colocar trampa cada 3 turnos
    if turno % 3 == 0:
        print("Turno estrategico: ¿Quieres colocar una trampa o seguir jugando?")
        print("Escribe 't' para colocar trampa o 's' para saltar:")
        eleccion = input('---> ').lower()
        if eleccion == 't':
            colocar_trampa_manual()
        elif eleccion == 's':
            print("Saltaste la trampa. Sigues jugando normalmente.")
        else:
            print("Opcion invalida. No se coloco trampa.")

    # Limpiar posición anterior del ratón
    tablero[raton[0]][raton[1]] = '[ ]'

    # Movimiento del ratón
    if raton_pierde_turno:
        print("El raton esta aturdido por el queso y pierde este turno.")
        raton_pierde_turno = False
    else:
        nueva_raton = minimax_raton(raton, gato)
        raton = nueva_raton

        # Verificar si el ratón comió un queso
        if raton in quesos:
            print("El raton comio un queso. ¡Pierde su proximo turno!")
            quesos.remove(raton)
            raton_pierde_turno = True

    tablero[raton[0]][raton[1]] = 'R'
    mostrar_tablero()

    # Verificar si el gato atrapó al ratón después del movimiento
    if gato == raton:
        print("El gato atrapo al ratón")
        break
else:
    print("El raton escapo del gato despues de 16 turnos")


