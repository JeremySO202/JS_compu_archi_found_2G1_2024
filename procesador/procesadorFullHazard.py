import time

from elementosArquitectonicos.ALU import ALU
from elementosArquitectonicos.memoriaDatos import memoriaDatos
from elementosArquitectonicos.memoriaInstrucciones import memoriaInstrucciones
from elementosArquitectonicos.archivoRegistros import archivoRegistros
from elementosNoArquitectonicos.registro import Registro
from instrucciones.branch import BranchEqual  # Importar BranchEqual
from UnidadRiesgos.HazardControl import HazardControl, BranchPredictor
from instrucciones.add import Add
from instrucciones.sub import Sub
from instrucciones.and_ import And
from instrucciones.or_ import Or


class ProcesadorFullHazard:
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
        self.hazard_control = HazardControl(self)
        self.branch_predictor = BranchPredictor(default_prediction=True)  # Instancia de BranchPredictor

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
                if isinstance(self.regRF.instruccion, BranchEqual):
                    self.manejar_branch(self.regRF.instruccion)
                else:
                    self.regRF.instruccion.ejecutar()
                # Enviar resultado al HazardControl
                if isinstance(self.regRF.instruccion, (Add, Sub, Or, And)):
                    destino = self.regRF.instruccion.destino
                    resultado = self.regALU.data  # Resultado de la ALU
                    self.hazard_control.forward_from_execute(destino, resultado)
                self.regALU.instruccion = self.regRF.instruccion
                self.regRF.clear()
            else:
                print("No hay instrucción en esta etapa")

            # DECODE
            print("Etapa DECODE")
            if self.regIM.instruccion is not None:
                execute = True
                # Verificar forwarding antes de ejecutar la instrucción
                self.hazard_control.check_forwarding(self.regIM.instruccion)

                if self.regRF.data is None:
                    self.regRF.data = [None, None]

                # Inicializar registros si no se forwardeó nada
                if isinstance(self.regIM.instruccion, (Add, Sub, Or, And)):
                    if not self.regIM.instruccion.procesador.regRF.data:
                        self.regIM.instruccion.procesador.regRF.data = [
                            self.RF.registros[self.regIM.instruccion.registro1],
                            self.RF.registros[self.regIM.instruccion.registro2],
                        ]

                if isinstance(self.regIM.instruccion, BranchEqual):
                    instruction_id = id(self.regIM.instruccion)
                    # Obtener la predicción del salto
                    predicted_taken = self.branch_predictor.predict(instruction_id)
                    if predicted_taken:
                        print(f"Predicción del salto: {predicted_taken}")
                        self.PC += self.regIM.instruccion.offset

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

    def manejar_branch(self, branch_instruction):
        """Manejo del BranchEqual dentro del procesador."""
        # Ejecutar la instrucción normalmente
        branch_instruction.ejecutar()

        # Determinar el resultado real
        actual_taken = self.regALU.data == 0
        print(f"Resultado real del salto: {actual_taken}")

        # Obtener la predicción del salto
        instruction_id = id(branch_instruction)
        predicted_taken = self.branch_predictor.predict(instruction_id)

        # Verificar si la predicción fue incorrecta
        if predicted_taken != actual_taken:
            self.hazard_unit.handle_misprediction(branch_instruction)

        # Actualizar el predictor
        self.branch_predictor.update(instruction_id, actual_taken)