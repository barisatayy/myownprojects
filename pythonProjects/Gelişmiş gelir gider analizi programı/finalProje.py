from tkinter import Tk, Canvas, Entry, Button, PhotoImage, ttk, END
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from tkinter import messagebox
import tkinter as tk
import sys

if hasattr(sys, '_MEIPASS'):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent

ASSETS_PATH = BASE_DIR / "assets" / "frame0"
EXCEL_PATH = BASE_DIR / "assets" / "database.xlsx"
renkler = {
    'Kira': 'blue',
    'İş/Maaş': 'red',
    'Diğer': 'green',
    'Alışveriş': 'purple',
    'Giyim': 'orange',
    'Ulaşım': 'brown'
}


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def aykiri_deger_analizi(veri, sutun, tur):
    tur_verisi = veri[veri['Tür'] == tur]
    Q1 = tur_verisi[sutun].quantile(0.25)
    Q3 = tur_verisi[sutun].quantile(0.75)
    IQR = Q3 - Q1
    alt_sinir = Q1 - 1.5 * IQR
    ust_sinir = Q3 + 1.5 * IQR
    aykirilar = tur_verisi[(tur_verisi[sutun] < alt_sinir) | (tur_verisi[sutun] > ust_sinir)]
    return aykirilar, alt_sinir, ust_sinir


def aykiri_deger_grafik(veri, sutun, veri_turu):
    turler = veri['Tür'].unique()
    for tur in turler:
        aykirilar, alt_sinir, ust_sinir = aykiri_deger_analizi(veri, sutun, tur)

        plt.figure(figsize=(8, 6))

        # Normal veriler
        plt.plot(veri[veri['Tür'] == tur].index, veri[veri['Tür'] == tur][sutun], 'o-', label=f'{tur} (Normal)',
                 color=renkler.get(tur, 'black'))

        # Alt ve üst sınırlar
        plt.axhline(alt_sinir, color='green', linestyle='--', label=f'{tur} Alt Sınır')
        plt.axhline(ust_sinir, color='green', linestyle='--', label=f'{tur} Üst Sınır')

        # Aykırı değerler
        for idx, row in aykirilar.iterrows():
            plt.plot(idx, row[sutun], 'ro', label=f'{tur} Aykırı Değer' if idx == aykirilar.index[0] else "")

        plt.title(f'{veri_turu} Aykırı Değer Analizi - {tur}')
        plt.xlabel('Veri İndeksi')
        plt.ylabel(sutun)
        plt.legend()
        plt.grid()

        plt.show()


def aykiri_deger_analizini_calistir():
    try:
        # Excel'den gelir ve gider verilerini yükle
        gelirler_df = pd.read_excel(EXCEL_PATH, sheet_name="Gelirler")
        giderler_df = pd.read_excel(EXCEL_PATH, sheet_name="Giderler")

        sutun = "Miktar"  # Analiz edilecek sütun

        # Gelirler için aykırı değer grafikleri
        if not gelirler_df.empty:
            aykiri_deger_grafik(gelirler_df, sutun, "Gelirler")

        # Giderler için aykırı değer grafikleri
        if not giderler_df.empty:
            aykiri_deger_grafik(giderler_df, sutun, "Giderler")

    except FileNotFoundError:
        messagebox.showerror("Hata", "Excel dosyası bulunamadı.")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")


def tahmin_grafik(df, veri_turu):
    turler = df['Tür'].unique()
    for tur in turler:
        tur_verileri = df[df['Tür'] == tur].reset_index()

        if len(tur_verileri) < 2:
            messagebox.showwarning("Uyarı", f"{tur} için yeterli veri yok. Tahmin yapılamaz.")
            continue

        renk = renkler.get(tur, 'black')
        X = np.arange(len(tur_verileri)).reshape(-1, 1)
        y = tur_verileri['Miktar'].values

        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)

        model = LinearRegression()
        model.fit(X_poly, y)

        next_index = np.array([[len(tur_verileri)]])
        next_index_poly = poly.transform(next_index)
        tahmini_miktar = model.predict(next_index_poly)[0]

        plt.figure(figsize=(8, 6))

        plt.plot(tur_verileri.index, y, 'o-', color=renk, label=f'{tur} (Gerçek)')
        plt.plot(np.append(tur_verileri.index, len(tur_verileri)),
                 np.append(model.predict(X_poly), tahmini_miktar), 'r--', label=f'{tur} Tahmini')

        plt.title(f'{veri_turu} Tahmin Grafiği - {tur}')
        plt.xlabel('Dönem')
        plt.ylabel('Miktar (TL)')
        plt.legend()
        plt.grid()
        plt.show()


def tahmin_hesapla():
    try:
        gelirler_df = pd.read_excel(EXCEL_PATH, sheet_name="Gelirler")
        giderler_df = pd.read_excel(EXCEL_PATH, sheet_name="Giderler")

        if not gelirler_df.empty:
            tahmin_grafik(gelirler_df, "Gelirler")

        if not giderler_df.empty:
            tahmin_grafik(giderler_df, "Giderler")

    except FileNotFoundError:
        messagebox.showerror("Hata", "Excel dosyası bulunamadı.")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")


gelirler = []
giderler = []


def gelir_ekle():
    try:
        if gelirTuru.get() == "Seçiniz":  # Combobox'ta seçim yapılmamışsa
            messagebox.showerror("Hata", "Lütfen bir gelir türü seçin.")
            return
        gelir_turu = gelirTuru.get()
        gelir_miktari = float(gelirEntry.get())
        if gelir_miktari > 0:
            gelirler.append({"Tür": gelir_turu, "Miktar": gelir_miktari})
            messagebox.showinfo("Başarılı", "Gelir başarıyla eklendi.")
            gelirEntry.delete(0, END)
            gelirTuru.set("Seçiniz")

        else:
            messagebox.showerror("Hata", "Geçerli bir miktar girin")
            gelirEntry.delete(0, END)
            gelirTuru.set("Seçiniz")

    except ValueError:
        messagebox.showerror("Hata", "Geçerli bir miktar girin.")
        gelirEntry.delete(0, END)
        gelirTuru.set("Seçiniz")


# Gider ekleme fonksiyonu
def gider_ekle():
    try:
        if giderTuru.get() == "Seçiniz":  # Combobox'ta seçim yapılmamışsa
            messagebox.showerror("Hata", "Lütfen bir gelir türü seçin.")
            return
        gider_turu = giderTuru.get()
        gider_miktari = float(giderEntry.get())
        if gider_miktari > 0:
            giderler.append({"Tür": gider_turu, "Miktar": gider_miktari})
            messagebox.showinfo("Başarılı", "Gelir başarıyla eklendi.")
            giderEntry.delete(0, END)
            giderTuru.set("Seçiniz")

        else:
            messagebox.showerror("Hata", "Geçerli bir miktar girin")
            giderEntry.delete(0, END)
            giderTuru.set("Seçiniz")


    except ValueError:
        messagebox.showerror("Hata", "Geçerli bir miktar girin.")
        giderEntry.delete(0, END)
        giderTuru.set("Seçiniz")


def hesapla():
    toplam_gelir = sum([gelir["Miktar"] for gelir in gelirler])
    toplam_gider = sum([gider["Miktar"] for gider in giderler])
    net_gelir = toplam_gelir - toplam_gider

    canvas.itemconfig(
        hesapText,
        text=f"Toplam Gelir: {toplam_gelir} TL\nToplam Gider: {toplam_gider} TL\nNet Gelir: {net_gelir} TL"
    )


def excelKaydet():
    try:
        if not gelirler and not giderler:
            messagebox.showerror("Hata", "Bir sorun oluştu")
            return

        gelirler_df = pd.DataFrame(gelirler)
        giderler_df = pd.DataFrame(giderler)

        with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl") as writer:
            if not gelirler_df.empty:
                gelirler_df.to_excel(writer, sheet_name="Gelirler", index=False)
            if not giderler_df.empty:
                giderler_df.to_excel(writer, sheet_name="Giderler", index=False)
            messagebox.showinfo("Başarılı", "Ekleme yapıldı")
    except Exception as e:
        messagebox.showerror("Hata", "Bir sorun oluştu")


def gelirGrafik():
    global gelirler_df
    try:
        # Excel dosyasını oku
        gelirler_df = pd.read_excel(EXCEL_PATH, sheet_name="Gelirler")

        # Boş mu kontrol et
        if gelirler_df.empty:
            messagebox.showerror("Hata", "Excel dosyasında gelir verisi bulunamadı.")
            return

        # Gelir türleri ve miktarlarını al
        gelir_turleri = gelirler_df['Tür'].tolist()
        gelir_miktarlari = gelirler_df['Miktar'].tolist()

        # Grafik oluştur
        plt.figure(figsize=(5, 5))
        plt.bar(gelir_turleri, gelir_miktarlari, color='skyblue', edgecolor='black')
        plt.title("Gelir Grafiği")
        plt.xlabel("Gelir Türleri")
        plt.ylabel("Miktar (TL)")
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        messagebox.showerror("Hata", "Excel dosyası bulunamadı.")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")


def giderGrafik():
    global giderler_df
    try:
        giderler_df = pd.read_excel(EXCEL_PATH, sheet_name="Giderler")
        if giderler_df.empty:
            messagebox.showerror("Hata", "Excel dosyasında gelir verisi bulunamadı.")
            return
        gider_turleri = giderler_df['Tür'].tolist()
        gider_miktarlari = giderler_df['Miktar'].tolist()

        plt.figure(figsize=(5, 5))
        plt.bar(gider_turleri, gider_miktarlari, color='skyblue', edgecolor='black')
        plt.title("Gider Grafiği")
        plt.xlabel("Gider Türleri")
        plt.ylabel("Miktar (TL)")
        plt.tight_layout()
        plt.show()
    except FileNotFoundError:
        messagebox.showerror("Hata", "Excel dosyası bulunamadı.")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")


def genelGrafik():
    global gelirler_df, giderler_df
    try:
        # Eğer gelirler_df veya giderler_df yoksa, oluşturulmuş gelirler ve giderler listesini kontrol et
        if 'gelirler_df' not in globals() or gelirler_df is None:
            if gelirler:
                gelirler_df = pd.DataFrame(gelirler)
            else:
                messagebox.showerror("Hata", "Gelir verisi bulunamadı. Lütfen gelir verilerini yükleyin veya ekleyin.")
                return

        if 'giderler_df' not in globals() or giderler_df is None:
            if giderler:
                giderler_df = pd.DataFrame(giderler)
            else:
                messagebox.showerror("Hata", "Gider verisi bulunamadı. Lütfen gider verilerini yükleyin veya ekleyin.")
                return

        # Gelir ve gider toplamlarını hesapla
        toplam_gelir = gelirler_df["Miktar"].sum()
        toplam_gider = giderler_df["Miktar"].sum()

        # Gelir ve gider karşılaştırması için veriler
        kategoriler = ["Gelir", "Gider"]
        miktarlar = [toplam_gelir, toplam_gider]

        # Grafik oluştur
        plt.figure(figsize=(5, 5))
        plt.pie(
            miktarlar,
            labels=kategoriler,
            autopct='%1.1f%%',  # Yüzde gösterimi
            colors=['green', 'red'],  # Pasta dilim renkleri
            startangle=90,  # Başlangıç açısı
            wedgeprops={"edgecolor": "black"}  # Dilimler arasında sınır çizgisi
        )
        plt.title("Genel Gelir-Gider Dağılımı")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")


def veriGoster():
    file_path = EXCEL_PATH  # Dosya yolunu belirtin

    try:
        # Excel'deki verileri oku
        dfGelir = pd.read_excel(file_path, sheet_name="Gelirler")
        dfGider = pd.read_excel(file_path, sheet_name="Giderler")

        # Yeni bir pencere oluştur
        veriWindow = tk.Toplevel(window)
        veriWindow.title("Veri Görüntüleyici")
        veriWindow.geometry("1000x600")
        veriWindow.resizable(False, False)

        # Canvas ve Scrollbar ekle
        canvas_frame = tk.Frame(veriWindow)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame)
        scroll_y = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_y.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        # Gelir ve gider metinlerini hazırlama
        gelir_str = dfGelir.to_string(index=True)
        gider_str = dfGider.to_string(index=True)

        # Gelir ve giderler için metin alanlarını oluştur
        canvas.create_text(10, 10, anchor="nw", text="Gelirler:\n" + gelir_str, font=("Courier", 18), tags="gelir")
        canvas.create_text(510, 10, anchor="nw", text="Giderler:\n" + gider_str, font=("Courier", 18), tags="gider")

        # Kaydırma alanını güncelle
        canvas.config(scrollregion=canvas.bbox("all"))

    except FileNotFoundError:
        print(f"{file_path} bulunamadı. Dosya yolunu kontrol edin.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")


def cikis():
    window.destroy()


# arayüz
window = Tk()
window.title("Veri Analizi")
screenX = window.winfo_screenwidth()
screenY = window.winfo_screenheight()

windowX = 1200
windowY = 600

posTop = int(screenY / 2 - windowY / 2)
posRight = int(screenX / 2 - windowX / 2)

window.geometry(f'{windowX}x{windowY}+{posRight}+{posTop}')

canvas = Canvas(
    window,
    bg="#FFFFFF",
    width=1200,
    height=600,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_text(
    21.0,
    35.0,
    anchor="nw",
    text="Gelir",
    fill="#000000",
    font=("Inter", 36 * -1)
)
canvas.create_text(
    20.0,
    86.0,
    anchor="nw",
    text="Gelir Tutarı",
    fill="#000000",
    font=("Inter", 36 * -1)
)

canvas.create_text(
    20.0,
    244.0,
    anchor="nw",
    text="Gider",
    fill="#000000",
    font=("Inter", 36 * -1)
)

canvas.create_text(
    20.0,
    299.0,
    anchor="nw",
    text="Gider Tutarı",
    fill="#000000",
    font=("Inter", 36 * -1)
)

hesapText = canvas.create_text(
    325.0,
    449.0,
    anchor="nw",
    text="",
    fill="#000000",
    font=("Inter", 17 * -1)
)

gelirEntry = Entry(
    bd=0,
    bg="lightgrey",
    fg="black",
    highlightthickness=1
)
gelirEntry.place(
    x=325.0,
    y=94.0,
    width=221.0,
    height=35.0
)

giderEntry = Entry(
    bd=0,
    bg="lightgrey",
    fg="black",
    highlightthickness=1
)
giderEntry.place(
    x=325.0,
    y=305.0,
    width=221.0,
    height=35.0
)

gelirListe = [
    'Kira',
    'İş/Maaş',
    'Diğer'
]
giderListe = [
    'Kira',
    'Alışveriş',
    'Giyim',
    'Ulaşım',
    'Diğer'
]

gelirTuru = combobox = ttk.Combobox(window, values=gelirListe, state="readonly")
gelirTuru.set("Seçiniz")
gelirTuru.place(x=317, y=38, width=240, height=32)

giderTuru = combobox = ttk.Combobox(window, values=giderListe, state="readonly")
giderTuru.set("Seçiniz")
giderTuru.place(x=317, y=258, width=240, height=32)

# birinci çizgi
canvas.create_rectangle(
    -1,
    218,
    625,
    219,
    fill="#000000",
    outline="")

# yan çizgi
canvas.create_rectangle(
    624,
    -10,
    625,
    620,
    fill="#000000",
    outline="")

# ikinci çizgi
canvas.create_rectangle(
    -1.0,
    421.0,
    625.0005493164062,
    422.0,
    fill="#000000",
    outline="")
ekleButton_image = PhotoImage(
    file=relative_to_assets("ekle.png")
)
gelirEklebutton = Button(
    bg="#FFFFFF",
    highlightthickness=0,
    image=ekleButton_image,
    command=gelir_ekle,
    relief="flat"
)
gelirEklebutton.place(
    x=33.0,
    y=154.0,
    width=128.0,
    height=40.0
)

giderEklebutton = Button(
    highlightthickness=0,
    bg="#FFFFFF",
    command=gider_ekle,
    image=ekleButton_image,
    relief="flat"
)
giderEklebutton.place(
    x=33.0,
    y=356.0,
    width=128.0,
    height=40.0
)
hesaplaButton_image = PhotoImage(
    file=relative_to_assets("hesapla.png")
)
hesaplaButton = Button(
    highlightthickness=0,
    command=hesapla,
    image=hesaplaButton_image,
    relief="flat"
)
hesaplaButton.place(
    x=32.0,
    y=452.0,
    width=141.0,
    height=40.0
)
excelButton_image = PhotoImage(
    file=relative_to_assets("excl.png")
)
excelButton = Button(
    highlightthickness=0,
    command=excelKaydet,
    image=excelButton_image,
    relief="flat"
)
excelButton.place(
    x=32.0,
    y=533.0,
    width=141.0,
    height=40.0
)
cikisButton_image = PhotoImage(
    file=relative_to_assets("cikis.png")
)
cikisButton = Button(
    highlightthickness=0,
    command=cikis,
    image=cikisButton_image,
    relief="flat"
)
cikisButton.place(
    x=540.0,
    y=520.0,
    width=70.0,
    height=70.0
)
getirButton_image = PhotoImage(
    file=relative_to_assets("gelirGrafik.png")
)
getirButton = Button(
    highlightthickness=0,
    image=getirButton_image,
    command=gelirGrafik,
    relief="flat"
)
getirButton.place(
    x=655.0,
    y=30.0,
    width=125.0,
    height=50.0
)

getir1Button_image = PhotoImage(
    file=relative_to_assets("giderGrafik.png")
)
getir1Button = Button(
    highlightthickness=0,
    image=getir1Button_image,
    command=giderGrafik,
    relief="flat"
)
getir1Button.place(
    x=870.0,
    y=30.0,
    width=125.0,
    height=50.0
)
getir2Button_image = PhotoImage(
    file=relative_to_assets("genelGrafik.png")
)
getir2Button = Button(
    highlightthickness=0,
    image=getir2Button_image,
    command=genelGrafik,
    relief="flat"
)
getir2Button.place(
    x=1070.0,
    y=30.0,
    width=125.0,
    height=50.0
)

tahminButton_image = PhotoImage(
    file=relative_to_assets("veriTahmin.png")
)
tahminButton = Button(
    highlightthickness=0,
    image=tahminButton_image,
    command=tahmin_hesapla,
    relief="flat"
)
tahminButton.place(
    x=655.0,
    y=130.0,
    width=125.0,
    height=50.0
)
aykiriButton_image = PhotoImage(
    file=relative_to_assets("aykiriVeri.png")
)
aykiriButton = Button(
    highlightthickness=0,
    image=aykiriButton_image,
    command=aykiri_deger_analizini_calistir,
    relief="flat"
)
aykiriButton.place(
    x=870.0,
    y=130.0,
    width=125.0,
    height=50.0
)
veriButton_image = PhotoImage(
    file=relative_to_assets("veriGoster.png")
)
veriButton = Button(
    highlightthickness=0,
    image=veriButton_image,
    command=veriGoster,
    relief="flat"
)
veriButton.place(
    x=1070.0,
    y=130.0,
    width=125.0,
    height=50.0
)
window.resizable(False, False)
window.mainloop()
