import streamlit as st
import pandas as pd
import plotly.express as px
import yaml
from pathlib import Path
import numpy as np

# Set page config
st.set_page_config(layout="wide", page_title="Visualization Gallery")

# Load theme configurations
def load_themes():
    themes_dir = Path("themes")
    themes = {}
    for theme_file in themes_dir.glob("*.yaml"):
        with open(theme_file, "r") as f:
            themes[theme_file.stem] = yaml.safe_load(f)
    return themes

# Replace get_abs_data with mock data
@st.cache_data
def get_mock_data(region):
    dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='M')
    
    # Base multipliers for different regions
    if region == "us":
        emp_base, gdp_base = 150000, 23000
        house_base = 400000
        wage_base = 35
    elif region == "aus":
        emp_base, gdp_base = 12000, 2000
        house_base = 800000  # Australian housing prices typically higher
        wage_base = 45  # Higher base wage in AUD
    else:  # EU
        emp_base, gdp_base = 160000, 18000
        house_base = 300000  # In EUR
        wage_base = 30
    
    datasets = {
        'Employment Trends': pd.DataFrame({
            'Date': dates,
            'Full Time': np.random.normal(emp_base, emp_base*0.04, len(dates)),
            'Part Time': np.random.normal(emp_base*0.6, emp_base*0.02, len(dates))
        }),
        'Unemployment Rate': pd.DataFrame({
            'Date': dates,
            'Rate': np.random.normal(5.5 if region == "us" else (4.5 if region == "aus" else 6.5), 
                                   0.5, len(dates))
        }),
        'GDP Growth': pd.DataFrame({
            'Date': dates,
            'GDP': np.cumsum(np.random.normal(0.5, 0.2, len(dates))) * gdp_base + gdp_base
        }),
        'CPI Trends': pd.DataFrame({
            'Date': dates,
            'CPI': np.cumsum(np.random.normal(0.2, 0.1, len(dates))) + 
                  (100 if region == "us" else (110 if region == "aus" else 105))
        }),
        'Wage Growth': pd.DataFrame({
            'Date': dates,
            'Wages': np.cumsum(np.random.normal(0.3, 0.1, len(dates))) + wage_base
        }),
        'Housing Prices': pd.DataFrame({
            'Date': dates,
            'Median Price': np.cumsum(np.random.normal(5000, 1000, len(dates))) + house_base
        }),
        'Interest Rates': pd.DataFrame({
            'Date': dates,
            'Rate': np.cumsum(np.random.normal(0.02, 0.01, len(dates))) + 
                   (4.5 if region == "us" else (3.5 if region == "aus" else 2.5))
        }),
        'Trade Balance': pd.DataFrame({
            'Date': dates,
            'Exports': np.random.normal(gdp_base*0.12, gdp_base*0.01, len(dates)),
            'Imports': np.random.normal(gdp_base*0.14, gdp_base*0.01, len(dates))
        }),
        'Business Confidence': pd.DataFrame({
            'Date': dates,
            'Index': np.random.normal(100, 5, len(dates)) * 
                    (1.1 if region == "us" else (1.0 if region == "aus" else 0.9))
        }),
        'Retail Sales': pd.DataFrame({
            'Date': dates,
            'Sales': np.cumsum(np.random.normal(0.4, 0.1, len(dates))) + 
                    (1000 if region == "us" else (800 if region == "aus" else 900))
        }),
        'Manufacturing Index': pd.DataFrame({
            'Date': dates,
            'Index': np.random.normal(55, 3, len(dates)) * 
                    (1.1 if region == "us" else (0.9 if region == "aus" else 1.0))
        }),
        'Consumer Confidence': pd.DataFrame({
            'Date': dates,
            'Index': np.random.normal(95, 4, len(dates)) * 
                    (1.2 if region == "us" else (1.1 if region == "aus" else 0.9))
        })
    }
    return datasets

# Create styled charts based on theme
def create_chart(data, chart_type, theme_config):
    fig = None
    
    # Determine if the DataFrame has multiple numeric columns
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    
    if chart_type == "line":
        if len(numeric_cols) > 1:
            fig = px.line(data, x='Date', y=numeric_cols,
                         template=theme_config["plotly_template"],
                         color_discrete_sequence=theme_config["color_palette"])
        else:
            fig = px.line(data, x='Date', y=numeric_cols[0],
                         template=theme_config["plotly_template"],
                         color_discrete_sequence=theme_config["color_palette"])
    
    if fig:
        # Apply modern styling
        fig.update_layout(
            font_family=theme_config["font_family"],
            plot_bgcolor=theme_config["background_color"],
            paper_bgcolor=theme_config["paper_color"],
            margin=dict(t=30, l=10, r=10, b=10),  # Tighter margins
            height=300,  # Fixed height for consistency
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor=theme_config.get("grid_color", "rgba(128, 128, 128, 0.1)"),
                showline=True,
                linewidth=1,
                linecolor=theme_config.get("line_color", "rgba(128, 128, 128, 0.3)"),
                tickformat='%b %Y',
                tickfont=dict(color=theme_config.get("text_color", "#1f2937"))
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor=theme_config.get("grid_color", "rgba(128, 128, 128, 0.1)"),
                showline=True,
                linewidth=1,
                linecolor=theme_config.get("line_color", "rgba(128, 128, 128, 0.3)"),
                tickfont=dict(color=theme_config.get("text_color", "#1f2937"))
            ),
            hoverlabel=dict(
                bgcolor=theme_config["paper_color"],
                font_size=12,
                font_family=theme_config["font_family"]
            ),
            font=dict(
                color=theme_config.get("text_color", "#1f2937")
            )
        )
        
        # Update line styling
        fig.update_traces(
            line=dict(width=2),
            hovertemplate='%{y:,.1f}<br>%{x|%B %Y}<extra></extra>'
        )
    
    return fig

# Main app
def main():
    st.title("Economic Data Visualization Gallery")
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .stButton > button {
            background-color: #2E86AB;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            float: right;
            margin-top: -10px;
        }
        [data-testid="stHorizontalBlock"] {
            gap: 1rem;
            padding: 0.5rem;
        }
        [data-testid="column"] {
            background-color: #f0f7ff;  /* Light blue background */
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: rgba(59, 130, 246, 0.1) 0px 4px 12px, rgba(59, 130, 246, 0.05) 0px 1px 3px;  /* Blue-tinted shadow */
            border: 1px solid rgba(59, 130, 246, 0.1);  /* Subtle blue border */
            margin: 0 0 1rem 0 !important;
            min-width: calc(33.33% - 1.33rem) !important;
        }
        .element-container {
            margin-bottom: 1rem;
        }
        .stPlotlyChart {
            margin-bottom: 1rem;
        }
        h3 {
            margin-bottom: 1.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    themes = load_themes()
    selected_theme = st.sidebar.selectbox("Select Theme", list(themes.keys()))
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["US Data", "AUS Data", "EU Data"])
    
    with tab1:
        st.markdown("### US Data")
        data_collections = get_mock_data("us")
        display_charts(data_collections, themes[selected_theme], "us")
    
    with tab2:
        st.markdown("### AUS Data")
        data_collections = get_mock_data("aus")
        display_charts(data_collections, themes[selected_theme], "aus")
    
    with tab3:
        st.markdown("### EU Data")
        data_collections = get_mock_data("eu")
        display_charts(data_collections, themes[selected_theme], "eu")

def display_charts(data_collections, theme_config, region_prefix):
    # Process data in groups of 3
    for i in range(0, len(data_collections), 3):
        # Create a new row for every 3 items
        cols = st.columns(3, gap="large")
        
        # Process the next 3 items (or fewer for the last row)
        for j in range(3):
            if i + j < len(data_collections):
                title, data = list(data_collections.items())[i + j]
                with cols[j]:
                    st.subheader(title)
                    fig = create_chart(data, "line", theme_config)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    st.button("Purchase", key=f"{region_prefix}_btn_{i+j}")

if __name__ == "__main__":
    main()
