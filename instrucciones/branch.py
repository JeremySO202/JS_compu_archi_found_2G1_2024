class Jump:
    def __init__(self, _offset, _procesador):
        self.offset = _offset
        self.procesador = _procesador

    def ejecutar(self):
        print(f"Realizando salto incondicional con offset {self.offset}")
        self.procesador.PC += self.offset - 1  # Ajustar por el incremento automático en FETCH
