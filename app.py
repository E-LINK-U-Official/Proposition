import streamlit as st
import pandas as pd
from supabase import create_client

# 1. Configuración de página
st.set_page_config(page_title="E-Link-U Strategy Dashboard", layout="wide", page_icon="🚄")

# Estilo para las tarjetas del Chip
st.markdown("""
    <style>
    .sector-card {
        padding: 20px; border-radius: 10px; border-left: 5px solid;
        background-color: #0e1117; margin-bottom: 10px; min-height: 180px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Selector de Idioma en el Sidebar
with st.sidebar:
    st.title("🌐 Language / Idioma")
    lang = st.radio("Select Interface Language:", ("English", "Español"), index=0)
    st.divider()

# Diccionario de textos
text = {
    "English": {
        "title": "📊 E-Link-U: Regional Recovery Dashboard",
        "subtitle": "Recovering the €459B Friction Gap in European Infrastructure",
        "calc_h": "🎯 Regional Savings Calculator",
        "select": "Select a Country to Audit:",
        "metric_l": "Potential Recovery",
        "chip_h": "🔒 Triple-Sector Sovereign Architecture",
        "chip_info": "The NFC antenna is physically locked until a live fingerprint is detected.",
        "s1_t": "🟢 Finance Sector", "s1_p": "Offline C2C payments & Energy credits",
        "s2_t": "🔴 Health Sector", "s2_p": "Sovereign medical history (ZKP)",
        "s3_t": "🔵 Identity Sector", "s3_p": "eIDAS 2.0 / SSI Master-Key",
        "roadmap_h": "🗺️ Implementation Roadmap",
        "r1_t": "📍 Phase 1: Rural", "r1_d": "Focus: Seniors & Low-Connectivity",
        "r2_t": "🚄 Phase 2: Corridors", "r2_d": "Focus: Cross-border Rail Identity",
        "r3_t": "🌐 Phase 3: Universal", "r3_d": "Focus: Full EU Interoperability",
        "legal": "⚠️ Legal Disclaimer: Proprietary assets of Lia Ariadna Ruiz Ben."
    },
    "Español": {
        "title": "📊 E-Link-U: Panel de Recuperación Regional",
        "subtitle": "Recuperando los 459.000 M€ de brecha de fricción en la infraestructura europea",
        "calc_h": "🎯 Calculadora de Ahorro Regional",
        "select": "Seleccione un país para auditar:",
        "metric_l": "Recuperación Potencial",
        "chip_h": "🔒 Arquitectura Soberana de Triple Sector",
        "chip_info": "La antena NFC está bloqueada físicamente hasta detectar una huella dactilar viva.",
        "s1_t": "🟢 Sector Finanzas", "s1_p": "Pagos C2C Offline y créditos energéticos",
        "s2_t": "🔴 Sector Salud", "s2_p": "Historial médico soberano (ZKP)",
        "s3_t": "🔵 Sector Identidad", "s3_p": "Llave Maestra eIDAS 2.0 / SSI",
        "roadmap_h": "🗺️ Hoja de Ruta de Implementación",
        "r1_t": "📍 Fase 1: Rural", "r1_d": "Foco: Mayores y baja conectividad",
        "r2_t": "🚄 Fase 2: Corredores", "r2_d": "Foco: Identidad ferroviaria fronteriza",
        "r3_t": "🌐 Fase 3: Universal", "r3_d": "Foco: Interoperabilidad total UE",
        "legal": "⚠️ Aviso Legal: Activos propietarios de Lia Ariadna Ruiz Ben."
    }
}[lang]

# 3. Conexión a Base de Datos
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
    
    @st.cache_data(ttl=3600)
    def fetch_data():
        response = supabase.table("country_impact").select("*").execute()
        return pd.DataFrame(response.data)

    df = fetch_data()

    if not df.empty:
        st.title(text["title"])
        st.markdown(f"### {text['subtitle']}")

        # --- CALCULADORA ---
        st.header(text["calc_h"])
        col1, col2 = st.columns(2)
        with col1:
            country_selected = st.selectbox(text["select"], df['country_name'].unique())
            country_data = df[df['country_name'] == country_selected].iloc[0]
        with col2:
            st.metric(label=f"{text['metric_l']} ({country_selected})", 
                      value=f"€{country_data['rural_recovery_potential']:.2f} B")

        st.divider()
        st.bar_chart(data=df, x='country_name', y=['annual_loss_billion', 'rural_recovery_potential'], color=["#dc3545", "#28a745"])

        # --- CHIP VISUAL ---
        st.header(text["chip_h"])
        st.info(text["chip_info"])
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="sector-card" style="border-left-color: #28a745;"><h3 style="color: #28a745;">{text["s1_t"]}</h3><p>{text["s1_p"]}</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="sector-card" style="border-left-color: #dc3545;"><h3 style="color: #dc3545;">{text["s2_t"]}</h3><p>{text["s2_p"]}</p></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="sector-card" style="border-left-color: #007bff;"><h3 style="color: #007bff;">{text["s3_t"]}</h3><p>{text["s3_p"]}</p></div>', unsafe_allow_html=True)

        # --- ROADMAP ---
        st.divider()
        st.header(text["roadmap_h"])
        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown(f"### {text['r1_t']}\n**{text['r1_d']}**")
        with r2:
            st.markdown(f"### {text['r2_t']}\n**{text['r2_d']}**")
        with r3:
            st.markdown(f"### {text['r3_t']}\n**{text['r3_d']}**")

        st.divider()
        st.warning(text["legal"])

    else:
        st.warning("Awaiting sync...")

except Exception as e:
    st.error(f"Status: {e}")

# SIDEBAR GOVERNANCE
with st.sidebar:
    st.subheader("Governance")
    st.write("👤 Lia Ariadna Ruiz Ben")
    st.write("🔗 DOI: [10.5281/zenodo.19876558](https://zenodo.org)")
    st.caption("© 2026 E-Link-U | Licensed under CC BY-NC-ND 4.0")
