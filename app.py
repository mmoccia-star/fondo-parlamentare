cat > /mnt/user-data/outputs/app_semplificato_finale.py << 'EOF'
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fondo Parlamentare", page_icon="📊", layout="wide")

st.title("📊 Fondo Parlamentare Interventi")
st.markdown("501 beneficiari • 1.002 record • 2026-2027")

@st.cache_data
def load_data():
    return pd.read_csv('Fondo_Parlamentare_LOOKER_READY.csv')

df = load_data()

st.sidebar.header("🔍 Filtri")
settore = st.sidebar.selectbox("Macro-Settore", ['TUTTI'] + sorted(df['Macro_Settore'].unique().tolist()))
tipologia = st.sidebar.selectbox("Tipologia", ['TUTTI'] + sorted(df['Tipologia_Soggetto'].unique().tolist()))
regione = st.sidebar.selectbox("Regione", ['TUTTE'] + sorted(df['Regione'].unique().tolist()))
anno = st.sidebar.selectbox("Anno", [None, 2026, 2027], format_func=lambda x: "Tutti" if x is None else str(x))
ricerca = st.sidebar.text_input("Ricerca beneficiario...")

filtrati = df.copy()
if settore != 'TUTTI':
    filtrati = filtrati[filtrati['Macro_Settore'] == settore]
if tipologia != 'TUTTI':
    filtrati = filtrati[filtrati['Tipologia_Soggetto'] == tipologia]
if regione != 'TUTTE':
    filtrati = filtrati[filtrati['Regione'] == regione]
if anno is not None:
    filtrati = filtrati[filtrati['Anno'] == anno]
if ricerca:
    filtrati = filtrati[filtrati['Beneficiario'].str.contains(ricerca, case=False, na=False)]

st.divider()
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Importo", f"€{filtrati['Importo'].sum() / 1e6:.1f}M")
col2.metric("👥 Beneficiari", len(filtrati['Beneficiario'].unique()))
col3.metric("📂 Settori", len(filtrati['Macro_Settore'].unique()))
col4.metric("🗺️ Regioni", len(filtrati[filtrati['Regione'] != 'Non assegnata']['Regione'].unique()))

st.divider()
col1, col2 = st.columns(2)
with col1:
    st.subheader("Per Macro-Settore")
    dati = filtrati.groupby('Macro_Settore')['Importo'].sum().sort_values(ascending=False)
    st.plotly_chart(px.pie(values=dati.values, names=dati.index), use_container_width=True)

with col2:
    st.subheader("Per Tipologia")
    dati = filtrati.groupby('Tipologia_Soggetto')['Importo'].sum().sort_values(ascending=False).head(8)
    st.plotly_chart(px.bar(x=dati.values, y=dati.index, orientation='h'), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Trend Annuale")
    dati = filtrati.groupby('Anno')['Importo'].sum().sort_index()
    st.plotly_chart(px.line(x=dati.index, y=dati.values, markers=True), use_container_width=True)

with col2:
    st.subheader("Top 12 Beneficiari")
    dati = filtrati.groupby('Beneficiario')['Importo'].sum().sort_values(ascending=False).head(12)
    st.plotly_chart(px.bar(x=dati.values, y=dati.index, orientation='h'), use_container_width=True)

st.subheader("Top 10 Regioni")
dati = filtrati[filtrati['Regione'] != 'Non assegnata'].groupby('Regione')['Importo'].sum().sort_values(ascending=False).head(10)
st.plotly_chart(px.bar(x=dati.values, y=dati.index, orientation='h'), use_container_width=True)

st.subheader("📋 Dettagli")
if len(filtrati) > 0:
    st.dataframe(filtrati[['Beneficiario', 'Tipologia_Soggetto', 'Provincia', 'Regione', 'Macro_Settore', 'Anno', 'Importo']], use_container_width=True)
    st.caption(f"Mostrando {len(filtrati)} record su {len(df)} totali")

st.divider()
st.caption("Dashboard Fondo Parlamentare 2026-2027")
EOF
cat /mnt/user-data/outputs/app_semplificato_finale.py
Output

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fondo Parlamentare", page_icon="📊", layout="wide")

st.title("📊 Fondo Parlamentare Interventi")
st.markdown("501 beneficiari • 1.002 record • 2026-2027")

@st.cache_data
def load_data():
    return pd.read_csv('Fondo_Parlamentare_LOOKER_READY.csv')

df = load_data()

st.sidebar.header("🔍 Filtri")
settore = st.sidebar.selectbox("Macro-Settore", ['TUTTI'] + sorted(df['Macro_Settore'].unique().tolist()))
tipologia = st.sidebar.selectbox("Tipologia", ['TUTTI'] + sorted(df['Tipologia_Soggetto'].unique().tolist()))
regione = st.sidebar.selectbox("Regione", ['TUTTE'] + sorted(df['Regione'].unique().tolist()))
anno = st.sidebar.selectbox("Anno", [None, 2026, 2027], format_func=lambda x: "Tutti" if x is None else str(x))
ricerca = st.sidebar.text_input("Ricerca beneficiario...")

filtrati = df.copy()
if settore != 'TUTTI':
    filtrati = filtrati[filtrati['Macro_Settore'] == settore]
if tipologia != 'TUTTI':
    filtrati = filtrati[filtrati['Tipologia_Soggetto'] == tipologia]
if regione != 'TUTTE':
    filtrati = filtrati[filtrati['Regione'] == regione]
if anno is not None:
    filtrati = filtrati[filtrati['Anno'] == anno]
if ricerca:
    filtrati = filtrati[filtrati['Beneficiario'].str.contains(ricerca, case=False, na=False)]

st.divider()
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Importo", f"€{filtrati['Importo'].sum() / 1e6:.1f}M")
col2.metric("👥 Beneficiari", len(filtrati['Beneficiario'].unique()))
col3.metric("📂 Settori", len(filtrati['Macro_Settore'].unique()))
col4.metric("🗺️ Regioni", len(filtrati[filtrati['Regione'] != 'Non assegnata']['Regione'].unique()))

st.divider()
col1, col2 = st.columns(2)
with col1:
    st.subheader("Per Macro-Settore")
    dati = filtrati.groupby('Macro_Settore')['Importo'].sum().sort_values(ascending=False)
    st.plotly_chart(px.pie(values=dati.values, names=dati.index), use_container_width=True)

with col2:
    st.subheader("Per Tipologia")
    dati = filtrati.groupby('Tipologia_Soggetto')['Importo'].sum().sort_values(ascending=False).head(8)
    st.plotly_chart(px.bar(x=dati.values, y=dati.index, orientation='h'), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Trend Annuale")
    dati = filtrati.groupby('Anno')['Importo'].sum().sort_index()
    st.plotly_chart(px.line(x=dati.index, y=dati.values, markers=True), use_container_width=True)

with col2:
    st.subheader("Top 12 Beneficiari")
    dati = filtrati.groupby('Beneficiario')['Importo'].sum().sort_values(ascending=False).head(12)
    st.plotly_chart(px.bar(x=dati.values, y=dati.index, orientation='h'), use_container_width=True)

st.subheader("Top 10 Regioni")
dati = filtrati[filtrati['Regione'] != 'Non assegnata'].groupby('Regione')['Importo'].sum().sort_values(ascending=False).head(10)
st.plotly_chart(px.bar(x=dati.values, y=dati.index, orientation='h'), use_container_width=True)

st.subheader("📋 Dettagli")
if len(filtrati) > 0:
    st.dataframe(filtrati[['Beneficiario', 'Tipologia_Soggetto', 'Provincia', 'Regione', 'Macro_Settore', 'Anno', 'Importo']], use_container_width=True)
    st.caption(f"Mostrando {len(filtrati)} record su {len(df)} totali")

st.divider()
st.caption("Dashboard Fondo Parlamentare 2026-2027")
