from instrucciones.loadWord import LoadWord
from instrucciones.storeWord import StoreWord
from instrucciones.add import Add
from instrucciones.addi import Addi
from instrucciones.sub import Sub
from instrucciones.subi import Subi
from instrucciones.and_ import And
from instrucciones.or_ import Or
from instrucciones.mov import Mov

from procesador.procesadorf import Procesadorf


procesador = Procesadorf()

procesador.RF.registros[0] = 7;
procesador.RF.registros[1] = 6;
procesador.RF.registros[9] = 5;
procesador.RF.registros[10] = 10;


#procesador.cargarInstrucciones(StoreWord(0,-4,4,procesador))
#procesador.cargarInstrucciones(StoreWord(1,-3,4,procesador))

procesador.cargarInstrucciones(Add(2, 0, 1, procesador))  # R2 = R0 + R1
procesador.cargarInstrucciones(Add(3, 0, 1, procesador))  # R3 = R2 + R1
procesador.cargarInstrucciones(Add(4, 0, 1, procesador))  # R4 = R3 + R2
procesador.cargarInstrucciones(Add(5, 1, 1, procesador))
procesador.cargarInstrucciones(Add(5,9,10,procesador))



procesador.iniciarEjecucion()