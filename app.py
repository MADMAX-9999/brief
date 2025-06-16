import streamlit as st
from fpdf import FPDF
import pandas as pd
import datetime

def generate_pdf(data, timestamp):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)

    pdf.cell(200, 10, txt="Brief Strategii Budowania Majątku", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Data: {datetime.date.today()}", ln=True)
    pdf.ln(10)

    for k, v in data.items():
        pdf.multi_cell(0, 10, f"{k}: {v if v else '—'}")

    filename = f"brief_{timestamp}.pdf"
    pdf.output(filename)
    return filename

def generate_csv(data, timestamp):
    df = pd.DataFrame(data.items(), columns=["Pytanie", "Odpowiedź"])
    filename = f"brief_{timestamp}.csv"
    df.to_csv(filename, index=False)
    return filename

def main():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    st.set_page_config(page_title="Brief Strategii Majątku", layout="centered")
    st.title("📘 Kompleksowy Brief Strategii Budowania Majątku")

    st.markdown("""
    Celem tego briefu jest kompleksowa diagnoza Państwa możliwości, preferencji i celów związanych z budową majątku,
    aby stworzyć spersonalizowaną i efektywną strategię inwestycyjną.
    """)

    imie = st.text_input("Imię:")
    email = st.text_input("Email:")
    st.header("ETAP 1/7 – Edukacja i wsparcie (opcjonalny)")
    wiedza = st.radio("1. Jak ocenia Pan/Pani swoją wiedzę na temat inwestycji?", ["Początkujący", "Średniozaawansowany", "Zaawansowany"])
    edukacja = st.radio("2. Czy jest Pan/Pani zainteresowany/a wsparciem edukacyjnym?", ["Tak", "Nie"])
    doswiadczenie = st.text_area("3. Jakie są dotychczasowe doświadczenia inwestycyjne?")

    st.header("ETAP 2/7 – Preferencje i wartości inwestycyjne")
    priorytety = st.multiselect("4. Co jest dla Państwa najważniejsze?", [
        "Trwałość wartości i ochrona siły nabywczej",
        "Wzrost wartości i potencjał zysku",
        "Płynność i dostępność środków",
        "Pełna niezależność systemowa i poufność"
    ])
    wlasnosc = st.radio("5. Czy zależy Państwu na pełnej własności fizycznego metalu?", ["Tak", "Nie"])
    sprzedaz = st.radio("6. Czy ważna jest możliwość częściowej sprzedaży?", ["Tak", "Nie"])
    sukcesja = st.radio("7. Czy interesują Państwa rozwiązania sukcesyjne?", ["Tak", "Nie"])
    forma_sukcesji = "—"
    if sukcesja == "Tak":
        forma_sukcesji = st.text_input("  a) Preferowana forma sukcesji:")

    st.header("ETAP 3/7 – Rezerwy i inne aktywa")
    aktywa = st.radio("8. Czy posiadają Państwo inne aktywa możliwe do konwersji w metale?", ["Tak", "Nie"])
    dodatkowa_alokacja = st.radio("9. Czy rozważają Państwo dodatkową alokację kapitału?", ["Tak", "Nie"])

    st.header("ETAP 4/7 – Podejście i świadomość")
    niezaleznosc = st.radio("10. Czy cenią Państwo niezależność i poufność?", ["Tak", "Nie"])
    poza_systemem = st.radio("11. Gotowość do działania poza systemem bankowym?", ["Tak", "Nie"])
    swiadomosc = st.radio("12. Czy są Państwo świadomi kwestii podatkowych?", ["Tak", "Nie"])
    wsparcie_podatki = "—"
    if swiadomosc == "Tak":
        wsparcie_podatki = st.radio("  Czy potrzebują Państwo wsparcia w tym zakresie?", ["Tak", "Nie"])

    st.header("ETAP 5/7 – Cele i horyzont czasowy")
    cel = st.text_input("13. Główny cel budowy majątku:")
    horyzont_budowy = st.text_input("14. Horyzont budowy majątku (np. 15 lat):")
    horyzont_korzystania = st.text_input("15. Horyzont korzystania z majątku:")
    pokolenia = st.radio("16. Czy budują Państwo majątek z myślą o kolejnych pokoleniach?", ["Tak", "Nie"])

    st.header("ETAP 6/7 – Styl i dynamika (DBM)")
    dynamika = st.slider("17. Styl budowania majątku (DBM):", 1, 5, 3)
    otwartosc = st.radio("18. Otwartość na zwiększenie zakupów w przyszłości?", ["Tak", "Nie"])
    ryzyko = st.radio("19. Akceptowalny poziom ryzyka?", ["Niski", "Umiarkowany", "Wysoki"])

    st.header("ETAP 7/7 – Diagnoza możliwości i zaangażowania")
    kapital = st.number_input("20. Kwota początkowa (EUR):", min_value=0.0, step=1000.0)
    miesiecznie = st.number_input("21. Kwota miesięczna na zakupy (EUR):", min_value=0.0, step=100.0)
    zwiekszanie_kwot = st.radio("22. Czy planują Państwo zwiększyć kwoty w przyszłości?", ["Tak", "Nie"])
    zrodlo = st.text_input("23. Źródło środków na start:")
    plan = st.radio("24. Czy to jednorazowa kwota, czy część większego planu?", ["Jednorazowa", "Plan alokacji"])

    firma = st.radio("25. Czy prowadzą Państwo działalność gospodarczą?", ["Tak", "Nie"])
    obroty = 0
    udzial = 0
    zysk_prywatny = "—"
    if firma == "Tak":
        obroty = st.number_input("  a) Roczne obroty firmy (EUR):", min_value=0.0, step=10000.0)
        udzial = st.slider("  b) Procentowy udział w firmie:", 1, 100, 50)
        zysk_prywatny = st.radio("  c) Czy chcą Państwo budować majątek z zysków firmy?", ["Tak", "Nie"])
        decyzyjnosc = st.radio("  d) Czy samodzielnie decydują Państwo o swoich pieniądzach?", ["Tak", "Nie"])


    if st.button("🔍 Przejdź do analizy odpowiedzi"):
        responses = {
            "Imię": imie,
            "Email": email,
            "Poziom wiedzy": wiedza,
            "Wsparcie edukacyjne": edukacja,
            "Doświadczenia inwestycyjne": doswiadczenie,
            "Priorytety": ', '.join(priorytety),
            "Własność metali": wlasnosc,
            "Możliwość sprzedaży": sprzedaz,
            "Sukcesja": sukcesja,
            "Forma sukcesji": forma_sukcesji,
            "Inne aktywa": aktywa,
            "Dodatkowa alokacja": dodatkowa_alokacja,
            "Niezależność i poufność": niezaleznosc,
            "Poza systemem bankowym": poza_systemem,
            "Świadomość podatkowa": swiadomosc,
            "Wsparcie podatkowe": wsparcie_podatki,
            "Cel budowy majątku": cel,
            "Horyzont budowy": horyzont_budowy,
            "Horyzont korzystania": horyzont_korzystania,
            "Strategia sukcesyjna": pokolenia,
            "DBM": dynamika,
            "Otwartość na zwiększanie": otwartosc,
            "Ryzyko": ryzyko,
            "Kapitał początkowy": f"{kapital:.2f} EUR",
            "Zakupy miesięczne": f"{miesiecznie:.2f} EUR",
            "Zwiększanie zakupów": zwiekszanie_kwot,
            "Źródło środków": zrodlo,
            "Charakter środków": plan,
            "Prowadzenie firmy": firma,
        }
        if firma == "Tak":
            responses["Obroty firmy"] = f"{obroty:.2f} EUR"
            responses["Udział w firmie"] = f"{udzial}%"
            responses["Zyski do majątku"] = zysk_prywatny
            responses["Decyzyjność"] = decyzyjnosc

        st.success("Dziękujemy! Formularz został wypełniony.")
        pdf_file = generate_pdf(responses, timestamp)
        csv_file = generate_csv(responses, timestamp)

        with open(pdf_file, "rb") as f:
            st.download_button("📄 Pobierz PDF", f, file_name=pdf_file, mime="application/pdf")

        with open(csv_file, "rb") as f:
            st.download_button("📊 Pobierz CSV", f, file_name=csv_file, mime="text/csv")

if __name__ == "__main__":
    main()
