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
        print("Comparando registros (resta)")
        self.procesador.regALU.data = self.procesador.ALU.operar(
            self.procesador.regRF.data[0], self.procesador.regRF.data[1], 1
        )
        print(f"Resultado de la resta: {self.procesador.regALU.data}")

        # Consultar el predictor
        instruction_id = id(self)  # Identificador único para esta instrucción
        predicted_taken = self.procesador.branch_predictor.predict(instruction_id)
        print(f"Predicción del salto (taken): {predicted_taken}")

        # Evaluar el resultado real
        actual_outcome = self.procesador.regALU.data == 0
        print(f"Resultado real del salto (taken): {actual_outcome}")

        # Si la predicción fue incorrecta
        if predicted_taken != actual_outcome:
            print("Predicción incorrecta. Activando Hazard Unit.")
            self.procesador.hazard_unit.handle_misprediction()

        # Realizar el salto si corresponde
        if actual_outcome:  # Salto se toma
            print(f"Registros iguales. Realizando salto con offset {self.offset}.")
            self.procesador.PC += self.offset - 1
        else:  # Salto no se toma
            print("Registros no son iguales. Continuando normalmente.")

        # Actualizar el predictor
        self.procesador.branch_predictor.update(instruction_id, actual_outcome)

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


