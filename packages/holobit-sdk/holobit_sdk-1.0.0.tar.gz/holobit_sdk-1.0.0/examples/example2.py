from assembler.parser import AssemblerParser
from visualization.projector import proyectar_holograma

# Instanciar el parser del ensamblador
parser = AssemblerParser()

# Definir un conjunto de instrucciones en lenguaje ensamblador
codigo_ensamblador = """
CREAR Q1 (0.1, 0.2, 0.3)        ; Crear un quark Q1
CREAR Q2 (0.4, 0.5, 0.6)        ; Crear un quark Q2
CREAR Q3 (0.7, 0.8, 0.9)        ; Crear un quark Q3
CREAR Q4 (1.0, 1.1, 1.2)        ; Crear un quark Q4
CREAR Q5 (1.3, 1.4, 1.5)        ; Crear un quark Q5
CREAR Q6 (1.6, 1.7, 1.8)        ; Crear un quark Q6

; Crear un Holobit H1 a partir de los quarks
CREAR H1 {Q1, Q2, Q3, Q4, Q5, Q6}

; Rotar el Holobit H1 en el eje Z
ROT H1 z 90
"""


# Interpretar y ejecutar cada línea del código ensamblador
for linea in codigo_ensamblador.strip().split("\n"):
    parser.parse_line(linea)

# Obtener el Holobit construido por el ensamblador
holobit = parser.holobits["H1"]

# Visualizar el Holobit resultante
proyectar_holograma(holobit)
