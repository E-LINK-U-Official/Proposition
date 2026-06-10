import streamlit as st
import pandas as pd
from supabase import create_client

# 1. SETUP & UI 
st.set_page_config(page_title="E-Link-U™ Strategy", layout="wide", page_icon="🚄")
st.markdown("""<style>
    .sector-card {padding:20px; border-radius:10px; border-left:5px solid; background-color:#1e293b; margin-bottom:10px; min-height:220px;}
    .stMetric {background-color:#0e1117; padding:15px; border-radius:10px;}
</style>""", unsafe_allow_html=True)

# 2. SIDEBAR (IDIOMA + GOBERNANZA + CONTACTO + FUENTES)
with st.sidebar:
    st.title("🌐 Menu")
    lang = st.radio("Language / Idioma", ("English", "Español"), horizontal=True)
    st.divider()
    
    st.subheader("Project Governance")
    st.write("👤 **Architect:** Lia Ariadna Ruiz Ben")
    st.write("🆔 **ORCID:** [0009-0006-2598-0625](https://orcid.org)")
    st.write("🔗 **DOI:** [10.5281/zenodo.20045806](https://doi.org)")
    st.markdown("**📬 Contact / Contacto:**")
    st.write("📧 [Email Me](mailto:Lia@elinku.org)")
    st.write("💼 [LinkedIn Profile](https://linkedin.com)")
    
    st.divider()

    # Fuentes y Metodología
    m_t = "Methodology 2025" if lang == "English" else "Metodología 2025"
    st.markdown(f"**{m_t}**")
    st.caption("• [Eurostat 2025 Labor Costs €34.9/h]")
    st.caption("• [EC Competitiveness 2025](https://europa.eu)")
    st.caption("• [JR East Report 2025](https://jreast.co.jp)")
    
    st.divider()
    st.info("E-Link-U™| Proprietary Architecture")
    st.caption("© 2026 E-Link-U™ | Patent Pending | CC BY-NC-ND 4.0")

# 3. DICCIONARIO DE TEXTOS (COMPLETO)
c_map = {"Spain":"España","Italy":"Italia","France":"Francia","Germany":"Alemania","Portugal":"Portugal","Belgium":"Bélgica","Netherlands":"Países Bajos","European Union":"Unión Europea"}
T = {
    "English": {
        "title": "📊 E-Link-U™: Regional Recovery Dashboard",
        "sub": "Optimizing the €459B Sovereign Friction Gap (2025 Audit Data)",
        "calc_h": "🎯 Regional Savings Calculator", "sel": "Select a Country to Audit:", "met": "Potential Recovery",
        "comp_h": "📉 Friction Benchmark: EU vs. Japan (2025)", 
        "comp_txt": "Japan (Suica architecture) operates at €50 friction/year per capita via hardware standardization. EU averages €1,020 due to fragmented digital silos. E-Link-U targets a recovery of up to €970/person.",
        "tab_h": "📋 Granular Financial Impact Profile (Annual Multi-Sector Loss in Billions)",
        "chip_h": "🔒 E-Link-U™: Energy-Harvesting Triple-Sector Sovereign Architecture",
        "chip_i": "Hardware Security: The NFC RF antenna is physical-gated by an on-card low-power biometric match. Operating purely on energy harvesting from regular smartphone/terminal fields, no raw biometric templates ever cross the air interface.",
        "s1_t": "🟢 Sovereign Finance", "s1_p": "Offline tokenized ledger infrastructure. Secures local commerce and programmable relief distribution during critical infrastructure failure or grid attacks.",
        "s2_t": "🔴 Decentralized Health Data", "s2_p": "Secure emergency health parameters accessible locally via zero-connectivity physical smart cards in remote or degraded operational environments.",
        "s3_t": "🔵 Self-Sovereign Identity", "s3_p": "Hardware-anchored offline master key for edge border validation, engineered to dynamically integrate with eIDAS 2.0 and W3C DIDs framework.",
        "pillar_h": "🛡️ Core Strategic Pillars: Auditable Privacy & Amortization",
        "p1_t": "Zero-Knowledge Attestation", "p1_d": "Verifying structural eligibility metrics without leaking private operational data. Cryptographic data sovereignty directly at the hardware layer.",
        "p2_t": "Phased Financial Amortization", "p2_d": "Targeting systemic cost savings of €459B/year. Infrastructure setup cap-ex is modeled to amortize within 30 days post-saturation in target regional deployments.",
        "p3_t": "Asymmetric Fault Resilience", "p3_d": "Sustaining high-throughput digital interfaces backed by biometric physical smart cards capable of processing transactions under prolonged grid blackouts.",
        "roadmap_h": "🗺️ Empirical Implementation Roadmap",
        "r1_t": "📍 Phase 1: Isolated Rural Baseline", "r1_d": "**Target Audience:** Senior Citizens & Low-Connectivity Zones.\n\n**Action:** Validating power-harvesting biometrics using high-durability smart cards as primary identity anchors.",
        "r2_t": "🚄 Phase 2: High-Velocity Transit Corridors", "r2_d": "**Target Audience:** Cross-Border Crossings & Rail Passengers.\n\n**Action:** Deploying hybrid offline validation endpoints for continuous low-latency check-ins across EU borders.",
        "r3_t": "🌐 Phase 3: Continental Interoperability Integration", "r3_d": "**Target Audience:** Universal Sovereign Citizenry.\n\n**Action:** Full structural consolidation, establishing the biometric smart card as the permanent physical anchor for eIDAS decentralized applications.",
        "leg": "⚠️ Structural Notice: Intellectual property assets of Lia Ariadna Ruiz Ben. Strictly GDPR, NIS 2, and EUDI Wallet framework compliant.", "col": "country_name"
    },
    "Español": {
        "title": "📊 E-Link-U™: Panel de Recuperación Regional",
        "sub": "Optimización de los 459.000 M€ de Brecha de Fricción Soberana (Datos de Auditoría 2025)",
        "calc_h": "🎯 Calculadora de Ahorro Regional", "sel": "Seleccione un país para auditar:", "met": "Recuperación Potencial",
        "comp_h": "📉 Benchmark de Fricción: UE vs. Japón (2025)", 
        "comp_txt": "Japón (arquitectura Suica) opera con 50€/año por cápita mediante estandarización de hardware. La UE promedia 1.020€ por silos digitales fragmentados. E-Link-U apunta a recuperar hasta 970€/persona.",
        "tab_h": "📋 Perfil de Impacto Financiero Granular (Pérdida Anual Multi-Sector en Billones)",
        "chip_h": "🔒 E-Link-U™: Arquitectura Soberana de Triple Sector por Recolección de Energía",
        "chip_i": "Hardware Security: La antena de RF NFC está bloqueada físicamente por un interruptor controlado por biometría local de ultra bajo consumo. Operando exclusivamente por recolección de energía (energy harvesting) de terminales, ningún dato biométrico crudo sale de la tarjeta.",
        "s1_t": "🟢 Finanzas Soberanas", "s1_p": "Economía C2C Offline. El comercio sigue durante apagones o hackeos. Créditos energéticos y ayudas.",
        "s2_t": "🔴 Datos de Salud Descentralizados", "s2_p": "Datos médicos críticos accesibles por tarjeta en emergencias o zonas sin señal de red.",
        "s3_t": "🔵 Identidad Autosoberana", "s3_p": "Identidad Autosoberana. Llave Maestra offline para seguridad fronzeriza e integración eIDAS 2.0.",
        "pillar_h": "🛡️ Pilares Estratégicos: Privacidad Auditable y Amortización",
        "p1_t": "Atestación Zero-Knowledge", "p1_d": "Verificación de métricas de elegibilidad sin filtrar datos privados. Soberanía criptográfica implementada directamente en la capa de hardware.",
        "p2_t": "Amortización Financiera Gradual", "p2_d": "Ahorro sistémico proyectado de 459B€/año. Los costes de infraestructura (cap-ex) están modelados para amortizarse dentro de los 30 días posteriores a la saturación del despliegue regional.",
        "p3_t": "Resiliencia Asimétrica a Fallos", "p3_d": "Conveniencia digital respaldada por tarjetas físicas biométricas capaces de procesar transacciones críticas bajo apagones prolongados.",
        "roadmap_h": "🗺️ Hoja de Ruta de Implementación Empírica",
        "r1_t": "📍 Fase 1: Línea Base Rural Aislada", "r1_d": "**Foco:** Zonas de Baja Conectividad y Tercera Edad.\n\n**Acción:** Validación de biometría por recolección de energía usando tarjetas de alta durabilidad como anclas primarias.",
        "r2_t": "🚄 Fase 2: Corredores de Tránsito de Alta Velocidad", "r2_d": "**Foco:** Pasajeros de Tren y Cruces Transfronterizos.\n\n**Acción:** Despliegue de endpoints de validación offline híbridos para registros continuos de baja latencia.",
        "r3_t": "🌐 Fase 3: Integración de Interoperabilidad Continental", "r3_d": "**Foco:** Ciudadanía Universal Soberana.\n\n**Acción:** Consolidación estructural total, estableciendo la tarjeta biométrica como el ancla física permanente para carteras descentralizadas eIDAS.",
        "leg": "⚠️ Aviso Estructural: Activos de propiedad intelectual de Lia Ariadna Ruiz Ben. Conforme a RGPD, NIS 2 y el marco de identidad digital de la UE (EUDI).", "col": "Nombre del País"
    }
}[lang]

# 4. DATA & CORE LOGIC
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    @st.cache_data(ttl=3600)
    def get_data(): 
        return pd.DataFrame(supabase.table("country_impact").select("*").execute().data)
    df_raw = get_data()
except Exception:
    df_raw = pd.DataFrame([
        {"country_name": "Spain", "annual_loss_billion": 45.2, "rural_recovery_potential": 12.4},
        {"country_name": "Italy", "annual_loss_billion": 55.1, "rural_recovery_potential": 15.3},
        {"country_name": "France", "annual_loss_billion": 68.0, "rural_recovery_potential": 18.1}
    ])

# 5. RENDERIZADO VISUAL SEGURO DE TODAS LAS SECCIONES
if not df_raw.empty:
    df = df_raw.copy()
    if lang == "Español": 
        df['country_name'] = df['country_name'].map(c_map).fillna(df['country_name'])
    
    st.title(T["title"])
    st.markdown(f"### {T['sub']}")

    # --- CUADRO 1: CALCULADORA & BENCHMARK ---
    col_c, col_b = st.columns(2)
    with col_c:
        st.header(T["calc_h"])
        sel = st.selectbox(T["sel"], df['country_name'].unique())
        data = df[df['country_name'] == sel].iloc[0]
        st.metric(label=f"{T['met']} ({sel})", value=f"€{data['rural_recovery_potential']:.2f} B")
    with col_b:
        st.subheader(T["comp_h"])
        st.write(T["comp_txt"])
        st.progress(0.05, text="Japan (Suica): €50")
        st.progress(1.0, text="European Union: €1,020")

    # --- CUADRO 2: GRÁFICO DE BARRAS DE IMPACTO ---
    st.divider()
    st.bar_chart(df, x='country_name', y=['annual_loss_billion', 'rural_recovery_potential'], color=["#dc3545", "#28a745"])
    
    # --- CUADRO 3: DATAFRAME DE IMPACTO GRANULAR ---
    st.subheader(T["tab_h"])
    st.dataframe(df.rename(columns={"country_name":T["col"]}).style.background_gradient(cmap="Reds", subset=["annual_loss_billion"]), use_container_width=True)

    # --- CUADRO 4: ARQUITECTURA DE TRIPLE SECTOR ---
    st.divider()
    st.header(T["chip_h"])
    st.info(f"💡 {T['chip_i']}")
    sc1, sc2, sc3 = st.columns(3)
    with sc1: 
        st.markdown(f'<div class="sector-card" style="border-left-color: #28a745;"><h3>{T["s1_t"]}</h3><p>{T["s1_p"]}</p></div>', unsafe_allow_html=True)
    with sc2: 
        st.markdown(f'<div class="sector-card" style="border-left-color: #dc3545;"><h3>{T["s2_t"]}</h3><p>{T["s2_p"]}</p></div>', unsafe_allow_html=True)
    with sc3: 
        st.markdown(f'<div class="sector-card" style="border-left-color: #007bff;"><h3>{T["s3_t"]}</h3><p>{T["s3_p"]}</p></div>', unsafe_allow_html=True)

    # --- CUADRO 5: PILARES ESTRATÉGICOS ---
    st.divider()
    st.header(T["pillar_h"])
    p1, p2, p3 = st.columns(3)
    with p1:
        st.subheader(T["p1_t"])
        st.write(T["p1_d"])
    with p2:
        st.subheader(T["p2_t"])
        st.write(T["p2_d"])
    with p3:
        st.subheader(T["p3_t"])
        st.write(T["p3_d"])

    # --- CUADRO 6: HOJA DE RUTA ---
    st.divider()
    st.header(T["roadmap_h"])
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f"### {T['r1_t']}")
        st.write(T['r1_d'])
    with r2:
        st.markdown(f"### {T['r2_t']}")
        st.write(T['r2_d'])
    with r3:
        st.markdown(f"### {T['r3_t']}")
        st.write(T['r3_d'])

    st.divider()
    st.caption(T["leg"])
else:
    st.error("❌ No data available.")
