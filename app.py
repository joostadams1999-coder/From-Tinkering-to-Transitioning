import streamlit as st
import matplotlib.pyplot as plt
import json
import os

# -------------------------
# 0. Language selector
# -------------------------
LANG_CHOICES = ["Nederlands", "English"]
# Sidebar language selector (left-top)
chosen_lang = st.sidebar.selectbox("Survey invoer / Survey input", LANG_CHOICES)

# Simple translation dict
TRANSLATIONS = {
    "Nederlands": {
        "page_title": "Innovatie Survey",
        "title": "Team Innovatie Kwaliteiten Survey",
        "section1": "1. Team & Positionering",
        "team_code_input": "Vul je Team Toegangscode in (bijv. INNO-2026):",
        "werkvorm_input": "Waar plaats jij jezelf qua werkvorm? (Y-as)",
        "werkaanpak_input": "Waar plaats jij jezelf qua werkaanpak? (X-as)",
        "section2": "2. Jouw Kwaliteiten",
        "bezit_input": "Welke kwaliteiten bezit jij?",
        "gemist_input": "Welke kwaliteiten mis je in het team/bij jezelf?",
        "gezien_input": "Welke kwaliteiten zie je het meest bij collega's?",
        "submit": "Sla mijn resultaten op",
        "require_team_error": "Vul een team toegangscode in!",
        "success_saved": "Resultaten voor team {team} opgeslagen! Bekijk hieronder de grafiek.",
        "view_label": "Voer toegangscode in om de teamgrafiek te bekijken:",
        "select_existing_team": "— Kies bestaand team —",
        "or_type_team": "OF typ hier een teamcode (overschrijft selectie):",
        "no_data": "Nog geen data voor dit team.",
        "results_for": "Resultaten voor team: {team} ({count} deelnemers)",
        "legend_md": """
**Legenda Grafiek:**
* **Grootte van de cirkel:** Hoe vaker deze kwaliteit aanwezig is.
* **Positie (X/Y):** Het gemiddelde profiel van de teamleden die deze kwaliteit bezitten.
* **Oranje / Blauw / Geel:** Absorptief, Adoptief, Adaptief.
* **Zwarte dikke rand:** Deze kwaliteit is het _meest gesignaleerd_ bij collega's.
* **Witte tekst:** Deze kwaliteit wordt het _meest gemist_ in dit team.
""",
        "admin_expander": "⚙️ Beheer (Alleen voor beheerders)",
        "admin_text": "Verwijder alle data van een specifiek team.",
        "reset_team_label": "Welk team wil je resetten?",
        "admin_password": "Beheerderswachtwoord:",
        "reset_button": "Reset Team Resultaten",
        "reset_success": "✅ Alle opgeslagen resultaten voor team '{team}' zijn succesvol gewist!",
        "wrong_password": "❌ Onjuist wachtwoord!",
        "no_teams_admin": "Er zijn momenteel geen teams om te resetten."
    },
    "English": {
        "page_title": "Innovation Survey",
        "title": "Team Innovation Qualities Survey",
        "section1": "1. Team & Positioning",
        "team_code_input": "Enter your Team Access Code (e.g. INNO-2026):",
        "werkvorm_input": "Where do you place yourself regarding work form? (Y-axis)",
        "werkaanpak_input": "Where do you place yourself regarding approach? (X-axis)",
        "section2": "2. Your Qualities",
        "bezit_input": "Which qualities do you possess?",
        "gemist_input": "Which qualities do you miss in the team/yourself?",
        "gezien_input": "Which qualities do you most see in colleagues?",
        "submit": "Save my results",
        "require_team_error": "Please enter a team access code!",
        "success_saved": "Results for team {team} saved! See the chart below.",
        "view_label": "Enter access code to view the team chart:",
        "select_existing_team": "— Select existing team —",
        "or_type_team": "OR type a team code here (overrides selection):",
        "no_data": "No data for this team yet.",
        "results_for": "Results for team: {team} ({count} participants)",
        "legend_md": """
**Chart Legend:**
* **Circle size:** How often this quality is present.
* **Position (X/Y):** The average profile of team members who have this quality.
* **Orange / Blue / Yellow:** Absorptive, Adoptive, Adaptive.
* **Black thick border:** This quality is the _most observed_ in colleagues.
* **White text:** This quality is the _most missed_ in this team.
""",
        "admin_expander": "⚙️ Admin (Administrators only)",
        "admin_text": "Delete all data for a specific team.",
        "reset_team_label": "Which team do you want to reset?",
        "admin_password": "Admin password:",
        "reset_button": "Reset Team Results",
        "reset_success": "✅ All stored results for team '{team}' have been deleted!",
        "wrong_password": "❌ Incorrect password!",
        "no_teams_admin": "There are currently no teams to reset."
    }
}

def tr(key):
    return TRANSLATIONS[chosen_lang][key]

# -------------------------
# 1. QUALITIES + Options (with translations)
# -------------------------
QUALITEITEN = {
    "1.1": {"naam": {"nl": "Mobiliseren van actoren", "en": "Mobilising actors"}, "kleur": "orange"},
    "1.2": {"naam": {"nl": "Integratie van kennis", "en": "Integration of knowledge"}, "kleur": "orange"},
    "1.3": {"naam": {"nl": "Benadrukken van kleine successen", "en": "Highlighting small wins"}, "kleur": "orange"},
    "1.4": {"naam": {"nl": "Concretiseren van ambities", "en": "Concretising ambitions"}, "kleur": "orange"},
    "1.5": {"naam": {"nl": "Framen van innovatie in specifieke context", "en": "Framing innovation in context"}, "kleur": "orange"},
    "2.1": {"naam": {"nl": "Verifiëren waarde in specifieke pilot", "en": "Verify value in specific pilot"}, "kleur": "cornflowerblue"},
    "2.2": {"naam": {"nl": "Verifiëren waarde in verschillende contexten", "en": "Verify value in various contexts"}, "kleur": "cornflowerblue"},
    "2.3": {"naam": {"nl": "Testen beheersbaarheid", "en": "Test controllability"}, "kleur": "cornflowerblue"},
    "2.4": {"naam": {"nl": "Overzicht bewaren", "en": "Keeping an overview"}, "kleur": "cornflowerblue"},
    "2.5": {"naam": {"nl": "Momentum creëren in ecosysteem", "en": "Create momentum in ecosystem"}, "kleur": "cornflowerblue"},
    "2.6": {"naam": {"nl": "Leren van algemene lessen", "en": "Learning general lessons"}, "kleur": "cornflowerblue"},
    "2.7": {"naam": {"nl": "Iteratief leren in de innovatie", "en": "Iterative learning in innovation"}, "kleur": "cornflowerblue"},
    "3.1": {"naam": {"nl": "Coördinatie adaptie voor openstaan organisatie", "en": "Coordinate adaptation for organization openness"}, "kleur": "gold"},
    "3.2": {"naam": {"nl": "Aanpassen routines met kleine stappen", "en": "Adjust routines with small steps"}, "kleur": "gold"},
    "3.3": {"naam": {"nl": "Creëer ondersteunend beleid", "en": "Create supportive policy"}, "kleur": "gold"},
    "3.4": {"naam": {"nl": "Verzeker gelijk speelveld in markt", "en": "Ensure a level playing field in market"}, "kleur": "gold"},
    "3.5": {"naam": {"nl": "Vergaar waarde over een langere tijd", "en": "Accumulate value over longer term"}, "kleur": "gold"}
}

# Workform / approach labels per language mapped to numeric scale
WERKVORM_OPTIES = {
    "nl": {
        "Alleen strategisch": 7,
        "Voornamelijk strategisch en lichtelijk tactisch": 6,
        "Lichtelijk strategisch en voornamelijk tactisch": 5,
        "Strategisch/tactisch/operationeel": 4,
        "Voornamelijk tactisch en lichtelijk operationeel": 3,
        "Lichtelijk tactisch en voornamelijk operationeel": 2,
        "Alleen operationeel": 1
    },
    "en": {
        "Only strategic": 7,
        "Primarily strategic and slightly tactical": 6,
        "Slightly strategic and mainly tactical": 5,
        "Strategic/tactical/operational": 4,
        "Primarily tactical and slightly operational": 3,
        "Slightly tactical and mainly operational": 2,
        "Only operational": 1
    }
}

WERKAANPAK_OPTIES = {
    "nl": {
        "Alleen hiërarchisch management": 1,
        "Voornamelijk hiërarchisch management": 2,
        "Lichtelijk hiërarchisch management": 3,
        "Evenveel hiërarchisch als netwerk": 4,
        "Lichtelijk netwerk management": 5,
        "Voornamelijk netwerk management": 6,
        "Alleen netwerk management": 7
    },
    "en": {
        "Only hierarchical management": 1,
        "Primarily hierarchical management": 2,
        "Slightly hierarchical management": 3,
        "Equal hierarchical and network": 4,
        "Slightly network management": 5,
        "Primarily network management": 6,
        "Only network management": 7
    }
}

# -------------------------
# 2. Data file helpers
# -------------------------
DATA_FILE = "survey_data.json"

def init_data():
    if not os.path.exists(DATA_FILE):
        # sample start data (same as before) for INNO-2026
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

# -------------------------
# 3. App UI
# -------------------------
st.set_page_config(page_title=tr("page_title"), layout="wide")
st.title(tr("title"))

# Initialize session_state keys for kijk_team selection if not present
if 'kijk_team_select' not in st.session_state:
    st.session_state['kijk_team_select'] = None
if 'kijk_team_input' not in st.session_state:
    st.session_state['kijk_team_input'] = "INNO-2026"

# Survey Form
with st.form("survey_form"):
    st.subheader(tr("section1"))
    # Team input for entering new team during submission (not the same as view-select)
    team_code_input = st.text_input(tr("team_code_input"), value="").strip().upper()
    # Choose the appropriate option dictionaries for the chosen language
    werkvorm_keuzes = WERKVORM_OPTIES['nl'] if chosen_lang == "Nederlands" else WERKVORM_OPTIES['en']
    werkaanpak_keuzes = WERKAANPAK_OPTIES['nl'] if chosen_lang == "Nederlands" else WERKAANPAK_OPTIES['en']
    werkvorm = st.selectbox(tr("werkvorm_input"), list(werkvorm_keuzes.keys()))
    werkaanpak = st.selectbox(tr("werkaanpak_input"), list(werkaanpak_keuzes.keys()))

    st.subheader(tr("section2"))
    # Build quality labels according to language
    kwaliteit_labels = [f"{k} - {v['naam']['nl'] if chosen_lang=='Nederlands' else v['naam']['en']}" for k, v in QUALITEITEN.items()]
    bezit_selectie = st.multiselect(tr("bezit_input"), kwaliteit_labels)
    gemist_selectie = st.multiselect(tr("gemist_input"), kwaliteit_labels)
    gezien_selectie = st.multiselect(tr("gezien_input"), kwaliteit_labels)
    submit = st.form_submit_button(tr("submit"))

if submit:
    team_code = team_code_input
    if not team_code:
        st.error(tr("require_team_error"))
    else:
        bezit_ids = [s.split(" - ")[0] for s in bezit_selectie]
        gemist_ids = [s.split(" - ")[0] for s in gemist_selectie]
        gezien_ids = [s.split(" - ")[0] for s in gezien_selectie]
        nieuwe_invoer = {
            "team": team_code,
            "y": werkvorm_keuzes[werkvorm],
            "x": werkaanpak_keuzes[werkaanpak],
            "bezit": bezit_ids,
            "gemist": gemist_ids,
            "gezien": gezien_ids
        }
        huidige_data = load_data()
        huidige_data.append(nieuwe_invoer)
        save_data(huidige_data)

        # Update view selectors in session_state so the new team is immediately shown
        st.session_state['kijk_team_input'] = team_code
        st.session_state['kijk_team_select'] = team_code

        st.success(tr("success_saved").format(team=team_code))

st.divider()

# --- VIEW SECTION ---
# Build list of available teams from data
alle_data = load_data()
teams_beschikbaar = sorted(list({r['team'] for r in alle_data}))
placeholder = tr("select_existing_team")
select_options = [placeholder] + teams_beschikbaar if teams_beschikbaar else [placeholder]

# Select existing team (dropdown) - key tied to session_state
kies_team = st.selectbox(tr("view_label"), options=select_options, key="kijk_team_select")

# Manual text input that overrides the dropdown if filled
st.write(tr("or_type_team"))
txt_team = st.text_input("", value=st.session_state.get('kijk_team_input', ''), key="kijk_team_input")

# Determine final team to view: manual input takes precedence if non-empty
if txt_team and txt_team.strip():
    kijk_team = txt_team.strip().upper()
else:
    if kies_team == placeholder:
        # If nothing chosen and nothing typed, default to session or empty
        kijk_team = st.session_state.get('kijk_team_input', '').strip().upper()
        if not kijk_team:
            kijk_team = ""
    else:
        kijk_team = kies_team.strip().upper()

if kijk_team:
    team_data = [r for r in alle_data if r['team'] == kijk_team]
    if len(team_data) == 0:
        st.info(tr("no_data"))
    else:
        st.write(tr("results_for").format(team=kijk_team, count=len(team_data)))
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

        # Plot
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(0.5, 7.5)
        ax.set_ylim(0.5, 7.5)

        x_options_sorted = [k for k, v in sorted(werkaanpak_keuzes.items(), key=lambda item: item[1])]
        y_options_sorted = [k for k, v in sorted(werkvorm_keuzes.items(), key=lambda item: item[1])]

        ax.set_xticks(range(1, 8))
        ax.set_yticks(range(1, 8))
        ax.set_xticklabels(x_options_sorted, rotation=45, ha='right', fontsize=9)
        ax.set_yticklabels(y_options_sorted, fontsize=9)
        ax.grid(True, linestyle='--', alpha=0.5)

        # Title translated: keep team id in title
        title_text = f"{'Kwaliteiten Mapping' if chosen_lang=='Nederlands' else 'Qualities Mapping'} - Team {kijk_team}"
        ax.set_title(title_text, fontsize=16, fontweight='bold', pad=20)

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
            # Annotate with quality id (could also add name on hover if interactive)
            ax.annotate(q_id, (gemiddelde_x, gemiddelde_y), color=tekst_kleur, ha='center', va='center', fontweight='bold', zorder=3)

        fig.tight_layout()
        st.pyplot(fig)
        st.markdown(tr("legend_md"))

st.divider()

# -------------------------
# Admin reset with dropdown of existing teams
# -------------------------
with st.expander(tr("admin_expander")):
    st.write(tr("admin_text"))
    alle_data = load_data()
    teams_beschikbaar = sorted(list({r['team'] for r in alle_data}))
    if not teams_beschikbaar:
        st.info(tr("no_teams_admin"))
    else:
        # Dropdown for admin to select a team to reset
        reset_team = st.selectbox(tr("reset_team_label"), options=teams_beschikbaar)
        admin_wachtwoord = st.text_input(tr("admin_password"), type="password")
        if st.button(tr("reset_button")):
            if admin_wachtwoord == "Ingrid_Bolier":
                data = load_data()
                nieuwe_data = [row for row in data if row['team'] != reset_team]
                save_data(nieuwe_data)
                st.success(tr("reset_success").format(team=reset_team))
                # Reset view session keys if the deleted team was selected
                if st.session_state.get('kijk_team_input', '').upper() == reset_team.upper():
                    st.session_state['kijk_team_input'] = ""
                    st.session_state['kijk_team_select'] = None
                # Rerun app to refresh UI and available teams
                st.experimental_rerun()
            else:
                st.error(tr("wrong_password"))
