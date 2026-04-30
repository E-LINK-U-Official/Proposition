import streamlit as st
import pandas as pd
from supabase import create_client

# 1. Page Configuration
st.set_page_config(page_title="E-Link-U Strategy Dashboard", layout="wide", page_icon="🚄")

# Estilo personalizado para las tarjetas del Chip
st.markdown("""
    <style>
    .sector-card {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid;
        background-color: #0e1117;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 E-Link-U: Regional Recovery Dashboard")
st.markdown("### Deteniendo la Hemorragia Administrativa de 459.000 M€")

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
        col_title, col_calc = st.columns([2, 1])
        with col_title:
            st.header("🎯 Calculadora de Recuperación Regional")
        
        col1, col2 = st.columns(2)
        with col1:
            country_selected = st.selectbox("Seleccione un país para auditar:", df['country_name'].unique())
            country_data = df[df['country_name'] == country_selected].iloc[0]
            
        with col2:
            st.metric(label=f"Potencial de recuperación para {country_selected}", 
                      value=f"€{country_data['rural_recovery_potential']:.2f} Billion",
                      delta="Objetivo Anual")

        st.divider()

        # --- SECTION 2: VISUALIZATION ---
        st.subheader("Comparativa: Pérdida Anual vs. Recuperación E-Link-U")
        st.bar_chart(data=df, x='country_name', y=['annual_loss_billion', 'rural_recovery_potential'], color=["#dc3545", "#28a745"])
        
        with st.expander("Ver tabla de datos detallada"):
            st.dataframe(df.style.background_gradient(cmap="Reds", subset=["annual_loss_billion"]), use_container_width=True)

        # --- NEW SECTION: TRIPLE-SECTOR CHIP ARCHITECTURE (VISUAL) ---
        st.divider()
        st.header("🔒 Arquitectura del Chip Triple-Sector")
        st.info("💡 **Gating Biométrico:** La antena NFC permanece físicamente inactiva hasta la validación de huella dactilar en vivo.")
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown(f"""
                <div class="sector-card" style="border-left-color: #28a745;">
                    <h3 style="color: #28a745;">🟢 Sector Verde</h3>
                    <p><b>Finanzas y Energía</b></p>
                    <ul>
                        <li>Pagos C2C Offline</li>
                        <li>Créditos Energéticos</li>
                        <li>Soberanía Transaccional</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
                <div class="sector-card" style="border-left-color: #dc3545;">
                    <h3 style="color: #dc3545;">🔴 Sector Rojo</h3>
                    <p><b>Salud Soberana</b></p>
                    <ul>
                        <li>Historial Médico Portátil</li>
                        <li>Validación ZKP</li>
                        <li>Acceso en Emergencias</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
        with c3:
            st.markdown(f"""
                <div class="sector-card" style="border-left-color: #007bff;">
                    <h3 style="color: #007bff;">🔵 Sector Azul</h3>
                    <p><b>Identidad Legal</b></p>
                    <ul>
                        <li>eIDAS 2.0 / SSI</li>
                        <li>DIDs (Identificadores)</li>
                        <li>Interoperabilidad Total</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        # --- SECTION 3: STRATEGIC PILLARS ---
        st.divider()
        st.header("🛡️ Pilares Estratégicos")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.subheader("Privacidad ZKP")
            st.write("Protocolos **Zero-Knowledge**. Verificamos elegibilidad *sin* exponer datos privados. Soberanía por diseño.")

        with col_b:
            st.subheader("ROI Instantáneo")
            st.write("Con una recuperación proyectada de **459B€/año**, los costes de implementación se amortizan en los primeros 30 días.")

        with col_c:
            st.subheader("Resiliencia Híbrida")
            st.write("Ecosistema a prueba de fallos: Interfaz Digital y **Tarjetas Físicas Biométricas** para apagones o ataques cibernéticos.")

        # --- SECTION 4: ROADMAP ---
        st.divider()
        st.header("🗺️ Hoja de Ruta de Implementación")
        
        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown("### 📍 Fase 1: Piloto Rural")
            st.info("**Foco:** Mayores y Zonas de Baja Conectividad\n\n**Acción:** Tarjeta Física como herramienta soberana primaria.")
        with r2:
            st.markdown("### 🚄 Fase 2: Corredores UE")
            st.info("**Foco:** Trabajadores Móviles y Viajeros\n\n**Acción:** Despliegue híbrido para identidad ferroviaria transfronteriza.")
        with r3:
            st.markdown("### 🌐 Fase 3: Interop Total")
            st.info("**Foco:** Ciudadanía Universal UE\n\n**Acción:** Integración total con la Tarjeta Física como 'Ancla' offline.")

        # --- LEGAL DISCLAIMER ---
        st.divider()
        st.markdown(
            """
            <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #f1c40f;">
                <p style="color: #f1c40f; font-weight: bold; margin-bottom: 5px;">⚠️ Aviso Legal y de Soberanía</p>
                <p style="color: white; font-size: 0.9em;">
                    La arquitectura e-link-u y el protocolo Umatter son activos propietarios de Lia Ariadna Ruiz Ben. 
                    Este marco híbrido cumple con los estándares GDPR e Identidad Digital Europea (EUDI). 
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    else:
        st.warning("Esperando sincronización de base de datos...")

except Exception as e:
    st.error(f"Estado de conexión del sistema: {e}")

# --- SIDEBAR ---
st.sidebar.title("E-Link-U Official")
st.sidebar.markdown("---")
st.sidebar.subheader("Gobernanza del Proyecto")
st.sidebar.write("👤 **Arquitecta:** Lia Ariadna Ruiz Ben")
st.sidebar.write("🆔 **ORCID:** [0009-0006-2598-0625](https://orcid.org)")
st.sidebar.write("🔗 **DOI:** [10.5281/zenodo.19876558](https://zenodo.org)")
st.sidebar.write("---")
st.sidebar.info("E-Link-U OÜ (Estonia) | Proprietary Architecture")
st.sidebar.caption("© 2026 E-Link-U | Patent Pending | Licensed under CC BY-NC-ND 4.0")
