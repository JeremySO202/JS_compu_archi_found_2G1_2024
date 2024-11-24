import time
import threading

from elementosArquitectonicos.ALU import ALU
from elementosArquitectonicos.memoriaDatos import memoriaDatos
from elementosArquitectonicos.memoriaInstrucciones import memoriaInstrucciones
from elementosArquitectonicos.archivoRegistros import archivoRegistros
from elementosNoArquitectonicos.registro import Registro
from instrucciones.branch import BranchEqual  # Importar BranchEqual
from UnidadRiesgos.HazardControl import HazardControl
from UnidadRiesgos.HazardControl import BranchPredictor
from GUI import GUI

class ProcesadorBranchPrediction:
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
        self.hazard_unit = HazardControl(self)  # Instancia de HazardUnit
        self.branch_predictor = BranchPredictor(default_prediction=True)  # Instancia de BranchPredictor

        self.time = 0
        self.pipeline_locations = ["", "", "", "", ""]  # Inicializa las ubicaciones del pipeline

        self.gui = GUI.PygameInterface()

        self.gui_thread = threading.Thread(target=self.gui.run)
        self.gui_thread.start()

    def cargarInstrucciones(self, instruccion):
        self.IM.instrucciones.append(instruccion)

    def clear_pipeline(self):
        print("Limpiando pipeline tras el salto.")
        self.regIM.clear()
        self.regRF.clear()

    def iniciarEjecucion(self):
        execute = True
        while execute:
            # WRITEBACK
            execute = False
            print("Etapa WRITEBACK")
            if self.regDM.instruccion is not None:
                self.gui.highlight_component([4], self.gui.LIGHT_GRAY)
                execute = True
                self.regDM.instruccion.ejecutar()
                self.pipeline_locations[4] = "Instrucción escribiendo"
                self.regDM.clear()
            else:
                print("No hay instrucción en esta etapa")
                self.pipeline_locations[4] = ""
                self.gui.highlight_component([4], self.gui.BLACK)

            # MEMORY
            print("Etapa MEMORY")
            if self.regALU.instruccion is not None:
                self.gui.highlight_component([3], self.gui.YELLOW)
                execute = True
                self.regALU.instruccion.ejecutar()
                self.pipeline_locations[3] = "Instrucción en memoria"
                self.regDM.instruccion = self.regALU.instruccion
                self.regALU.clear()
            else:
                print("No hay instrucción en esta etapa")
                self.pipeline_locations[3] = ""
                self.gui.highlight_component([3], self.gui.BLACK)

            # EXECUTE
            print("Etapa EXECUTE")
            if self.regRF.instruccion is not None:
                self.gui.highlight_component([2], self.gui.RED)
                execute = True
                if isinstance(self.regRF.instruccion, BranchEqual):
                    self.manejar_branch(self.regRF.instruccion)
                else:
                    self.regRF.instruccion.ejecutar()
                self.pipeline_locations[2] = "Instrucción ejecutando"
                self.regALU.instruccion = self.regRF.instruccion
                self.regRF.clear()
            else:
                print("No hay instrucción en esta etapa")
                self.pipeline_locations[2] = ""
                self.gui.highlight_component([2], self.gui.BLACK)

            # DECODE
            print("Etapa DECODE")
            if self.regIM.instruccion is not None:
                self.gui.highlight_component([1], self.gui.GREEN)
                execute = True

                if isinstance(self.regIM.instruccion, BranchEqual):
                    instruction_id = id(self.regIM.instruccion)
                    # Obtener la predicción del salto
                    predicted_taken = self.branch_predictor.predict(instruction_id)
                    if predicted_taken:
                        print(f"Predicción del salto: {predicted_taken}")
                        self.PC += self.regIM.instruccion.offset
                self.pipeline_locations[1] = f"Instrucción {self.PC - 1}"
                self.regIM.instruccion.ejecutar()
                self.regRF.instruccion = self.regIM.instruccion
                self.regIM.clear()
            else:
                print("No hay instrucción en esta etapa")
                self.pipeline_locations[1] = ""
                self.gui.highlight_component([1], self.gui.BLACK)

            # FETCH
            print("Etapa FETCH")
            if self.PC < len(self.IM.instrucciones):
                self.gui.highlight_component([0], self.gui.BLUE)
                execute = True
                print(f"Cargando instrucción {self.PC}")
                self.pipeline_locations[0] = f"Instrucción {self.PC}"
                self.regIM.instruccion = self.IM.instrucciones[self.PC]
                self.PC += 1
            else:
                print("No hay más instrucciones")
                self.pipeline_locations[0] = ""
                self.gui.highlight_component([0], self.gui.BLACK)

            print("#####################################")

            # Actualizar interfaz
            self.gui.update_pipeline_locations(self.pipeline_locations)
            self.time = self.time + 10
            self.gui.update_pc_value(self.PC)
            self.gui.update_time_value(self.time)
            self.gui.update_register_values(self.RF.registros)
            self.gui.update_memory_content(self.DM.datos)
            time.sleep(1)

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
