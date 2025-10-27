import streamlit as st
import random

st.title("🧭 Decision Helper")

# --- INITIAL SETUP ---
if "page" not in st.session_state:
    st.session_state.page = 1

# Datenstruktur vorbereiten
if "scores" not in st.session_state:
    st.session_state.scores = {}

# --- STEP 1: Welcome ---
if st.session_state.page == 1:
    st.write("Willkommen beim Decision Helper!")
    if st.button("Start Decision"):
        st.session_state.page = 2
        st.rerun()

# --- STEP 2: Describe Decision ---
elif st.session_state.page == 2:
    decision = st.text_input("Welche Entscheidung willst du treffen?")
    if st.button("Weiter"):
        if not decision.strip():
            st.warning("Bitte gib eine Entscheidung ein.")
        else:
            st.session_state.decision = decision
            st.session_state.page = 3
            st.rerun()

# --- STEP 3: Number of Options ---
elif st.session_state.page == 3:
    num = st.number_input("Wie viele Optionen hast du?", min_value=1, max_value=10, step=1)
    if st.button("Weiter"):
        st.session_state.num_options = int(num)
        st.session_state.page = 4
        st.rerun()

# --- STEP 4: Option Names ---
elif st.session_state.page == 4:
    st.write("Gib den Namen jeder Option ein:")
    option_names = []
    for i in range(st.session_state.num_options):
        name = st.text_input(f"Option {i+1}", key=f"opt{i}")
        option_names.append(name)

    if st.button("Weiter"):
        if all(name.strip() for name in option_names):
            st.session_state.option_names = option_names
            st.session_state.page = 5
            st.rerun()
        else:
            st.warning("Bitte fülle alle Optionen aus.")

# --- STEP 5: Vergleichbarkeit & Konsequenz ---
elif st.session_state.page == 5:
    st.subheader("Beurteile die Situation:")

    vergleichbarkeit = st.selectbox(
        "Wie gut lassen sich die Optionen vergleichen?",
        ["gut", "schlecht"],
        key="vergleichbarkeit"
    )

    konsequenz = st.selectbox(
        "Wie gross sind die Konsequenzen deiner Entscheidung?",
        ["gross", "klein"],
        key="konsequenz"
    )

    if st.button("Weiter"):

        # Entscheidungstyp bestimmen
        if vergleichbarkeit == "schlecht" and konsequenz == "klein":
            st.session_state.page = "6_1"
        elif vergleichbarkeit == "gut" and konsequenz == "klein":
            st.session_state.page = "6_2"
        elif vergleichbarkeit == "schlecht" and konsequenz == "gross":
            st.session_state.page = "6_3"
        elif vergleichbarkeit == "gut" and konsequenz == "gross":
            st.session_state.page = "6_4"
        st.rerun()

# --- STEP 6.1: Apfel-Birne ---
elif st.session_state.page == "6_1":
    st.subheader("🍏 Apfel-Birne Entscheidung")
    st.write("Deine Entscheidung ist **nicht gut vergleichbar** und hat **kleine Konsequenzen**.")
    st.info("Es ist egal, wie du dich entscheidest – lass den Zufall entscheiden!")

    if st.button("Zufallsentscheidung treffen 🎲"):
        choice = random.choice(st.session_state.option_names)
        st.success(f"🎉 Der Zufall hat entschieden: **{choice}**")

    if st.button("Neue Entscheidung treffen 🔄"):
        st.session_state.clear()
        st.rerun()

# --- STEP 6.2: No-Brainer ---
elif st.session_state.page == "6_2":
    st.subheader("🧠 No-Brainer Entscheidung")
    st.write("Deine Optionen sind **gut vergleichbar** und die Konsequenzen sind **klein**.")
    st.info("Diese Entscheidung ist einfach: Nimm die Option, die dir spontan besser erscheint!")
    choice = st.radio("Optionen", st.session_state.option_names)
    if st.button("Fertig"):
        st.success(f"🎉 Du hast dich entschieden für: **{choice}**")
        st.session_state.clear()

    if st.button("Neue Entscheidung treffen 🔄"):
        st.session_state.clear()
        st.rerun()

# --- STEP 6.3 & 6.4: Hard Choice / Big Choice ---
elif st.session_state.page in ["6_3", "6_4"]:
    typ = "Hard Choice" if st.session_state.page == "6_3" else "Big Choice"
    st.subheader(f"💭 {typ} Entscheidung")

    if st.session_state.page == "6_3":
        st.write("Vergleiche sind schwierig und Konsequenzen gross: Hier gibt es keine Entscheidung, die eindeutig richtig ist. – "
                 "nimm dir Zeit und bewerte **subjektiv**.")
    else:
        st.write("Vergleiche sind möglich und Konsequenzen gross: Mit rationalem abwägen sollte eine überlegene Option ausfindig gemacht werden – "
                 "versuche, **objektiv** zu bewerten.")

    if st.button("Weiter zu Pro & Contra-Analyse"):
        st.session_state.current_option = 0
        st.session_state.pros_cons = {}
        st.session_state.page = "6_x_1"
        st.rerun()

# --- STEP 6.3.1.n.1 / 6.4.1.n.1: Pros & Contras auflisten ---
elif st.session_state.page == "6_x_1":
    i = st.session_state.current_option
    option = st.session_state.option_names[i]
    st.subheader(f"Option {i+1}: {option}")
    st.write("Liste alle Pros und Contras dieser Option auf (jeweils eine Zeile und bitte keine doppelten Auflistungen).")

    pros = st.text_area("Pros", key=f"pros_{i}")
    cons = st.text_area("Contras", key=f"cons_{i}")

    if st.button("Weiter zur Bewertung"):
        st.session_state.pros_cons[option] = {
            "pros": pros.splitlines(),
            "cons": cons.splitlines(),
        }
        st.session_state.page = "6_x_2"
        st.rerun()

# --- STEP 6.3.1.n.2 / 6.4.1.n.2: Bewertung der Argumente ---
elif st.session_state.page == "6_x_2":
    i = st.session_state.current_option
    option = st.session_state.option_names[i]
    st.subheader(f"Bewertung der Argumente – {option}")

    pros_cons = st.session_state.pros_cons[option]
    bewertungen = {}

    def bewertungsauswahl(label, key):
        return st.selectbox(
            label,
            ["++ starker Vorteil (+2)", "+ Vorteil (+1)", "- Nachteil (-1)", "-- starker Nachteil (-2)"],
            key=key
        )

    for arg in pros_cons["pros"] + pros_cons["cons"]:
        if arg.strip():
            bewertungen[arg] = bewertungsauswahl(arg, f"{option}_{arg}")

    if st.button("Speichern und nächste Option"):
        st.session_state.pros_cons[option]["bewertungen"] = bewertungen
        st.session_state.current_option += 1

        if st.session_state.current_option < len(st.session_state.option_names):
            st.session_state.page = "6_x_1"  # nächste Option
        else:
            st.session_state.page = "6_x_summary"  # alle fertig
        st.rerun()

# --- STEP 6.3.2 / 6.4.2: Übersicht & finale Entscheidung ---
elif st.session_state.page == "6_x_summary":
    st.subheader("📊 Zusammenfassung deiner Bewertung")

    def berechne_summe(bewertungen):
        mapping = {"++": 2, "+": 1, "-": -1, "--": -2}
        total = 0
        for val in bewertungen.values():
            for k, v in mapping.items():
                if k in val:
                    total += v
        return total

    scores = {}
    for option, data in st.session_state.pros_cons.items():
        scores[option] = berechne_summe(data["bewertungen"])
        st.write(f"**{option}**: {scores[option]} Punkte")

    choice = st.radio("Welche Option möchtest du wählen?", list(scores.keys()))

    if st.button("Entscheidung treffen ✅"):
        st.success(f"🎯 Du hast dich entschieden für: **{choice}**")

    if st.button("Neu Entscheidung treffen 🔄"):
        st.session_state.clear()
        st.rerun()
