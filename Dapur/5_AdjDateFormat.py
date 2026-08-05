import pandas as pd

df = pd.read_excel("ARClean_temp.xlsx")

mapping_bulan = {
    1: 'Jan',  2: 'Feb',  3: 'Mar',  4: 'Apr',  5: 'Mei',  6: 'Jun',
    7: 'Jul',  8: 'Agu',  9: 'Sep',  10: 'Okt', 11: 'Nov', 12: 'Des'
}

def ubah_format(nilai):
    if pd.isna(nilai):
        return nilai

    dt = None

    try:
        if isinstance(nilai, str):
            nilai_bersih = nilai.replace(".", "").replace(",", ".")
            angka_serial = float(nilai_bersih)
        else:
            angka_serial = float(nilai)

        dt = pd.to_datetime(angka_serial, unit="D", origin="1899-12-30")

        if pd.notna(dt):
            hari_asli = dt.month 
            bulan_asli = (
                dt.day
            )
            tahun_asli = dt.year

            if 1 <= bulan_asli <= 12:
                return f"{hari_asli} {mapping_bulan[bulan_asli]} {tahun_asli}"
            else:
                return f"{dt.day} {mapping_bulan[dt.month]} {dt.year}"

    except (ValueError, TypeError):
        dt = pd.to_datetime(nilai, errors="coerce")
        if pd.notna(dt):
            return f"{dt.day} {mapping_bulan[dt.month]} {dt.year}"

    return nilai


df["Tgl Faktur"] = df["Tgl Faktur"].apply(ubah_format)
df["Jatuh Tempo"] = df["Jatuh Tempo"].apply(ubah_format)

df.to_excel("ARClean_temp.xlsx", index=False)

print(
    "--> Format tanggal pada kolom Tgl Faktur dan Jatuh Tempo berhasil diubah."
)