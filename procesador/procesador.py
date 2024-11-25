import threading
import time

from UnidadRiesgos.HazardControl import BranchPredictor
from elementosArquitectonicos.ALU import ALU
from elementosArquitectonicos.memoriaDatos import memoriaDatos
from elementosArquitectonicos.memoriaInstrucciones import memoriaInstrucciones
from elementosArquitectonicos.archivoRegistros import archivoRegistros
from elementosNoArquitectonicos.registro import Registro

from GUI import GUI

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
        self.time = 1
        self.interval = 1

        # Inicializa las ubicaciones del pipeline
        self.pipeline_locations = ["", "", "", "", ""]

        # Métricas de desempeño
        self.total_cycles = 0
        self.instructions_completed = 0

        # Interfaz gráfica
        self.gui = GUI.PygameInterface()

        # Hilo para la interfaz
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
        start_time = time.time()  # Marca de tiempo inicial

        while execute:
            self.total_cycles += 1  # Incrementar ciclos totales en cada iteración

            # WRITEBACK
            execute = False
            print("Etapa WRITEBACK")
            if self.regDM.instruccion is not None:
                self.gui.highlight_component([4], self.gui.LIGHT_GRAY)
                execute = True
                self.regDM.instruccion.ejecutar()
                self.pipeline_locations[4] = "Instrucción escribiendo"
                self.regDM.clear()
                self.instructions_completed += 1  # Incrementar instrucciones completadas
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
                self.regIM.instruccion.ejecutar()
                self.pipeline_locations[1] = f"Instrucción {self.PC - 1}"
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

            # Calcular métricas
            elapsed_time = self.time # Tiempo total en segundos
            if elapsed_time > 0:  # Evitar cálculos con tiempo 0
                cpi = self.total_cycles / max(1, self.instructions_completed)
                ipc = self.instructions_completed / max(1, self.total_cycles)
                clock_rate = self.total_cycles / (elapsed_time * 1e9)  # Clock Rate en GHz
            else:
                clock_rate = 0

            # Debugging: Verificar cálculos
            print(f"Total Cycles: {self.total_cycles}, Instructions Completed: {self.instructions_completed}, Elapsed Time: {elapsed_time}, Clock Rate: {clock_rate} GHz")

            # Actualizar la GUI
            self.gui.update_pipeline_locations(self.pipeline_locations)
            self.gui.update_performance_metrics(cpi, ipc, clock_rate)
            self.time += 10
            self.gui.update_pc_value(self.PC)
            self.gui.update_time_value(self.time)
            self.gui.update_register_values(self.RF.registros)
            self.gui.update_memory_content(self.DM.datos)

            # Simulación: ralentizar ejecución para observar cambios
            time.sleep(self.interval)

        self.gui.stop()
        self.gui_thread.join
