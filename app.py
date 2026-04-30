import streamlit as st
import pandas as pd
from supabase import create_client

# 1. Configuración de página
st.set_page_config(page_title="E-Link-U Strategy Dashboard", layout="wide", page_icon="🚄")

# Estilos visuales
st.markdown("""
    <style>
    .sector-card {
        padding: 20px; border-radius: 10px; border-left: 5px solid;
        background-color: #1e293b; margin-bottom: 10px; min-height: 220px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Selector de Idioma en el Sidebar
with st.sidebar:
    st.title("🌐 Language / Idioma")
    lang = st.radio("Select Interface Language:", ("English", "Español"), index=0)
    st.divider()

# Diccionario Maestro 2025
text = {
    "English": {
        "title": "📊 E-Link-U: Regional Recovery Dashboard",
        "subtitle": "Recovering the €459B Friction Gap (2025 Audit Data)",
        "calc_h": "🎯 Regional Savings Calculator",
        "select": "Select a Country to Audit:",
        "metric_l": "Potential Recovery",
        "comp_h": "📉 Friction Benchmark: EU vs. Japan (2025)",
        "comp_txt": "Japan (Suica) operates at €50 friction/year. EU averages €1,020. Recovery: €970/person.",
        "chip_h": "🔒 e-link-u: Triple-Sector Sovereign Architecture",
        "chip_info": "Antenna is physically locked until a live fingerprint is detected.",
        "s1_t": "🟢 Finance", "s1_p": "Offline C2C Economy. Trade continues during outages.",
        "s2_t": "🔴 Health", "s2_p": "Critical medical history accessible via Card offline.",
        "s3_t": "🔵 Identity", "s3_p": "SSI Master-Key for eIDAS 2.0 / DIDs.",
        "roadmap_h": "🗺️ Implementation Roadmap",
        "r1_t": "📍 Phase 1: Rural", "r1_d": "Smart Cards for low-connectivity areas.",
        "r2_t": "🚄 Phase 2: Corridors", "r2_d": "Hybrid deployment for Madrid-Paris-Berlin.",
        "r3_t": "🌐 Phase 3: Universal", "r3_d": "Total EU integration and €459B recovery.",
        "legal": "⚠️ Legal: Proprietary assets of Lia Ariadna Ruiz Ben. GDPR/EUDI.",
        "meth": "Data Methodology (2025 Sources)"
    },
    "Español": {
        "title": "📊 E-Link-U: Panel de Recuperación Regional",
        "subtitle": "Recuperando los 459.000 M€ de fricción (Auditoría 2025)",
        "calc_h": "🎯 Calculadora de Ahorro Regional",
        "select": "Seleccione un país para auditar:",
        "metric_l": "Recuperación Potencial",
        "comp_h": "📉 Benchmark de Fricción: UE vs. Japón (2025)",
        "comp_txt": "Japón opera con 50€/año; la UE con 1.020€. E-Link-U recupera esos 970€/persona.",
        "chip_h": "🔒 e-link-u: Arquitectura Soberana de Triple Sector",
        "chip_info": "La antena NFC está bloqueada físicamente hasta detectar huella viva.",
        "s1_t": "🟢 Finanzas", "s1_p": "Economía C2C Offline. Comercio sin interrupciones.",
        "s2_t": "🔴 Salud", "s2_p": "Historial médico portátil para emergencias offline.",
        "s3_t": "🔵 Identidad", "s3_p": "Llave Maestra SSI para eIDAS 2.0 / DIDs.",
        "roadmap_h": "🗺️ Hoja de Ruta de Implementación",
        "r1_t": "📍 Fase 1: Rural", "r1_d": "Tarjetas inteligentes para zonas de baja conectividad.",
        "r2_t": "🚄 Fase 2: Corredores", "r2_d": "Despliegue híbrido para Madrid-París-Berlín.",
        "r3_t": "🌐 Fase 3: Universal", "r3_d": "Integración total UE y recuperación de 459B€.",
        "legal": "⚠️ Aviso Legal: Activos de Lia Ariadna Ruiz Ben. RGPD/EUDI.",
        "meth": "Metodología de Datos (Fuentes 2025)"
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

        # --- CALCULADORA Y BENCHMARK ---
        st.header(text["calc_h"])
        c_calc, c_bench = st.columns(2)
        with c_calc:
            country_selected = st.selectbox(text["select"], df['country_name'].unique())
            country_data = df[df['country_name'] == country_selected].iloc[0]
            st.metric(label=f"{text['metric_l']} ({country_selected})", 
                      value=f"€{country_data['rural_recovery_potential']:.2f} B")
        with c_bench:
            st.subheader(text["comp_h"])
            st.write(text["comp_txt"])
            st.progress(5/100, text="Japan (Suica): €50")
            st.progress(100/100, text="European Union: €1,020")

        st.divider()
        st.bar_chart(data=df, x='country_name', y=['annual_loss_billion', 'rural_recovery_potential'], color=["#dc3545", "#28a745"])
        st.dataframe(df.style.background_gradient(cmap="Reds", subset=["annual_loss_billion"]), use_container_width=True)

        # --- CHIP VISUAL ---
        st.divider()
        st.header(text["chip_h"])
        st.info(f"💡 {text['chip_info']}")
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
        with r1: st.info(f"### {text['r1_t']}\n\n{text['r1_d']}")
        with r2: st.info(f"### {text['r2_t']}\n\n{text['r2_d']}")
        with r3: st.info(f"### {text['r3_t']}\n\n{text['r3_d']}")

        st.divider()
        st.warning(text["legal"])

    else:
        st.warning("Awaiting database sync...")

except Exception as e:
    st.error(f"Connection status: {e}")

# SIDEBAR (FUENTES Y GOBERNANZA)
with st.sidebar:
    st.subheader("Project Governance")
    st.write("👤 **Architect:** Lia Ariadna Ruiz Ben")
    st.write("🆔 **ORCID:** [0009-0006-2598-0625](https://orcid.org)")
    st.write("🔗 **DOI:** [10.5281/zenodo.19876558](https://zenodo.org)")
    st.divider()
    st.markdown(f"**{text['meth']}**")
    st.caption("• [Eurostat 2025 - Labor Costs](https://europa.eu)")
    st.caption("• [EC Single Market Report 2024/25](https://europa.eu)")
    st.caption("• [JR East Financial Report 2025](https://jreast.co.jp)")
    st.divider()
    st.info("E-Link-U OÜ (Estonia)")
    st.caption("© 2026 E-Link-U | Patent Pending | Licensed under CC BY-NC-ND 4.0")
