class BarraProgreso:
    def __init__(self, total, longitud=30):
        self.total = total
        self.longitud = longitud
        self.iteracion_actual = 0

    def actualizar(self, incremento=1):
        self.iteracion_actual += incremento
        porcentaje = self.iteracion_actual / self.total
        caracteres_llenos = int(self.longitud * porcentaje)
        caracteres_vacios = self.longitud - caracteres_llenos
        barra = '#' * caracteres_llenos + '-' * caracteres_vacios
        porcentaje_completado = porcentaje * 100
        mensaje = f"[{barra}] {porcentaje_completado:.1f}%"
        return mensaje