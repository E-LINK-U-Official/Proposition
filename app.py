import streamlit as st
import pandas as pd
from supabase import create_client

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="E-Link-U Strategy Dashboard", layout="wide", page_icon="🚄")

# Estilos CSS
st.markdown("""
    <style>
    .sector-card {
        padding: 20px; border-radius: 10px; border-left: 5px solid;
        background-color: #1e293b; margin-bottom: 10px; min-height: 220px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SELECTOR DE IDIOMA
with st.sidebar:
    st.title("🌐 Language / Idioma")
    lang = st.radio("Select Interface Language:", ("English", "Español"), index=0)
    st.divider()

# Mapeador de países para traducción dinámica
country_translation = {
    "Spain": "España", "Italy": "Italia", "France": "Francia",
    "Germany": "Alemania", "Portugal": "Portugal", "Belgium": "Bélgica",
    "Netherlands": "Países Bajos", "European Union": "Unión Europea"
}

# 3. DICCIONARIO MAESTRO (HÍBRIDO COMPLETO 2025)
text = {
    "English": {
        "title": "📊 E-Link-U: Regional Recovery Dashboard",
        "subtitle": "Recovering the €459B Friction Gap (2025 Audit Data)",
        "calc_h": "🎯 Regional Savings Calculator",
        "select": "Select a Country to Audit:",
        "metric_l": "Potential Recovery",
        "comp_h": "📉 Friction Benchmark: EU vs. Japan (2025)",
        "comp_txt": "Japan (Suica) operates at €50 friction/year. EU averages €1,020. Gap to recover: €970/person.",
        "table_h": "📋 Detailed Impact Data (Annual Loss in Billions)",
        "chip_h": "🔒 e-link-u: Triple-Sector Sovereign Architecture",
        "chip_info": "Antenna is physically locked until a live fingerprint is detected.",
        "s1_t": "🟢 Finance (Green)", "s1_p": "Offline C2C Economy. Trade continues during outages.",
        "s2_t": "🔴 Health (Red)", "s2_p": "Sovereign medical history via Card (ZKP).",
        "s3_t": "🔵 Identity (Blue)", "s3_p": "Self-Sovereign Identity. Offline Master-Key for eIDAS 2.0.",
        "pillar_h": "🛡️ Strategic Pillars: Privacy & Resilience",
        "p1_t": "Zero-Knowledge Privacy", "p1_d": "Verifying without exposing private data.",
        "p2_t": "Instant ROI", "p2_d": "Implementation costs recovered in 30 days.",
        "p3_t": "Hybrid Resilience", "p3_d": "Digital convenience + Biometric Physical Cards for blackouts.",
        "roadmap_h": "🗺️ Implementation Roadmap",
        "r1_t": "📍 Phase 1: Rural", "r1_d": "Focus: Seniors & Low-Connectivity.",
        "r2_t": "🚄 Phase 2: EU Corridors", "r2_d": "Focus: Cross-border Rail Identity.",
        "r3_t": "🌐 Phase 3: Total Interop", "r3_d": "Focus: Universal EU Citizenry.",
        "legal": "⚠️ Legal: Proprietary assets of Lia Ariadna Ruiz Ben. GDPR/EUDI.",
        "meth": "Verified 2025 Methodology",
        "col_c": "country_name"
    },
    "Español": {
        "title": "📊 E-Link-U: Panel de Recuperación Regional",
        "subtitle": "Recuperando los 459.000 M€ de fricción (Auditoría 2025)",
        "calc_h": "🎯 Calculadora de Ahorro Regional",
        "select": "Seleccione un país para auditar:",
        "metric_l": "Recuperación Potencial",
        "comp_h": "📉 Benchmark de Fricción: UE vs. Japón (2025)",
        "comp_txt": "Japón opera con 50€/año; la UE con 1.020€. Brecha a recuperar: 970€/persona.",
        "table_h": "📋 Datos de Impacto Detallados (Pérdida Anual en Billones)",
        "chip_h": "🔒 e-link-u: Arquitectura Soberana de Triple Sector",
        "chip_info": "Antena bloqueada físicamente hasta detectar huella viva.",
        "s1_t": "🟢 Finanzas (Verde)", "s1_p": "Economía C2C Offline y créditos energéticos.",
        "s2_t": "🔴 Salud (Rojo)", "s2_p": "Historial médico soberano portátil (ZKP).",
        "s3_t": "🔵 Identidad (Azul)", "s3_p": "Llave Maestra offline para eIDAS 2.0 / DIDs.",
        "pillar_h": "🛡️ Pilares Estratégicos: Privacidad y Resiliencia",
        "p1_t": "Privacidad Zero-Knowledge", "p1_d": "Verificación sin exponer datos privados (ZKP).",
        "p2_t": "ROI Instantáneo", "p2_d": "Costes amortizados en los primeros 30 días.",
        "p3_t": "Resiliencia Híbrida", "p3_d": "Interfaz Digital + Tarjeta Física para ciberataques.",
        "roadmap_h": "🗺️ Hoja de Ruta de Implementación",
        "r1_t": "📍 Fase 1: Rural", "r1_d": "Foco: Mayores y baja conectividad.",
        "r2_t": "🚄 Fase 2: Corredores UE", "r2_d": "Foco: Identidad ferroviaria transfronteriza.",
        "r3_t": "🌐 Fase 3: Universal", "r3_d": "Interoperabilidad total UE y recuperación de 459B€.",
        "legal": "⚠️ Aviso Legal: Activos propietarios de Lia Ariadna Ruiz Ben. RGPD/EUDI.",
        "meth": "Metodología Verificada 2025",
        "col_c": "Nombre del País"
    }
}[lang]

# 4. CONEXIÓN A BASE DE DATOS
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
    
    @st.cache_data(ttl=3600)
    def fetch_data():
        response = supabase.table("country_impact").select("*").execute()
        return pd.DataFrame(response.data)

    df_raw = fetch_data()

    if not df_raw.empty:
        df = df_raw.copy()
        if lang == "Español":
            df['country_name'] = df['country_name'].map(country_translation).fillna(df['country_name'])

        st.title(text["title"])
        st.markdown(f"### {text['subtitle']}")

        # --- CALCULADORA Y BENCHMARK ---
        st.header(text["calc_h"])
        c_calc, c_bench = st.columns(2)
        with c_calc:
            country_selected = st.selectbox(text["select"], df['country_name'].unique())
            country_data = df[df['country_name'] == country_selected].iloc
            st.metric(label=f"{text['metric_l']} ({country_selected})", 
                      value=f"€{country_data['rural_recovery_potential']:.2f} B")
        with c_bench:
            st.subheader(text["comp_h"])
            st.write(text["comp_txt"])
            st.progress(0.05, text="Japan (Suica): €50")
            st.progress(1.0, text="European Union: €1,020")

        st.divider()
        st.bar_chart(data=df, x='country_name', y=['annual_loss_billion', 'rural_recovery_potential'], color=["#dc3545", "#28a745"])
        
        st.subheader(text["table_h"])
        df_display = df.rename(columns={"country_name": text["col_c"]})
        st.dataframe(df_display.style.background_gradient(cmap="Reds", subset=["annual_loss_billion"]), use_container_width=True)

        # --- CHIP VISUAL ---
        st.divider()
        st.header(text["chip_h"])
        st.info(f"💡 {text['chip_info']}")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="sector-card" style="border-left-color: #28a745;"><h3 style="color: #28a745;">{text["s1_t"]}</h3><p>{text["s1_p"]}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="sector-card" style="border-left-color: #dc3545;"><h3 style="color: #dc3545;">{text["s2_t"]}</h3><p>{text["s2_p"]}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="sector-card" style="border-left-color: #007bff;"><h3 style="color: #007bff;">{text["s3_t"]}</h3><p>{text["s3_p"]}</p></div>', unsafe_allow_html=True)

        # --- PILARES ESTRATÉGICOS ---
        st.divider()
        st.header(text["pillar_h"])
        pa, pb, pc = st.columns(3)
        with pa: st.subheader(text["p1_t"]); st.write(text["p1_d"])
        with pb: st.subheader(text["p2_t"]); st.write(text["p2_d"])
        with pc: st.subheader(text["p3_t"]); st.write(text["p3_d"])

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
        st.warning("Awaiting sync...")

except Exception as e:
    st.error(f"Status: {e}")

# --- SIDEBAR (CON ENLACES ESPECÍFICOS VERIFICADOS) ---
with st.sidebar:
    st.subheader("Project Governance")
    st.write("👤 **Architect:** Lia Ariadna Ruiz Ben")
    st.write("🆔 **ORCID:** [0009-0006-2598-0625](https://orcid.org)")
    st.write("🔗 **DOI:** [10.5281/zenodo.19876558](https://zenodo.org)")
    st.divider()
    st.markdown(f"**{text['meth']}**")
    st.caption("• [Eurostat 2025 Labor Cost Analysis (€34.9/h)](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20260331-2)")
    st.caption("• [EC Competitiveness Report 2025](https://single-market-economy.ec.europa.eu/publications/2025-annual-single-market-and-competitiveness-report_en)")
    st.caption("• [JR East Integrated Report 2025 (PDF)](https://www.jreast.co.jp/eco/pdf/pdf_2025/all_e.pdf)")
    st.divider()
    st.info("E-Link-U OÜ (Estonia)")
    st.caption("© 2026 E-Link-U | Patent Pending | CC BY-NC-ND 4.0")
