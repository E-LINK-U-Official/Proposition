import streamlit as st
import pandas as pd
from supabase import create_client

# 1. SETUP & UI 
st.set_page_config(page_title="E-Link-U Strategy", layout="wide", page_icon="🚄")
st.markdown("""<style>
    .sector-card {padding:20px; border-radius:10px; border-left:5px solid; background-color:#1e293b; margin-bottom:10px; min-height:220px;}
    .stMetric {background-color:#0e1117; padding:15px; border-radius:10px;}
</style>""", unsafe_allow_html=True)

# 2. SIDEBAR (IDIOMA + GOBERNANZA + FUENTES)
with st.sidebar:
    st.title("🌐 Menu")
    lang = st.radio("Language / Idioma", ("English", "Español"), horizontal=True)
    st.divider()
    st.subheader("Project Governance")
    st.write("👤 **Architect:** Lia Ariadna Ruiz Ben")
    # Enlaces corregidos y funcionales
    st.write("🆔 **ORCID:** [0009-0006-2598-0625](https://orcid.org/0009-0006-2598-0625)")
    st.write("🔗 **DOI:** [10.5281/zenodo.19876558](//doi.org/10.5281/zenodo.19876558)")
    st.divider()
    m_t = "Methodology 2025" if lang == "English" else "Metodología 2025"
    st.markdown(f"**{m_t}**")
    with st.sidebar:
    st.divider()
    
    # --- SECCIÓN DE FINANCIACIÓN PAYPAL ---
    titulo_pago = "Project Funding" if lang == "English" else "Financiación"
    # CAMBIA 'TU_USUARIO' por tu usuario real de PayPal.me (ej. LiaRuiz)
    mi_paypal = "https://paypal.me/LiaRB" 
    
    st.markdown(
        f"""
        <a href="https://paypal.com


{mi_paypal}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #0070ba; color: white; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; font-size: 14px;">
                { 'Contribute via PayPal' if lang == 'English' else 'Contribuir vía PayPal' }
            </div>
        </a>
        """, 
        unsafe_allow_html=True
    )
    
    st.divider()
    
    # Enlaces a fuentes oficiales 2025 corregidos
    st.caption("• [Eurostat 2025 Labor Costs (€34.9/h)]")
    st.caption("• [EC Single Market Report 2025](https://single-market-economy.ec.europa.eu/publications/2025-annual-single-market-and-competitiveness-report_en)")
    st.caption("• [JR East Financial Report 2025](https://www.jreast.co.jp/eco/pdf/pdf_2025/all_e.pdf)")
    st.divider()
    st.info("E-Link-U OÜ (Estonia) | Proprietary Architecture")
    st.caption("© 2026 E-Link-U | Patent Pending | CC BY-NC-ND 4.0")
    st.sidebar.divider()
st.sidebar.subheader("Support the Mission")

# 3. DICCIONARIO DE TEXTOS (COMPLETO)
c_map = {"Spain":"España","Italy":"Italia","France":"Francia","Germany":"Alemania","Portugal":"Portugal","Belgium":"Bélgica","Netherlands":"Países Bajos","European Union":"Unión Europea"}
T = {
    "English": {
        "title": "📊 E-Link-U: Regional Recovery Dashboard",
        "sub": "Recovering the €459B Friction Gap (2025 Audit)",
        "calc_h": "🎯 Regional Savings Calculator", "sel": "Select a Country to Audit:", "met": "Potential Recovery",
        "comp_h": "📉 Friction Benchmark: EU vs. Japan (2025)", 
        "comp_txt": "Japan (Suica) operates at €50 friction/year. EU averages €1,020. Recovery: €970/person.",
        "tab_h": "📋 Detailed Impact Data (Annual Loss in Billions)",
        "chip_h": "🔒 e-link-u: Triple-Sector Sovereign Architecture",
        "chip_i": "Antenna is physically locked until a live fingerprint is detected. No biometric data ever leaves the card.",
        "s1_t": "🟢 Finance Sector", "s1_p": "Offline C2C Economy. Trade continues during power outages or bank hacks. Energy credits and managed aids.",
        "s2_t": "🔴 Health Sector", "s2_p": "Critical health data accessible via Card during emergencies in remote areas with no signal.",
        "s3_t": "🔵 Identity Sector", "s3_p": "Self-Sovereign Identity. Offline Master-Key for border security and eIDAS 2.0 / DIDs integration.",
        "pillar_h": "🛡️ Strategic Pillars: Privacy & Resilience",
        "p1_t": "Zero-Knowledge Privacy", "p1_d": "Verifying eligibility without exposing private data. Sovereignty by design.",
        "p2_t": "Instant ROI", "p2_d": "Projected recovery of €459B/year. Implementation costs recovered in 30 days.",
        "p3_t": "Hybrid Resilience", "p3_d": "Digital convenience + Biometric Physical Cards for blackouts or zero-battery.",
        "roadmap_h": "🗺️ Implementation Roadmap",
        "r1_t": "📍 Phase 1: Rural Pilot", "r1_d": "**Focus:** Seniors & Low-Connectivity.\n\n**Action:** Smart Physical Cards as the primary sovereign tool.",
        "r2_t": "🚄 Phase 2: EU Corridors", "r2_d": "**Focus:** Mobile Workforce & Travelers.\n\n**Action:** Hybrid deployment (Digital + Card) for cross-border rail.",
        "r3_t": "🌐 Phase 3: Total Interop", "r3_d": "**Focus:** Universal EU Citizenry.\n\n**Action:** Full integration with the Physical Card as the permanent offline 'Anchor'.",
        "leg": "⚠️ Legal: Proprietary assets of Lia Ariadna Ruiz Ben. GDPR & EUDI compliant.", "col": "country_name"
    },
    "Español": {
        "title": "📊 E-Link-U: Panel de Recuperación Regional",
        "sub": "Recuperando los 459.000 M€ de brecha de fricción (Auditoría 2025)",
        "calc_h": "🎯 Calculadora de Ahorro Regional", "sel": "Seleccione un país para auditar:", "met": "Recuperación Potencial",
        "comp_h": "📉 Benchmark de Fricción: UE vs. Japón (2025)", 
        "comp_txt": "Japón opera con 50€/año; la UE promedia 1.020€. E-Link-U recupera esos 970€ de diferencia.",
        "tab_h": "📋 Datos de Impacto Detallados (Pérdida Anual en Billones)",
        "chip_h": "🔒 e-link-u: Arquitectura Soberana de Triple Sector",
        "chip_i": "La antena está bloqueada físicamente hasta detectar huella viva. Ningún dato biométrico sale de la tarjeta.",
        "s1_t": "🟢 Sector Finanzas", "s1_p": "Economía C2C Offline. El comercio sigue durante apagones o hackeos. Créditos energéticos y ayudas.",
        "s2_t": "🔴 Sector Salud", "s2_p": "Datos médicos críticos accesibles por tarjeta en emergencias o zonas sin señal de red.",
        "s3_t": "🔵 Sector Identidad", "s3_p": "Identidad Autosoberana. Llave Maestra offline para seguridad fronteriza e integración eIDAS 2.0.",
        "pillar_h": "🛡️ Pilares Estratégicos: Privacidad y Resiliencia",
        "p1_t": "Privacidad Zero-Knowledge", "p1_d": "Verificación sin exponer datos privados. Soberanía ZKP por diseño.",
        "p2_t": "ROI Instantáneo", "p2_d": "Recuperación de 459B€/año. Costes amortizados en los primeros 30 días.",
        "p3_t": "Resiliencia Híbrida", "p3_d": "Interfaz Digital + Tarjeta Física Biométrica para apagones o ataques cibernéticos.",
        "roadmap_h": "🗺️ Hoja de Ruta de Implementación",
        "r1_t": "📍 Fase 1: Piloto Rural", "r1_d": "**Foco:** Mayores y Baja Conectividad.\n\n**Acción:** Tarjeta Física como herramienta soberana primaria.",
        "r2_t": "🚄 Fase 2: Corredores UE", "r2_d": "**Foco:** Trabajadores Móviles.\n\n**Acción:** Despliegue híbrido para identidad ferroviaria fronteriza.",
        "r3_t": "🌐 Fase 3: Interop Total", "r3_d": "**Foco:** Ciudadanía Universal UE.\n\n**Acción:** Integración total con la Tarjeta Física como 'Ancla' offline.",
        "leg": "⚠️ Aviso Legal: Activos de Lia Ariadna Ruiz Ben. Conforme a RGPD y EUDI.", "col": "Nombre del País"
    }
}[lang]

# 4. DATA & CORE LOGIC
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    @st.cache_data(ttl=3600)
    def get_data(): return pd.DataFrame(supabase.table("country_impact").select("*").execute().data)
    df_raw = get_data()

    if not df_raw.empty:
        df = df_raw.copy()
        if lang == "Español": df['country_name'] = df['country_name'].map(c_map).fillna(df['country_name'])
        
        st.title(T["title"])
        st.markdown(f"### {T['sub']}")

        # --- CALCULADORA & BENCHMARK ---
        col_c, col_b = st.columns(2)
        with col_c:
            st.header(T["calc_h"])
            sel = st.selectbox(T["sel"], df['country_name'].unique())
            # CORRECCIÓN ILOC: Se añade .iloc[0] para extraer la fila correctamente
            data = df[df['country_name'] == sel].iloc[0]
            st.metric(label=f"{T['met']} ({sel})", value=f"€{data['rural_recovery_potential']:.2f} B")
        with col_b:
            st.subheader(T["comp_h"])
            st.write(T["comp_txt"])
            st.progress(0.05, text="Japan (Suica): €50")
            st.progress(1.0, text="European Union: €1,020")

        st.divider()
        st.bar_chart(df, x='country_name', y=['annual_loss_billion', 'rural_recovery_potential'], color=["#dc3545", "#28a745"])
        
        st.subheader(T["tab_h"])
        st.dataframe(df.rename(columns={"country_name":T["col"]}).style.background_gradient(cmap="Reds", subset=["annual_loss_billion"]), use_container_width=True)

        # --- TRIPLE SECTOR ---
        st.divider()
        st.header(T["chip_h"])
        st.info(f"💡 {T['chip_i']}")
        sc1, sc2, sc3 = st.columns(3)
        with sc1: st.markdown(f'<div class="sector-card" style="border-left-color: #28a745;"><h3 style="color:#28a745;">{T["s1_t"]}</h3><p>{T["s1_p"]}</p></div>', unsafe_allow_html=True)
        with sc2: st.markdown(f'<div class="sector-card" style="border-left-color: #dc3545;"><h3 style="color:#dc3545;">{T["s2_t"]}</h3><p>{T["s2_p"]}</p></div>', unsafe_allow_html=True)
        with sc3: st.markdown(f'<div class="sector-card" style="border-left-color: #007bff;"><h3 style="color:#007bff;">{T["s3_t"]}</h3><p>{T["s3_p"]}</p></div>', unsafe_allow_html=True)

        # --- PILARES ---
        st.divider()
        st.header(T["pillar_h"])
        pa, pb, pc = st.columns(3)
        with pa: st.subheader(T["p1_t"]); st.write(T["p1_d"])
        with pb: st.subheader(T["p2_t"]); st.write(T["p2_d"])
        with pc: st.subheader(T["p3_t"]); st.write(T["p3_d"])

        # --- ROADMAP ---
        st.divider()
        st.header(T["roadmap_h"])
        r1, r2, r3 = st.columns(3)
        with r1: st.info(f"### {T['r1_t']}\n\n{T['r1_d']}")
        with r2: st.info(f"### {T['r2_t']}\n\n{T['r2_d']}")
        with r3: st.info(f"### {T['r3_t']}\n\n{T['r3_d']}")

        st.divider()
        st.warning(T["leg"])
except Exception as e: st.error(f"System status: {e}")
