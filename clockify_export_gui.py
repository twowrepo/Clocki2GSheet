import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pandas as pd
import os
import sys
import importlib.util

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.abspath(".")

CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.py")
SERVICE_ACCOUNT_PATH = os.path.join(BASE_DIR, "config", "service_account.json")

# Debug
print("Base dir:", BASE_DIR)
print("CONFIG_PATH:", CONFIG_PATH)
print("SERVICE_ACCOUNT_PATH:", SERVICE_ACCOUNT_PATH)

spec = importlib.util.spec_from_file_location("config", CONFIG_PATH)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

import clockify
from google_spreadsheet import GoogleSheet


def get_month_range(year, month):
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)
    return start, end

def generate_monthly_report_from_gui(year, month):
    start, end = get_month_range(year, month)
    period_label = f"{year}-{month:02d}"
    print(f"Exporting report for: {period_label}")

    time_data = clockify.get_timeentries_raw(start, end, config)
    if not time_data or 'timeentries' not in time_data:
        raise ValueError("Nessun dato trovato per il periodo selezionato.")

    rows = []
    for entry in time_data['timeentries']:
        rows.append({
            'Entry start date': entry['timeInterval']['start'][:10],
            'User name': entry['userName'],
            'Tags': ', '.join(tag['name'] for tag in entry.get('tags', [])),
            'Project note': '',
            'Project name': entry.get('projectName', ''),
            'Client name': entry.get('clientName', ''),
            'Description': entry.get('description', ''),
            'Duration (h)': round(entry['timeInterval']['duration'] / 3600, 2)
        })

    df_export = pd.DataFrame(rows)
    sheet = GoogleSheet(SERVICE_ACCOUNT_PATH)
    spreadsheet = sheet.client.open_by_key(config.GOOGLE_SHEET_EXPORT_FILE_ID)

    try:
        ws = spreadsheet.worksheet(period_label)
        ws.clear()
    except:
        ws = spreadsheet.add_worksheet(title=period_label, rows="1000", cols="10")

    ws.update([df_export.columns.values.tolist()] + df_export.values.tolist())
    print(f"Export completato per: {period_label}")

def run_gui():
    def run_export():
        try:
            year = int(entry_year.get())
            month = int(entry_month.get())
            generate_monthly_report_from_gui(year, month)
            messagebox.showinfo("Successo", "Dati esportati con successo!")
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    root = tk.Tk()
    root.title("Clocki2GSheet")

    tk.Label(root, text="Anno:").grid(row=0, column=0)
    entry_year = tk.Entry(root)
    entry_year.grid(row=0, column=1)

    tk.Label(root, text="Mese:").grid(row=1, column=0)
    entry_month = tk.Entry(root)
    entry_month.grid(row=1, column=1)

    tk.Button(root, text="Esporta", command=run_export).grid(row=2, column=0, columnspan=2, pady=10)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
