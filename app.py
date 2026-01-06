import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configurazione pagina
st.set_page_config(
    page_title="Fondo Parlamentare",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
    }
    .title-main {
        color: #1f2937;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Titolo
st.markdown('<p class="title-main">📊 Fondo Parlamentare Interventi</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">501 beneficiari • 1.002 record • Dati 2026-2027 • Analisi interattiva</p>', unsafe_allow_html=True)

# Carica dati
@st.cache_data
def load_data():
    df = pd.read_csv('Fondo_Parlamentare_LOOKER_READY.csv')
    return df

df = load_data()

# Barra laterale - Filtri
st.sidebar.header("🔍 Filtri Dinamici")

# Estrazioni opzioni
settori = ['TUTTI'] + sorted([s for s in df['Macro_Settore'].unique() if pd.notna(s)])
tipologie = ['TUTTI'] + sorted([t for t in df['Tipologia_Soggetto'].unique() if pd.notna(t)])
regioni = ['TUTTE', 'Non assegnata'] + sorted([r for r in df['Regione'].unique() if r not in ['Non assegnata'] and pd.notna(r)])

# Selezioni
settore_sel = st.sidebar.selectbox(
    "**Macro-Settore**",
    settori,
    help="Filtra per categoria di intervento"
)

tipologia_sel = st.sidebar.selectbox(
    "**Tipologia Soggetto**",
    tipologie,
    help="Filtra per tipo di beneficiario"
)

regione_sel = st.sidebar.selectbox(
    "**Regione**",
    regioni,
    help="Filtra per regione geografica"
)

anno_sel = st.sidebar.selectbox(
    "**Anno**",
    ["Tutti", 2026, 2027],
    help="Filtra per anno finanziario"
)

ricerca = st.sidebar.text_input(
    "**Ricerca Beneficiario**",
    help="Digita nome, provincia o regione"
)

# Applica filtri
filtrati = df.copy()

if settore_sel != 'TUTTI':
    filtrati = filtrati[filtrati['Macro_Settore'] == settore_sel]

if tipologia_sel != 'TUTTI':
    filtrati = filtrati[filtrati['Tipologia_Soggetto'] == tipologia_sel]

if regione_sel != 'TUTTE':
    filtrati = filtrati[filtrati['Regione'] == regione_sel]

if anno_sel != "Tutti":
    filtrati = filtrati[filtrati['Anno'] == anno_sel]

if ricerca:
    filtrati = filtrati[
        (filtrati['Beneficiario'].str.contains(ricerca, case=False, na=False)) |
        (filtrati['Provincia'].str.contains(ricerca, case=False, na=False)) |
        (filtrati['Regione'].str.contains(ricerca, case=False, na=False))
    ]

# KPI principali
st.divider()
col1, col2, col3, col4 = st.columns(4)

with col1:
    importo_totale = filtrati['Importo'].sum()
    st.metric(
        "💰 Importo Totale",
        f"€{importo_totale / 1e6:.1f}M",
        f"€{importo_totale:,.0f}",
        help="Somma di tutti gli importi"
    )

with col2:
    beneficiari_unici = len(filtrati['Beneficiario'].unique())
    st.metric(
        "👥 Beneficiari Unici",
        beneficiari_unici,
        help="Numero di enti diversi"
    )

with col3:
    settori_count = len(filtrati['Macro_Settore'].unique())
    st.metric(
        "📂 Macro-Settori",
        settori_count,
        help="Categorie di intervento"
    )

with col4:
    regioni_count = len(filtrati[filtrati['Regione'] != 'Non assegnata']['Regione'].unique())
    st.metric(
        "🗺️ Regioni",
        regioni_count,
        help="Copertura geografica"
    )

st.divider()

# Grafici principali
st.header("📈 Visualizzazioni")

col1, col2 = st.columns(2)

# Grafico 1: Pie Chart Settori
with col1:
    st.subheader("Distribuzione per Macro-Settore")
    dati_settore = filtrati.groupby('Macro_Settore')['Importo'].sum().sort_values(ascending=False)
    
    if len(dati_settore) > 0:
        fig_pie = px.pie(
            values=dati_settore.values,
            names=dati_settore.index,
            color_discrete_sequence=px.colors.qualitative.Set2,
            hole=0.4
        )
        fig_pie.update_traces(
            hovertemplate="<b>%{label}</b><br>€%{value:,.0f}<extra></extra>"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Nessun dato disponibile")

# Grafico 2: Bar Chart Tipologia
with col2:
    st.subheader("Distribuzione per Tipologia (Top 8)")
    dati_tipologia = filtrati.groupby('Tipologia_Soggetto')['Importo'].sum().sort_values(ascending=False).head(8)
    
    if len(dati_tipologia) > 0:
        fig_bar = px.bar(
            y=dati_tipologia.index,
            x=dati_tipologia.values,
            orientation='h',
            color=dati_tipologia.values,
            color_continuous_scale='Blues'
        )
        fig_bar.update_xaxes(title_text="Importo (€)")
        fig_bar.update_yaxes(title_text="")
        fig_bar.update_traces(
            hovertemplate="<b>%{y}</b><br>€%{x:,.0f}<extra></extra>"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Nessun dato disponibile")

st.divider()

# Grafici secondari
col1, col2 = st.columns(2)

# Grafico 3: Line Chart Anno
with col1:
    st.subheader("Trend Annuale")
    dati_anno = filtrati.groupby('Anno')['Importo'].sum().sort_index()
    
    if len(dati_anno) > 0:
        fig_line = px.line(
            x=dati_anno.index,
            y=dati_anno.values,
            markers=True,
            color_discrete_sequence=['#ef4444']
        )
        fig_line.update_xaxes(title_text="Anno")
        fig_line.update_yaxes(title_text="Importo (€)")
        fig_line.update_traces(
            hovertemplate="<b>Anno %{x}</b><br>€%{y:,.0f}<extra></extra>",
            marker=dict(size=10)
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Nessun dato disponibile")

# Grafico 4: Top Beneficiari
with col2:
    st.subheader("Top 12 Beneficiari")
    top_beneficiari = filtrati.groupby('Beneficiario')['Importo'].sum().sort_values(ascending=False).head(12)
    
    if len(top_beneficiari) > 0:
        fig_top = px.bar(
            y=top_beneficiari.index,
            x=top_beneficiari.values,
            orientation='h',
            color=top_beneficiari.values,
            color_continuous_scale='Viridis'
        )
        fig_top.update_xaxes(title_text="Importo (€)")
        fig_top.update_yaxes(title_text="")
        fig_top.update_traces(
            hovertemplate="<b>%{y}</b><br>€%{x:,.0f}<extra></extra>"
        )
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.info("Nessun dato disponibile")

st.divider()

# Top Regioni (grafico a barre)
st.subheader("Top 10 Regioni")
regioni_non_assign = filtrati[filtrati['Regione'] != 'Non assegnata']
top_regioni = regioni_non_assign.groupby('Regione')['Importo'].sum().sort_values(ascending=False).head(10)

if len(top_regioni) > 0:
    fig_regioni = px.bar(
        y=top_regioni.index,
        x=top_regioni.values,
        orientation='h',
        color=top_regioni.values,
        color_continuous_scale='Greens'
    )
    fig_regioni.update_xaxes(title_text="Importo (€)")
    fig_regioni.update_yaxes(title_text="")
    fig_regioni.update_traces(
        hovertemplate="<b>%{y}</b><br>€%{x:,.0f}<extra></extra>"
    )
    st.plotly_chart(fig_regioni, use_container_width=True)
else:
    st.info("Nessun dato disponibile")

st.divider()

# Tabella dettagli
st.subheader("📋 Dettagli Completi")

colonne_visualizzate = [
    'Beneficiario',
    'Tipologia_Soggetto',
    'Provincia',
    'Regione',
    'Macro_Settore',
    'Finalita_Oggetto',
    'Anno',
    'Importo'
]

if len(filtrati) > 0:
    # Formattazione per visualizzazione
    tabella_display = filtrati[colonne_visualizzate].copy()
    tabella_display['Importo'] = tabella_display['Importo'].apply(lambda x: f"€{x:,.0f}")
    
    st.dataframe(
        tabella_display,
        use_container_width=True,
        height=500,
        hide_index=True
    )
    
    st.caption(f"📌 Mostrando {len(filtrati)} record su {len(df)} totali")
else:
    st.warning("❌ Nessun record corrisponde ai tuoi filtri. Prova a modificarli.")

st.divider()

# Footer
st.markdown("""
---
**Dashboard interattiva - Fondo Parlamentare per l'Attuazione di Interventi**
- 501 beneficiari | 1.002 record | 2026-2027
- Dati aggiornati | Filtri dinamici in tempo reale
""")

# Info ultima modifica
st.caption(f"Ultimo aggiornamento: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
