from instrucciones.loadWord import LoadWord
from instrucciones.storeWord import StoreWord
from procesador.procesador import Procesador

procesador = Procesador()

procesador.RF.registros[0] = 7;
procesador.RF.registros[1] = 6;

procesador.cargarInstrucciones(StoreWord(0,-4,4,procesador))
procesador.cargarInstrucciones(StoreWord(1,-3,4,procesador))
procesador.iniciarEjecucion()