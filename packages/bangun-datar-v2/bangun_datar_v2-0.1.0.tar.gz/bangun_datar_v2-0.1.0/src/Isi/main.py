import math

def luas_persegi(s):
    return s * s

def keliling_persegi(s):
    return 4 * s

def luas_persegi_panjang(p, l):
    return p * l

def keliling_persegi_panjang(p, l):
    return 2 * (p + l)

def luas_segitiga(a, t):
    return 0.5 * a * t

def keliling_segitiga(a, b, c):
    return a + b + c

def luas_lingkaran(r):
    return math.pi * r * r

def keliling_lingkaran(r):
    return 2 * math.pi * r

def luas_trapesium(a, b, t):
    return 0.5 * (a + b) * t

def keliling_trapesium(a, b, c, d):
    return a + b + c + d

def luas_jajargenjang(a, t):
    return a * t

def keliling_jajargenjang(a, b):
    return 2 * (a + b)

def luas_belah_ketupat(d1, d2):
    return 0.5 * d1 * d2

def keliling_belah_ketupat(s):
    return 4 * s

def luas_layang_layang(d1, d2):
    return 0.5 * d1 * d2

def keliling_layang_layang(a, b):
    return 2 * (a + b)

# Contoh penggunaan
if __name__ == "__main__":
    print("Pilih bangun datar yang ingin dihitung:")
    print("1. Persegi")
    print("2. Persegi Panjang")
    print("3. Segitiga")
    print("4. Lingkaran")
    print("5. Trapesium")
    print("6. Jajargenjang")
    print("7. Belah Ketupat")
    print("8. Layang-layang")
    
    pilihan = int(input("Masukkan pilihan (1-8): "))
    
    if pilihan == 1:
        s = float(input("Masukkan sisi persegi: "))
        print("Luas:", luas_persegi(s))
        print("Keliling:", keliling_persegi(s))
    elif pilihan == 2:
        p = float(input("Masukkan panjang: "))
        l = float(input("Masukkan lebar: "))
        print("Luas:", luas_persegi_panjang(p, l))
        print("Keliling:", keliling_persegi_panjang(p, l))
    elif pilihan == 3:
        a = float(input("Masukkan alas: "))
        t = float(input("Masukkan tinggi: "))
        b = float(input("Masukkan sisi kedua: "))
        c = float(input("Masukkan sisi ketiga: "))
        print("Luas:", luas_segitiga(a, t))
        print("Keliling:", keliling_segitiga(a, b, c))
    elif pilihan == 4:
        r = float(input("Masukkan jari-jari lingkaran: "))
        print("Luas:", luas_lingkaran(r))
        print("Keliling:", keliling_lingkaran(r))
    elif pilihan == 5:
        a = float(input("Masukkan sisi atas: "))
        b = float(input("Masukkan sisi bawah: "))
        t = float(input("Masukkan tinggi: "))
        c = float(input("Masukkan sisi miring kiri: "))
        d = float(input("Masukkan sisi miring kanan: "))
        print("Luas:", luas_trapesium(a, b, t))
        print("Keliling:", keliling_trapesium(a, b, c, d))
    elif pilihan == 6:
        a = float(input("Masukkan alas: "))
        t = float(input("Masukkan tinggi: "))
        b = float(input("Masukkan sisi miring: "))
        print("Luas:", luas_jajargenjang(a, t))
        print("Keliling:", keliling_jajargenjang(a, b))
    elif pilihan == 7:
        d1 = float(input("Masukkan diagonal pertama: "))
        d2 = float(input("Masukkan diagonal kedua: "))
        s = float(input("Masukkan panjang sisi: "))
        print("Luas:", luas_belah_ketupat(d1, d2))
        print("Keliling:", keliling_belah_ketupat(s))
    elif pilihan == 8:
        d1 = float(input("Masukkan diagonal pertama: "))
        d2 = float(input("Masukkan diagonal kedua: "))
        a = float(input("Masukkan sisi pertama: "))
        b = float(input("Masukkan sisi kedua: "))
        print("Luas:", luas_layang_layang(d1, d2))
        print("Keliling:", keliling_layang_layang(a, b))
    else:
        print("Pilihan tidak valid.")
