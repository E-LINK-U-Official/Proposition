import streamlit as st
import pandas as pd
from supabase import create_client

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="E-Link-U Strategy Dashboard", layout="wide", page_icon="🚄")

# Estilos CSS para el Chip y la interfaz
st.markdown("""
    <style>
    .sector-card {
        padding: 20px; border-radius: 10px; border-left: 5px solid;
        background-color: #1e293b; margin-bottom: 10px; min-height: 220px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SELECTOR DE IDIOMA EN EL SIDEBAR
with st.sidebar:
    st.title("🌐 Language / Idioma")
    lang = st.radio("Select Interface Language:", ("English", "Español"), index=0)
    st.divider()

# Diccionario de Traducción de Países (Extraídos de Supabase)
country_translation = {
    "Spain": "España",
    "Italy": "Italia",
    "France": "Francia",
    "Germany": "Alemania",
    "Portugal": "Portugal",
    "Belgium": "Bélgica",
    "Netherlands": "Países Bajos",
    "European Union": "Unión Europea"
}

# 3. DICCIONARIO MAESTRO DE TEXTOS (HÍBRIDO FINAL)
text = {
    "English": {
        "title": "📊 E-Link-U: Regional Recovery Dashboard",
        "subtitle": "Recovering the €459B Friction Gap in European Infrastructure (2025 Audit Data)",
        "calc_h": "🎯 Regional Savings Calculator",
        "select": "Select a Country to Audit:",
        "metric_l": "Potential Recovery",
        "comp_h": "📉 Friction Benchmark: EU vs. Japan (2025)",
        "comp_txt": "Japan (Suica) operates at €50 friction/year, while the EU averages €1,020. E-Link-U targets that €970 gap.",
        "table_h": "📋 Detailed Impact Data (Annual Loss in Billions)",
        "chip_h": "🔒 e-link-u: Triple-Sector Sovereign Architecture",
        "chip_info": "Antenna is physically locked until a live fingerprint is detected. No biometric data ever leaves the card.",
        "s1_t": "🟢 Finance (Green)", "s1_p": "Offline C2C Economy. Trade continues during power outages or bank hacks.",
        "s2_t": "🔴 Health (Red)", "s2_p": "Critical health data accessible via Card during emergencies in remote areas.",
        "s3_t": "🔵 Identity (Blue)", "s3_p": "Self-Sovereign Identity. Offline Master-Key for border security & eIDAS 2.0.",
        "pillar_h": "🛡️ Strategic Pillars: Privacy & Resilience",
        "p1_t": "Zero-Knowledge Privacy", "p1_d": "Verifying eligibility without exposing private data. Sovereignty by design.",
        "p2_t": "Instant ROI", "p2_d": "Projected recovery of €459B/year. Implementation costs recovered in 30 days.",
        "p3_t": "Hybrid Resilience", "p3_d": "Digital convenience + Biometric Physical Cards for blackouts or zero-battery.",
        "roadmap_h": "🗺️ Implementation Roadmap",
        "r1_t": "📍 Phase 1: Rural Pilot", "r1_d": "Focus: Seniors & Low-Connectivity. Smart Physical Cards as primary tool.",
        "r2_t": "🚄 Phase 2: EU Corridors", "r2_d": "Focus: Mobile Workforce. Hybrid deployment for cross-border rail identity.",
        "r3_t": "🌐 Phase 3: Total Interop", "r3_d": "Focus: Universal EU Citizenry. Card as permanent offline 'Anchor'.",
        "legal_h": "⚠️ Legal Disclaimer & Sovereignty Notice",
        "legal_d": "The e-link-u architecture and the Umatter protocol are proprietary assets of Lia Ariadna Ruiz Ben. Aligned with GDPR and EUDI standards.",
        "meth": "Verified 2025 Methodology",
        "col_country": "country_name"
    },
    "Español": {
        "title": "📊 E-Link-U: Panel de Recuperación Regional",
        "subtitle": "Recuperando los 459.000 M€ de brecha de fricción europea (Datos 2025)",
        "calc_h": "🎯 Calculadora de Ahorro Regional",
        "select": "Seleccione un país para auditar:",
        "metric_l": "Recuperación Potencial",
        "comp_h": "📉 Benchmark de Fricción: UE vs. Japón (2025)",
        "comp_txt": "Japón (Suica) opera con 50€/año; la UE promedia 1.020€. E-Link-U recupera esos 970€ de diferencia.",
        "table_h": "📋 Datos de Impacto Detallados (Pérdida Anual en Billones)",
        "chip_h": "🔒 e-link-u: Arquitectura Soberana de Triple Sector",
        "chip_info": "La antena está bloqueada físicamente hasta detectar huella viva. Los datos biométricos no salen de la tarjeta.",
        "s1_t": "🟢 Finanzas (Verde)", "s1_p": "Economía C2C Offline. El comercio sigue durante apagones o hackeos bancarios.",
        "s2_t": "🔴 Salud (Rojo)", "s2_p": "Datos médicos accesibles por tarjeta en emergencias o zonas sin señal.",
        "s3_t": "🔵 Identidad (Azul)", "s3_p": "Identidad Autosoberana. Llave Maestra offline para eIDAS 2.0 y DIDs.",
        "pillar_h": "🛡️ Pilares Estratégicos: Privacidad y Resiliencia",
        "p1_t": "Privacidad Zero-Knowledge", "p1_d": "Verificación sin exponer datos privados. Soberanía ZKP por diseño.",
        "p2_t": "ROI Instantáneo", "p2_d": "Recuperación de 459B€/año. Costes amortizados en los primeros 30 días.",
        "p3_t": "Resiliencia Híbrida", "p3_d": "Interfaz Digital + Tarjeta Física Biométrica para apagones o ciberataques.",
        "roadmap_h": "🗺️ Hoja de Ruta de Implementación",
        "r1_t": "📍 Fase 1: Piloto Rural", "r1_d": "Foco: Mayores y Baja Conectividad. Tarjeta Física como herramienta primaria.",
        "r2_t": "🚄 Fase 2: Corredores UE", "r2_d": "Foco: Trabajadores Móviles. Despliegue híbrido para trenes fronterizos.",
        "r3_t": "🌐 Fase 3: Interop Total", "r3_d": "Foco: Ciudadanía Universal UE. La tarjeta como 'Ancla' offline permanente.",
        "legal_h": "⚠️ Aviso Legal y de Soberanía",
        "legal_d": "Activos propietarios de Lia Ariadna Ruiz Ben. Conforme a RGPD y estándares EUDI.",
        "meth": "Metodología Verificada 2025",
        "col_country": "País"
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
        # TRADUCCIÓN DINÁMICA DE LA TABLA
        df = df_raw.copy()
        if lang == "Español":
            df['country_name'] = df['country_name'].map(country_translation).fillna(df['country_name'])

        st.title(text["title"])
        st.markdown(f"### {text['subtitle']}")

        # --- SECCIÓN 1: CALCULADORA Y BENCHMARK ---
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
            st.progress(0.05, text="Japan (Suica): €50")
            st.progress(1.0, text="European Union: €1,020")

        st.divider()
        st.bar_chart(data=df, x='country_name', y=['annual_loss_billion', 'rural_recovery_potential'], color=["#dc3545", "#28a745"])

        # --- SECCIÓN 2: TABLA CON DEGRADADO ---
        st.subheader(text["table_h"])
        df_display = df.rename(columns={"country_name": text["col_country"]})
        st.dataframe(df_display.style.background_gradient(cmap="Reds", subset=["annual_loss_billion"]), use_container_width=True)

        # --- SECCIÓN 3: CHIP VISUAL ---
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

        # --- SECCIÓN 4: PILARES ---
        st.divider()
        st.header(text["pillar_h"])
        pa, pb, pc = st.columns(3)
        with pa: st.subheader(text["p1_t"]); st.write(text["p1_d"])
        with pb: st.subheader(text["p2_t"]); st.write(text["p2_d"])
        with pc: st.subheader(text["p3_t"]); st.write(text["p3_d"])

        # --- SECCIÓN 5: ROADMAP ---
        st.divider()
        st.header(text["roadmap_h"])
        r1, r2, r3 = st.columns(3)
        with r1: st.info(f"### {text['r1_t']}\n\n{text['r1_d']}")
        with r2: st.info(f"### {text['r2_t']}\n\n{text['r2_d']}")
        with r3: st.info(f"### {text['r3_t']}\n\n{text['r3_d']}")

        # --- SECCIÓN 6: AVISO LEGAL ---
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

# --- SIDEBAR: GOBERNANZA Y FUENTES 2025 ---
with st.sidebar:
    st.subheader("Project Governance")
    st.write("👤 **Architect:** Lia Ariadna Ruiz Ben")
    st.write("🆔 **ORCID:** [0009-0006-2598-0625](https://orcid.org)")
    st.write("🔗 **DOI:** [10.5281/zenodo.19876558](https://zenodo.org)")
    st.divider()
    st.markdown(f"**{text['meth']}**")
    st.caption("• [Eurostat 2025 Labor Costs: €34.9/h](https://europa.eu)")
    st.caption("• [EC Single Market & Competitiveness Report 2025](https://europa.eu)")
    st.caption("• [JR East Financial Integrated Report 2025](https://jreast.co.jp)")
    st.divider()
    st.info("E-Link-U OÜ (Estonia) | Proprietary Architecture")
    st.caption("© 2026 E-Link-U | Patent Pending | Licensed under CC BY-NC-ND 4.0")
