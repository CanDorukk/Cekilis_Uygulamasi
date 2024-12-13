import tkinter as tk
import random 
from tkinter import ttk 
import sqlite3
from tkinter import messagebox


def kazanan_kisi():
    rastgele_sayi = random.randint(0, len(elemanlar) - 1)
    kazanan_kisi = elemanlar[rastgele_sayi]
    kazanan_listesi.append(kazanan_kisi)
    elemanlar.pop(rastgele_sayi)
    
    




def kazanan_ekranda_gosterme():
    kazanan_tablosu.delete(*kazanan_tablosu.get_children())  # Önceki kazananları temizle
    for sira, kazanan_yazdirma in enumerate(kazanan_listesi, start=1):
        kazanan_tablosu.insert("", "end", values=(sira, kazanan_yazdirma))


        

def yeni_cekilis():
    global kazanan_listesi, elemanlar, label_listesi
    kazanan_listesi = []
    elemanlar = [satir[0] for satir in cursor.execute("SELECT isim FROM isimler")]
    
    for label in label_listesi:
        label.destroy()
    label_listesi = []
    
    toplam_cekim = int(combo.get())
    
    while toplam_cekim > 0:
        if len(elemanlar) == 0:
            elemanlar = [satir[0] for satir in cursor.execute("SELECT isim FROM isimler")]
        kazanan_kisi()
        toplam_cekim -= 1
    
    kazanan_ekranda_gosterme()
  
    



def metni_al():
    metin = text_box.get("1.0", tk.END)  # Metni al
    x = metin.split(',')  # Virgüllerle ayır
    
    yeni_eklenenler = []  # Yeni eklenen isimleri takip etmek için bir liste
    
    for isim in x:  # Liste elemanlarını döngüyle işle
        isim = isim.strip()  # Baştaki ve sondaki boşlukları temizle
        
        if isim:  # Boş olmayan değerleri işle
            # Veritabanında ismin olup olmadığını kontrol et
            cursor.execute("SELECT COUNT(*) FROM isimler WHERE isim = ?", (isim,))
            sonuc = cursor.fetchone()
            
            if sonuc[0] == 0:  # İsim veritabanında yoksa ekle
                cursor.execute("INSERT INTO isimler (isim) VALUES (?)", (isim,))
                yeni_eklenenler.append(isim)  # Yeni eklenen ismi listeye ekle
            else:
                # İsim zaten mevcutsa uyarı mesajı göster
                messagebox.showwarning("Uyarı", f"{isim} zaten listede mevcut!")
    
    conn.commit()  # Tüm işlemleri kaydet
    
    # Eğer yeni eklenen isimler varsa, başarı mesajı göster
    if yeni_eklenenler:
        messagebox.showinfo("Bilgi", f"{', '.join(yeni_eklenenler)} başarıyla eklendi.")


    
def text_placeholder_in(event):
    """Kullanıcı yazmaya başladığında placeholder'ı siler."""
    if text_box.get("1.0", tk.END).strip() == placeholder_text:
        text_box.delete("1.0", tk.END)
        text_box.config(fg="black")  # Yazı rengini normal yap

def text_placeholder_out(event):
    """Kullanıcı text box'tan ayrıldığında eğer içerik boşsa placeholder'ı ekler."""
    if text_box.get("1.0", tk.END).strip() == "":
        text_box.insert("1.0", placeholder_text)
        text_box.config(fg="grey")  # Placeholder yazısı rengi








# TKINTER Kodları

root = tk.Tk()
root.resizable(0,0)
root.geometry('1000x700')
root.title('Çekiliş Uygulaması')
root.iconbitmap('first-prize.ico')
# Üst ve alt çerçeveleri oluştur
ust_frame = tk.Frame(root, bg="#D6EAF8", height=400, width=1000)  # Açık mavi
alt_frame = tk.Frame(root, bg="#D5F5E3", height=300, width=1000)  # Açık yeşil

# Çerçeveleri yerleştir
ust_frame.pack(side="top", fill="x")
alt_frame.pack(side="bottom", fill="x")



# Veritabanına bağlan
conn = sqlite3.connect("cekilis_verisi.db")
cursor = conn.cursor()


# Başlangıç verilerini al
elemanlar = [satir[0] for satir in cursor.execute("SELECT isim FROM isimler")]
kazanan_listesi = []
label_listesi = []





placeholder_text = "İsimleri virgülle ayırarak girin..."

# Text box oluşturma
text_box = tk.Text(root, wrap="word", font=("Calibri", 12), height=5, width=50, bg="#F9EBEA")
text_box.place(x=300, y=100)
text_box.insert("1.0", placeholder_text)

# Placeholder için bind olayları
text_box.bind("<FocusIn>", text_placeholder_in)  # Kullanıcı text'e odaklandığında
text_box.bind("<FocusOut>", text_placeholder_out)  # Kullanıcı text'ten çıktığında


button = tk.Button(
    root,
    text="Metni Al",
    command=metni_al,
    bg="#5DADE2",
    fg="white",
    font=("Arial", 12, "bold"),
    relief="raised",
)


button.place(x=550, y=250)
cekilis_buton = tk.Button(
    ust_frame,
    text="Çekiliş Başlat",
    command=yeni_cekilis,
    bg="#5DADE2",
    fg="white",
    font=("Arial", 12, "bold"),
    relief="raised",
)
cekilis_buton.place(x=350, y=250)

kazanan_tablosu = ttk.Treeview(alt_frame, columns=("Sıra", "Kazanan"), show="headings", height=10)
kazanan_tablosu.heading("Sıra", text="Sıra")
kazanan_tablosu.heading("Kazanan", text="Kazanan")
kazanan_tablosu.column("Sıra", width=50, anchor="center")
kazanan_tablosu.column("Kazanan", width=800, anchor="center")
kazanan_tablosu.place(x=100, y=50)


numbers = [str(i) for i in range(1, 17)]
combo = ttk.Combobox(root, values=numbers,state="readonly",width=30)
combo.set("1")  # Varsayılan değeri "1" olarak ayarla
combo.place(x=395,y=305)


# tekrar_cek_buton = tk.Button(ust_frame,text='Yeniden Çek')
# tekrar_cek_buton.place(x=)




root.mainloop()