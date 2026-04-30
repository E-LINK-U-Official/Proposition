import streamlit as st
import pandas as pd
from supabase import create_client

# 1. Configuración de página
st.set_page_config(page_title="E-Link-U Strategy Dashboard", layout="wide", page_icon="🚄")

# Estilos visuales para los Sectores del Chip
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

# Diccionario Maestro (Híbrido Total y Definitivo)
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
        "s1_t": "🟢 Finance (Green)", "s1_p": "Offline C2C Economy. Trade continues during power outages or bank hacks.",
        "s2_t": "🔴 Health (Red)", "s2_p": "Critical health data accessible via Card during emergencies or remote areas.",
        "s3_t": "🔵 Identity (Blue)", "s3_p": "Self-Sovereign Identity. Offline Master-Key for border security & eIDAS 2.0.",
        "pillar_h": "🛡️ Strategic Pillars: Privacy & Resilience",
        "p1_t": "Zero-Knowledge Privacy", "p1_d": "Verifying eligibility without exposing private data. Sovereignty by design.",
        "p2_t": "Instant ROI", "p2_d": "Projected recovery of €459B/year. Costs recovered in 30 days.",
        "p3_t": "Hybrid Resilience", "p3_d": "Digital Interface + Biometric Physical Cards for blackouts or zero-battery.",
        "roadmap_h": "🗺️ Implementation Roadmap",
        "r1_t": "📍 Phase 1: Rural Pilot", "r1_d": "Focus: Seniors & Low-Connectivity. Smart Physical Cards as primary tool.",
        "r2_t": "🚄 Phase 2: EU Corridors", "r2_d": "Focus: Mobile Workforce. Hybrid deployment for cross-border rail identity.",
        "r3_t": "🌐 Phase 3: Total Interop", "r3_d": "Focus: Universal EU Citizenry. Card as permanent offline 'Anchor'.",
        "legal_h": "⚠️ Legal Disclaimer & Sovereignty Notice",
        "legal_d": "The e-link-u architecture and the Umatter protocol are proprietary assets of Lia Ariadna Ruiz Ben. Conforms to GDPR and EUDI standards."
    },
    "Español": {
        "title": "📊 E-Link-U: Panel de Recuperación Regional",
        "subtitle": "Recuperando los 459.000 M€ de brecha de fricción europea",
        "calc_h": "🎯 Calculadora de Ahorro Regional",
        "select": "Seleccione un país para auditar:",
        "metric_l": "Recuperación Potencial",
        "comp_h": "📉 Benchmark de Fricción: UE vs. Japón",
        "comp_txt": "Japón opera con 50€ de fricción/año; la UE promedia 1.020€. E-Link-U recupera esos 970€ de diferencia.",
        "table_h": "📋 Datos de Impacto Detallados (Pérdida Anual en Billones)",
        "chip_h": "🔒 e-link-u: Arquitectura Soberana de Triple Sector",
        "chip_info": "Antenna bloqueada físicamente hasta detectar huella viva. Ningún dato biométrico sale de la tarjeta.",
        "s1_t": "🟢 Finanzas (Verde)", "s1_p": "Economía C2C Offline. El comercio sigue durante apagones o hackeos.",
        "s2_t": "🔴 Salud (Rojo)", "s2_p": "Datos médicos accesibles por tarjeta en emergencias o zonas sin señal.",
        "s3_t": "🔵 Identidad (Azul)", "s3_p": "Identidad Autosoberana. Llave Maestra offline para eIDAS 2.0.",
        "pillar_h": "🛡️ Pilares Estratégicos: Privacidad y Resiliencia",
        "p1_t": "Privacidad Zero-Knowledge", "p1_d": "Verificación sin exponer datos privados. Soberanía ZKP.",
        "p2_t": "ROI Instantáneo", "p2_d": "Recuperación de 459B€/año. Costes amortizados en 30 días.",
        "p3_t": "Resiliencia Híbrida", "p3_d": "Interfaz Digital + Tarjeta Física para apagones o ataques cibernéticos.",
        "roadmap_h": "🗺️ Hoja de Ruta de Implementación",
        "r1_t": "📍 Fase 1: Piloto Rural", "r1_d": "Foco: Mayores y Baja Conectividad. Tarjeta Física como herramienta primaria.",
        "r2_t": "🚄 Fase 2: Corredores UE", "r2_d": "Foco: Trabajadores Móviles. Despliegue híbrido para trenes fronterizos.",
        "r3_t": "🌐 Fase 3: Interop Total", "r3_d": "Foco: Ciudadanía Universal UE. La tarjeta como 'Ancla' offline.",
        "legal_h": "⚠️ Aviso Legal y de Soberanía",
        "legal_d": "La arquitectura e-link-u y el protocolo Umatter son activos propietarios de Lia Ariadna Ruiz Ben. Conforme a RGPD/EUDI."
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
            st.progress(5/100, text="Japan (Suica): €50")
            st.progress(100/100, text="European Union: €1,020")

        st.divider()
        st.bar_chart(data=df, x='country_name', y=['annual_loss_billion', 'rural_recovery_potential'], color=["#dc3545", "#28a745"])

        # --- TABLA CON DEGRADADO REDS ---
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

        # --- ROADMAP ---
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
        st.markdown(f"""
            <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #f1c40f;">
                <p style="color: #f1c40f; font-weight: bold; margin-bottom: 5px;">{text['legal_h']}</p>
                <p style="color: white; font-size: 0.9em;">{text['legal_d']}</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.warning("Awaiting database sync...")

except Exception as e:
    st.error(f"System connection status: {e}")

# SIDEBAR (RESTAURADO COMPLETO)
with st.sidebar:
    st.subheader("Project Governance")
    st.write("👤 **Architect:** Lia Ariadna Ruiz Ben")
    st.write("🆔 **ORCID:** [0009-0006-2598-0625](https://orcid.org)")
    st.write("🔗 **DOI:** [10.5281/zenodo.19876558](https://zenodo.org)")
    st.divider()
    st.info("E-Link-U OÜ (Estonia) | Proprietary Architecture")
    st.caption("© 2026 E-Link-U | Patent Pending | Licensed under CC BY-NC-ND 4.0")
