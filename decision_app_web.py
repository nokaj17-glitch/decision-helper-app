import streamlit as st

st.title("🧭 Decision Helper Web App")

# Step 1
if "page" not in st.session_state:
    st.session_state.page = 1

# Step 1 – Welcome
if st.session_state.page == 1:
    st.write("Willkommen beim Decision Helper!")
    if st.button("Start Decision"):
        st.session_state.page = 2
        st.rerun()

# Step 2 – Describe Decision
elif st.session_state.page == 2:
    decision = st.text_input("Welche Entscheidung willst du treffen?")
    if st.button("Weiter"):
        if not decision.strip():
            st.warning("Bitte gib eine Entscheidung ein.")
        else:
            st.session_state.decision = decision
            st.session_state.page = 3
            st.rerun()

# Step 3 – Number of Options
elif st.session_state.page == 3:
    num = st.number_input("Wie viele Optionen hast du?", min_value=1, max_value=10, step=1)
    if st.button("Weiter"):
        st.session_state.num_options = int(num)
        st.session_state.page = 4
        st.rerun()

# Step 4 – Option Names
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

# Step 5 – Pros & Cons
elif st.session_state.page == 5:
    st.write("💭 Denke über jede Option nach und notiere dir die Pros & Cons (auf Papier oder im Kopf).")
    if st.button("Weiter"):
        st.session_state.page = 6
        st.rerun()

# Step 6 – Choose Option
elif st.session_state.page == 6:
    st.write("Wähle deine bevorzugte Option:")
    choice = st.radio("Optionen", st.session_state.option_names)
    if st.button("Fertig"):
        st.success(f"🎉 Du hast dich entschieden für: **{choice}**")
        st.session_state.clear()
