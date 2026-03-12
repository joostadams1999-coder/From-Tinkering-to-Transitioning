import streamlit as st
import matplotlib.pyplot as plt
import json
import os

# --- 1. CONFIGURATIE EN DATA ---
QUALITEITEN = {
    # Absorptief (Oranje)
    "1.1": {"naam": "Mobiliseren van actoren", "kleur": "orange"},
    "1.2": {"naam": "Integratie van kennis", "kleur": "orange"},
    "1.3": {"naam": "Benadrukken van kleine successen", "kleur": "orange"},
    "1.4": {"naam": "Concretiseren van ambities", "kleur": "orange"},
    "1.5": {"naam": "Framen van innovatie in specifieke context", "kleur": "orange"},
    # Adoptief (Blauw)
    "2.1": {"naam": "Verifiëren waarde in specifieke pilot", "kleur": "cornflowerblue"},
    "2.2": {"naam": "Verifiëren waarde in verschillende contexten", "kleur": "cornflowerblue"},
    "2.3": {"naam": "Testen beheersbaarheid", "kleur": "cornflowerblue"},
    "2.4": {"naam": "Overzicht bewaren", "kleur": "cornflowerblue"},
    "2.5": {"naam": "Momentum creëren in ecosysteem", "kleur": "cornflowerblue"},
    "2.6": {"naam": "Leren van algemene lessen", "kleur": "cornflowerblue"},
    "2.7": {"naam": "Iteratief leren in de innovatie", "kleur": "cornflowerblue"},
    # Adaptief (Geel)
    "3.1": {"naam": "Coördinatie adaptie voor openstaan organisatie", "kleur": "gold"},
    "3.2": {"naam": "Aanpassen routines met kleine stappen", "kleur": "gold"},
    "3.3": {"naam": "Creëer ondersteunend beleid", "kleur": "gold"},
    "3.4": {"naam": "Verzeker gelijk speelveld in markt", "kleur": "gold"},
    "3.5": {"naam": "Vergaar waarde over een langere tijd", "kleur": "gold"}
}

WERKVORM_OPTIES = {
    "Alleen strategisch": 7,
    "Voornamelijk strategisch en lichtelijk tactisch": 6,
    "Lichtelijk strategisch en voornamelijk tactisch": 5,
    "Strategisch/tactisch/operationeel": 4,
    "Voornamelijk tactisch en lichtelijk operationeel": 3,
    "Lichtelijk tactisch en voornamelijk operationeel": 2,
    "Alleen operationeel": 1
}

WERKAANPAK_OPTIES = {
    "Alleen hiërarchisch management": 1,
    "Voornamelijk hiërarchisch management": 2,
    "Lichtelijk hiërarchisch management": 3,
    "Evenveel hiërarchisch als netwerk": 4,
    "Lichtelijk netwerk management": 5,
    "Voornamelijk netwerk management": 6,
    "Alleen netwerk management": 7
}

# --- 2. DATABASE (JSON) SIMULATIE ---
DATA_FILE = "survey_data.json"

def init_data():
    if not os.path.exists(DATA_FILE):
        # 23 fictieve personen voor team INNO-2026
        start_data = [
            {"team": "INNO-2026", "y": 1, "x": 3, "bezit": ["1.1", "2.4", "3.2"], "gemist": ["3.5"], "gezien": ["1.1"]},
            {"team": "INNO-2026", "y": 7, "x": 3, "bezit": ["1.1", "1.4", "3.5"], "gemist": ["2.4", "3.5"], "gezien": ["1.4"]},
            {"team": "INNO-2026", "y": 4, "x": 5, "bezit": ["2.1", "2.4", "3.5"], "gemist": ["3.5"], "gezien": ["1.1"]},
            {"team": "INNO-2026", "y": 6, "x": 2, "bezit": ["1.2", "1.3"], "gemist": ["2.1"], "gezien": ["3.1"]},
            {"team": "INNO-2026", "y": 5, "x": 4, "bezit": ["3.1", "3.3", "1.5"], "gemist": ["2.6"], "gezien": ["2.4"]},
            {"team": "INNO-2026", "y": 2, "x": 6, "bezit": ["2.2", "2.3", "2.7"], "gemist": ["1.1"], "gezien": ["3.5"]},
            {"team": "INNO-2026", "y": 3, "x": 5, "bezit": ["1.4", "2.5", "3.4"], "gemist": ["3.5"], "gezien": ["1.1"]},
            {"team": "INNO-2026", "y": 4, "x": 4, "bezit": ["1.1", "3.2"], "gemist": ["2.4"], "gezien": ["2.1"]},
            {"team": "INNO-2026", "y": 7, "x": 7, "bezit": ["3.5", "1.5"], "gemist": ["1.2"], "gezien": ["1.1"]},
            {"team": "INNO-2026", "y": 1, "x": 1, "bezit": ["2.6"], "gemist": ["3.3"], "gezien": ["2.4"]},
            {"team": "INNO-2026", "y": 5, "x": 3, "bezit": ["1.1", "1.3", "2.1"], "gemist": ["3.5"], "gezien": ["3.2"]},
            {"team": "INNO-2026", "y": 6, "x": 4, "bezit": ["3.1", "3.5"], "gemist": ["2.7"], "gezien": ["1.4"]},
            {"team": "INNO-2026", "y": 4, "x": 6, "bezit": ["2.4", "2.5"], "gemist": ["1.1"], "gezien": ["3.5"]},
            {"team": "INNO-2026", "y": 3, "x": 2, "bezit": ["1.2", "3.4"], "gemist": ["3.5"], "gezien": ["2.4"]},
            {"team": "INNO-2026", "y": 2, "x": 3, "bezit": ["2.1", "2.2"], "gemist": ["1.4"], "gezien": ["1.1"]},
            {"team": "INNO-2026", "y": 5, "x": 5, "bezit": ["1.1", "3.3"], "gemist": ["2.4"], "gezien": ["3.1"]},
            {"team": "INNO-2026", "y": 4, "x": 4, "bezit": ["2.7", "3.5"], "gemist": ["1.5"], "gezien": ["1.1"]},
            {"team": "INNO-2026", "y": 6, "x": 6, "bezit": ["1.4", "2.4"], "gemist": ["3.5"], "gezien": ["2.1"]},
            {"team": "INNO-2026", "y": 7, "x": 2, "bezit": ["3.1", "3.2"], "gemist": ["2.5"], "gezien": ["1.1"]},
            {"team": "INNO-2026", "y": 3, "x": 7, "bezit": ["1.5", "2.6"], "gemist": ["3.5"], "gezien": ["2.4"]},
            {"team": "INNO-2026", "y": 2, "x": 4, "bezit": ["1.1", "2.3"], "gemist": ["3.4"], "gezien": ["1.4"]},
            {"team": "INNO-2026", "y": 4, "x": 5, "bezit": ["3.5", "2.4"], "gemist": ["1.1"], "gezien": ["2.1"]},
            {"team": "INNO-2026", "y": 5, "x": 3, "bezit": ["1.3", "2.1", "3.1"], "gemist": ["3.5"], "gezien": ["1.1"]}
        ]
        with open(DATA_FILE, "w") as f:
            json.dump(start_data, f)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

init_data()

# --- 3. APPLICATIE INTERFACE ---
st.set_page_config(page_title="Innovatie Survey", layout="wide")
st.title("Team Innovatie Kwaliteiten Survey")

# Survey Formulier
with st.form("survey_form"):
    st.subheader("1. Team & Positionering")
    team_code = st.text_input("Vul je Team Toegangscode in (bijv. INNO-2026):").strip().upper()
    
    werkvorm = st.selectbox("Waar plaats jij jezelf qua werkvorm? (Y-as)", list(WERKVORM_OPTIES.keys()))
    werkaanpak = st.selectbox("Waar plaats jij jezelf qua werkaanpak? (X-as)", list(WERKAANPAK_OPTIES.keys()))
    
    st.subheader("2. Jouw Kwaliteiten")
    kwaliteit_labels = [f"{k} - {v['naam']}" for k, v in QUALITEITEN.items()]
    
    bezit_selectie = st.multiselect("Welke kwaliteiten bezit jij?", kwaliteit_labels)
    gemist_selectie = st.multiselect("Welke kwaliteiten mis je in het team/bij jezelf?", kwaliteit_labels)
    gezien_selectie = st.multiselect("Welke kwaliteiten zie je het meest bij collega's?", kwaliteit_labels)
    
    submit = st.form_submit_button("Sla mijn resultaten op")

if submit:
    if not team_code:
        st.error("Vul een team toegangscode in!")
    else:
        bezit_ids = [s.split(" - ")[0] for s in bezit_selectie]
        gemist_ids = [s.split(" - ")[0] for s in gemist_selectie]
        gezien_ids = [s.split(" - ")[0] for s in gezien_selectie]
        
        nieuwe_invoer = {
            "team": team_code,
            "y": WERKVORM_OPTIES[werkvorm],
            "x": WERKAANPAK_OPTIES[werkaanpak],
            "bezit": bezit_ids,
            "gemist": gemist_ids,
            "gezien": gezien_ids
        }
        
        huidige_data = load_data()
        huidige_data.append(nieuwe_invoer)
        save_data(huidige_data)
        
        st.success(f"Resultaten voor team {team_code} opgeslagen! Bekijk hieronder de grafiek.")

# --- 4. DATA VERWERKING EN VISUALISATIE ---
st.divider()
kijk_team = st.text_input("Voer toegangscode in om de teamgrafiek te bekijken:", value="INNO-2026").strip().upper()

if kijk_team:
    alle_data = load_data()
    team_data = [r for r in alle_data if r['team'] == kijk_team]
    
    if len(team_data) == 0:
        st.info("Nog geen data voor dit team.")
    else:
        st.write(f"### Resultaten voor team: {kijk_team} ({len(team_data)} deelnemers)")
        
        plot_data = {}
        teller_gemist = {}
        teller_gezien = {}
        
        for p in team_data:
            for q in p['gemist']: teller_gemist[q] = teller_gemist.get(q, 0) + 1
            for q in p['gezien']: teller_gezien[q] = teller_gezien.get(q, 0) + 1
            
            for q in p['bezit']:
                if q not in plot_data:
                    plot_data[q] = {"x_som": 0, "y_som": 0, "count": 0}
                plot_data[q]["x_som"] += p['x']
                plot_data[q]["y_som"] += p['y']
                plot_data[q]["count"] += 1
        
        max_gemist = max(teller_gemist.values()) if teller_gemist else 0
        meest_gemiste_lijst = [k for k, v in teller_gemist.items() if v == max_gemist and v > 0]
        
        max_gezien = max(teller_gezien.values()) if teller_gezien else 0
        meest_geziene_lijst = [k for k, v in teller_gezien.items() if v == max_gezien and v > 0]

        # Bouw de grafiek
        fig, ax = plt.subplots(figsize=(14, 10)) # Grafiek groter gemaakt voor de tekst
        
        ax.set_xlim(0.5, 7.5)
        ax.set_ylim(0.5, 7.5)
        
        # Sorteer labels zodat 1 tot 7 overeenkomt met de juiste text
        x_labels_gesorteerd = [k for k, v in sorted(WERKAANPAK_OPTIES.items(), key=lambda item: item[1])]
        y_labels_gesorteerd = [k for k, v in sorted(WERKVORM_OPTIES.items(), key=lambda item: item[1])]
        
        ax.set_xticks(range(1, 8))
        ax.set_yticks(range(1, 8))
        
        # Zet de volledige labels op de assen
        ax.set_xticklabels(x_labels_gesorteerd, rotation=45, ha='right', fontsize=9)
        ax.set_yticklabels(y_labels_gesorteerd, fontsize=9)
        
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_title(f"Kwaliteiten Mapping - Team {kijk_team}", fontsize=16, fontweight='bold', pad=20)

        # Teken de cirkels
        for q_id, data in plot_data.items():
            gemiddelde_x = data["x_som"] / data["count"]
            gemiddelde_y = data["y_som"] / data["count"]
            grootte = data["count"] * 500 
            
            kleur = QUALITEITEN[q_id]["kleur"]
            is_meest_gezien = q_id in meest_geziene_lijst
            is_meest_gemist = q_id in meest_gemiste_lijst
            
            edge_color = "black" if is_meest_gezien else "none"
            lijn_dikte = 3 if is_meest_gezien else 0
            tekst_kleur = "white" if is_meest_gemist else "black"
            
            ax.scatter(gemiddelde_x, gemiddelde_y, s=grootte, c=kleur, edgecolors=edge_color, linewidths=lijn_dikte, alpha=0.85, zorder=2)
            ax.annotate(q_id, (gemiddelde_x, gemiddelde_y), color=tekst_kleur, ha='center', va='center', fontweight='bold', zorder=3)

        fig.tight_layout() # Zorgt dat de lange tekst labels niet buiten beeld vallen
        st.pyplot(fig)
        
        st.markdown("""
        **Legenda Grafiek:**
        * **Grootte van de cirkel:** Hoe vaker deze kwaliteit aanwezig is.
        * **Positie (X/Y):** Het gemiddelde profiel van de teamleden die deze kwaliteit bezitten.
        * **Oranje / Blauw / Geel:** Absorptief, Adoptief, Adaptief.
        * **Zwarte dikke rand:** Deze kwaliteit is het *meest gesignaleerd* bij collega's.
        * **Witte tekst:** Deze kwaliteit wordt het *meest gemist* in dit team.
        """)

# --- 5. ADMIN RESET ---
st.divider()
with st.expander("⚙️ Beheer (Alleen voor beheerders)"):
    st.write("Verwijder alle data van een specifiek team.")
    reset_team = st.text_input("Welk team wil je resetten? (bijv. INNO-2026)").strip().upper()
    admin_wachtwoord = st.text_input("Beheerderswachtwoord:", type="password")
    
    if st.button("Reset Team Resultaten"):
        if admin_wachtwoord == "Ingrid_Bolier":
            data = load_data()
            # Filter de data: bewaar alles BEHALVE het team dat gereset moet worden
            nieuwe_data = [row for row in data if row['team'] != reset_team]
            save_data(nieuwe_data)
            st.success(f"✅ Alle opgeslagen resultaten voor team '{reset_team}' zijn succesvol gewist!")
            st.rerun() # Ververs de pagina
        else:
            st.error("❌ Onjuist wachtwoord!")