import time
import threading
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
from GUI import GUI

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

        self.time = 0
        self.pipeline_locations = ["", "", "", "", ""]  # Inicializa las ubicaciones del pipeline

        # Interfaz gráfica
        self.gui = GUI.PygameInterface()

        # Hilo para la GUI
        self.gui_thread = threading.Thread(target=self.gui.run)
        self.gui_thread.start()

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
                # Enviar resultado al HazardControl
                if isinstance(self.regRF.instruccion, (Add, Sub, Or, And)):
                    destino = self.regRF.instruccion.destino
                    resultado = self.regALU.data  # Resultado de la ALU
                    self.hazard_control.forward_from_execute(destino, resultado)
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
            self.hazard_control.handle_misprediction(branch_instruction)

        # Actualizar el predictor
        self.branch_predictor.update(instruction_id, actual_taken)
