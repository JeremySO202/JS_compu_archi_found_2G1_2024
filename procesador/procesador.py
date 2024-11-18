import time

from elementosArquitectonicos.ALU import ALU
from elementosArquitectonicos.memoriaDatos import memoriaDatos
from elementosArquitectonicos.memoriaInstrucciones import memoriaInstrucciones
from elementosArquitectonicos.archivoRegistros import archivoRegistros
from elementosNoArquitectonicos.registro import Registro
from instrucciones.branch import BranchEqual  # Importar BranchEqual
from UnidadRiesgos.HazardControl import HazardUnit
from UnidadRiesgos.HazardControl import BranchPredictor

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
        self.jump_pending = False
        self.hazard_unit = HazardUnit(self)  # Instancia de HazardUnit
        self.branch_predictor = BranchPredictor(default_prediction=True)  # Instancia de BranchPredictor
        self.misprediction_penalty = 0

    def clear_pipeline(self):
        print("Limpiando pipeline tras el salto.")
        self.regIM.clear()
        self.regRF.clear()

    def iniciarEjecucion(self):
        while True:
            if self.misprediction_penalty > 0:
                print(f"Ciclo desperdiciado por penalización. {self.misprediction_penalty} ciclos restantes.")
                self.misprediction_penalty -= 1
                time.sleep(1)
                continue

            # WRITEBACK
            print("Etapa WRITEBACK")
            if self.regDM.instruccion is not None:
                self.regDM.instruccion.ejecutar()
                self.regDM.clear()
            else:
                print("No hay instrucción en esta etapa")

            # MEMORY
            print("Etapa MEMORY")
            if self.regALU.instruccion is not None:
                self.regALU.instruccion.ejecutar()
                self.regDM.instruccion = self.regALU.instruccion
                self.regALU.clear()
            else:
                print("No hay instrucción en esta etapa")

            # EXECUTE
            print("Etapa EXECUTE")
            if self.regRF.instruccion is not None:
                if isinstance(self.regRF.instruccion, BranchEqual):
                    instruction_id = id(self.regRF.instruccion)
                    predicted_taken = self.branch_predictor.predict(instruction_id)
                    self.regRF.instruccion.ejecutar()
                    actual_taken = self.regALU.data == 0
                    print(f"Predicción del salto (taken): {predicted_taken}")
                    print(f"Resultado real del salto (taken): {actual_taken}")
                    if predicted_taken != actual_taken:
                        self.hazard_unit.handle_misprediction()  # Usar HazardUnit
                    self.branch_predictor.update(instruction_id, actual_taken)  # Actualizar predictor
                else:
                    self.regRF.instruccion.ejecutar()
                self.regALU.instruccion = self.regRF.instruccion
                self.regRF.clear()
            else:
                print("No hay instrucción en esta etapa")

            # DECODE
            print("Etapa DECODE")
            if self.regIM.instruccion is not None:
                self.regIM.instruccion.ejecutar()
                self.regRF.instruccion = self.regIM.instruccion
            else:
                print("No hay instrucción en esta etapa")

            # FETCH
            print("Etapa FETCH")
            if self.PC < len(self.IM.instrucciones):
                print(f"Cargando instrucción {self.PC}")
                self.regIM.instruccion = self.IM.instrucciones[self.PC]
                self.PC += 1
            else:
                print("No hay más instrucciones")
                break

            print("#####################################")
            time.sleep(1)
