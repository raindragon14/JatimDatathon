import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Jatim Datathon Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Jatim Datathon Interactive Dashboard")
st.markdown("""
Welcome to the interactive data visualization dashboard for the **Jatim Datathon**.
This application explores macroeconomic indicators across East Java (Jawa Timur), such as Minimum Wage (UMK), Inflation, and MSME growth.
""")

# --- Sidebar ---
st.sidebar.header("Navigation & Filters")
page = st.sidebar.radio("Select Analysis:", ["Minimum Wage (UMK)", "Macroeconomic Overview"])

# --- Helper Functions ---
@st.cache_data
def load_data(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        st.error(f"Error loading {filepath}: {e}")
        return None

# --- Pages ---
if page == "Minimum Wage (UMK)":
    st.header("💵 Analisis Upah Minimum Kabupaten/Kota (UMK) Jawa Timur")
    
    umk_path = os.path.join("data", "processed", "data_upah_minimum_kabkota_umk.csv")
    df_umk = load_data(umk_path)
    
    if df_umk is not None:
        # Standardize column names just in case
        df_umk.columns = [str(c).strip().lower().replace(' ', '_') for c in df_umk.columns]
        
        # Check required columns
        req_cols = ['nama_kabupaten_kota', 'upah_minimum', 'tahun']
        if all(col in df_umk.columns for col in req_cols):
            
            # Filters
            available_years = sorted(df_umk['tahun'].unique(), reverse=True)
            selected_year = st.sidebar.selectbox("Pilih Tahun:", available_years)
            
            # Filter Data
            df_filtered = df_umk[df_umk['tahun'] == selected_year]
            df_filtered = df_filtered.sort_values(by='upah_minimum', ascending=False)
            
            st.subheader(f"Distribusi UMK Tahun {selected_year}")
            
            # Bar Chart
            fig = px.bar(
                df_filtered, 
                x='nama_kabupaten_kota', 
                y='upah_minimum',
                color='upah_minimum',
                color_continuous_scale='Viridis',
                title=f'UMK Kabupaten/Kota di Jawa Timur ({selected_year})',
                labels={'nama_kabupaten_kota': 'Kabupaten/Kota', 'upah_minimum': 'Upah Minimum (Rp)'}
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Top 5 and Bottom 5
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Top 5 UMK Tertinggi ({selected_year})**")
                st.dataframe(df_filtered[['nama_kabupaten_kota', 'upah_minimum']].head(5).reset_index(drop=True))
                
            with col2:
                st.warning(f"**Top 5 UMK Terendah ({selected_year})**")
                st.dataframe(df_filtered[['nama_kabupaten_kota', 'upah_minimum']].tail(5).reset_index(drop=True))
                
            # Line Chart over time for selected cities
            st.subheader("Tren UMK Dari Waktu ke Waktu")
            all_cities = sorted(df_umk['nama_kabupaten_kota'].unique())
            default_cities = ['KOTA SURABAYA', 'KABUPATEN GRESIK', 'KABUPATEN SIDOARJO', 'KABUPATEN MALANG', 'KABUPATEN PASURUAN']
            selected_cities = st.multiselect("Pilih Kota/Kabupaten untuk perbandingan:", all_cities, default=default_cities)
            
            if selected_cities:
                df_trend = df_umk[df_umk['nama_kabupaten_kota'].isin(selected_cities)]
                df_trend = df_trend.sort_values('tahun')
                fig_trend = px.line(
                    df_trend, 
                    x='tahun', 
                    y='upah_minimum', 
                    color='nama_kabupaten_kota',
                    markers=True,
                    title='Perkembangan UMK',
                    labels={'tahun': 'Tahun', 'upah_minimum': 'Upah Minimum (Rp)', 'nama_kabupaten_kota': 'Wilayah'}
                )
                # Ensure x-axis shows only integer years
                fig_trend.update_layout(xaxis=dict(tickmode='linear', dtick=1))
                st.plotly_chart(fig_trend, use_container_width=True)
                
        else:
            st.error("Dataset UMK tidak memiliki kolom yang dibutuhkan ('nama_kabupaten_kota', 'upah_minimum', 'tahun').")
    else:
        st.warning("Dataset UMK tidak ditemukan di direktori yang diharapkan (`data/processed/data_upah_minimum_kabkota_umk.csv`).")

elif page == "Macroeconomic Overview":
    st.header("🌍 Macroeconomic Overview")
    st.markdown("""
    Welcome to the macroeconomic overview section. 
    Here you can integrate other datasets like PDRB, Inflation, and Poverty rates.
    """)
    st.info("💡 **Tip for Developers**: Load additional datasets from `data/processed/` and use Plotly to visualize regional economic disparities across East Java.")

st.markdown("---")
st.markdown("Developed for the Jatim Datathon Portfolio Project.")
