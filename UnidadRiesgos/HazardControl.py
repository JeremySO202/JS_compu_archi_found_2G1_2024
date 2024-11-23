class HazardControl:
    def __init__(self, procesador):
        self.procesador = procesador

    def handle_misprediction(self, instruction):
        """Maneja la penalización por predicción incorrecta."""
        print("Predicción incorrecta detectada. Penalización aplicada.")
        self.procesador.clear_pipeline()
        self.procesador.PC -= instruction.offset + 1  # Penalización por mal predicción


class BranchPredictor:
    def __init__(self, default_prediction=False):
        """
        Inicializa el BranchPredictor con una política predeterminada.
        default_prediction: True para 'salto tomado', False para 'no tomado'.
        """
        self.history = {}  # Diccionario con el historial dinámico
        self.default_prediction = default_prediction  # Política predeterminada

    def predict(self, instruction_id):
        """Devuelve la predicción para una instrucción específica."""
        # Si no hay historial, aplica la predicción por defecto
        return self.history.get(instruction_id, self.default_prediction)

    def update(self, instruction_id, actual_outcome):
        """Actualiza el historial dinámico basado en el resultado real."""
        self.history[instruction_id] = actual_outcome
        print(f"Historial actualizado para instrucción {instruction_id}: {actual_outcome}")

    def reset(self):
        """Resetea el historial dinámico."""
        self.history = {}
