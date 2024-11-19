from instrucciones.add import Add
from instrucciones.addi import Addi
class HazardControl:
    def __init__(self, procesador):
        self.procesador = procesador

    def check_forwarding(self, current_instruction):
        """Verifica y aplica forwarding para instrucciones que usan registros."""
        if not isinstance(current_instruction, Add):
            print("No se aplica forwarding: instrucción no es de tipo Add.")
            return  # Por ahora, solo procesamos instrucciones tipo Add

        # Asegurarse de que regRF.data sea una lista inicializada
        if current_instruction.procesador.regRF.data is None:
            current_instruction.procesador.regRF.data = [None, None]

        # Bandera para detectar si hubo forwarding
        forwarding_applied = False

        # Forwarding desde ALU
        if self.procesador.regALU.instruccion:
            alu_inst = self.procesador.regALU.instruccion
            if alu_inst.destino == current_instruction.registro1:
                print(f"Forwarding desde ALU a DECODE para registro {current_instruction.registro1}.")
                current_instruction.procesador.regRF.data[0] = self.procesador.regALU.data
                forwarding_applied = True
            if alu_inst.destino == current_instruction.registro2:
                print(f"Forwarding desde ALU a DECODE para registro {current_instruction.registro2}.")
                current_instruction.procesador.regRF.data[1] = self.procesador.regALU.data
                forwarding_applied = True

        # Forwarding desde MEM
        if self.procesador.regDM.instruccion:
            dm_inst = self.procesador.regDM.instruccion
            if dm_inst.destino == current_instruction.registro1:
                print(f"Forwarding desde MEM a DECODE para registro {current_instruction.registro1}.")
                current_instruction.procesador.regRF.data[0] = self.procesador.RF.registros[dm_inst.destino]
                forwarding_applied = True
            if dm_inst.destino == current_instruction.registro2:
                print(f"Forwarding desde MEM a DECODE para registro {current_instruction.registro2}.")
                current_instruction.procesador.regRF.data[1] = self.procesador.RF.registros[dm_inst.destino]
                forwarding_applied = True

        # Mensaje si no hubo forwarding
        if not forwarding_applied:
            print("No hubo necesidad de aplicar forwarding para esta instrucción.")

    def forward_from_execute(self, destino, resultado):
        """Envía el resultado de ALU al registro correspondiente."""
        print(f"Forwarding directo desde EXECUTE al destino R{destino}")
        # Actualiza el valor en el archivo de registros
        self.procesador.RF.registros[destino] = resultado
        # Si hay instrucciones esperando este valor, lo forwardea a ellas
        if self.procesador.regRF.instruccion:
            inst = self.procesador.regRF.instruccion
            if isinstance(inst, Add):
                if inst.registro1 == destino:
                    print(f"Forwarding R{destino} a registro1 en DECODE.")
                    self.procesador.regRF.data[0] = resultado
                if inst.registro2 == destino:
                    print(f"Forwarding R{destino} a registro2 en DECODE.")
                    self.procesador.regRF.data[1] = resultado
