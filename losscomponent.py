# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import date

st.set_page_config(page_title="Loss Component Calculator", layout="wide")

# ---------- CUSTOM CSS (African Actuarial Consultants theme) ----------
st.markdown("""
<style>
    /* Global */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
        font-family: 'Calisto MT', serif;
        font-size: 11pt;
    }
    
    /* Apply Calisto MT to all text elements */
    body, p, h1, h2, h3, h4, h5, h6, div, span, label, .stMarkdown, 
    .stTextInput label, .stDateInput label, .stSelectbox label, .stMultiSelect label,
    .stButton button, .stDownloadButton button, .stFileUploader label,
    .stAlert, .stInfo, .stWarning, .stError, .stSuccess, .stSpinner, 
    .stProgress, .stToast, .stSidebar, .stMetric, .stExpander {
        font-family: 'Calisto MT', serif !important;
    }
    
    /* Header / Navigation */
    .header {
        background-color: #000000;
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        border-bottom: 3px solid #D4AF37;
    }
    .nav-links a {
        color: #FFFFFF;
        margin-left: 2rem;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s;
        font-family: 'Calisto MT', serif;
    }
    .nav-links a:hover {
        color: #D4AF37;
    }
    
    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #000000 0%, #333333 100%);
        color: #FFFFFF;
        padding: 2rem 2rem;
        text-align: center;
        border-bottom: 3px solid #D4AF37;
    }
    .hero h1 {
        color: #D4AF37;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-family: 'Calisto MT', serif;
    }
    .hero p {
        font-size: 1.2rem;
        max-width: 800px;
        margin: 0 auto;
        font-family: 'Calisto MT', serif;
    }
    
    /* Main container */
    .main-container {
        max-width: 1400px;
        margin: 2rem auto;
        padding: 0 2rem;
    }
    
    /* Required Column Containers */
    .required-container {
        background-color: #F9F9F9;
        border: 2px solid #D4AF37;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        min-height: 100px;
        height: auto;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: 100%;
        margin-bottom: 1rem;
    }
    .required-container h3 {
        color: #D4AF37;
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
        font-weight: bold;
        font-family: 'Calisto MT', serif;
    }
    .required-container p {
        color: #666666;
        font-size: 0.8rem;
        margin-bottom: 0;
        line-height: 1.3;
        font-family: 'Calisto MT', serif;
    }
    
    /* Cards */
    .card {
        background-color: #F9F9F9;
        border: 1px solid #D4AF37;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .card h3 {
        color: #D4AF37;
        margin-top: 0;
        border-bottom: 2px solid #D4AF37;
        padding-bottom: 0.5rem;
        font-family: 'Calisto MT', serif;
    }
    
    /* Footer */
    .footer {
        background-color: #000000;
        color: #FFFFFF;
        text-align: center;
        padding: 1.5rem;
        border-top: 3px solid #D4AF37;
        margin-top: 3rem;
    }
    .footer a {
        color: #D4AF37;
        text-decoration: none;
        font-family: 'Calisto MT', serif;
    }
    
    /* Streamlit element overrides */
    .stButton > button, .stDownloadButton > button {
        background-color: #D4AF37;
        color: #000000;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
        font-family: 'Calisto MT', serif !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #B8960F;
        color: #FFFFFF;
    }
    
    .stFileUploader {
        border: 2px dashed #D4AF37;
        border-radius: 5px;
        padding: 1rem;
    }
    
    .stMultiSelect [data-baseweb="select"], 
    .stSelectbox [data-baseweb="select"] {
        border: 1px solid #D4AF37;
        border-radius: 4px;
    }
    
    .dataframe {
        border: 1px solid #D4AF37;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Fix for select box container */
    .stSelectbox div[data-baseweb="select"] {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="header">
    <div class="nav-links">
        <a href="#">Home</a>
        <a href="#">Services</a>
        <a href="#">Tools</a>
        <a href="#">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown("""
<div class="hero">
    <h1>Loss Component Calculator</h1>
    <p>Upload your CSV or Excel file. Map your columns to the required fields below. The app calculates Loss Ratio, Commission Ratio, Expense Ratio, Risk Adjustment Ratio, Combined Ratio, and the Loss Component.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Main Container ----------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- User inputs ---
col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("Client Name (for file name)", value="Client").strip()
with col2:
    # empty for spacing
    pass

# File uploader (same as OCR app)
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Read file based on extension
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='cp1252')
                st.info("File read with Windows-1252 encoding.")
        else:
            df = pd.read_excel(uploaded_file)

        # Drop unnamed columns
        unnamed = [c for c in df.columns if c.startswith('Unnamed:')]
        if unnamed:
            df = df.drop(columns=unnamed)
            st.info(f"Dropped {len(unnamed)} unnamed column(s).")

        # Preview
        st.markdown("#### Preview of uploaded data")
        st.dataframe(df.head())
        st.markdown("---")

        # --- Column Mapping Section ---
        st.markdown("### Map Your Columns to Required Fields")
        st.markdown("The calculator requires the following columns. Please select which column in your data corresponds to each required field:")

        # Get all column names for selection
        all_columns = df.columns.tolist()
        
        # Define required fields with descriptions
        required_fields = {
            'Line_of_business': 'Line of Business - The category/segment for grouping results',
            'Gross_Written_Premiums': 'Gross Written Premiums - Total premiums written',
            'Gross_Attributable_Expenses': 'Gross Attributable Expenses - Operating expenses',
            'Gross_Commission_Paid': 'Gross Commission Paid - Commission expenses',
            'Gross_Paid_Claims': 'Gross Paid Claims - Claims paid during the period',
            'Gross_Opening_OCR': 'Gross Opening OCR - Opening outstanding claims reserve',
            'Gross_Closing_OCR': 'Gross Closing OCR - Closing outstanding claims reserve',
            'Gross_Opening_IBNR': 'Gross Opening IBNR - Opening incurred but not reported reserve',
            'Gross_Closing_IBNR': 'Gross Closing IBNR - Closing incurred but not reported reserve',
            'Gross_Opening_UPR': 'Gross Opening UPR - Opening unearned premium reserve',
            'Gross_Closing_UPR': 'Gross Closing UPR - Closing unearned premium reserve',
            'Gross_Risk_Adjustment': 'Gross Risk Adjustment - Risk adjustment amount'
        }
        
        # Store mapped columns
        mapped_columns = {}
        
        # Create rows of 3 columns for mapping
        field_list = list(required_fields.keys())
        for i in range(0, len(field_list), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(field_list):
                    field = field_list[i + j]
                    with cols[j]:
                        description = required_fields[field]
                        field_name, field_desc = description.split(' - ', 1)
                        
                        st.markdown(f"""
                        <div class="required-container">
                            <h3>{field}</h3>
                            <p>{field_desc}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        mapped_columns[field] = st.selectbox(
                            f"Select your {field} column",
                            options=[""] + all_columns,
                            key=f"map_{field}",
                            label_visibility="collapsed"
                        )
                        if mapped_columns[field] == "":
                            mapped_columns[field] = None

        st.markdown("---")

        # Validate all mappings
        missing_mappings = [field for field, col in mapped_columns.items() if col is None]
        if missing_mappings:
            st.error(f"Please map all required columns. Missing: {', '.join(missing_mappings)}")
            st.stop()

        # Show mapping summary button
        if st.button("View Column Mapping Summary", use_container_width=False):
            mapping_data = {
                'Required Field': list(mapped_columns.keys()),
                'Your Column': list(mapped_columns.values()),
            }
            mapping_df = pd.DataFrame(mapping_data)
            st.dataframe(mapping_df, use_container_width=True)

        # --- Rename columns for internal processing ---
        df_processed = df.rename(columns=mapped_columns)

        # --- Perform calculations ---
        
        # 1. Gross Actual Incurred Claims
        df_processed["Gross_Actual_Incurred_Claims"] = (
            df_processed["Gross_Paid_Claims"] +
            df_processed["Gross_Closing_IBNR"] +
            df_processed["Gross_Closing_OCR"] -
            df_processed["Gross_Opening_IBNR"] -
            df_processed["Gross_Opening_OCR"]
        )
        
        # 2. Gross Earned Premiums
        df_processed["Gross_Earned_Premiums"] = (
            df_processed["Gross_Written_Premiums"] +
            df_processed["Gross_Opening_UPR"] -
            df_processed["Gross_Closing_UPR"]
        )
        
        # 3. Loss Ratio (avoid division by zero)
        df_processed["Loss_Ratio"] = np.where(
            df_processed["Gross_Earned_Premiums"] != 0,
            df_processed["Gross_Actual_Incurred_Claims"] / df_processed["Gross_Earned_Premiums"],
            np.nan
        )
        
        # 4. Commission Ratio
        df_processed["Commission_Ratio"] = np.where(
            df_processed["Gross_Written_Premiums"] != 0,
            df_processed["Gross_Commission_Paid"] / df_processed["Gross_Written_Premiums"],
            np.nan
        )
        
        # 5. Expense Ratio
        df_processed["Expense_Ratio"] = np.where(
            df_processed["Gross_Written_Premiums"] != 0,
            df_processed["Gross_Attributable_Expenses"] / df_processed["Gross_Written_Premiums"],
            np.nan
        )
        
        # 6. Risk Adjustment Ratio (sum of closing IBNR and OCR)
        risk_adjustment_denom = df_processed["Gross_Closing_IBNR"] + df_processed["Gross_Closing_OCR"]
        df_processed["Risk_Adjustment_Ratio"] = np.where(
            risk_adjustment_denom != 0,
            df_processed["Gross_Risk_Adjustment"] / risk_adjustment_denom,
            np.nan
        )
        
        # 7. Combined Ratio
        df_processed["Combined_Ratio"] = (
            df_processed["Loss_Ratio"] +
            df_processed["Commission_Ratio"] +
            df_processed["Expense_Ratio"] +
            df_processed["Risk_Adjustment_Ratio"]
        )
        
        # 8. Loss Component (excess above 100%)
        df_processed["Loss_Component"] = np.maximum(df_processed["Combined_Ratio"] - 1, 0) * df_processed["Gross_Closing_UPR"]
        
        # --- Aggregate results by Line of Business ---
        result = df_processed.groupby('Line_of_business').agg({
            'Gross_Written_Premiums': 'sum',
            'Gross_Earned_Premiums': 'sum',
            'Gross_Actual_Incurred_Claims': 'sum',
            'Loss_Ratio': 'mean',
            'Commission_Ratio': 'mean',
            'Expense_Ratio': 'mean',
            'Risk_Adjustment_Ratio': 'mean',
            'Combined_Ratio': 'mean',
            'Loss_Component': 'sum'
        }).reset_index()
        
        # Rename columns for clarity
        result = result.rename(columns={
            'Gross_Written_Premiums': 'Total_Written_Premiums',
            'Gross_Earned_Premiums': 'Total_Earned_Premiums',
            'Gross_Actual_Incurred_Claims': 'Total_Incurred_Claims'
        })
        
        # Display results
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Loss Component Results by Line of Business")
        
        # Format numeric columns for display
        display_result = result.copy()
        for col in display_result.columns:
            if col != 'Line_of_business':
                if 'Ratio' in col:
                    display_result[col] = display_result[col].apply(lambda x: f"{x:.2%}" if pd.notna(x) else "N/A")
                else:
                    display_result[col] = display_result[col].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
        
        st.dataframe(display_result, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Prepare Excel download (raw numbers, not formatted)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            result.to_excel(writer, index=False, sheet_name='Loss_Component_Results')
        output.seek(0)
        
        # Filename with client name
        safe_client = "".join(c for c in client_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        file_name = f"{safe_client}_Loss_Component_Results.xlsx" if safe_client else "Loss_Component_Results.xlsx"
        
        st.download_button(
            label="Download results as Excel",
            data=output,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Optional: Show raw data with all calculations
        with st.expander("View Detailed Calculations (all rows)"):
            # Format for display
            detail_display = df_processed.copy()
            for col in detail_display.columns:
                if 'Ratio' in col:
                    detail_display[col] = detail_display[col].apply(lambda x: f"{x:.2%}" if pd.notna(x) else "N/A")
                elif col not in ['Line_of_business'] and col not in list(mapped_columns.values()):
                    detail_display[col] = detail_display[col].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
            st.dataframe(detail_display, use_container_width=True)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.write("Please check your file format and column selections.")

st.markdown('</div>', unsafe_allow_html=True)  # close main-container

# ---------- Footer ----------
st.markdown("""
<div class="footer">
    <p>2026 African Actuarial Consultants. All rights reserved. | <a href="#">Privacy</a> | <a href="#">Terms</a></p>
    <p style="margin-top: 0.5rem; font-size: 0.9rem;">Powered by Vanababa</p>
</div>
""", unsafe_allow_html=True)
