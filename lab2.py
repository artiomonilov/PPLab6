class BaseClass:
    num_base_calls = 0
    def call_me(self, caller):
        print(f"BaseClass a fost apelata de {caller}")
        BaseClass.num_base_calls += 1

class LeftSubclass(BaseClass):
    def call_me(self, caller):
        BaseClass.call_me(self, "LeftSubclass")
        print(f"LeftSubclass a fost apelata de {caller}")

class RightSubclass(BaseClass):
    def call_me(self, caller):
        BaseClass.call_me(self, "RightSubclass")
        print(f"RightSubclass a fost apelata de {caller}")

class Subclass(LeftSubclass, RightSubclass):
    def call_me(self, caller):
        LeftSubclass.call_me(self, "Subclass")
        RightSubclass.call_me(self, "Subclass")
        print(f"Subclass a fost apelata de {caller}")

if __name__ == "__main__":
    print("Testare cu apel explicit BaseClass.call_me() in loc de super():")
    s = Subclass()lab
    s.call_me("Main")
    
    print("\nOBSERVATIE:")
    print("Inlocuirea apelului super() cu BaseClass.call_me(...) duce la pierderea mecanismului de MRO (Method Resolution Order).")
    print("Astfel, metoda call_me a clasei de baza (BaseClass) este apelata de 2 ori (o data pentru LeftSubclass si o data pentru RightSubclass), ceea ce este ineficient si poate cauza duplicarea prelucrarilor sau a initializarii.")