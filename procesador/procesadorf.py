import time

from elementosArquitectonicos.ALU import ALU
from elementosArquitectonicos.memoriaDatos import memoriaDatos
from elementosArquitectonicos.memoriaInstrucciones import memoriaInstrucciones
from elementosArquitectonicos.archivoRegistros import archivoRegistros
from elementosNoArquitectonicos.registro import Registro
from instrucciones.branch import BranchEqual  # Importar BranchEqual
from UnidadRiesgos.HazardControl import HazardControl
from instrucciones.add import Add
from instrucciones.sub import Sub
from instrucciones.and_ import And
from instrucciones.or_ import Or

class Procesadorf:
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
        self.hazard_control = HazardControl(self)

    def cargarInstrucciones(self, instruccion):
        self.IM.instrucciones.append(instruccion)

    def clear_pipeline(self):
        """Limpia las etapas DECODE y EXECUTE del pipeline tras un salto."""
        print("Limpiando pipeline tras el salto.")
        time.sleep(0.1)
        self.regIM.clear()  # Anular instrucción en DECODE
        self.regRF.clear()  # Anular instrucción en EXECUTE

    def iniciarEjecucion(self):
        while True:
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
                break  # Termina la ejecución si no hay más instrucciones

            print("#####################################")

            time.sleep(1)







