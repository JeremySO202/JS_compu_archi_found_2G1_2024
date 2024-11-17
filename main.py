from instrucciones.loadWord import LoadWord
from instrucciones.storeWord import StoreWord
from instrucciones.add import Add
from instrucciones.addi import Addi
from instrucciones.sub import Sub
from instrucciones.subi import Subi
from instrucciones.and_ import And
from instrucciones.or_ import Or
from instrucciones.mov import Mov
from instrucciones.branch import Jump  # Importar Jump desde branch.py

from procesador.procesador import Procesador

procesador = Procesador()

# Inicializar registros
procesador.RF.registros[0] = 7
procesador.RF.registros[1] = 6
procesador.RF.registros[9] = 5
procesador.RF.registros[10] = 10

# Cargar instrucciones en el procesador
procesador.cargarInstrucciones(Add(2, 0, 1, procesador))  # Suma
procesador.cargarInstrucciones(Addi(3, 0, 3, procesador))  # Suma inmediata

procesador.cargarInstrucciones(Sub(4, 0, 1, procesador))  # Resta
procesador.cargarInstrucciones(Subi(5, 0, 3, procesador))  # Resta inmediata

procesador.cargarInstrucciones(And(6, 9, 10, procesador))  # AND
procesador.cargarInstrucciones(Or(7, 9, 10, procesador))  # OR
procesador.cargarInstrucciones(Mov(8, 54, procesador))  # MOV

# Insertar una instrucción Jump
procesador.cargarInstrucciones(Jump(3, procesador))  # Salta 3 instrucciones adelante

# Agregar instrucciones que podrían ser saltadas
procesador.cargarInstrucciones(Add(9, 1, 0, procesador))  # Se salta esta
procesador.cargarInstrucciones(Or(10, 0, 1, procesador))  # Se salta esta también
procesador.cargarInstrucciones(Sub(11, 9, 10, procesador))  # Se salta esta también

procesador.cargarInstrucciones(And(12, 1, 9, procesador))  # Esta se ejecuta después del salto

# Iniciar ejecución
procesador.iniciarEjecucion()
