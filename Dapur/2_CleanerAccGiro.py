import pandas as pd
import os

config_file = 'config.conf'
run_giro = False

if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    if '[GIRO]' in lines:
        idx = lines.index('[GIRO]')
        if idx + 1 < len(lines):
            line_val = lines[idx + 1].replace(' ', '').lower()
            if line_val == 'giro_stats=ya':
                run_giro = True

if not run_giro:
    print("--> Proses GIRO di-skip berdasarkan config.conf.")
    exit()

df = pd.read_excel('Giro.xls', header=4)

df.columns = df.columns.astype(str).str.strip()

mapping_kolom = {
    'Kode': 'No. Pelanggan',
    'Nama Pelanggan': 'Nama Pelanggan',
    'Tgl Faktur': 'Tgl Faktur',
    'No': 'No. Faktur. (SO)',
    'No. Faktur': 'No. Faktur. (SO)',
    'No Cek': 'No. Form',
    'Nilai Faktur': 'Total Diterima',
    'Nilai Dibayar': 'Nilai terima',
    'Bayar Via': 'Nama Bank',
    'Tgl Bayar': 'Tgl Cek'
}

kolom_tersedia = [k for k in mapping_kolom.keys() if k in df.columns]
hasil_df = df[kolom_tersedia].copy()

hasil_df = hasil_df.rename(columns=mapping_kolom)

if 'No. Pelanggan' in hasil_df.columns:
    hasil_df = hasil_df.dropna(subset=['No. Pelanggan'])
    
    hasil_df['No. Pelanggan'] = hasil_df['No. Pelanggan'].astype(str).str.strip()
    hasil_df = hasil_df[~hasil_df['No. Pelanggan'].isin(['', 'nan', 'None'])]

# if 'No. Faktur. (SO)' in hasil_df.columns:
#    hasil_df['No. Faktur. (SO)'] = hasil_df['No. Faktur. (SO)'].astype(str).str.replace('INV/', '', regex=False)

if 'Total Diterima' in hasil_df.columns:
    hasil_df['Total Diterima'] = hasil_df['Total Diterima'].astype(str).str.replace(',', '.', regex=False)
    hasil_df['Total Diterima'] = pd.to_numeric(hasil_df['Total Diterima'], errors='coerce')

if 'Nilai terima' in hasil_df.columns:
    hasil_df['Nilai terima'] = hasil_df['Nilai terima'].astype(str).str.replace(',', '.', regex=False)
    hasil_df['Nilai terima'] = pd.to_numeric(hasil_df['Nilai terima'], errors='coerce')

hasil_df.to_excel('Giro_temp.xlsx', index=False)

print("--> File Giro_temp.xlsx telah berhasil dibuat")