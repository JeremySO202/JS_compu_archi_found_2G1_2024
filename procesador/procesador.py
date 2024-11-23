import time

from UnidadRiesgos.HazardControl import BranchPredictor
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
        self.jump_pending = False  # Señal para manejar saltos
        self.branch_predictor = BranchPredictor(default_prediction=False)  # Instancia de BranchPredictor

    def cargarInstrucciones(self, instruccion):
        self.IM.instrucciones.append(instruccion)

    def clear_pipeline(self):
        """Limpia las etapas DECODE y EXECUTE del pipeline tras un salto."""
        print("Limpiando pipeline tras el salto.")
        time.sleep(0.1)
        self.regIM.clear()  # Anular instrucción en DECODE
        self.regRF.clear()  # Anular instrucción en EXECUTE

    def iniciarEjecucion(self):
        execute = True

        while execute:
            # WRITEBACK
            execute = False
            # WRITEBACK
            print("Etapa WRITEBACK")
            if self.regDM.instruccion is not None:
                execute = True
                self.regDM.instruccion.ejecutar()
                self.regDM.clear()
            else:
                print("No hay instrucción en esta etapa")

            # MEMORY
            print("Etapa MEMORY")
            if self.regALU.instruccion is not None:
                execute = True
                self.regALU.instruccion.ejecutar()
                self.regDM.instruccion = self.regALU.instruccion
                self.regALU.clear()
            else:
                print("No hay instrucción en esta etapa")

            # EXECUTE
            print("Etapa EXECUTE")
            if self.regRF.instruccion is not None:
                execute = True
                self.regRF.instruccion.ejecutar()
                self.regALU.instruccion = self.regRF.instruccion
                self.regRF.clear()
            else:
                print("No hay instrucción en esta etapa")

            # DECODE
            print("Etapa DECODE")
            if self.regIM.instruccion is not None:
                execute = True
                self.regIM.instruccion.ejecutar()
                self.regRF.instruccion = self.regIM.instruccion
                self.regIM.clear()
            else:
                print("No hay instrucción en esta etapa")

            # FETCH
            print("Etapa FETCH")
            if self.PC < len(self.IM.instrucciones):
                execute = True
                print(f"Cargando instrucción {self.PC}")
                self.regIM.instruccion = self.IM.instrucciones[self.PC]
                self.PC += 1
            else:
                print("No hay más instrucciones")

            print("#####################################")
