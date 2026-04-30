import streamlit as st
import pandas as pd
from supabase import create_client

# 1. SETUP & COMPACT UI
st.set_page_config(page_title="E-Link-U Strategy", layout="wide", page_icon="🚄")
st.markdown("""<style>
    .sector-card {padding:15px; border-radius:8px; border-left:5px solid; background-color:#1e293b; margin-bottom:8px; font-size:0.9em;}
    .stMetric {background-color:#0e1117; padding:10px; border-radius:10px;}
    section[data-testid="stSidebar"] {width: 250px !important;}
</style>""", unsafe_allow_html=True)

# 2. SIDEBAR (IDIOMA + GOBERNANZA)
with st.sidebar:
    lang = st.radio("Language / Idioma", ("English", "Español"), horizontal=True)
    st.divider()
    st.caption("👤 **Architect:** Lia Ariadna Ruiz Ben")
    st.caption("🆔 **ORCID:** [0009-0006-2598-0625](https://orcid.org)")
    st.caption("🔗 **DOI:** [10.5281/zenodo.19876558](https://zenodo.org)")
    st.divider()
    m_t = "Methodology 2025" if lang == "English" else "Metodología 2025"
    st.markdown(f"**{m_t}**")
    st.caption("• [Eurostat 2025 (€34.9/h)](https://europa.eu)")
    st.caption("• [EC Competitiveness 2025](https://europa.eu)")
    st.caption("• [JR East Report 2025](https://jreast.co.jp)")
    st.divider()
    st.info("E-Link-U OÜ (Estonia) | Patent Pending")
    st.caption("© 2026 | CC BY-NC-ND 4.0")

# 3. TRADUCCIÓN DINÁMICA
c_map = {"Spain":"España","Italy":"Italia","France":"Francia","Germany":"Alemania","Portugal":"Portugal","Belgium":"Bélgica","Netherlands":"Países Bajos","European Union":"Unión Europea"}
T = {
    "English": {
        "title": "📊 E-Link-U: Regional Recovery (2025 Audit)",
        "sub": "Recovering the €459B Friction Gap in EU Infrastructure",
        "calc": "🎯 Savings Calculator", "sel": "Select Country:", "met": "Potential Recovery",
        "bench": "📉 Benchmark: EU vs Japan", "b_txt": "Gap to recover: €970/person (EU €1,020 vs JP €50)",
        "tab": "📋 Detailed Impact (Billions)", "chip": "🔒 Triple-Sector Sovereign Architecture",
        "chip_i": "Antenna physically locked until live fingerprint detected.",
        "s1": "🟢 Finance: Offline C2C & Energy.", "s2": "🔴 Health: Portable ZKP History.", "s3": "🔵 Legal: SSI/eIDAS 2.0 Identity.",
        "pil": "🛡️ Strategic Pillars", "p1": "Zero-Knowledge Privacy", "p2": "Instant ROI (30 days)", "p3": "Hybrid Resilience",
        "map": "🗺️ Roadmap", "r1": "📍 Phase 1: Rural", "r2": "🚄 Phase 2: Corridors", "r3": "🌐 Phase 3: Total Interop",
        "leg": "⚠️ Legal: Proprietary Assets of Lia Ariadna Ruiz Ben. GDPR/EUDI.", "col": "country_name"
    },
    "Español": {
        "title": "📊 E-Link-U: Recuperación Regional (Auditoría 2025)",
        "sub": "Recuperando los 459.000 M€ de brecha de fricción en la UE",
        "calc": "🎯 Calculadora de Ahorro", "sel": "País:", "met": "Recuperación Potencial",
        "bench": "📉 Benchmark: UE vs Japón", "b_txt": "Brecha: 970€/persona (UE 1.020€ vs JP 50€)",
        "tab": "📋 Datos de Impacto (Billones)", "chip": "🔒 Arquitectura Soberana Triple-Sector",
        "chip_i": "Antena bloqueada físicamente hasta detectar huella viva.",
        "s1": "🟢 Finanzas: C2C Offline y Energía.", "s2": "🔴 Salud: Historial ZKP Portátil.", "s3": "🔵 Legal: Identidad SSI/eIDAS 2.0.",
        "pil": "🛡️ Pilares Estratégicos", "p1": "Privacidad Zero-Knowledge", "p2": "ROI Instantáneo (30 días)", "p3": "Resiliencia Híbrida",
        "map": "🗺️ Hoja de Ruta", "r1": "📍 Fase 1: Rural", "r2": "🚄 Fase 2: Corredores", "r3": "🌐 Fase 3: Interop Total",
        "leg": "⚠️ Legal: Activos de Lia Ariadna Ruiz Ben. RGPD/EUDI.", "col": "País"
    }
}[lang]

# 4. DATA & CORE LOGIC
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    @st.cache_data(ttl=3600)
    def get_data(): return pd.DataFrame(supabase.table("country_impact").select("*").execute().data)
    df = get_data()

    if not df.empty:
        if lang == "Español": df['country_name'] = df['country_name'].map(c_map).fillna(df['country_name'])
        
        st.title(T["title"])
        st.caption(T["sub"])

        # DASHBOARD
        c_calc, c_bench = st.columns([1, 1])
        with c_calc:
            sel = st.selectbox(T["sel"], df['country_name'].unique())
            data = df[df['country_name'] == sel].iloc[0]
            st.metric(T["met"], f"€{data['rural_recovery_potential']:.2f} B")
        with c_bench:
            st.write(f"**{T['bench']}**")
            st.caption(T["b_txt"])
            st.progress(0.05, text="JP: €50")
            st.progress(1.0, text="EU: €1,020")

        st.bar_chart(df, x='country_name', y=['annual_loss_billion', 'rural_recovery_potential'], color=["#dc3545", "#28a745"])
        with st.expander(T["tab"]):
            st.dataframe(df.rename(columns={"country_name":T["col"]}).style.background_gradient(cmap="Reds", subset=["annual_loss_billion"]), use_container_width=True)

        # ARCHITECTURE & PILLARS
        st.write(f"### {T['chip']}")
        st.info(T["chip_i"])
        sc1, sc2, sc3 = st.columns(3)
        with sc1: st.markdown(f'<div class="sector-card" style="border-left-color:#28a745;">{T["s1"]}</div>', unsafe_allow_html=True)
        with sc2: st.markdown(f'<div class="sector-card" style="border-left-color:#dc3545;">{T["s2"]}</div>', unsafe_allow_html=True)
        with sc3: st.markdown(f'<div class="sector-card" style="border-left-color:#007bff;">{T["s3"]}</div>', unsafe_allow_html=True)

        st.write(f"**{T['pil']}**")
        p1, p2, p3 = st.columns(3)
        p1.caption(f"**{T['p1']}**"); p2.caption(f"**{T['p2']}**"); p3.caption(f"**{T['p3']}**")

        # ROADMAP
        st.write(f"### {T['map']}")
        r1, r2, r3 = st.columns(3)
        r1.info(T["r1"]); r2.info(T["r2"]); r3.info(T["r3"])

        st.warning(T["leg"])
except Exception as e: st.error(f"System status: {e}")
