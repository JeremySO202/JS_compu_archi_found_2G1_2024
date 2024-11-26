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
    def __init__(self, interval=1):  # Intervalo predeterminado de 1 segundo
        self.PC = 0
        self.interval = interval  # Configurable al crear el procesador
        self.IM = memoriaInstrucciones()
        self.regIM = Registro()
        self.RF = archivoRegistros()
        self.regRF = Registro()
        self.ALU = ALU()
        self.regALU = Registro()
        self.DM = memoriaDatos()
        self.regDM = Registro()
        self.jump_pending = False
        self.branch_predictor = BranchPredictor(default_prediction=False)
        self.time = 1
        self.pipeline_locations = ["", "", "", "", ""]
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
        self.regIM.clear()
        self.regRF.clear()

    def iniciarEjecucion(self):
        execute = True
        start_time = time.time()  # Marca de tiempo inicial

        while execute:
            self.total_cycles += 1
            execute = False

            # WRITEBACK
            if self.regDM.instruccion is not None:
                self.gui.highlight_component([4], self.gui.LIGHT_GRAY)
                execute = True
                self.regDM.instruccion.ejecutar()
                self.pipeline_locations[4] = "Instrucción escribiendo"
                self.regDM.clear()
                self.instructions_completed += 1
            else:
                self.pipeline_locations[4] = ""
                self.gui.highlight_component([4], self.gui.BLACK)

            # MEMORY
            if self.regALU.instruccion is not None:
                self.gui.highlight_component([3], self.gui.YELLOW)
                execute = True
                self.regALU.instruccion.ejecutar()
                self.pipeline_locations[3] = "Instrucción en memoria"
                self.regDM.instruccion = self.regALU.instruccion
                self.regALU.clear()
            else:
                self.pipeline_locations[3] = ""
                self.gui.highlight_component([3], self.gui.BLACK)

            # EXECUTE
            if self.regRF.instruccion is not None:
                self.gui.highlight_component([2], self.gui.RED)
                execute = True
                self.regRF.instruccion.ejecutar()
                self.pipeline_locations[2] = "Instrucción ejecutando"
                self.regALU.instruccion = self.regRF.instruccion
                self.regRF.clear()
            else:
                self.pipeline_locations[2] = ""
                self.gui.highlight_component([2], self.gui.BLACK)

            # DECODE
            if self.regIM.instruccion is not None:
                self.gui.highlight_component([1], self.gui.GREEN)
                execute = True
                self.regIM.instruccion.ejecutar()
                self.pipeline_locations[1] = f"Instrucción {self.PC - 1}"
                self.regRF.instruccion = self.regIM.instruccion
                self.regIM.clear()
            else:
                self.pipeline_locations[1] = ""
                self.gui.highlight_component([1], self.gui.BLACK)

            # FETCH
            if self.PC < len(self.IM.instrucciones):
                self.gui.highlight_component([0], self.gui.BLUE)
                execute = True
                self.pipeline_locations[0] = f"Instrucción {self.PC}"
                self.regIM.instruccion = self.IM.instrucciones[self.PC]
                self.PC += 1
            else:
                self.pipeline_locations[0] = ""
                self.gui.highlight_component([0], self.gui.BLACK)

            # Calcular métricas de rendimiento
            elapsed_time = self.time  # Tiempo total en segundos
            if elapsed_time > 0:  # Evitar división por 0
                cpi = self.total_cycles / max(1, self.instructions_completed)
                ipc = self.instructions_completed / max(1, self.total_cycles)
                clock_rate = self.total_cycles / (elapsed_time * 1e9)  # Clock rate en GHz
            else:
                cpi = ipc = clock_rate = 0

            # Actualizar la GUI con métricas
            self.gui.update_pipeline_locations(self.pipeline_locations)
            self.gui.update_performance_metrics(cpi, ipc, clock_rate)
            self.gui.update_pc_value(self.PC)
            self.gui.update_time_value(self.time)
            self.gui.update_register_values(self.RF.registros)
            self.gui.update_memory_content(self.DM.datos)

            # Ralentizar ejecución
            time.sleep(self.interval)

        # Detener la GUI y el hilo
        self.gui.stop()
        self.gui_thread.join()
  

