print("Algebra Structures Project")
A = list(map(int, input("Himpunan: ").split(",")))
op1 = input("Definisikan operasi penjumlahan(a,b): ")
op2 = input("Definisikan operasi perkalian  (a,b): ")
def tambah(a,b):
    return eval(op1, {},{"a":a, "b":b})
def kali(a,b):
    return eval(op1, {},{"a":a, "b":b})
#Ring checker
check = input("cek: ")

#closure
def closure():
    if check == "grup abel":
        for x in A:
            for y in A:
                hasil = tambah(x,y)
                if hasil not in A:
                    print("x+y tidak tertutup")
                    break
            if hasil not in A:
                break
    else:
        for x in A:
            for y in A:
                hasil = kali(x,y)
                if hasil not in A:
                    print("x*y tidak tertutup")
                    break
            if hasil not in A:
                break
closure()

def asosiatif():
    if check=="grup abel":
       for x in A:
            for y in A:
                for z in A:
                    hasil1=tambah(x,tambah(y,z))
                    hasil2=tambah(tambah(x,y),z)
                    if hasil1!=hasil2 or hasil1&hasil2 not in A:
                        print("+ tidak asosiatif")
                        break
                if hasil1!=hasil2 or hasil1&hasil2 not in A:
                        print("+ tidak asosiatif")
                        break
            if hasil1!=hasil2 or hasil1&hasil2 not in A:
                        print("+ tidak asosiatif")
                        break
    else:
       for x in A:
            for y in A:
                for z in A:
                    hasil1=kali(x,kali(y,z))
                    hasil2=kali(kali(x,y),z)
                    if hasil1!=hasil2 or hasil1&hasil2 not in A:
                        print("+ tidak asosiatif")
                        break
                if hasil1!=hasil2 or hasil1&hasil2 not in A:
                        break
            if hasil1!=hasil2 or hasil1&hasil2 not in A:
                        break
asosiatif()

def identity():
    for x in A:
        e = x
        for y in A:
            if tambah(e,y)==tambah(y,e) in A:
                return e
identity()

def inverse():
    if check == "grup abel":
        for x in A:
            for y in A:
                if tambah(x,y)==
                    print("x+y tidak tertutup")
                    break
            if hasil not in A:
                break
invese()