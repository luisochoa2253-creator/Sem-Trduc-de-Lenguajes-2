import re

class AnalizadorLR:
    def __init__(self, tabla_accion, tabla_ir_a, reglas):
        self.tabla_accion = tabla_accion
        self.tabla_ir_a = tabla_ir_a
        self.reglas = reglas

    def _tokenize(self, expr):
        """
        Convierte la cadena en tokens (id, +, $).
        Todos los identificadores se transforman en 'id',
        pero guardamos el lexema original para mostrarlo.
        """
        tokens = []
        for m in re.finditer(r'[A-Za-z_]\w*|\+|\$', expr.replace(' ', '')):
            lex = m.group(0)
            if lex == '+':
                tokens.append(('+' , '+'))
            elif lex == '$':
                tokens.append(('$' , '$'))
            else:
                tokens.append(('id', lex))  # cualquier identificador es 'id'
        return tokens

    def _pila_str(self, pila):
        """
        Convierte la pila [0, 'hola', 2, '+', 3, 'mundo', 4...] 
        a string estilo $0hola2+3mundo4
        """
        s = "$0"
        for i in range(1, len(pila), 2):
            s += str(pila[i]) + str(pila[i+1])
        return s

    def analizar(self, expr):
        tokens = self._tokenize(expr) + [('$', '$')]  # fin de cadena
        pila = [0]  # pila empieza en estado 0
        i = 0

        print(f"{'pila':<25}{'entrada':<25}{'salida'}")
        print("-"*70)

        while True:
            estado = pila[-1]
            simbolo, lexema = tokens[i]
            accion = self.tabla_accion.get((estado, simbolo))

            if accion is None:
                print(f"Error de sintaxis en '{lexema}' con estado {estado}")
                break

            entrada_str = ''.join(lx for _, lx in tokens[i:])
            pila_str = self._pila_str(pila)

            # SHIFT (desplazar)
            if accion.startswith("d"):
                nuevo_estado = int(accion[1:])
                pila.append(lexema)       # guardamos el lexema real
                pila.append(nuevo_estado)
                print(f"{pila_str:<25}{entrada_str:<25}{accion}")
                i += 1

            # REDUCE (reducir)
            elif accion.startswith("r"):
                if accion == "r0":
                    print(f"{pila_str:<25}{entrada_str:<25}r0 (acept)")
                    break
                num_regla = int(accion[1:])
                izq, der = self.reglas[num_regla]
                for _ in range(2 * len(der)):
                    pila.pop()
                estado = pila[-1]
                goto = self.tabla_ir_a[(estado, izq)]
                pila.append(izq)
                pila.append(goto)
                print(f"{pila_str:<25}{entrada_str:<25}r{num_regla} {izq} -> {' '.join(der)}")


# =================== Gramática 1 ===================
# E -> id + id

tabla_accion_1 = {
    (0, "id"): "d2",
    (2, "+"): "d3",
    (3, "id"): "d4",
    (4, "$"): "r1",   # reducir E -> id + id
    (1, "$"): "r0"    # aceptar
}
tabla_ir_a_1 = {
    (0, "E"): 1
}
reglas_1 = {
    1: ("E", ["id", "+", "id"])
}

analizador1 = AnalizadorLR(tabla_accion_1, tabla_ir_a_1, reglas_1)

# =================== Gramática 2 ===================
# r1: E -> id + E
# r2: E -> id

tabla_accion_2 = {
    (0, "id"): "d2",
    (2, "+"): "d3",
    (2, "$"): "r2",
    (3, "id"): "d2",
    (4, "$"): "r1",
    (4, "+"): "r1",
    (1, "$"): "r0"
}
tabla_ir_a_2 = {
    (0, "E"): 1,
    (3, "E"): 4
}
reglas_2 = {
    1: ("E", ["id", "+", "E"]),
    2: ("E", ["id"])
}

analizador2 = AnalizadorLR(tabla_accion_2, tabla_ir_a_2, reglas_2)


# =================== PRUEBAS ===================

print("=== Análisis con Gramática 1 (E -> id + id) ===")
analizador1.analizar("hola + mundo")

print("\n=== Análisis con Gramática 2 (E -> id + E | id) ===")
analizador2.analizar("a+b+c+d+f+g")
