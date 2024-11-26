from instrucciones.branch import BranchEqual
from instrucciones.add import Add
from instrucciones.sub import Sub
from instrucciones.and_ import And
from instrucciones.or_ import Or
from instrucciones.mov import Mov
from procesador.procesadorBranchPrediction import ProcesadorBranchPrediction



import sys

if __name__ == "__main__":
    # Leer intervalo desde argumentos de la línea de comandos (si no, usar 1 por defecto)
    interval = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0

    procesador = ProcesadorBranchPrediction(interval=interval)

    # Caso 1: Salto No Tomado
    print("\n--- Caso 1: Salto No Tomado, Penalizacion aplicada ---")
    procesador.RF.registros[0] = 7
    procesador.RF.registros[1] = 6  # Diferente de R0
    procesador.RF.registros[2] = 5
    procesador.RF.registros[3] = 10
    procesador.RF.registros[4] = 12  # Necesario para Add(7, 3, 4, procesador)
    procesador.RF.registros[5] = 15  # Necesario para Sub(8, 7, 5, procesador)
    procesador.RF.registros[6] = 0  # Inicializar R6 para evitar problemas en Sub y Or
    procesador.RF.registros[7] = 0  # Inicializar R7
    procesador.RF.registros[8] = 0  # Inicializar R8
    procesador.RF.registros[9] = 0  # Inicializar R9
    procesador.RF.registros[10] = 0  # Inicializar R10
    procesador.RF.registros[11] = 0  # Inicializar R11
    procesador.RF.registros[12] = 0  # Inicializar R12
    procesador.RF.registros[13] = 0  # Inicializar R13
    procesador.RF.registros[14] = 0  # Inicializar R14

    procesador.cargarInstrucciones(Add(4, 0, 2, procesador))
    procesador.cargarInstrucciones(BranchEqual(0, 1, 3, procesador))  # Salto no tomado
    procesador.cargarInstrucciones(Sub(5, 3, 2, procesador))
    procesador.cargarInstrucciones(Add(6, 0, 3, procesador))
    procesador.cargarInstrucciones(Add(7, 3, 4, procesador))  # Suma: R7 = R3 + R4

    # Instrucciones después del salto
    procesador.cargarInstrucciones(Sub(8, 7, 5, procesador))  # R8 = R7 - R5
    procesador.cargarInstrucciones(And(9, 8, 2, procesador))  # R9 = R8 & R2
    procesador.cargarInstrucciones(Or(10, 1, 6, procesador))  # R10 = R1 | R6

    procesador.iniciarEjecucion()
'''
# Reinicia el procesador para los siguientes casos
procesador = ProcesadorBranchPrediction()

print("\n--- Caso 2: Salto Tomado, Penalizacion Aplicada ---")
procesador.RF.registros[0] = 7
procesador.RF.registros[1] = 7  # Igual a R0
procesador.RF.registros[2] = 5
procesador.RF.registros[3] = 10
procesador.RF.registros[4] = 12  # Necesario para Add(7, 3, 4, procesador)
procesador.RF.registros[5] = 15
procesador.RF.registros[6] = 0  # Inicializar R6 para evitar problemas en Sub y Or
procesador.RF.registros[7] = 0  # Inicializar R7
procesador.RF.registros[8] = 0  # Inicializar R8
procesador.RF.registros[9] = 0  # Inicializar R9
procesador.RF.registros[10] = 0  # Inicializar R10
procesador.RF.registros[11] = 0  # Inicializar R11
procesador.RF.registros[12] = 0  # Inicializar R12
procesador.RF.registros[13] = 0  # Inicializar R13
procesador.RF.registros[14] = 0  # Inicializar R14

# Cargar instrucciones
procesador.cargarInstrucciones(Add(4, 0, 2, procesador))  # R4 = R0 + R2
procesador.cargarInstrucciones(BranchEqual(0, 1, 3, procesador))  # Salto tomado
procesador.cargarInstrucciones(Sub(5, 3, 2, procesador))  # R5 = R3 - R2 (será saltado)
procesador.cargarInstrucciones(Add(6, 0, 3, procesador))  # R6 = R0 + R3 (será saltado)
procesador.cargarInstrucciones(Add(7, 3, 4, procesador))  # R7 = R3 + R4

# Instrucciones después del salto
procesador.cargarInstrucciones(Sub(8, 7, 5, procesador))  # R8 = R7 - R5
procesador.cargarInstrucciones(And(9, 8, 2, procesador))  # R9 = R8 & R2
procesador.cargarInstrucciones(Or(10, 1, 6, procesador))  # R10 = R1 | R6

# Iniciar ejecución
procesador.iniciarEjecucion()
'''