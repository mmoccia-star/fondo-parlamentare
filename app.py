import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fondo Parlamentare", page_icon="📊", layout="wide")
st.title("📊 Fondo Parlamentare")
st.markdown("501 beneficiari | 1.002 record")

df = pd.read_csv('Fondo_Parlamentare_LOOKER_READY.csv')

st.sidebar.header("Filtri")
settore = st.sidebar.selectbox("Settore", ['TUTTI'] + list(df['Macro_Settore'].unique()))
tipologia = st.sidebar.selectbox("Tipologia", ['TUTTI'] + list(df['Tipologia_Soggetto'].unique()))
regione = st.sidebar.selectbox("Regione", ['TUTTE'] + list(df['Regione'].unique()))
ricerca = st.sidebar.text_input("Ricerca beneficiario...")

filtrati = df.copy()
if settore != 'TUTTI':
    filtrati = filtrati[filtrati['Macro_Settore'] == settore]
if tipologia != 'TUTTI':
    filtrati = filtrati[filtrati['Tipologia_Soggetto'] == tipologia]
if regione != 'TUTTE':
    filtrati = filtrati[filtrati['Regione'] == regione]
if ricerca:
    filtrati = filtrati[filtrati['Beneficiario'].str.contains(ricerca, case=False, na=False)]

col1, col2, col3 = st.columns(3)
col1.metric("Importo", f"€{filtrati['Importo'].sum()/1e6:.1f}M")
col2.metric("Beneficiari", len(filtrati['Beneficiario'].unique()))
col3.metric("Settori", len(filtrati['Macro_Settore'].unique()))

if len(filtrati) > 0:
    st.subheader("Per Settore")
    dati_settore = filtrati.groupby('Macro_Settore')['Importo'].sum().sort_values(ascending=False)
    if len(dati_settore) > 0:
        fig = px.pie(values=dati_settore.values, names=dati_settore.index)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Top Beneficiari")
    dati_ben = filtrati.groupby('Beneficiario')['Importo'].sum().sort_values(ascending=False).head(12)
    if len(dati_ben) > 0:
        fig = px.bar(x=dati_ben.values, y=dati_ben.index, orientation='h')
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Tabella Dati")
    st.dataframe(filtrati[['Beneficiario', 'Tipologia_Soggetto', 'Provincia', 'Regione', 'Macro_Settore', 'Anno', 'Importo']], use_container_width=True)
else:
    st.warning("Nessun risultato per questa ricerca")
