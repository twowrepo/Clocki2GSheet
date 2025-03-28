# Clocki2GSheet

App desktop per macOS che consente di esportare i dati mensili da Clockify a Google Sheets, organizzati per tab mensile (`YYYY-MM`).
Semplice interfaccia grafica basata su Tkinter, nessun terminale richiesto.

## ✅ Funzionalità

- Esporta i time entries di Clockify per un mese/anno specifico
- Crea (o aggiorna) un tab per ogni mese nel Google Sheet target
- Si autentica via Service Account Google (no OAuth)
- Configurazione esterna e modificabile anche dopo la compilazione

## 📁 Struttura dei file

```
Clocki2GSheet.app/
config.py
service_account.json
```

## ⚙️ Configurazione

Crea un file `config.py` nella stessa cartella della `.app`, con le seguenti variabili:

```python
CLOCKIFY_API_KEY = "xxx"
CLOCKIFY_WORKSPACE_ID = "xxx"
GOOGLE_SHEET_EXPORT_FILE_ID = "xxx"
```

Copia accanto anche il file `service_account.json` del tuo Service Account Google.

Assicurati che il file Google Sheet e la cartella Drive siano **condivisi** con l'email del Service Account.

## 🚀 Esecuzione

1. Fai doppio clic sull'app `Clocki2GSheet.app`
2. Inserisci l'anno e il mese da esportare
3. Clicca "Esporta"
4. I dati verranno scritti nel tab `"YYYY-MM"` del Google Sheet

## 🧱 Per sviluppatori (compilare .app)

### 1. Crea ambiente

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Compila `.app`

```bash
pyinstaller --windowed clockify_export_gui.py --name "Clocki2GSheet"
```

### 3. Struttura finale per la distribuzione

```
dist/
├── Clocki2GSheet.app
├── config.py
└── service_account.json
```

**Non serve build con `--onefile`**.

## 🛡️ Problemi comuni

- Se macOS blocca l'app: clic destro > Apri > "Apri comunque"
- Se la GUI non si apre: avvia da terminale per vedere gli errori

## 📝 Licenza

MIT
