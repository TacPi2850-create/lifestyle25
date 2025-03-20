import streamlit as st
import pandas as pd
import datetime
import sqlite3
import plotly.express as px
from pathlib import Path

# Imposta la directory base
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "habit_tracker.db"
IMG_DIR = BASE_DIR / "assets"
IMG_PATH_TOP = IMG_DIR / "image_1.jpg"
IMG_PATH_BOTTOM = IMG_DIR / "image_2.jpg"

# Assicurati che la cartella assets esista
IMG_DIR.mkdir(parents=True, exist_ok=True)

# Connessione al database SQLite
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

# Creazione tabella se non esiste
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

# Funzioni gestione dati
def load_data():
    return pd.read_sql("SELECT * FROM habits ORDER BY date DESC", conn)

def save_data(entry):
    c.execute('''INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                 ON CONFLICT(date) DO UPDATE SET
                 passeggiata=excluded.passeggiata,
                 pulizia_stanza=excluded.pulizia_stanza,
                 sistemazione_appunti=excluded.sistemazione_appunti,
                 meditazione=excluded.meditazione,
                 danza=excluded.danza,
                 journaling=excluded.journaling,
                 lettura=excluded.lettura,
                 punti=excluded.punti''', entry)
    conn.commit()

def delete_entry(date):
    c.execute("DELETE FROM habits WHERE date=?", (date,))
    conn.commit()

def delete_all_entries():
    c.execute("DELETE FROM habits")
    conn.commit()

# Caricamento iniziale dei dati
habit_data = load_data()

# Configurazione pagina
st.set_page_config(layout="wide", page_title="Life Style Tracker")

# Immagine introduttiva
if IMG_PATH_TOP.exists():
    st.image(str(IMG_PATH_TOP), use_container_width=True)

# Titolo e sottotitolo
st.markdown("""
<h1 style='text-align: center; color: #3498db;'>🏆 Life Style - Sfida e Crescita</h1>
<h3 style='text-align: center; color: #7f8c8d;'>Trasforma la disciplina in gioco!</h3>
""", unsafe_allow_html=True)

# Data selezionata
selected_date = st.date_input("📅 Data", datetime.date.today())
selected_date_str = selected_date.strftime('%Y-%m-%d')
entry_exists = not habit_data[habit_data['date'] == selected_date_str].empty

# Attività
st.markdown("### ✅ Attività completate oggi")
col1, col2, col3 = st.columns(3)

def activity_checkbox(label, points, default=False):
    return st.checkbox(f"{label} (+{points} punti)", value=bool(default))

with col1:
    passeggiata = activity_checkbox("🏃 Passeggiata", 10, entry_exists)
    pulizia_stanza = activity_checkbox("🏡 Pulizia Stanza", 5, entry_exists)
with col2:
    sistemazione_appunti = activity_checkbox("📖 Sistemazione Appunti", 5, entry_exists)
    meditazione = activity_checkbox("🧘 Meditazione", 7, entry_exists)
with col3:
    danza = activity_checkbox("💃 Danza", 15, entry_exists)
    journaling = activity_checkbox("✍️ Journaling", 10, entry_exists)
    lettura = activity_checkbox("📚 Lettura prima di dormire", 8, entry_exists)

# Calcolo punti
total_points = sum([
    passeggiata * 10, pulizia_stanza * 5, sistemazione_appunti * 5,
    meditazione * 7, danza * 15, journaling * 10, lettura * 8
])

st.markdown(f"### 🌟 Punti totali oggi: **{total_points}**")
st.progress(min(total_points / 50, 1.0))

# Pulsanti gestione dati
col_save, col_del, col_del_all = st.columns(3)

with col_save:
    if st.button("💾 Salva i progressi"):
        save_data((selected_date_str, passeggiata, pulizia_stanza, sistemazione_appunti,
                   meditazione, danza, journaling, lettura, total_points))
        st.success("✅ Progressi salvati!")
        st.rerun()

with col_del:
    if st.button("🗑️ Elimina i progressi di oggi"):
        delete_entry(selected_date_str)
        st.warning("⚠️ Progressi di oggi eliminati!")
        st.rerun()

with col_del_all:
    if st.button("🗑️ Elimina tutti i progressi"):
        delete_all_entries()
        st.warning("⚠️ Tutti i progressi eliminati!")
        st.rerun()

# Grafici e storico
data_updated = load_data()
if not data_updated.empty:
    st.markdown("---")
    st.subheader("📊 Andamento dei Punti")
    fig = px.line(data_updated, x="date", y="punti", markers=True, title="Punti giornalieri")
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📜 Storico Progressi")
    st.dataframe(data_updated, use_container_width=True)
    
    current_week = datetime.date.today().isocalendar()[1]
    data_updated['date'] = pd.to_datetime(data_updated['date'])
    weekly_points = data_updated[data_updated['date'].dt.isocalendar().week == current_week]['punti'].sum()
    st.markdown(f"### 🎯 Punti totalizzati questa settimana: **{weekly_points}**")

# Immagine e frase motivazionale finale
if IMG_PATH_BOTTOM.exists():
    st.image(str(IMG_PATH_BOTTOM), use_container_width=True)

st.markdown("🚀 *'Il successo è la somma di piccoli sforzi, ripetuti giorno dopo giorno.'* – Robert Collier")
