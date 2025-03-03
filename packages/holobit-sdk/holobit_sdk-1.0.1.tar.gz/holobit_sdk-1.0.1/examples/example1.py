from core.quark import Quark
from core.holobit import Holobit
from visualization.projector import proyectar_holograma

# Crear 6 quarks con diferentes posiciones
q1 = Quark(0.1, 0.2, 0.3)
q2 = Quark(0.4, 0.5, 0.6)
q3 = Quark(0.7, 0.8, 0.9)
q4 = Quark(1.0, 1.1, 1.2)
q5 = Quark(1.3, 1.4, 1.5)
q6 = Quark(1.6, 1.7, 1.8)

# Crear antiquarks con posiciones opuestas a los quarks
antiquarks = [
    Quark(-q.posicion[0], -q.posicion[1], -q.posicion[2])
    for q in [q1, q2, q3, q4, q5, q6]
]

# Crear el Holobit
h1 = Holobit([q1, q2, q3, q4, q5, q6], antiquarks)

# Realizar una rotación del Holobit
h1.rotar("z", 180)

# Proyectar el Holobit en un espacio 3D
proyectar_holograma(h1)

