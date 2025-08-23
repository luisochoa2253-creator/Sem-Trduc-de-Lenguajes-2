En el archivo Analizador_Sintactico se implementa un algoritmo en el cual contamos con:
Una clase AnalizadorLr en la cual se definen las acciones a realizar en cada estado y simbolodo diferente.
class AnalizadorLR:
    def __init__(self, tabla_acciones, tabla_ir_a, producciones):
        self.tabla_acciones = tabla_acciones
        self.tabla_ir_a = tabla_ir_a
        self.producciones = producciones
        
Tenemos un metodo analizar el cual se encarga de convertir la entrada en token para su procesamiento
iniciando la pila en 0 con simbolo $
def analizar(self, cadena):
    cadena = self.tokenizar(cadena) + ["$"]
    pila = [(0, "$")]
    pasos = []

