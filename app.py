import streamlit as st
import pandas as pd
from supabase import create_client

# 1. Page Configuration
st.set_page_config(page_title="E-Link-U Strategy Dashboard", layout="wide", page_icon="🚄")

st.title("📊 E-Link-U: Regional Recovery Dashboard")
st.markdown("### Recovering the €459B Friction Gap in European Infrastructure")

# 2. Secure Database Connection
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
    
    # 3. Data Retrieval
    @st.cache_data(ttl=3600)
    def fetch_data():
        response = supabase.table("country_impact").select("*").execute()
        return pd.DataFrame(response.data)

    df = fetch_data()

    if not df.empty:
        
        # --- SECTION 1: REGIONAL SAVINGS CALCULATOR ---
        st.header("🎯 Regional Savings Calculator")
        col1, col2 = st.columns(2)
        
        with col1:
            country_selected = st.selectbox("Select a Country to Audit:", df['country_name'].unique())
            country_data = df[df['country_name'] == country_selected].iloc[0]
            
        with col2:
            st.metric(label=f"Potential Recovery for {country_selected}", 
                      value=f"€{country_data['rural_recovery_potential']:.2f} Billion")

        st.divider()

        # --- SECTION 2: VISUALIZATION ---
        st.subheader("Comparison: Annual Loss vs. E-Link-U Recovery")
        st.bar_chart(data=df, x='country_name', y=['annual_loss_billion', 'rural_recovery_potential'])
        
        st.dataframe(df.style.background_gradient(cmap="Reds", subset=["annual_loss_billion"]), use_container_width=True)

        # --- SECTION 3: STRATEGIC PILLARS (Hybrid Resilience) ---
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
            st.subheader("Hybrid Access & Resilience")
            st.write("A fail-safe ecosystem: **Digital Interface** for daily convenience and **Biometric Physical Cards** for blackouts, cyber-attacks, or zero-battery scenarios.")

        # --- SECTION 4: ROADMAP (Hybrid Approach) ---
        st.divider()
        st.header("🗺️ Implementation Roadmap (Hoja de Ruta)")
        
        r1, r2, r3 = st.columns(3)
        
        with r1:
            st.markdown("### 📍 Phase 1: Rural Pilot")
            st.info("**Focus:** Seniors & Low-Connectivity Regions\n\n**Action:** Smart Physical Cards as the primary sovereign tool.")
            
        with r2:
            st.markdown("### 🚄 Phase 2: EU Corridors")
            st.info("**Focus:** Mobile Workforce & Travelers\n\n**Action:** Hybrid deployment (Digital + Physical Card) for uninterrupted cross-border rail identity.")
            
        with r3:
            st.markdown("### 🌐 Phase 3: Total Interop")
            st.info("**Focus:** Universal EU Citizenry\n\n**Action:** Full integration with the Physical Card acting as the permanent offline 'Anchor'.")

        # --- THE TRIPLE SECTOR SECTIONS ---
        st.divider()
        st.header("🔒 e-link-u: Triple-Sector Sovereign Architecture")
        t1, t2, t3 = st.tabs(["💰 Finance", "🏥 Health", "🆔 Identity"])
        
        with t1:
            st.markdown("<h3 style='color: #28a745;'>💰 Finance Sector (Green)</h3>", unsafe_allow_html=True)
            st.write("Offline C2C Economy. The Physical Card ensures trade continues during power outages or bank hacks.")
        with t2:
            st.markdown("<h3 style='color: #dc3545;'>🏥 Health Sector (Red)</h3>", unsafe_allow_html=True)
            st.write("Critical health data accessible via Card during emergencies in tunnels or remote areas with no signal.")
        with t3:
            st.markdown("<h3 style='color: #007bff;'>🆔 Identity Sector (Blue)</h3>", unsafe_allow_html=True)
            st.write("Self-Sovereign Identity. The card serves as the offline Master-Key for border security.")
            import pandas as pd

# Datos del Benchmark
df_friccion = pd.DataFrame({
    'Región': ['Japón (Suica)', 'Unión Europea'],
    'Coste de Fricción (€)': [50, 1020]
})

st.write("### Visualización del 'Impuesto de Ineficiencia'")
st.bar_chart(data=df_friccion, x='Región', y='Coste de Fricción (€)', color="#2e7d32")


        # --- LEGAL DISCLAIMER ---
        st.divider()
        st.markdown(
            """
            <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #f1c40f;">
                <p style="color: #f1c40f; font-weight: bold; margin-bottom: 5px;">⚠️ Legal Disclaimer & Sovereignty Notice</p>
                <p style="color: white; font-size: 0.9em;">
                    The e-link-u architecture and the Umatter protocol are proprietary assets of Lia Ariadna Ruiz Ben. 
                    This hybrid framework aligns with GDPR and European Digital Identity (EUDI) standards. 
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    else:
        st.warning("Awaiting database sync...")

except Exception as e:
    st.error(f"System connection status: {e}")

# --- SIDEBAR ---
st.sidebar.markdown("---")
st.sidebar.subheader("Project Governance")
st.sidebar.write("👤 **Architect:** Lia Ariadna Ruiz Ben")
with st.sidebar:
    st.image("https://icons8.com", width=80)
    st.title("Documentación")
    st.markdown("[📄 White Paper 1](https://zenodo.org)")
    st.markdown("[📄 White Paper 2](https://zenodo.org)")
    st.write("---")
    st.info("DOI: 10.5281/zenodo.19876558")

st.sidebar.write("🆔 **ORCID:** [0009-0006-2598-0625](https://orcid.org)")
st.sidebar.write("🔗 **DOI:** [10.5281/zenodo.19876558](https://zenodo.org)")
st.sidebar.info("E-Link-U OÜ (Estonia) | Proprietary Architecture")
st.sidebar.caption("© 2026 E-Link-U | Patent Pending| Licensed under CC BY-NC-ND 4.0 ")
