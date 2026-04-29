import streamlit as st
import pandas as pd
from supabase import create_client

# 1. Configuración de la página (Tu diseño original)
st.set_page_config(page_title="E-Link-U Strategy Dashboard", layout="wide", page_icon="🚄")
st.title("📊 E-Link-U: Regional Recovery Dashboard")
st.markdown("### Recovering the €459B Friction Gap in European Infrastructure")

# 2. Conexión Segura (Usando los Secrets que configuramos)
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
    
    # 3. Traer datos de Supabase (Tu tabla de impacto)
    response = supabase.table("country_impact").select("*").execute()
    df = pd.DataFrame(response.data)

    if not df.empty:
        # --- SECCIÓN 1: CALCULADORA REGIONAL (Tu diseño) ---
        st.header("🎯 Regional Savings Calculator")
        col1, col2 = st.columns(2)
        
        with col1:
            country_selected = st.selectbox("Select a Country to Audit:", df['country_name'].unique())
            country_data = df[df['country_name'] == country_selected].iloc[0]
            
        with col2:
            st.metric(label=f"Potential Recovery for {country_selected}", 
                      value=f"€{country_data['rural_recovery_potential']:.2f} Billion")

        st.divider()

        # --- SECCIÓN 2: VISUALIZACIÓN (Tu diseño) ---
        st.subheader("Comparison: Annual Loss vs. E-Link-U Recovery")
        st.bar_chart(data=df, x='country_name', y=['annual_loss_billion', 'rural_recovery_potential'])
        
        st.dataframe(df.style.background_gradient(cmap="Reds", subset=["annual_loss_billion"]), use_container_width=True)

        # --- SECCIÓN NUEVA: LOS TRES SECTORES SOBERANOS (Arquitectura e-link-u) ---
        st.divider()
        st.header("🔒 e-link-u: Triple-Sector Sovereign Architecture")
        t1, t2, t3 = st.tabs(["💰 Finance (Green)", "🏥 Health (Red)", "🆔 Identity (Blue)"])
        
        with t1:
            st.write("**C2C Offline Economy:** Simulación de pagos Card-to-Card y créditos de energía sin internet.")
        with t2:
            st.write("**Portable Medical Records:** Historial de salud cifrado y soberano para corredores TEN-T.")
        with t3:
            st.write("**Self-Sovereign Identity:** Identidad legal basada en SSI y eIDAS 2.0 para cruce de fronteras.")

        # --- SECCIÓN 3: PILARES ESTRATÉGICOS ---
        st.divider()
        st.header("🛡️ Strategic Pillars: Privacy & Implementation")
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.subheader("Zero-Knowledge Privacy")
            st.write("E-Link-U uses **ZKP protocols**. We verify eligibility *without* exposing private data. Sovereignty by design.")

        with col_b:
            st.subheader("Instant ROI")
            st.write("With a projected recovery of **€459B/year**, implementation costs are recovered within the first 30 days.")

        with col_c:
            st.subheader("Hybrid Access")
            st.write("Inclusion first: **Physical Cards** for rural seniors and **Digital Wallets** for the mobile workforce.")

        # --- SECCIÓN 4: ROADMAP HÍBRIDO ---
        st.divider()
        st.header("🗺️ Implementation Roadmap (Hoja de Ruta)")
        r1, r2, r3 = st.columns(3)
        
        with r1:
            st.markdown("### 📍 Phase 1: Rural Pilot")
            st.info("**Focus:** Seniors & Rural Spain/Italy\n\n**Action:** Smart Physical Cards with ZKP pre-validation.")
        with r2:
            st.markdown("### 🚄 Phase 2: EU Corridors")
            st.info("**Focus:** Migrants & High-freq Travelers\n\n**Action:** Digital Wallet for cross-border rail & identity.")
        with r3:
            st.markdown("### 🌐 Phase 3: Total Interop")
            st.info("**Focus:** Universal EU Citizenry\n\n**Action:** Full integration of tax, social security & payments.")

    else:
        st.warning("Awaiting database sync...")

except Exception as e:
    st.error(f"System connection status: {e}")

# --- SECCIÓN FINAL: CREDENCIALES OFICIALES (Tu blindaje) ---
st.sidebar.markdown("---")
st.sidebar.subheader("Project Governance")
st.sidebar.write("👤 **Architect:** Lia Ariadna Ruiz Ben")
st.sidebar.write("🆔 **ORCID:** [0009-0000-8439-517X](https://orcid.org)")
st.sidebar.write("🔗 **DOI:** [10.5281/zenodo.11088635](https://zenodo.org)")
st.sidebar.info("e-link-u OÜ (Estonia) | Proprietary Architecture")
st.sidebar.caption("© 2026 e-link-u | Built for TEN-T & Global Inclusion | Patent Pending")
