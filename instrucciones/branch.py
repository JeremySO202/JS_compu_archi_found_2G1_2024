class BranchEqual:
    def __init__(self, _registro1, _registro2, _offset, _procesador):
        self.registro1 = _registro1
        self.registro2 = _registro2
        self.offset = _offset
        self.procesador = _procesador

        self.ejecucion = [self.instruccion1, self.instruccion2, self.instruccion3]

    def instruccion1(self):
        print(f"Obteniendo valores de registros {self.registro1} y {self.registro2}")
        self.procesador.regRF.data = [None] * 2
        self.procesador.regRF.data[0] = self.procesador.RF.registros[self.registro1]
        self.procesador.regRF.data[1] = self.procesador.RF.registros[self.registro2]
        print(f"Valores obtenidos: {self.procesador.regRF.data}")

    def instruccion2(self):
        print("Comparando registros")
        self.procesador.regALU.data = self.procesador.ALU.operar(
            self.procesador.regRF.data[0], self.procesador.regRF.data[1], 1
        )
        print(f"Resultado de la resta: {self.procesador.regALU.data}")



    def instruccion3(self):
        print("Finalizando BranchEqual. No hay resultado que guardar en registros.")

    def instruccion4(self):
        pass

    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en BranchEqual.")

