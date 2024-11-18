from instrucciones.branch import BranchEqual
from instrucciones.add import Add
from instrucciones.sub import Sub
from instrucciones.and_ import And
from instrucciones.or_ import Or
from instrucciones.mov import Mov
from procesador.procesador import Procesador

procesador = Procesador()

procesador.RF.registros[0] = 7
procesador.RF.registros[1] = 7  # Igual al registro 0 (para probar el salto)
procesador.RF.registros[2] = 5
procesador.RF.registros[3] = 10

# Cargar instrucciones
procesador.cargarInstrucciones(Add(4, 0, 2, procesador))  # Suma R4 = R0 + R2
procesador.cargarInstrucciones(Sub(5, 3, 2, procesador))  # Resta R5 = R3 - R2
procesador.cargarInstrucciones(BranchEqual(0, 1, 4, procesador))  # Salto si R0 == R1 (4 instrucciones adelante)
procesador.cargarInstrucciones(And(6, 3, 2, procesador))  # AND (Se anulará si hay salto)
procesador.cargarInstrucciones(Or(7, 0, 2, procesador))  # OR (Se anulará si hay salto)
procesador.cargarInstrucciones(Mov(8, 42, procesador))  # MOV inmediato a R8 (Se anulará si hay salto)

# Instrucciones después del salto
procesador.cargarInstrucciones(Add(9, 0, 3, procesador))  # Suma R9 = R0 + R3
procesador.cargarInstrucciones(Sub(10, 2, 3, procesador))  # Resta R10 = R2 - R3
procesador.cargarInstrucciones(And(11, 1, 3, procesador))  # AND R11 = R1 & R3
procesador.cargarInstrucciones(Or(12, 1, 2, procesador))  # OR R12 = R1 | R2

procesador.iniciarEjecucion()