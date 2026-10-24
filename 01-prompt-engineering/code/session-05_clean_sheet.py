"""An assistant was asked: 'Clean this messy attendance sheet and summarise it.'
Below is the kind of pandas code it suggests (the same steps map to Google Sheets functions)."""
import pandas as pd

raw = pd.DataFrame({
    "Name": [" ali khan", "SARA AHMED", "Bilal  Raza", "sara ahmed", "Hina Shah", None],
    "Class": ["BSCS-1", "bscs-1", "BSCS-2", "BSCS-1", "BSCS-2", "BSCS-1"],
    "Attended": ["14", "16", "9", "16", "n/a", "12"],
    "Total": [16, 16, 16, 16, 16, 16],
})
df = raw.dropna(subset=["Name"]).copy()                       # = FILTER out blanks
df["Name"] = df["Name"].str.split().str.join(" ").str.title()  # = PROPER(TRIM())
df["Class"] = df["Class"].str.upper()                         # = UPPER()
df = df.drop_duplicates(subset=["Name", "Class"])              # = Data > Remove duplicates
df["Attended"] = pd.to_numeric(df["Attended"], errors="coerce").fillna(0).astype(int)
df["Attendance %"] = (df["Attended"] / df["Total"] * 100).round(1)
df["Status"] = df["Attendance %"].apply(lambda p: "OK" if p >= 75 else "At risk")  # = IF()
print(df.to_string(index=False))
print("\nClass averages:")
print(df.groupby("Class")["Attendance %"].mean().round(1).to_string())
