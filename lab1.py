class Contact:
    def __init__(self, name, email, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.email = email

    def display(self):
        print(f"Nume: {self.name}, Email: {self.email}")

class Friend(Contact):
    def __init__(self, name, email, phone, **kwargs):
        super().__init__(name=name, email=email, **kwargs)
        self.phone = phone

    def display(self):
        super().display()
        print(f"Telefon: {self.phone}")

def main():
    print("--- Testare clasa Friend ---")
    prieten = Friend(name="Andrei", email="andrei@exemplu.ro", phone="0712345678")
    prieten.display()

if __name__ == "__main__":
    main()
