class Cell:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MuscleCell(Cell):
    def __init__(self, mass, scopes=None, **kwargs):
        super().__init__(**kwargs)
        self.mass = mass
        self.scopes = scopes if scopes else set()

class NerveCell(Cell):
    def __init__(self, length, **kwargs):
        super().__init__(**kwargs)
        self.length = length


class Biceps(MuscleCell):
    def __init__(self, arm, mass, **kwargs):
        super().__init__(mass=mass, scopes={"locomotor", f"incordare brat {arm}"}, **kwargs)
        self.arm = arm

class Triceps(MuscleCell):
    def __init__(self, arm, mass, **kwargs):
        super().__init__(mass=mass, scopes={"locomotor", f"relaxare brat {arm}"}, **kwargs)
        self.arm = arm

class LegMuscle(MuscleCell):
    def __init__(self, part, mass, **kwargs):
        super().__init__(mass=mass, scopes={"locomotor", part}, **kwargs)
        self.part = part

class SpineNerve(NerveCell):
    def __init__(self, location, length, **kwargs):
        super().__init__(length=length, **kwargs)
        self.location = location

def get_muscle_mass(cells):
    return sum(cell.mass for cell in cells if isinstance(cell, MuscleCell))

def get_nerve_length(cells):
    return sum(cell.length for cell in cells if isinstance(cell, NerveCell))

def get_locomotor_muscles(cells):
    return [c for c in cells if isinstance(c, MuscleCell) and "locomotor" in c.scopes]

def get_spine_nerves(cells):
    return [c for c in cells if isinstance(c, SpineNerve)]

if __name__ == "__main__":
    cells = [
        Biceps("stanga", mass=500),
        Biceps("dreapta", mass=550),
        Triceps("stanga", mass=400),
        Triceps("dreapta", mass=420),
        LegMuscle("miscare glezna stanga", mass=600),
        SpineNerve("cervicala", length=15),
        SpineNerve("lombara", length=20)
    ]

    print("=== Subpunctul B: Calcule ===")
    print(f"Masa musculara totala: {get_muscle_mass(cells)} grame")
    print(f"Lungimea nervilor totala: {get_nerve_length(cells)} cm")

    print("\n=== Subpunctul C: Afisari specifice ===")
    print("Muschii cu rol locomotor:")
    for m in get_locomotor_muscles(cells):
        print(f" - {type(m).__name__} (scopuri: {m.scopes})")

    print("\nFibrele nervoase din zona coloanei:")
    for n in get_spine_nerves(cells):
        print(f" - Zona {n.location}, lungime: {n.length} cm")