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
        background-color: #0e1117; margin-bottom: 10px; min-height: 200px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Selector de Idioma en el Sidebar
with st.sidebar:
    st.title("🌐 Language / Idioma")
    lang = st.radio("Select Interface Language:", ("English", "Español"), index=0)
    st.divider()

# Diccionario Maestro (Híbrido Completo)
text = {
    "English": {
        "title": "📊 E-Link-U: Regional Recovery Dashboard",
        "subtitle": "Recovering the €459B Friction Gap in European Infrastructure",
        "calc_h": "🎯 Regional Savings Calculator",
        "select": "Select a Country to Audit:",
        "metric_l": "Potential Recovery",
        "comp_h": "📉 Friction Benchmark: EU vs. Japan",
        "comp_txt": "Japan (Suica) operates at €50 friction/year, while the EU averages €1,020. E-Link-U recovers that €970 gap.",
        "table_h": "📋 Detailed Impact Data (Annual Loss in Billions)",
        "chip_h": "🔒 e-link-u: Triple-Sector Sovereign Architecture",
        "chip_info": "Antenna is physically locked until a live fingerprint is detected. No biometric data ever leaves the card.",
        "s1_t": "🟢 Finance Sector", "s1_p": "Offline C2C Economy. Trade continues during power outages.",
        "s2_t": "🔴 Health Sector", "s2_p": "Critical health data accessible via Card during emergencies.",
        "s3_t": "🔵 Identity Sector", "s3_p": "Self-Sovereign Identity. Offline Master-Key for eIDAS 2.0.",
        "pillar_h": "🛡️ Strategic Pillars: Privacy & Resilience",
        "p1_t": "Zero-Knowledge Privacy", "p1_d": "Verifying eligibility without exposing private data. Sovereignty by design.",
        "p2_t": "Instant ROI", "p2_d": "Projected recovery of €459B/year. Costs recovered in 30 days.",
        "p3_t": "Hybrid Resilience", "p3_d": "Digital convenience + Biometric Physical Cards for blackouts.",
        "roadmap_h": "🗺️ Implementation Roadmap (Hoja de Ruta)",
        "r1_t": "📍 Phase 1: Rural Pilot", "r1_d": "Focus: Seniors & Low-Connectivity. Smart Physical Cards as primary tool.",
        "r2_t": "🚄 Phase 2: EU Corridors", "r2_d": "Focus: Mobile Workforce. Hybrid deployment for cross-border rail.",
        "r3_t": "🌐 Phase 3: Total Interop", "r3_d": "Focus: Universal EU Citizenry. Card as permanent offline 'Anchor'.",
        "legal": "⚠️ Legal Disclaimer: Proprietary assets of Lia Ariadna Ruiz Ben. Conforms to GDPR/EUDI."
    },
    "Español": {
        "title": "📊 E-Link-U: Panel de Recuperación Regional",
        "subtitle": "Recuperando los 459.000 M€ de brecha de fricción europea",
        "calc_h": "🎯 Calculadora de Ahorro Regional",
        "select": "Seleccione un país para auditar:",
        "metric_l": "Recuperación Potencial",
        "comp_h": "📉 Benchmark de Fricción: UE vs. Japón",
        "comp_txt": "Japón promedia 50€ de fricción/año; la UE 1.020€. E-Link-U recupera esos 970€ de diferencia.",
        "table_h": "📋 Datos de Impacto Detallados (Pérdida Anual en Billones)",
        "chip_h": "🔒 e-link-u: Arquitectura Soberana de Triple Sector",
        "chip_info": "La antena está bloqueada físicamente hasta detectar huella dactilar viva.",
        "s1_t": "🟢 Sector Finanzas", "s1_p": "Economía C2C Offline. El comercio sigue durante apagones.",
        "s2_t": "🔴 Sector Salud", "s2_p": "Datos médicos accesibles por tarjeta en emergencias.",
        "s3_t": "🔵 Sector Identidad", "s3_p": "Identidad Autosoberana. Llave Maestra para eIDAS 2.0.",
        "pillar_h": "🛡️ Pilares Estratégicos: Privacidad y Resiliencia",
        "p1_t": "Privacidad Zero-Knowledge", "p1_d": "Verificación sin exponer datos privados. Soberanía ZKP.",
        "p2_t": "ROI Instantáneo", "p2_d": "Recuperación de 459B€/año. Costes amortizados en 30 días.",
        "p3_t": "Resiliencia Híbrida", "p3_d": "Digital + Tarjeta Física Biométrica para ciberataques.",
        "roadmap_h": "🗺️ Hoja de Ruta de Implementación",
        "r1_t": "📍 Fase 1: Piloto Rural", "r1_d": "Foco: Mayores y Baja Conectividad. Tarjeta Física como herramienta primaria.",
        "r2_t": "🚄 Fase 2: Corredores UE", "r2_d": "Foco: Trabajadores Móviles. Despliegue híbrido para trenes fronterizos.",
        "r3_t": "🌐 Fase 3: Interop Total", "r3_d": "Foco: Ciudadanía Universal UE. La tarjeta como 'Ancla' offline.",
        "legal": "⚠️ Aviso Legal: Activos propietarios de Lia Ariadna Ruiz Ben. Conforme a RGPD/EUDI."
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
        col_calc, col_bench = st.columns(2)
        with col_calc:
            country_selected = st.selectbox(text["select"], df['country_name'].unique())
            country_data = df[df['country_name'] == country_selected].iloc[0]
            st.metric(label=f"{text['metric_l']} ({country_selected})", 
                      value=f"€{country_data['rural_recovery_potential']:.2f} B")
        with col_bench:
            st.subheader(text["comp_h"])
            st.write(text["comp_txt"])
            st.progress(5/100, text="Japan: €50")
            st.progress(100/100, text="EU: €1,020")

        st.divider()
        st.bar_chart(data=df, x='country_name', y=['annual_loss_billion', 'rural_recovery_potential'], color=["#dc3545", "#28a745"])

        # --- TABLA CON DEGRADADO ---
        st.subheader(text["table_h"])
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

        # --- PILARES ESTRATÉGICOS ---
        st.divider()
        st.header(text["pillar_h"])
        pa, pb, pc = st.columns(3)
        with pa:
            st.subheader(text["p1_t"]); st.write(text["p1_d"])
        with pb:
            st.subheader(text["p2_t"]); st.write(text["p2_d"])
        with pc:
            st.subheader(text["p3_t"]); st.write(text["p3_d"])

        # --- ROADMAP (RESTAURADO) ---
        st.divider()
        st.header(text["roadmap_h"])
        r1, r2, r3 = st.columns(3)
        with r1:
            st.info(f"### {text['r1_t']}\n\n{text['r1_d']}")
        with r2:
            st.info(f"### {text['r2_t']}\n\n{text['r2_d']}")
        with r3:
            st.info(f"### {text['r3_t']}\n\n{text['r3_d']}")

        # --- AVISO LEGAL ---
        st.divider()
        st.warning(text["legal"])

    else:
        st.warning("Awaiting sync...")

except Exception as e:
    st.error(f"Status: {e}")

# SIDEBAR
with st.sidebar:
    st.subheader("Project Governance")
    st.write("👤 **Architect:** Lia Ariadna Ruiz Ben")
    st.write("🔗 DOI: [10.5281/zenodo.19876558](https://zenodo.org)")
    st.divider()
    st.info("E-Link-U OÜ (Estonia)")
    st.caption("© 2026 E-Link-U | Patent Pending")
