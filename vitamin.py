from tkinter import * 
from pyswip import Prolog

# Daftar gejala yang ditanyakan
gejala_list = [
    "penglihatan malam terganggu",
    "kulit kering",
    "mata kering",
    "mudah lelah",
    "sariawan",
    "kesemutan",
    "gusi berdarah",
    "luka lama sembuh",
    "mudah memar"
]

# Mapping nama vitamin
vitamin_labels = {
    'vitamin_a': 'Vitamin A',
    'vitamin_b': 'Vitamin B',
    'vitamin_c': 'Vitamin C'
}

# Inisialisasi Prolog
prolog = Prolog()
prolog.consult("vitamin.pl")  # Pastikan file .pl ada di direktori yang sama

# Setup GUI
root = Tk()
root.title("Sistem Pakar Kekurangan Vitamin A, B, C")
root.geometry("550x500")
root.configure(bg="#FFFDD0")  # Background cream

index = 0
jawaban_gejala = {}

# Label pertanyaan
label = Label(root, text="Pertanyaan gejala akan muncul di sini", font=('Arial', 14), wraplength=400, bg="#FFFDD0")
label.pack(pady=20)

# Kotak hasil
hasil_box = Text(root, height=18, width=60, bg="#FFFFF0")
hasil_box.pack(pady=10)

# Fungsi untuk menampilkan pertanyaan
def tampilkan_pertanyaan():
    global index
    if index < len(gejala_list):
        label.config(text=f"Apakah Anda mengalami: {gejala_list[index]}?")
    else:
        diagnosa()

# Fungsi untuk merekam jawaban
def jawab(ya):
    global index
    gejala = gejala_list[index]
    jawaban_gejala[gejala] = ya
    index += 1
    tampilkan_pertanyaan()

# Fungsi diagnosa
def diagnosa():
    label.pack_forget()
    btn_ya.pack_forget()
    btn_tidak.pack_forget()
    hasil_box.delete('1.0', END)

    prolog.retractall("tanya(_)")

    for gejala, ya in jawaban_gejala.items():
        if ya:
            prolog.assertz(f"tanya('{gejala}')")

    gejala_dialami = [g for g, ya in jawaban_gejala.items() if ya]
    if gejala_dialami:
        hasil_box.insert(END, "Gejala yang Anda alami:\n")
        for g in gejala_dialami:
            hasil_box.insert(END, f"- {g}\n")
        hasil_box.insert(END, "\n")

    hasil = list(prolog.query("diagnosa_unik(Vitamin)"))

    if hasil:
        hasil_box.insert(END, "Kemungkinan kekurangan vitamin:\n")
        ditampilkan = set()
        for item in hasil:
            vitamin_code = str(item['Vitamin'])
            if vitamin_code not in ditampilkan:
                vitamin_nama = vitamin_labels.get(vitamin_code, vitamin_code)
                hasil_box.insert(END, f"- {vitamin_nama}\n")
                ditampilkan.add(vitamin_code)
    else:
        hasil_box.insert(END, "Tidak terdeteksi kekurangan vitamin A, B, atau C.")

# Tombol Ya dan Tidak
btn_ya = Button(root, text="Ya", width=15, bg='#ADD8E6', activebackground='#87CEFA', command=lambda: jawab(True))
btn_ya.pack(pady=5)

btn_tidak = Button(root, text="Tidak", width=15, bg='#ADD8E6', activebackground='#87CEFA', command=lambda: jawab(False))
btn_tidak.pack(pady=5)

tampilkan_pertanyaan()
root.mainloop()
