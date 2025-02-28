

class RumusMatematika:
    def kurang(a, b):
        return a - b
    
    def tambah(a, b): 
        return a + b

    def kali(a, b):
        return a * b

    def bagi(a, b):
        return a / b
    
    def luasPersegi(sisi):
        return sisi * sisi


def main():
    print("Hello from main-app!")

    hasil = RumusMatematika.luasPersegi(4)
    print(hasil)

if __name__ == "__main__":
    main()
