import streamlit as st
import pandas as pd
import datetime
import sqlite3
import plotly.express as px

# Creazione database SQLite
conn = sqlite3.connect("habit_tracker.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS habits (
                date TEXT PRIMARY KEY,
                passeggiata INTEGER,
                pulizia_stanza INTEGER,
                sistemazione_appunti INTEGER,
                meditazione INTEGER,
                danza INTEGER,
                journaling INTEGER,
                lettura INTEGER,
                punti INTEGER)''')
conn.commit()

# Funzione per caricare dati
def load_data():
    return pd.read_sql("SELECT * FROM habits", conn)

# Funzione per salvare dati
def save_data(entry):
    c.execute("""
        INSERT INTO habits (date, passeggiata, pulizia_stanza, sistemazione_appunti, meditazione, danza, journaling, lettura, punti)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
        passeggiata=excluded.passeggiata,
        pulizia_stanza=excluded.pulizia_stanza,
        sistemazione_appunti=excluded.sistemazione_appunti,
        meditazione=excluded.meditazione,
        danza=excluded.danza,
        journaling=excluded.journaling,
        lettura=excluded.lettura,
        punti=excluded.punti
    """, entry)
    conn.commit()

# Funzione per eliminare un record
def delete_entry(date):
    c.execute("DELETE FROM habits WHERE date = ?", (date,))
    conn.commit()

# Funzione per eliminare tutti i progressi
def delete_all_entries():
    c.execute("DELETE FROM habits")
    conn.commit()

# Carica i dati
habit_data = load_data()

# UI
st.set_page_config(layout="wide")  # Imposta la UI su tutta la larghezza dello schermo

# Immagine sopra il titolo
st.image("assets/background1.jpg", use_container_width=True)

st.markdown("""
    <h1 style='text-align: center; font-size: 36px; color: #3498db;'>🏆 Life Style - Sfida e Crescita</h1>
    <h3 style='text-align: center; font-size: 24px; color: #7f8c8d;'>Trasforma la disciplina in gioco!</h3>
""", unsafe_allow_html=True)

# Selezione data
selected_date = st.date_input("📅 Data", datetime.date.today()).strftime('%Y-%m-%d')
entry_exists = selected_date in habit_data["date"].values if not habit_data.empty else False

# Attività giornaliere
st.markdown("<h3 style='font-size: 22px;'>Seleziona le attività completate per guadagnare punti!</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    passeggiata = st.checkbox("🏃 Passeggiata (+10 punti)")
    pulizia_stanza = st.checkbox("🏡 Pulizia Stanza (+5 punti)")
with col2:
    sistemazione_appunti = st.checkbox("📖 Sistemazione Appunti (+5 punti)")
    meditazione = st.checkbox("🧘 Meditazione (+7 punti)")
with col3:
    danza = st.checkbox("💃 Danza (+15 punti)")
    journaling = st.checkbox("✍️ Journaling (+10 punti)")
    lettura = st.checkbox("📚 Lettura prima di dormire (+8 punti)")

# Calcolo punti
total_points = (
    10 * passeggiata + 5 * pulizia_stanza + 5 * sistemazione_appunti +
    7 * meditazione + 15 * danza + 10 * journaling + 8 * lettura
)

st.markdown(f"<h3 style='font-size: 22px;'>🌟 Punti totali oggi: <b>{total_points}</b></h3>", unsafe_allow_html=True)

# Barra di progresso
progress = min(total_points / 50 * 100, 100)
st.progress(progress / 100)

# Salvataggio dati
if st.button("💾 Salva i progressi"):
    entry = (selected_date, passeggiata, pulizia_stanza, sistemazione_appunti, meditazione, danza, journaling, lettura, total_points)
    save_data(entry)
    st.success("✅ Progressi salvati con successo!")
    st.rerun()

# Eliminazione di un record specifico
if st.button("🗑️ Elimina i progressi di oggi"):
    delete_entry(selected_date)
    st.warning("⚠️ Progressi eliminati!")
    st.rerun()

# Eliminazione di tutti i record
if st.button("🗑️ Elimina tutti i progressi"):
    delete_all_entries()
    st.warning("⚠️ Tutti i progressi sono stati eliminati!")
    st.rerun()

# Grafico andamento punti
habit_data = load_data()
if not habit_data.empty:
    st.subheader("📊 Andamento dei Punti")
    fig = px.line(habit_data, x="date", y="punti", markers=True, title="Punti giornalieri")
    st.plotly_chart(fig)

# Storico progressi
st.subheader("📜 Storico Progressi")
st.dataframe(habit_data)

# Obiettivo settimanale
st.subheader("🎯 Obiettivi Settimanali")
total_weekly_points = habit_data['punti'].sum() if not habit_data.empty else 0
st.markdown(f"<h3 style='font-size: 22px;'>Hai totalizzato <b>{total_weekly_points}</b> punti questa settimana!</h3>", unsafe_allow_html=True)

# Immagine in fondo alla pagina
st.image("assets/background2.jpg", use_container_width=True)

# Frase motivazionale
st.markdown("<h3 style='font-size: 22px;'>🚀 'Il successo è la somma di piccoli sforzi, ripetuti giorno dopo giorno.' - Robert Collier</h3>", unsafe_allow_html=True)
