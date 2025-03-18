import os
import pandas as pd
import streamlit as st
import plotly.express as px

# 📌 Imposta il percorso del file CSV per salvare i dati
FILE_PATH = "habit_tracker.csv"

# 📌 Funzione per caricare i dati salvati
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    else:
        return pd.DataFrame(columns=["Data", "Ora", "Passeggiata", "Pulizia Stanza", "Sistemazione Appunti", "Meditazione", "Danza", "Journaling", "Punti"])

# 📌 Funzione per salvare i dati
def save_data(df):
    df.to_csv(FILE_PATH, index=False)

# 📌 Carica i dati esistenti
habit_data = load_data()

# 📌 Funzione per calcolare i punti
def calcola_punti(row):
    punti = 0
    if row["Passeggiata"]: punti += 10
    if row["Pulizia Stanza"]: punti += 5
    if row["Sistemazione Appunti"]: punti += 7
    if row["Meditazione"]: punti += 8
    if row["Danza"]: punti += 15
    if row["Journaling"]: punti += 10
    return punti

# 📌 UI Streamlit
st.set_page_config(page_title="Life Style", layout="wide")

st.title("📅 Life Style - Monitoraggio Abitudini e Gamification")
st.subheader("🚀 Trasforma la tua crescita in una sfida!")

# 📌 Sezione per selezionare la data e l'ora
data = st.date_input("📆 Seleziona la data")
ora = st.time_input("⏰ Seleziona l'orario")

# 📌 Griglia delle abitudini
st.subheader("🎯 Seleziona le attività completate")
col1, col2 = st.columns(2)
with col1:
    passeggiata = st.checkbox("🏃 Passeggiata (10 punti)")
    pulizia_stanza = st.checkbox("🏡 Pulizia Stanza (5 punti)")
    sistemazione_appunti = st.checkbox("📖 Sistemazione Appunti (7 punti)")
with col2:
    meditazione = st.checkbox("🧘 Meditazione (8 punti)")
    danza = st.checkbox("💃 Danza (15 punti)")
    journaling = st.checkbox("✍️ Journaling (10 punti)")

# 📌 Pulsante per salvare i progressi
if st.button("💾 Salva i progressi"):
    nuovo_record = pd.DataFrame([{
        "Data": data,
        "Ora": ora,
        "Passeggiata": passeggiata,
        "Pulizia Stanza": pulizia_stanza,
        "Sistemazione Appunti": sistemazione_appunti,
        "Meditazione": meditazione,
        "Danza": danza,
        "Journaling": journaling
    }])
    nuovo_record["Punti"] = nuovo_record.apply(calcola_punti, axis=1)
    
    habit_data = pd.concat([habit_data, nuovo_record], ignore_index=True)
    save_data(habit_data)
    st.success("✅ Progressi salvati con successo!")

# 📌 Sezione per eliminare un record
st.subheader("🗑️ Elimina un progresso specifico")
if not habit_data.empty:
    eliminare = st.selectbox("Seleziona il record da eliminare", habit_data["Data"] + " " + habit_data["Ora"].astype(str))
    if st.button("🗑️ Elimina la riga selezionata"):
        habit_data = habit_data[~((habit_data["Data"] + " " + habit_data["Ora"].astype(str)) == eliminare)]
        save_data(habit_data)
        st.warning("❌ Progresso eliminato!")

# 📌 Tabella dei progressi registrati
st.subheader("📊 Progressi Registrati")
st.dataframe(habit_data)

# 📌 Grafico dei punti settimanali
st.subheader("📈 Andamento dei Punti")
if not habit_data.empty:
    habit_data["Data"] = pd.to_datetime(habit_data["Data"])
    punti_giornalieri = habit_data.groupby("Data")["Punti"].sum().reset_index()
    fig = px.line(punti_giornalieri, x="Data", y="Punti", markers=True, title="Punti accumulati nel tempo")
    st.plotly_chart(fig)

# 📌 Frase motivazionale
st.markdown("""
    🌟 **Ricorda:** La disciplina è il ponte tra gli obiettivi e i risultati! Continua così! 💪  
""", unsafe_allow_html=True)
