import streamlit as st
import pandas as pd
from supabase import create_client

# 1. Page Configuration
st.set_page_config(page_title="e-link-u Strategy Dashboard", layout="wide", page_icon="🚄")

# Custom CSS for UI styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 e-link-u: Regional Recovery Dashboard")
st.markdown("### Recovering the €459B Friction Gap in European Infrastructure")

# 2. Secure Database Connection
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
    
    # 3. Data Retrieval (Impact Table)
    @st.cache_data(ttl=3600)
    def fetch_impact_data():
        response = supabase.table("country_impact").select("*").execute()
        return pd.DataFrame(response.data)

    df = fetch_impact_data()

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
        st.subheader("Comparison: Annual Loss vs. e-link-u Recovery")
        st.bar_chart(data=df, x='country_name', y=['annual_loss_billion', 'rural_recovery_potential'])
        
        st.dataframe(df.style.background_gradient(cmap="Reds", subset=["annual_loss_billion"]), use_container_width=True)

        # --- SECTION 3: TRIPLE-SECTOR SOVEREIGN ARCHITECTURE ---
        st.divider()
        st.header("🔒 e-link-u: Triple-Sector Sovereign Architecture")
        t1, t2, t3 = st.tabs(["💰 Finance (Green)", "🏥 Health (Red)", "🆔 Identity (Blue)"])
        
        with t1:
            st.markdown("<h3 style='color: #28a745;'>💰 Finance Sector</h3>", unsafe_allow_html=True)
            st.write("**C2C Offline Economy:** Offline Card-to-Card payments and energy credit synchronization without internet connectivity.")
            st.info("Priority: Rural financial inclusion and resilient micro-transactions.")

        with t2:
            st.markdown("<h3 style='color: #dc3545;'>🏥 Health Sector</h3>", unsafe_allow_html=True)
            st.write("**Portable Medical Records:** Encrypted and sovereign health history specifically for TEN-T transit corridors.")
            st.info("Priority: International continuity of care for mobile workforces and travelers.")

        with t3:
            st.markdown("<h3 style='color: #007bff;'>🆔 Identity Sector</h3>", unsafe_allow_html=True)
            st.write("**Self-Sovereign Identity (SSI):** Legal identity based on DIDs and eIDAS 2.0 standards for secure border crossing.")
            st.info("Priority: Data sovereignty and EUDI Wallet compliance.")

        # --- SECTION 4: STRATEGIC PILLARS ---
        st.divider()
        st.header("🛡️ Strategic Pillars: Privacy & Implementation")
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.subheader("Zero-Knowledge Privacy")
            st.write("e-link-u utilizes **ZKP protocols**. We verify eligibility *without* exposing private data. Sovereignty by design.")

        with col_b:
            st.subheader("Instant ROI")
            st.write("With a projected recovery of **€459B/year**, infrastructure implementation costs are recovered within the first fiscal month.")

        with col_c:
            st.subheader("Hybrid Access")
            st.write("Inclusion first: **Physical Cards** for rural seniors and **Digital Wallets** for the high-frequency mobile workforce.")

        # --- SECTION 5: IMPLEMENTATION ROADMAP ---
        st.divider()
        st.header("🗺️ Implementation Roadmap")
        r1, r2, r3 = st.columns(3)
        
        with r1:
            st.markdown("### 📍 Phase 1: Rural Pilot")
            st.info("**Focus:** Seniors & Rural Regions\n\n**Action:** Smart Physical Cards with ZKP pre-validation.")
        with r2:
            st.markdown("### 🚄 Phase 2: EU Corridors")
            st.info("**Focus:** Cross-border Logistics\n\n**Action:** Digital Wallet integration for TEN-T rail and legal ID.")
        with r3:
            st.markdown("### 🌐 Phase 3: Total Interoperability")
            st.info("**Focus:** Universal EU Citizenry\n\n**Action:** Full integration of tax, social security, and retail payments.")

        # --- FINAL SECTION: LEGAL DISCLAIMER ---
        st.divider()
        st.markdown(
            """
            <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #f1c40f;">
                <p style="color: #f1c40f; font-weight: bold; margin-bottom: 5px;">⚠️ Legal Disclaimer & Sovereignty Notice</p>
                <p style="color: white; font-size: 0.9em;">
                    The e-link-u architecture and the Umatter protocol are proprietary assets of Lia Ariadna Ruiz Ben. 
                    This framework is architected to align with GDPR and European Digital Identity (EUDI) standards. 
                    Unauthorized commercial reproduction of this logical framework is strictly prohibited.
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    else:
        st.warning("Awaiting database synchronization...")

except Exception as e:
    st.error(f"System connection status: {e}")

# --- SIDEBAR: OFFICIAL GOVERNANCE ---
st.sidebar.markdown("---")
st.sidebar.subheader("Project Governance")
st.sidebar.write("👤 **Architect:** Lia Ariadna Ruiz Ben")
st.sidebar.write("🆔 **ORCID:** [0009-0000-8439-517X](https://orcid.org)")
st.sidebar.write("🔗 **DOI:** [10.5281/zenodo.11088635](https://zenodo.org)")
st.sidebar.info("e-link-u OÜ (Estonia) | Proprietary Architecture")
st.sidebar.caption("© 2026 e-link-u | Patent Pending")
