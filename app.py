"""
Investor ITR & GST Calculator - Streamlit Application

A web application for calculating capital gains, GST, and tax liability
from investment portfolio CSV data using FIFO method.
"""

import streamlit as st
import pandas as pd
import io
from calculator import InvestorCalculator
from datetime import datetime


def main():
    # Page configuration with enhanced settings
    st.set_page_config(
        page_title="Investor ITR & GST Calculator",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="collapsed"  # Collapse sidebar since we're not using it
    )
    
    # Ultra-advanced CSS for modern, professional interface
    st.markdown("""
    <style>
    /* Import premium fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* CSS Variables for consistent theming */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        --glass-bg: rgba(255, 255, 255, 0.25);
        --glass-border: rgba(255, 255, 255, 0.18);
        --shadow-soft: 0 8px 32px rgba(31, 38, 135, 0.37);
        --shadow-hover: 0 15px 45px rgba(31, 38, 135, 0.5);
        --transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
    }
    
    /* Global styling with enhanced typography */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        padding-top: 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Ultra-modern header with advanced animations */
    .ultra-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%);
        background-size: 200% 200%;
        animation: gradientShift 6s ease infinite;
        padding: 4rem 2rem;
        border-radius: 24px;
        margin-bottom: 3rem;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    }
    
    .ultra-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: float 20s linear infinite;
        pointer-events: none;
    }
    
    .ultra-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 0; }
        50% { opacity: 1; }
    }
    
    .ultra-header h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 20px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
        background: linear-gradient(45deg, #ffffff, #f0f0f0, #ffffff);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: textShine 3s ease-in-out infinite;
    }
    
    @keyframes textShine {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Advanced feature cards with 3D effects */
    .feature-card-3d {
        background: linear-gradient(145deg, #ffffff, #f8f9ff);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        transition: var(--transition);
        box-shadow: 
            0 10px 30px rgba(102, 126, 234, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.6);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .feature-card-3d::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: var(--primary-gradient);
        opacity: 0;
        transition: var(--transition);
        z-index: 0;
    }
    
    .feature-card-3d:hover::before {
        opacity: 0.05;
    }
    
    .feature-card-3d:hover {
        transform: translateY(-10px) rotateX(5deg);
        box-shadow: 
            0 25px 50px rgba(102, 126, 234, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
    }
    
    /* Glassmorphism elements */
    .glass-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-soft);
        transition: var(--transition);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.35);
        box-shadow: var(--shadow-hover);
    }
    
    /* Enhanced buttons with animations */
    .stDownloadButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: var(--transition) !important;
        box-shadow: 
            0 8px 25px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stDownloadButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
        transition: var(--transition) !important;
    }
    
    .stDownloadButton > button:hover::before {
        left: 100% !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 
            0 15px 40px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Enhanced sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9ff 0%, #e8ecff 100%) !important;
        border-right: 1px solid rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Advanced metric cards */
    .metric-card-ultra {
        background: linear-gradient(145deg, #ffffff, #f7fafc);
        padding: 2rem;
        border-radius: 18px;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.7);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .metric-card-ultra:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }
    
    /* Enhanced data tables */
    .dataframe {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Custom scrollbar with gradient */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(248, 249, 255, 0.5);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 6px;
        border: 2px solid rgba(248, 249, 255, 0.5);
    }
    
    .pulse-glow {
        animation: pulseGlow 2s ease-in-out infinite;
    }
    
    @keyframes pulseGlow {
        0%, 100% { 
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        }
        50% { 
            box-shadow: 0 0 30px rgba(102, 126, 234, 0.6);
        }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .ultra-header h1 {
            font-size: 2.8rem;
        }
        
        .feature-card-3d {
            padding: 2rem 1.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Ultra-modern header section
    st.markdown("""
    <div class="ultra-header">
        <h1>💰 Investor Tax Calculator</h1>
        <h3>Professional ITR & GST Calculator with Advanced Analytics</h3>
        <p>Ultra-modern FIFO calculation engine for professional tax compliance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Advanced feature highlights with 3D cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card-3d">
            <div style="font-size: 2.5rem; margin-bottom: 1rem; text-align: center;">⚡</div>
            <h4 style="text-align: center; margin-bottom: 1rem; color: #2d3748; font-weight: 700;">FIFO Engine</h4>
            <p style="text-align: center; color: #4a5568; margin: 0;">Advanced First-In-First-Out calculation with precision matching</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card-3d">
            <div style="font-size: 2.5rem; margin-bottom: 1rem; text-align: center;">📊</div>
            <h4 style="text-align: center; margin-bottom: 1rem; color: #2d3748; font-weight: 700;">Smart Classification</h4>
            <p style="text-align: center; color: #4a5568; margin: 0;">Automatic STCG/LTCG classification with 12-month precision</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card-3d">
            <div style="font-size: 2.5rem; margin-bottom: 1rem; text-align: center;">💎</div>
            <h4 style="text-align: center; margin-bottom: 1rem; color: #2d3748; font-weight: 700;">GST Analytics</h4>
            <p style="text-align: center; color: #4a5568; margin: 0;">Professional 18% GST computation on all brokerage charges</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card-3d">
            <div style="font-size: 2.5rem; margin-bottom: 1rem; text-align: center;">🚀</div>
            <h4 style="text-align: center; margin-bottom: 1rem; color: #2d3748; font-weight: 700;">Export Ready</h4>
            <p style="text-align: center; color: #4a5568; margin: 0;">Professional reports formatted for ITR filing and CA consultation</p>
        </div>
        """, unsafe_allow_html=True)
    
    # File Upload Section (moved from sidebar to main page)
    st.markdown("---")
    st.markdown("### 📁 Upload Your Portfolio Data")
    
    # Create two columns for upload and instructions
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #2d3748; font-weight: 700; margin-bottom: 1.5rem; text-align: center;">
                📁 Upload CSV File
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # File uploader with enhanced styling
        uploaded_file = st.file_uploader(
            "Choose your portfolio CSV file",
            type=['csv'],
            help="Upload your portfolio transactions in CSV format"
        )
        
        # Enhanced sample data with glassmorphism
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #4c51bf; margin-bottom: 1rem;">📄 Sample Data Format</h4>
        </div>
        """, unsafe_allow_html=True)
        
        sample_df = pd.DataFrame({
            'Date': ['2023-01-15', '2023-06-20', '2024-02-10'],
            'Type': ['BUY', 'BUY', 'SELL'],
            'Stock': ['RELIANCE', 'RELIANCE', 'RELIANCE'],
            'Qty': [100, 50, 75],
            'Price': [2500.0, 2600.0, 2800.0],
            'Brokerage': [25.0, 15.0, 20.0]
        })
        st.dataframe(sample_df, use_container_width=True)
    
    with col2:
        # Enhanced format instructions
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #4c51bf; margin-bottom: 1rem;">📋 Required CSV Format</h3>
            <div style="background: rgba(102, 126, 234, 0.1); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                <h4 style="margin: 0 0 1rem 0; font-weight: 700; color: #2d3748;">✅ Required Columns:</h4>
                <div style="display: grid; gap: 0.8rem; color: #4a5568; font-size: 0.95rem;">
                    <div style="display: flex; align-items: center;"><code style="background: rgba(102, 126, 234, 0.2); padding: 0.3rem 0.6rem; border-radius: 4px; margin-right: 0.5rem; font-weight: 600;">Date</code> Transaction date (YYYY-MM-DD)</div>
                    <div style="display: flex; align-items: center;"><code style="background: rgba(102, 126, 234, 0.2); padding: 0.3rem 0.6rem; border-radius: 4px; margin-right: 0.5rem; font-weight: 600;">Type</code> BUY or SELL</div>
                    <div style="display: flex; align-items: center;"><code style="background: rgba(102, 126, 234, 0.2); padding: 0.3rem 0.6rem; border-radius: 4px; margin-right: 0.5rem; font-weight: 600;">Stock</code> Stock/Security name</div>
                    <div style="display: flex; align-items: center;"><code style="background: rgba(102, 126, 234, 0.2); padding: 0.3rem 0.6rem; border-radius: 4px; margin-right: 0.5rem; font-weight: 600;">Qty</code> Quantity traded</div>
                    <div style="display: flex; align-items: center;"><code style="background: rgba(102, 126, 234, 0.2); padding: 0.3rem 0.6rem; border-radius: 4px; margin-right: 0.5rem; font-weight: 600;">Price</code> Price per unit</div>
                    <div style="display: flex; align-items: center;"><code style="background: rgba(102, 126, 234, 0.2); padding: 0.3rem 0.6rem; border-radius: 4px; margin-right: 0.5rem; font-weight: 600;">Brokerage</code> Brokerage charges</div>
                </div>
                <h4 style="margin: 1.5rem 0 0.5rem 0; font-weight: 700; color: #2d3748;">✨ Optional Column:</h4>
                <div style="color: #4a5568; font-size: 0.95rem;">
                    <div style="display: flex; align-items: center;"><code style="background: rgba(102, 126, 234, 0.2); padding: 0.3rem 0.6rem; border-radius: 4px; margin-right: 0.5rem; font-weight: 600;">Dividend</code> Dividend received (if any)</div>
                </div>
            </div>
            <div style="background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #38b2ac;">
                <h4 style="margin: 0 0 1rem 0; color: #234e52; font-weight: 700;">💡 Quick Tips:</h4>
                <ul style="margin: 0; color: #285e61; font-size: 0.9rem; line-height: 1.6;">
                    <li>Ensure dates are in YYYY-MM-DD format</li>
                    <li>Type should be exactly 'BUY' or 'SELL'</li>
                    <li>All numeric values should be positive</li>
                    <li>Stock names should be consistent across transactions</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Main content area with enhanced processing
    if uploaded_file is not None:
        try:
            # Initialize calculator
            calculator = InvestorCalculator()
            
            # Enhanced loading animation
            with st.spinner("🔄 Processing your portfolio with AI precision..."):
                results_df, summary = calculator.process_portfolio(uploaded_file)
            
            # Display results with ultra-modern design
            if not results_df.empty:
                # Ultra-modern success banner
                st.markdown("""
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 20px; color: white; text-align: center; margin: 2rem 0; box-shadow: 0 15px 40px rgba(79, 172, 254, 0.3); position: relative; overflow: hidden;">
                    <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px); background-size: 30px 30px; animation: float 15s linear infinite; pointer-events: none;"></div>
                    <h2 style="margin: 0 0 0.5rem 0; font-size: 2rem; font-weight: 800; position: relative; z-index: 1;">✨ Portfolio Analysis Complete!</h2>
                    <p style="margin: 0; opacity: 0.9; font-size: 1.2rem; position: relative; z-index: 1;">Your professional tax calculations are ready for review</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Simplified Calculator Preview Section
                st.markdown("---")
                st.markdown("### 📊 Quick Calculator Preview")
                
                # Create tabs for ITR and GST calculators
                tab1, tab2 = st.tabs(["📈 ITR Calculator", "🧮 GST Calculator"])
                
                with tab1:
                    st.markdown("""
                    <div style="background: #f8fafc; padding: 2rem; border-radius: 16px; margin: 1rem 0; border: 1px solid #e2e8f0;">
                        <h4 style="color: #1a365d; margin: 0 0 1.5rem 0; font-weight: 700; font-size: 1.2rem;">Capital Gains & Dividends Calculator</h4>
                        <p style="color: #4a5568; margin: 0 0 1.5rem 0; font-size: 0.95rem;">Calculate your tax liability on capital gains and dividend income</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if not results_df.empty:
                        # Add summary cards first
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            total_gains = results_df['Gain/Loss'].sum()
                            gain_color = "#22c55e" if total_gains >= 0 else "#ef4444"
                            gain_symbol = "+" if total_gains >= 0 else ""
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c8 100%); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #a3d977;">
                                <h3 style="margin: 0 0 0.5rem 0; color: {gain_color}; font-size: 1.8rem; font-weight: 800;">{gain_symbol}₹{total_gains:,.0f}</h3>
                                <p style="margin: 0; color: #2d5016; font-weight: 600;">Total Gains/Loss</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            stcg_amount = summary['Total STCG']
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #fef3e2 0%, #fed7aa 100%); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #fb8500;">
                                <h3 style="margin: 0 0 0.5rem 0; color: #c2410c; font-size: 1.8rem; font-weight: 800;">₹{stcg_amount:,.0f}</h3>
                                <p style="margin: 0; color: #9a3412; font-weight: 600;">STCG (≤ 12m)</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            ltcg_amount = summary['Total LTCG']
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #0284c7;">
                                <h3 style="margin: 0 0 0.5rem 0; color: #0c4a6e; font-size: 1.8rem; font-weight: 800;">₹{ltcg_amount:,.0f}</h3>
                                <p style="margin: 0; color: #075985; font-weight: 600;">LTCG (> 12m)</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Create a simplified stock summary table
                    if not results_df.empty:
                        # Group by stock and calculate summary
                        stock_summary = results_df.groupby('Stock').agg({
                            'Buy Price': 'mean',
                            'Sell Price': 'mean', 
                            'Qty': 'sum',
                            'Gain/Loss': 'sum'
                        }).round(2)
                        
                        # Create the preview table using Streamlit's native dataframe with custom styling
                        st.markdown("""
                        <style>
                        .stDataFrame {
                            background: white;
                            border-radius: 12px;
                            overflow: hidden;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                            border: 1px solid #e2e8f0;
                        }
                        .stDataFrame [data-testid="stTable"] {
                            background: white;
                        }
                        .stDataFrame th {
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                            color: white !important;
                            font-weight: 600 !important;
                            text-align: center !important;
                            padding: 1rem !important;
                        }
                        .stDataFrame td {
                            text-align: center !important;
                            padding: 0.8rem !important;
                            border-bottom: 1px solid #f1f5f9 !important;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        # Prepare the display dataframe
                        display_df = stock_summary.copy()
                        display_df['Buy Price'] = display_df['Buy Price'].apply(lambda x: f"₹{x:,.0f}")
                        display_df['Sell Price'] = display_df['Sell Price'].apply(lambda x: f"₹{x:,.0f}")
                        display_df['Qty'] = display_df['Qty'].apply(lambda x: f"{x:,.0f}")
                        display_df['Gain/Loss'] = display_df['Gain/Loss'].apply(
                            lambda x: f"₹{x:+,.0f}" if x >= 0 else f"₹{x:,.0f}"
                        )
                        
                        # Rename columns for better display
                        display_df.columns = ['Buy Price (₹)', 'Sell Price (₹)', 'Quantity', 'Gain/Loss (₹)']
                        
                        # Display the dataframe
                        st.dataframe(
                            display_df,
                            use_container_width=True,
                            height=400
                        )
                        
                        # Calculate ITR button and summary
                        st.markdown("<br>", unsafe_allow_html=True)
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            total_taxable = summary['Final Taxable Income']
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 16px; text-align: center; color: white; margin: 1rem 0; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);">
                                <h4 style="margin: 0 0 0.5rem 0; font-weight: 700;">Total Taxable Income</h4>
                                <h2 style="margin: 0 0 1rem 0; font-size: 2.2rem; font-weight: 900;">₹{total_taxable:,.0f}</h2>
                                <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Ready for ITR filing</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                with tab2:
                    st.markdown("""
                    <div style="background: #f0fdf4; padding: 2rem; border-radius: 16px; margin: 1rem 0; border: 1px solid #bbf7d0;">
                        <h4 style="color: #14532d; margin: 0 0 1.5rem 0; font-weight: 700; font-size: 1.2rem;">GST Calculator</h4>
                        <p style="color: #4a5568; margin: 0 0 1.5rem 0; font-size: 0.95rem;">Calculate GST on brokerage charges (18% rate)</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if not results_df.empty:
                        # GST Summary Cards
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #81d4fa;">
                                <h3 style="margin: 0 0 0.5rem 0; color: #01579b; font-size: 1.8rem; font-weight: 800;">₹{summary['Total Brokerage']:,.0f}</h3>
                                <p style="margin: 0; color: #0277bd; font-weight: 600;">Total Brokerage</p>
                                <small style="color: #0288d1; opacity: 0.8;">Before GST</small>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffcc02 100%); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #ffb300;">
                                <h3 style="margin: 0 0 0.5rem 0; color: #e65100; font-size: 1.8rem; font-weight: 800;">₹{summary['Total GST on Brokerage']:,.0f}</h3>
                                <p style="margin: 0; color: #ef6c00; font-weight: 600;">Total GST (18%)</p>
                                <small style="color: #f57c00; opacity: 0.8;">On brokerage charges</small>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            total_with_gst = summary['Total Brokerage'] + summary['Total GST on Brokerage']
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #f3e8ff 0%, #ddd6fe 100%); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #a855f7;">
                                <h3 style="margin: 0 0 0.5rem 0; color: #6b21a8; font-size: 1.8rem; font-weight: 800;">₹{total_with_gst:,.0f}</h3>
                                <p style="margin: 0; color: #7c3aed; font-weight: 600;">Total with GST</p>
                                <small style="color: #8b5cf6; opacity: 0.8;">Brokerage + GST</small>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # GST Breakdown Table by Stock
                        st.markdown("""
                        <h5 style="color: #2d3748; margin: 1.5rem 0 1rem 0; font-weight: 700;">GST Breakdown by Stock:</h5>
                        """)
                        
                        # Create GST breakdown by stock
                        gst_breakdown = results_df.groupby('Stock').agg({
                            'Brokerage': 'sum',
                            'GST on Brokerage': 'sum'
                        }).round(2)
                        
                        # Add calculated columns
                        gst_breakdown['Total Cost'] = gst_breakdown['Brokerage'] + gst_breakdown['GST on Brokerage']
                        
                        # Apply custom styling for GST table
                        st.markdown("""
                        <style>
                        .gst-dataframe {
                            background: white;
                            border-radius: 12px;
                            overflow: hidden;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                            border: 1px solid #e2e8f0;
                        }
                        .gst-dataframe [data-testid="stTable"] {
                            background: white;
                        }
                        .gst-dataframe th {
                            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
                            color: white !important;
                            font-weight: 600 !important;
                            text-align: center !important;
                            padding: 1rem !important;
                        }
                        .gst-dataframe td {
                            text-align: center !important;
                            padding: 0.8rem !important;
                            border-bottom: 1px solid #f1f5f9 !important;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        # Prepare display dataframe for GST
                        gst_display_df = gst_breakdown.copy()
                        gst_display_df['Brokerage'] = gst_display_df['Brokerage'].apply(lambda x: f"₹{x:,.2f}")
                        gst_display_df['GST on Brokerage'] = gst_display_df['GST on Brokerage'].apply(lambda x: f"₹{x:,.2f}")
                        gst_display_df['Total Cost'] = gst_display_df['Total Cost'].apply(lambda x: f"₹{x:,.2f}")
                        
                        # Rename columns for better display
                        gst_display_df.columns = ['Brokerage (₹)', 'GST Amount (₹)', 'Total Cost (₹)']
                        
                        # Display the GST dataframe with custom class
                        st.markdown('<div class="gst-dataframe">', unsafe_allow_html=True)
                        st.dataframe(
                            gst_display_df,
                            use_container_width=True,
                            height=350
                        )
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # GST Details
                        st.markdown("""
                        <div style="background: white; padding: 1.5rem; border-radius: 12px; margin: 1.5rem 0; border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                            <h5 style="margin: 0 0 1rem 0; color: #2d3748; font-weight: 700;">GST Calculation Details:</h5>
                            <div style="display: grid; gap: 0.5rem; color: #4a5568; font-size: 0.9rem;">
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #f1f5f9;">
                                    <span>Brokerage Amount:</span>
                                    <span style="font-weight: 600;">₹{:.2f}</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #f1f5f9;">
                                    <span>GST Rate:</span>
                                    <span style="font-weight: 600;">18%</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; color: #e65100; font-weight: 700;">
                                    <span>Total GST:</span>
                                    <span>₹{:.2f}</span>
                                </div>
                            </div>
                        </div>
                        """.format(summary['Total Brokerage'], summary['Total GST on Brokerage']), unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Download Section
                st.markdown("""
                <div style="text-align: center; margin: 2rem 0;">
                    <h3 style="color: #2d3748; font-weight: 700; margin-bottom: 1.5rem;">📥 Download Detailed Results</h3>
                    <p style="color: #4a5568; margin-bottom: 2rem; font-size: 1rem;">Export complete trade-by-trade analysis for tax filing</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Center the download button
                col1, col2, col3 = st.columns([2, 1, 2])
                
                with col2:
                    # Prepare CSV data for download
                    csv_buffer = io.StringIO()
                    results_df.to_csv(csv_buffer, index=False)
                    csv_data = csv_buffer.getvalue()
                    
                    st.download_button(
                        label="📊 Download Report (CSV)",
                        data=csv_data,
                        file_name=f"tax_calculation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        help="Download complete trade-by-trade analysis for tax filing",
                        use_container_width=True
                    )
                


            else:
                st.warning("⚠️ No trades could be matched. Please check your data format.")
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.markdown("""
            **Please check:**
            - CSV file format matches the required structure
            - All required columns are present
            - Date format is YYYY-MM-DD
            - Numeric values are valid
            - Type column contains only 'BUY' or 'SELL'
            """)
    
    else:
        # Enhanced landing page with better instructions
        st.markdown("---")
        st.markdown("### 🚀 How to Get Started")
        
        # Enhanced getting started section
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4ecdc4 100%); padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; text-align: center; box-shadow: 0 15px 40px rgba(240, 147, 251, 0.3);">
            <h3 style="margin: 0 0 1rem 0; font-size: 2rem; font-weight: 700;">✨ Professional Tax Calculation in 3 Simple Steps</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 2rem;">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📁</div>
                    <h4 style="margin: 0 0 0.5rem 0; font-weight: 600;">1. Prepare Your Data</h4>
                    <p style="margin: 0; opacity: 0.9; font-size: 1rem;">Use the format shown above with all required columns</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
                    <h4 style="margin: 0 0 0.5rem 0; font-weight: 600;">2. Upload & Process</h4>
                    <p style="margin: 0; opacity: 0.9; font-size: 1rem;">Our FIFO engine calculates everything instantly</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📈</div>
                    <h4 style="margin: 0 0 0.5rem 0; font-weight: 600;">3. Download Results</h4>
                    <p style="margin: 0; opacity: 0.9; font-size: 1rem;">Get professional reports for ITR filing</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced features section with glassmorphism cards
        st.markdown("### 🎆 Why Choose Our Calculator?")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔥</div>
                <h4 style="color: #2d3748; font-weight: 700; margin-bottom: 1rem;">Core Features</h4>
                <div style="text-align: left; color: #4a5568; line-height: 1.8;">
                    ✅ <strong>FIFO Method</strong> - Industry standard calculation<br>
                    ✅ <strong>Auto Classification</strong> - STCG/LTCG detection<br>
                    ✅ <strong>GST Calculation</strong> - 18% on brokerage charges<br>
                    ✅ <strong>Dividend Tracking</strong> - Complete income analysis
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📈</div>
                <h4 style="color: #2d3748; font-weight: 700; margin-bottom: 1rem;">Supported Transactions</h4>
                <div style="text-align: left; color: #4a5568; line-height: 1.8;">
                    📊 <strong>Equity Trading</strong> - All stock transactions<br>
                    📊 <strong>Multiple Stocks</strong> - Portfolio-wide analysis<br>
                    📊 <strong>Partial Matching</strong> - Precise quantity handling<br>
                    📊 <strong>Date Intelligence</strong> - Smart holding period calculation
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💾</div>
                <h4 style="color: #2d3748; font-weight: 700; margin-bottom: 1rem;">Professional Reports</h4>
                <div style="text-align: left; color: #4a5568; line-height: 1.8;">
                    📝 <strong>Detailed Analysis</strong> - Trade-by-trade breakdown<br>
                    📝 <strong>Tax Summary</strong> - Ready for CA consultation<br>
                    📝 <strong>ITR Ready</strong> - Formatted for tax filing<br>
                    📝 <strong>CSV Export</strong> - Professional formatting
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Call to action with scroll-to-upload
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0 2rem 0;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 16px; color: white; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);">
                <h3 style="margin: 0 0 1rem 0; font-weight: 700;">👆 Ready to Calculate Your Taxes?</h3>
                <p style="margin: 0 0 1rem 0; opacity: 0.9; font-size: 1.1rem;">Scroll up to the upload section and get started with your portfolio analysis!</p>
                <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                    <small style="opacity: 0.8;">⬆️ Upload your CSV file in the section above to begin</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced footer with better formatting
    st.markdown("---")
    
    # Feature highlights section
    st.markdown("### 🌟 Why Choose Our Calculator")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e6f3ff 0%, #bae6fd 100%); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #93c5fd;">
            <h4 style="color: #1e40af; margin: 0 0 0.8rem 0; font-weight: 700; font-size: 1.1rem;">⚡ Ultra-Fast Processing</h4>
            <p style="color: #374151; margin: 0; font-size: 0.9rem; line-height: 1.5;">Advanced FIFO algorithm processes thousands of transactions in seconds</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #6ee7b7;">
            <h4 style="color: #047857; margin: 0 0 0.8rem 0; font-weight: 700; font-size: 1.1rem;">🔒 Secure & Private</h4>
            <p style="color: #374151; margin: 0; font-size: 0.9rem; line-height: 1.5;">No data storage - all calculations happen in real-time on your browser</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fae8ff 0%, #f3e8ff 100%); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #d8b4fe;">
            <h4 style="color: #7c3aed; margin: 0 0 0.8rem 0; font-weight: 700; font-size: 1.1rem;">📊 Professional Reports</h4>
            <p style="color: #374151; margin: 0; font-size: 0.9rem; line-height: 1.5;">Export-ready formats for CAs and tax filing software</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Simple footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; border-top: 1px solid #e5e7eb; margin-top: 2rem;">
        <p style="color: #6b7280; margin: 0; font-size: 0.9rem;">©  Investor ITR & GST Calculator | Powered by Advanced FIFO Algorithm</p>
        <p style="color: #9ca3af; margin: 0.5rem 0 0 0; font-size: 0.8rem;">Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
