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
        initial_sidebar_state="expanded"
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
    
    # Enhanced sidebar with glassmorphism design
    with st.sidebar:
        st.markdown("""
        <div class="glass-card">
            <h2 style="color: #2d3748; font-weight: 700; margin-bottom: 1.5rem; text-align: center;">
                📁 Upload Portfolio
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # File uploader with enhanced styling
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload your portfolio transactions in CSV format"
        )
        
        st.markdown("---")
        
        # Enhanced format instructions
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #4c51bf; margin-bottom: 1rem;">📋 Required CSV Format</h3>
            <div style="background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <p style="margin: 0; font-weight: 600; color: #2d3748;">Required Columns:</p>
                <ul style="margin: 0.5rem 0; color: #4a5568;">
                    <li><code>Date</code> - YYYY-MM-DD format</li>
                    <li><code>Type</code> - BUY or SELL</li>
                    <li><code>Stock</code> - Security name</li>
                    <li><code>Qty</code> - Quantity traded</li>
                    <li><code>Price</code> - Price per unit</li>
                    <li><code>Brokerage</code> - Brokerage charges</li>
                </ul>
                <p style="margin: 0.5rem 0 0 0; font-weight: 600; color: #2d3748;">Optional:</p>
                <ul style="margin: 0.5rem 0 0 0; color: #4a5568;">
                    <li><code>Dividend</code> - Dividend received</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced sample data with glassmorphism
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #4c51bf; margin-bottom: 1rem;">📄 Sample Format</h3>
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
                
                # Ultra-modern tax summary dashboard
                st.markdown("### 🎯 Tax Summary Dashboard")
                
                # Enhanced metric cards with custom styling
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card-ultra pulse-glow" style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%); color: white; text-align: center;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">📈</div>
                        <h2 style="margin: 0; font-size: 2.5rem; font-weight: 800;">₹{summary['Total STCG']:,.0f}</h2>
                        <p style="margin: 0.5rem 0; opacity: 0.9; font-size: 1.1rem; font-weight: 600;">Short Term Capital Gains</p>
                        <small style="opacity: 0.8; font-size: 0.9rem;">≤ 12 months holding period</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card-ultra pulse-glow" style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); color: white; text-align: center;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">🏆</div>
                        <h2 style="margin: 0; font-size: 2.5rem; font-weight: 800;">₹{summary['Total LTCG']:,.0f}</h2>
                        <p style="margin: 0.5rem 0; opacity: 0.9; font-size: 1.1rem; font-weight: 600;">Long Term Capital Gains</p>
                        <small style="opacity: 0.8; font-size: 0.9rem;">> 12 months holding period</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card-ultra pulse-glow" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); color: #2d3748; text-align: center;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">💎</div>
                        <h2 style="margin: 0; font-size: 2.5rem; font-weight: 800;">₹{summary['Total Dividends']:,.0f}</h2>
                        <p style="margin: 0.5rem 0; font-size: 1.1rem; font-weight: 600;">Total Dividends</p>
                        <small style="opacity: 0.7; font-size: 0.9rem;">Dividend income received</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="metric-card-ultra pulse-glow" style="background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%); color: #2d3748; text-align: center;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
                        <h2 style="margin: 0; font-size: 2.5rem; font-weight: 800;">₹{summary['Total GST on Brokerage']:,.0f}</h2>
                        <p style="margin: 0.5rem 0; font-size: 1.1rem; font-weight: 600;">GST on Brokerage</p>
                        <small style="opacity: 0.7; font-size: 0.9rem;">18% of total brokerage</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Ultra-modern final tax calculation
                st.markdown("---")
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### 🎯 Professional Tax Calculation")
                    
                    # Ultra-modern tax summary with glassmorphism
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); backdrop-filter: blur(15px); padding: 3rem 2rem; border-radius: 20px; color: white; margin: 1rem 0; box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4); position: relative; overflow: hidden;">
                        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 20% 80%, rgba(255,255,255,0.1) 0%, transparent 50%), radial-gradient(circle at 80% 20%, rgba(255,255,255,0.1) 0%, transparent 50%); pointer-events: none;"></div>
                        <div style="position: relative; z-index: 1;">
                            <h3 style="margin: 0 0 2rem 0; font-size: 1.5rem; font-weight: 700; text-align: center;">💼 Final Tax Breakdown</h3>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
                                <span style="font-size: 1.2rem; font-weight: 500;">Short Term Capital Gains (STCG)</span>
                                <span style="font-size: 1.4rem; font-weight: 700;">₹{summary['Total STCG']:,.2f}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
                                <span style="font-size: 1.2rem; font-weight: 500;">Long Term Capital Gains (LTCG)</span>
                                <span style="font-size: 1.4rem; font-weight: 700;">₹{summary['Total LTCG']:,.2f}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
                                <span style="font-size: 1.2rem; font-weight: 500;">Dividend Income</span>
                                <span style="font-size: 1.4rem; font-weight: 700;">₹{summary['Total Dividends']:,.2f}</span>
                            </div>
                            <div style="border-top: 2px solid rgba(255,255,255,0.3); padding-top: 1.5rem;">
                                <div style="display: flex; justify-content: space-between; align-items: center; padding: 1.5rem; background: rgba(255,255,255,0.2); border-radius: 15px;">
                                    <span style="font-size: 1.5rem; font-weight: 800;">Total Taxable Income</span>
                                    <span style="font-size: 2.2rem; font-weight: 900; color: #ffeaa7; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">₹{summary['Final Taxable Income']:,.2f}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("### 📊 Portfolio Statistics")
                    
                    # Enhanced statistics with glassmorphism
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4 style="margin-top: 0; color: #2b6cb0; font-weight: 700; text-align: center;">💼 Trading Summary</h4>
                        <div style="display: grid; gap: 1rem; margin-top: 1.5rem;">
                            <div style="background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%); padding: 1rem; border-radius: 10px; text-align: center;">
                                <div style="font-size: 1.5rem; font-weight: 700; color: #234e52;">₹{summary['Total Brokerage']:,.2f}</div>
                                <div style="font-size: 0.9rem; color: #285e61;">Total Brokerage</div>
                            </div>
                            <div style="background: linear-gradient(135deg, #fef5e7 0%, #fed7aa 100%); padding: 1rem; border-radius: 10px; text-align: center;">
                                <div style="font-size: 1.5rem; font-weight: 700; color: #744210;">₹{summary['Total GST on Brokerage']:,.2f}</div>
                                <div style="font-size: 0.9rem; color: #975a16;">GST (18%)</div>
                            </div>
                            <div style="background: linear-gradient(135deg, #e6f3ff 0%, #bae6fd 100%); padding: 1rem; border-radius: 10px; text-align: center;">
                                <div style="font-size: 1.5rem; font-weight: 700; color: #1e3a8a;">{summary['Total Trades Matched']}</div>
                                <div style="font-size: 0.9rem; color: #1e40af;">Trades Matched</div>
                            </div>
                            <div style="background: linear-gradient(135deg, #f0f9ff 0%, #dbeafe 100%); padding: 0.8rem; border-radius: 8px; display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; text-align: center;">
                                <div>
                                    <div style="font-size: 1.2rem; font-weight: 600; color: #1e40af;">{summary['Total Buy Trades']}</div>
                                    <div style="font-size: 0.8rem; color: #3b82f6;">Buy Orders</div>
                                </div>
                                <div>
                                    <div style="font-size: 1.2rem; font-weight: 600; color: #1e40af;">{summary['Total Sell Trades']}</div>
                                    <div style="font-size: 0.8rem; color: #3b82f6;">Sell Orders</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

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
        # Landing page content
        st.markdown("---")
        st.subheader("🚀 Get Started")
        st.markdown("""
        1. **Prepare your CSV file** with the required format (see sidebar)
        2. **Upload the file** using the file uploader in the sidebar
        3. **Review the results** including STCG, LTCG, and GST calculations
        4. **Download the analysis** for your tax filing
        """)
        
        # Features highlight
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🔥 Key Features:**
            - FIFO method calculation
            - Automatic STCG/LTCG classification
            - GST calculation on brokerage
            - Dividend income tracking
            """)
        
        with col2:
            st.markdown("""
            **📈 Supported:**
            - Equity transactions
            - Multiple stocks
            - Partial quantity matching
            - Date-based holding period
            """)
        
        with col3:
            st.markdown("""
            **💾 Export Options:**
            - Detailed trade analysis CSV
            - Tax summary CSV  
            - Ready for ITR filing
            - Professional formatting
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888;'>
        <p>Investor ITR & GST Calculator | Built with Streamlit</p>
        <p><small>⚠️ This tool is for informational purposes. Please consult a tax professional for official advice.</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()