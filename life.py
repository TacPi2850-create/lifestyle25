import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# Nome del file CSV per il salvataggio dei progressi
FILE_PATH = "habit_tracker.csv"

# Funzione per caricare i dati
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    else:
        return pd.DataFrame(columns=["Data", "Passeggiata", "Pulizia Stanza", "Sistemazione Appunti", "Meditazione", "Danza", "Journaling", "Punti"])

# Funzione per salvare i dati
def save_data(df):
    df.to_csv(FILE_PATH, index=False)

# Carica i dati
habit_data = load_data()

# Personalizzazione stile CSS
st.markdown(
    """
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
            text-align: center;
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .main-title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #3498db;
        }
        .sub-title {
            text-align: center;
            font-size: 22px;
            color: #7f8c8d;
            margin-bottom: 30px;
        }
        .progress-bar {
            width: 100%;
            background-color: #ddd;
            border-radius: 5px;
        }
        .progress-bar-fill {
            height: 20px;
            background-color: #4CAF50;
            text-align: center;
            color: white;
            border-radius: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Titolo principale
st.markdown("<div class='main-title'>🏆 Life Style - Sfida e Crescita</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Trasforma la disciplina in gioco!</div>", unsafe_allow_html=True)

# Seleziona la data
selected_date = st.date_input("📅 Data", datetime.date.today())
selected_datetime = selected_date.strftime('%Y-%m-%d')
entry_exists = selected_datetime in habit_data["Data"].values

# Attività
st.markdown("### Seleziona le attività completate per guadagnare punti!")
col1, col2, col3 = st.columns(3)

with col1:
    passeggiata = st.checkbox("🏃 Passeggiata (+10 punti)", value=False if not entry_exists else habit_data.loc[habit_data["Data"] == selected_datetime, "Passeggiata"].values[0])
    pulizia_stanza = st.checkbox("🏡 Pulizia Stanza (+5 punti)", value=False if not entry_exists else habit_data.loc[habit_data["Data"] == selected_datetime, "Pulizia Stanza"].values[0])
with col2:
    sistemazione_appunti = st.checkbox("📖 Sistemazione Appunti (+5 punti)", value=False if not entry_exists else habit_data.loc[habit_data["Data"] == selected_datetime, "Sistemazione Appunti"].values[0])
    meditazione = st.checkbox("🧘 Meditazione (+7 punti)", value=False if not entry_exists else habit_data.loc[habit_data["Data"] == selected_datetime, "Meditazione"].values[0])
with col3:
    danza = st.checkbox("💃 Danza (+15 punti)", value=False if not entry_exists else habit_data.loc[habit_data["Data"] == selected_datetime, "Danza"].values[0])
    journaling = st.checkbox("✍️ Journaling (+10 punti)", value=False if not entry_exists else habit_data.loc[habit_data["Data"] == selected_datetime, "Journaling"].values[0])

# Calcolo del punteggio
total_points = 0
total_points += 10 if passeggiata else 0
total_points += 5 if pulizia_stanza else 0
total_points += 5 if sistemazione_appunti else 0
total_points += 7 if meditazione else 0
total_points += 15 if danza else 0
total_points += 10 if journaling else 0

st.markdown(f"### 🌟 Punti totali oggi: **{total_points}**")

# Barra di progresso
progress = min(total_points / 50 * 100, 100)  # 50 punti massimo per giornata
st.markdown(f"""
    <div class='progress-bar'>
        <div class='progress-bar-fill' style='width:{progress}%'>{int(progress)}%</div>
    </div>
""", unsafe_allow_html=True)

# Bottone per salvare
if st.button("💾 Salva i progressi"):
    new_entry = {
        "Data": selected_datetime,
        "Passeggiata": passeggiata,
        "Pulizia Stanza": pulizia_stanza,
        "Sistemazione Appunti": sistemazione_appunti,
        "Meditazione": meditazione,
        "Danza": danza,
        "Journaling": journaling,
        "Punti": total_points
    }
    
    if entry_exists:
        habit_data.loc[habit_data["Data"] == selected_datetime] = new_entry
    else:
        habit_data = pd.concat([habit_data, pd.DataFrame([new_entry])], ignore_index=True)
    
    save_data(habit_data)
    st.success("✅ Progressi salvati con successo!")

# Grafico dei progressi
if not habit_data.empty:
    st.subheader("📊 Andamento dei Punti")
    fig = px.line(habit_data, x="Data", y="Punti", markers=True, title="Punti giornalieri")
    st.plotly_chart(fig)

# Mostra i dati salvati
st.subheader("📜 Storico Progressi")
st.dataframe(habit_data)

# Frase motivazionale
st.markdown("### 🚀 'Il successo è la somma di piccoli sforzi, ripetuti giorno dopo giorno.' - Robert Collier")
