import time

from elementosArquitectonicos.ALU import ALU
from elementosArquitectonicos.memoriaDatos import memoriaDatos
from elementosArquitectonicos.memoriaInstrucciones import memoriaInstrucciones
from elementosArquitectonicos.archivoRegistros import archivoRegistros
from elementosNoArquitectonicos.registro import Registro


class Procesador:
    def __init__(self):
        self.PC = 0
        self.IM = memoriaInstrucciones()
        self.regIM = Registro()
        self.RF = archivoRegistros()
        self.regRF = Registro()
        self.ALU = ALU()
        self.regALU = Registro()
        self.DM = memoriaDatos()
        self.regDM = Registro()


    def cargarInstrucciones(self, instruccion):
        self.IM.instrucciones.append(instruccion)



    def iniciarEjecucion(self):
        while True:
            # WRITEBACK
            print("Etapa WRITEBACK")
            if self.regDM.instruccion!=None:
                self.regDM.instruccion.ejecutar()
                self.regDM.clear()
            else:
                print("No hay instruccion en esta etapa")

            # MEMORY
            print("Etapa MEMORY")
            if self.regALU.instruccion != None:
                self.regALU.instruccion.ejecutar()
                self.regDM.instruccion = self.regALU.instruccion
                self.regALU.clear()
            else:
                print("No hay instruccion en esta etapa")

            # EXECUTE
            print("Etapa EXECUTE")
            if self.regRF.instruccion != None:
                self.regRF.instruccion.ejecutar()
                self.regALU.instruccion = self.regRF.instruccion
                self.regRF.clear()
            else:
                print("No hay instruccion en esta etapa")

            # DECODE
            print("Etapa DECODE")
            if self.regIM.instruccion != None:
                self.regIM.instruccion.ejecutar()
                self.regRF.instruccion = self.regIM.instruccion
                self.regIM.clear()
            else:
                print("No hay instruccion en esta etapa")

            #FETCH
            print("Etapa FETCH")
            if self.PC < len(self.IM.instrucciones):
                print("Cargando instruccion "+ str(self.PC))
                self.regIM.instruccion = self.IM.instrucciones[self.PC]
            else:
                print("No hay mas instrucciones")
                break


            #NEXT PC

            self.PC = self.PC+1

            print("#####################################")

            time.sleep(1)






