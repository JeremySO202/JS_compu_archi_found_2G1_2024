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

    def cargarInstrucciones(self, instruccion):
        self.IM.instrucciones.append(instruccion)

    def clear_pipeline(self):
        print("Limpiando pipeline tras el salto.")
        self.regIM.clear()
        self.regRF.clear()

    def iniciarEjecucion(self):
        while True:
            # Penalización por predicción incorrecta
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
                    self.manejar_branch(self.regRF.instruccion)
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

    def manejar_branch(self, branch_instruction):
        """Manejo del BranchEqual dentro del procesador."""
        instruction_id = id(branch_instruction)

        # Obtener la predicción del salto
        predicted_taken = self.branch_predictor.predict(instruction_id)
        print(f"Predicción del salto (taken): {predicted_taken}")

        # Ejecutar la instrucción normalmente
        branch_instruction.ejecutar()

        # Determinar el resultado real
        actual_taken = self.regALU.data == 0
        print(f"Resultado real del salto (taken): {actual_taken}")

        # Verificar si la predicción fue incorrecta
        if predicted_taken != actual_taken:
            print("Predicción incorrecta detectada.")
            self.hazard_unit.handle_misprediction()

        # Si el salto es tomado, ajustar el PC
        if actual_taken:
            self.PC += branch_instruction.offset - 1  # Ajustar el incremento automático

        # Actualizar el predictor
        self.branch_predictor.update(instruction_id, actual_taken)
