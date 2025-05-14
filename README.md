# lifestyle25
🏆 Life Style Tracker – Sfida e Crescita
"Il successo è la somma di piccoli sforzi, ripetuti giorno dopo giorno." – Robert Collier

🎯 Descrizione
Life Style Tracker è un'app web interattiva creata con Streamlit per tracciare abitudini quotidiane, migliorare la disciplina personale e visualizzare i progressi in modo semplice e motivante.

Ogni attività completata assegna dei punti. I dati sono salvati in un database SQLite, e i grafici vengono generati con Plotly per mostrare i progressi settimanali e giornalieri.

🚀 Funzionalità principali
Selezione della data e tracciamento delle abitudini quotidiane:

🏃 Passeggiata

🏡 Pulizia stanza

📖 Sistemazione appunti

🧘 Meditazione

💃 Danza

✍️ Journaling

📚 Lettura

Calcolo automatico dei punti totali giornalieri

Salvataggio persistente dei dati su SQLite

Visualizzazione dello storico progressi

Grafico dell’andamento dei punti nel tempo

Somma dei punti settimanali in corso

📸 Supporto a immagini motivazionali tramite la cartella assets

🛠️ Tecnologie utilizzate
Linguaggio/Tool	Descrizione
Python	Linguaggio di programmazione
Streamlit	Framework per web app interattive
SQLite	Database leggero locale
Plotly Express	Grafici interattivi
Pandas	Manipolazione dati
pathlib	Gestione portabile dei path

📦 Installazione
Clona il repository

bash
Copia
Modifica
git clone https://github.com/tuo-username/lifestyle-tracker.git
cd lifestyle-tracker
Crea un ambiente virtuale (opzionale ma consigliato)

bash
Copia
Modifica
python -m venv .venv
source .venv/bin/activate  # su Windows: .venv\Scripts\activate
Installa le dipendenze

bash
Copia
Modifica
pip install -r requirements.txt
Avvia l'app Streamlit

bash
Copia
Modifica
streamlit run app.py
📁 Struttura del progetto
bash
Copia
Modifica
📦 lifestyle-tracker/
├── app.py                   # File principale Streamlit
├── habit_tracker.db         # Database SQLite (generato al primo avvio)
├── assets/
│   ├── image_1.jpg          # Immagine finale motivazionale
│   └── image_2.jpg          # Immagine iniziale motivazionale
├── requirements.txt         # Librerie necessarie
└── README.md                # Documentazione (questo file)
📊 Screenshot dell'app
(Inserisci qui uno screenshot dell'interfaccia Streamlit e del grafico dei punti)

🧠 Istruzioni didattiche (per studenti/devs)
Questo progetto dimostra come usare Streamlit per creare dashboard personali con salvataggio locale.

Ottimo esercizio per:

Imparare l’integrazione tra frontend interattivo e backend dati

Comprendere le basi della persistenza con SQLite

Costruire grafici time-series con Plotly

Allenare l’abitudine al miglioramento personale 😄

🔐 Note sulla privacy
Tutti i dati sono salvati in locale, nel file habit_tracker.db. Non vengono inviati su internet.

❤️ Contribuisci
Hai idee per nuove abitudini, notifiche giornaliere o supporto mobile? Sentiti libero di aprire una issue o fare una pull request.

📄 Licenza
Distribuito sotto licenza MIT. Vedi il file LICENSE per dettagli.

👨‍💻 Autore
Piero Crispin Tacunan Eulogio
📬 LinkedIn — 🧠 ITS Big Data Specialist 2023–2025