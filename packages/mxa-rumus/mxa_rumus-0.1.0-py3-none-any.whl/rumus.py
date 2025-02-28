import math

class Aritmatika:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def tambah(self):
        return self.x + self.y

    def kurang(self):
        return self.x - self.y

    def kali(self):
        return self.x * self.y

    def bagi(self):
        if self.y != 0:
            return self.x / self.y
        else:
            return "Tidak bisa membagi dengan nol"

class Segitiga:
    def __init__(self, alas, tinggi):
        self.alas = alas
        self.tinggi = tinggi

    def luas(self):
        return 0.5 * self.alas * self.tinggi

    def keliling(self):
        return 3 * self.alas

class Persegi:
    def __init__(self, sisi):
        self.sisi = sisi

    def luas(self):
        return self.sisi ** 2

    def keliling(self):
        return 4 * self.sisi
    

class Lingkaran:
    def __init__(self, radius):
        self.radius = radius

    def luas(self):
        return 3.14 * self.radius ** 2

    def keliling(self):
        return 2 * 3.14 * self.radius
    
class Permutasi:
    def __init__(self, n, r):
        self.n = n
        self.r = r

    def hitung(self):
        return math.factorial(self.n) / math.factorial(self.n - self.r)
    
class Kombinasi:
    def __init__(self, n, r):
        self.n = n
        self.r = r

    def hitung(self):
        return math.factorial(self.n) / (math.factorial(self.r) * math.factorial(self.n - self.r))
