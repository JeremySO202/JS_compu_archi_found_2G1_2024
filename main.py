from instrucciones.loadWord import LoadWord
from procesador.procesador import Procesador

procesador = Procesador()

procesador.DM.datos[4] = 10;
procesador.RF.registros[0] = 0;

procesador.cargarInstrucciones(LoadWord(5,4,0,procesador))
procesador.cargarInstrucciones(LoadWord(6,4,0,procesador))
procesador.iniciarEjecucion()