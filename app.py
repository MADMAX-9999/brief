import streamlit as st
from fpdf import FPDF
import pandas as pd
import datetime

def score_horyzont(horyzont):
    try:
        h = int(horyzont)
        if h <= 7:
            return 1
        elif h <= 15:
            return 2
        elif h <= 25:
            return 3
        else:
            return 4
    except:
        return 0

def calculate_ri(data):
    score = 0
    score += {"Początkujący": 3, "Średniozaawansowany": 2, "Zaawansowany": 1}.get(data["wiedza"], 0)
    score += {"Tak": 2, "Nie": 1}.get(data["edukacja"], 0)
    priorytety_scores = {
        "Trwałość wartości i ochrona siły nabywczej": 4,
        "Wzrost wartości i potencjał zysku": 1,
        "Płynność i dostępność środków": 2,
        "Pełna niezależność systemowa i poufność": 3
    }
    score += sum([priorytety_scores.get(p, 0) for p in data["priorytety"]])
    score += {"Tak": 2, "Nie": 1}.get(data["wlasnosc"], 0)
    score += {"Tak": 2, "Nie": 1}.get(data["sprzedaz"], 0)
    score += {"Tak": 2, "Nie": 1}.get(data["sukcesja"], 0)
    score += {"Tak": 2, "Nie": 1}.get(data["aktywa"], 0)
    score += {"Tak": 2, "Nie": 1}.get(data["dodatkowa_alokacja"], 0)
    score += {"Tak": 2, "Nie": 1}.get(data["niezaleznosc"], 0)
    score += {"Tak": 2, "Nie": 1}.get(data["poza_systemem"], 0)
    score += {"Tak": 2, "Nie": 1}.get(data["swiadomosc"], 0)
    score += {"Tak": 2, "Nie": 1}.get(data["wsparcie_podatki"], 0)
    score += score_horyzont(data["horyzont_budowy"])
    score += {"Tak": 2, "Nie": 1}.get(data["pokolenia"], 0)
    score += int(data["dynamika"])
    score += {"Tak": 2, "Nie": 1}.get(data["otwartosc"], 0)
    score += {"Niski": 3, "Umiarkowany": 2, "Wysoki": 1}.get(data["ryzyko"], 0)
    score += {"Tak": 2, "Nie": 1}.get(data["zwiększanie_kwot"], 0)
    score += {"Jednorazowa": 1, "Plan alokacji": 2}.get(data["plan"], 0)
    score += {"Tak": 2, "Nie": 1}.get(data["firma"], 0)
    score += {"Tak": 2, "Nie": 1}.get(data["zysk_prywatny"], 0)
    score += {"Tak": 2, "Nie": 1}.get(data["decyzyjnosc"], 0)
    return score

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)
    pdf.cell(200, 10, txt="Brief Strategii Budowania Majątku", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Data: {datetime.date.today()}", ln=True)
    pdf.ln(10)
    for k, v in data.items():
        pdf.multi_cell(0, 10, f"{k}: {v if v else '—'}")
    filename = f"brief_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(filename)
    return filename

def generate_csv(data):
    df = pd.DataFrame(data.items(), columns=["Pytanie", "Odpowiedź"])
    filename = f"brief_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    df.to_csv(filename, index=False)
    return filename

def main():
    st.set_page_config(page_title="Brief Strategii Majątku")
    st.title("📘 Brief Strategii Budowania Majątku z Rating Index")

    wiedza = st.radio("Jak ocenia Pan/Pani swoją wiedzę na temat inwestycji?", ["Początkujący", "Średniozaawansowany", "Zaawansowany"])
    edukacja = st.radio("Czy jest Pan/Pani zainteresowany/a wsparciem edukacyjnym?", ["Tak", "Nie"])
    priorytety = st.multiselect("Co jest dla Państwa najważniejsze?", [
        "Trwałość wartości i ochrona siły nabywczej",
        "Wzrost wartości i potencjał zysku",
        "Płynność i dostępność środków",
        "Pełna niezależność systemowa i poufność"])
    wlasnosc = st.radio("Czy zależy Państwu na pełnej własności fizycznego metalu?", ["Tak", "Nie"])
    sprzedaz = st.radio("Czy ważna jest możliwość częściowej sprzedaży?", ["Tak", "Nie"])
    sukcesja = st.radio("Czy interesują Państwa rozwiązania sukcesyjne?", ["Tak", "Nie"])
    aktywa = st.radio("Czy posiadają Państwo inne aktywa możliwe do konwersji w metale?", ["Tak", "Nie"])
    dodatkowa_alokacja = st.radio("Czy rozważają Państwo dodatkową alokację kapitału?", ["Tak", "Nie"])
    niezaleznosc = st.radio("Czy cenią Państwo niezależność i poufność?", ["Tak", "Nie"])
    poza_systemem = st.radio("Gotowość do działania poza systemem bankowym?", ["Tak", "Nie"])
    swiadomosc = st.radio("Czy są Państwo świadomi kwestii podatkowych?", ["Tak", "Nie"])
    wsparcie_podatki = st.radio("Czy potrzebują Państwo wsparcia podatkowego?", ["Tak", "Nie"])
    horyzont_budowy = st.text_input("Horyzont budowy majątku (np. 15 lat):")
    pokolenia = st.radio("Czy budują Państwo majątek z myślą o kolejnych pokoleniach?", ["Tak", "Nie"])
    dynamika = st.slider("Styl budowania majątku (DBM)", 1, 5, 3)
    otwartosc = st.radio("Otwartość na zwiększenie zakupów w przyszłości?", ["Tak", "Nie"])
    ryzyko = st.radio("Akceptowalny poziom ryzyka?", ["Niski", "Umiarkowany", "Wysoki"])
    zwiększanie_kwot = st.radio("Czy planują Państwo zwiększyć kwoty w przyszłości?", ["Tak", "Nie"])
    plan = st.radio("Czy to jednorazowa kwota, czy część większego planu?", ["Jednorazowa", "Plan alokacji"])
    firma = st.radio("Czy prowadzą Państwo działalność gospodarczą?", ["Tak", "Nie"])
    zysk_prywatny = st.radio("Czy chcą Państwo budować majątek z zysków firmy?", ["Tak", "Nie"])
    decyzyjnosc = st.radio("Czy samodzielnie decydują Państwo o swoich pieniądzach?", ["Tak", "Nie"])

    data = locals()
    data_dict = {k: v for k, v in data.items() if k not in ["st", "pd", "datetime", "FPDF", "generate_pdf", "generate_csv", "main", "score_horyzont", "calculate_ri"]}
    ri_score = calculate_ri(data_dict)
    data_dict["Rating Index"] = ri_score

    st.markdown(f"## 📊 Rating Index (RI): **{ri_score}**")

    if st.button("📄 Generuj PDF i CSV"):
        pdf_file = generate_pdf(data_dict)
        csv_file = generate_csv(data_dict)

        with open(pdf_file, "rb") as f:
            st.download_button("📥 Pobierz PDF", f, file_name=pdf_file, mime="application/pdf")

        with open(csv_file, "rb") as f:
            st.download_button("📥 Pobierz CSV", f, file_name=csv_file, mime="text/csv")

if __name__ == "__main__":
    main()
