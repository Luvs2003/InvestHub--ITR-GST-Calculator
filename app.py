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
    
    # Clean, fresh CSS theme
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    :root {
        --bg: #f6f7fb;
        --card: #ffffff;
        --text: #0f172a;
        --muted: #475569;
        --primary: #6d28d9; /* purple */
        --primary-600: #5b21b6;
        --accent: #0ea5a4; /* teal */
        --border: #e5e7eb;
        --radius: 14px;
        --shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
    }

    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--bg);
    }

    .hero {
        background: radial-gradient(1200px 500px at 10% -10%, #7c3aed 10%, transparent 60%),
                    radial-gradient(1000px 500px at 90% 0%, #4f46e5 10%, transparent 60%),
                    linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: #fff;
        text-align: left;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(79,70,229,0.25);
        position: relative;
        overflow: hidden;
    }
    .hero::after {
        content: '';
        position: absolute;
        inset: 0;
        background-image: radial-gradient(#ffffff33 2px, transparent 2px);
        background-size: 28px 28px;
        opacity: .25;
        pointer-events: none;
    }
    .hero-title { font-size: 2.25rem; font-weight: 800; margin: 0 0 .5rem 0; }
    .hero-sub { max-width: 720px; color: #e9e9ff; margin: 0 0 1rem 0; font-size: 1rem; }
    .badge-row { display:flex; gap:.5rem; align-items:center; margin-top:.75rem; }
    .pill { background:#ffffff1a; border:1px solid #ffffff33; color:#fff; padding:.35rem .65rem; border-radius:999px; font-size:.8rem; }
    .hero-cta { display:flex; gap:.75rem; margin-top:1rem; }
    .hero-btn { background:#fff; color:#4f46e5; padding:.6rem 1rem; border-radius:10px; font-weight:700; border:1px solid #e5e7eb; }

    .feature-card-3d {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: var(--shadow);
    }

    .glass-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.25rem;
        box-shadow: var(--shadow);
    }

    .stDownloadButton > button {
        background: var(--primary) !important;
        color: #fff !important;
        border: 1px solid var(--primary-600) !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.25rem !important;
        font-weight: 600 !important;
    }

    .stDataFrame th {
        background: var(--primary) !important;
        color: #fff !important;
        font-weight: 600 !important;
        text-align: center !important;
    }
    .stDataFrame td { text-align: center !important; }

    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 6px; }

    /* Top navbar */
    .topnav { position: sticky; top: 0; z-index: 100; background: rgba(255,255,255,0.9); backdrop-filter: saturate(180%) blur(8px); border-bottom: 1px solid var(--border); padding:.6rem 1rem; margin-bottom:1rem; border-radius:12px; box-shadow: var(--shadow); }
    .topnav .links { display:flex; gap:1rem; align-items:center; }
    .topnav a { color: var(--text); text-decoration:none; font-weight:600; padding:.35rem .6rem; border-radius:8px; }
    .topnav a:hover { background:#f1f5f9; }

    /* Stepper */
    .stepper { display:flex; gap:1rem; align-items:center; justify-content:center; margin: 0.5rem 0 1rem; }
    .step { display:flex; align-items:center; gap:.5rem; color:#64748b; }
    .dot { width:28px; height:28px; border-radius:999px; display:inline-flex; align-items:center; justify-content:center; border:2px solid #cbd5e1; background:#fff; font-weight:700; }
    .active .dot { border-color: var(--primary); background: var(--primary); color:#fff; }
    .active { color: var(--text); font-weight:700; }

    /* Material-style cards (Google colors) */
    .material-card { background:#fff; border:1px solid var(--border); border-radius:16px; box-shadow:0 6px 16px rgba(0,0,0,.06); padding:1.25rem 1.5rem; text-align:left; display:flex; gap:1rem; align-items:flex-start; min-height:160px; }
    .material-icon { width:56px; height:56px; border-radius:14px; display:inline-flex; align-items:center; justify-content:center; color:#fff; font-size:1.25rem; font-weight:800; flex:0 0 56px; }
    .mat-blue { background:#2196F3; }
    .mat-green { background:#4CAF50; }
    .mat-amber { background:#FFC107; color:#111; }
    .mat-red { background:#F44336; }
    .material-title { margin:0 0 .25rem 0; font-weight:700; color:var(--text); font-size:1.15rem; }
    .material-sub { margin:0; color:#64748b; font-size:.97rem; line-height:1.55; }

    /* Benefits section */
    .benefits-wrap { padding: 1.5rem 0 0.5rem; }
    .benefits-title { display:flex; align-items:center; gap:.5rem; font-weight:800; color:var(--text); margin:0 0 0.75rem 0; }
    .benefit-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1rem; }
    .benefit-card { background:#fff; border:1px solid var(--border); border-radius:18px; padding:1.25rem 1.25rem; box-shadow:0 10px 28px rgba(79,70,229,.06); }
    .benefit-card h4 { text-align:center; margin:.5rem 0 1rem 0; }
    .benefit-item { display:flex; align-items:center; gap:.5rem; color:#334155; margin:.35rem 0; }
    .benefit-bullet { color:#10b981; }

    /* Gradient CTA */
    .cta { margin-top:1rem; background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); border-radius:18px; padding:1.5rem 1rem; color:#fff; box-shadow:0 16px 40px rgba(79,70,229,.2); }
    .cta h3 { margin:0 0 .5rem 0; display:flex; align-items:center; gap:.5rem; }
    .cta-bar { margin-top:.75rem; background: linear-gradient(90deg, rgba(255,255,255,.25), rgba(255,255,255,.15)); height:44px; border-radius:10px; border:1px solid rgba(255,255,255,.3); display:flex; align-items:center; justify-content:center; font-size:.85rem; color:#e8e8ff; }

    /* Intro feature cards (four-up) */
    .feature-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:1rem; margin: .5rem 0 1.25rem; }
    .feature-card { background:#fff; border:1px solid var(--border); border-radius:18px; padding:1.25rem; text-align:center; box-shadow:0 12px 30px rgba(15,23,42,.06); }
    .feature-icon { width:40px; height:40px; border-radius:12px; margin:0 auto .5rem; display:flex; align-items:center; justify-content:center; font-size:1.25rem; }
    .fx-blue { background:#e0f2fe; color:#0369a1; }
    .fx-green { background:#dcfce7; color:#166534; }
    .fx-purple { background:#ede9fe; color:#6d28d9; }
    .fx-pink { background:#ffe4e6; color:#be185d; }
    </style>
    """, unsafe_allow_html=True)
    
    # Navbar
    st.markdown("""
    <div class="topnav">
        <div class="links">
            <a href="#top">Home</a>
            <a href="#upload">Upload</a>
            <a href="#results">Results</a>
            <a href="#download">Download</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero header section (purple style like reference)
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Calculate your tax liabilities</div>
        <div class="hero-sub">Upload your portfolio CSV and get professional ITR and GST-ready summaries using a precise FIFO engine. Clean, exportable results for quick filing.</div>
        <div class="hero-cta">
            <span class="pill">Fast • Accurate • Private</span>
            <span class="pill">No signup required</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Four-up feature row under hero
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon fx-blue">⚡</div>
            <h4 style="margin:.25rem 0 .25rem 0;">FIFO Engine</h4>
            <p style="margin:0;color:#64748b;">Advanced First-In-First-Out calculation with precision matching</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon fx-green">📊</div>
            <h4 style="margin:.25rem 0 .25rem 0;">Smart Classification</h4>
            <p style="margin:0;color:#64748b;">Automatic STCG/LTCG classification with 12-month precision</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon fx-purple">💎</div>
            <h4 style="margin:.25rem 0 .25rem 0;">GST Analytics</h4>
            <p style="margin:0;color:#64748b;">Professional 18% GST computation on all brokerage charges</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon fx-pink">🚀</div>
            <h4 style="margin:.25rem 0 .25rem 0;">Export Ready</h4>
            <p style="margin:0;color:#64748b;">Professional reports formatted for ITR filing and CA consultation</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stepper progress indicator
    if 'has_results' not in st.session_state:
        st.session_state['has_results'] = False
    active_results = 'active' if st.session_state['has_results'] else ''
    st.markdown(f"""
    <div class="stepper">
        <div class="step active"><span class="dot">1</span>Upload</div>
        <div class="step {active_results}"><span class="dot">2</span>Results</div>
        <div class="step {active_results}"><span class="dot">3</span>Download</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Keep header minimal and remove extra feature cards for a cleaner look
    
    # File Upload Section (centered)
    st.markdown("---")
    st.markdown("""
    <a id="upload"></a>
    <h3 style="text-align:center; margin-top:0;">📁 Upload Your Portfolio Data</h3>
    """, unsafe_allow_html=True)
    left, center, right = st.columns([1, 2, 1])
    with center:
        st.markdown("""
        <div class="glass-card" style="text-align:center;">
            <h3 style="margin:0 0 1rem 0; font-weight:700; color: var(--text);">📁 Upload CSV File</h3>
        </div>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose your portfolio CSV file",
            type=['csv'],
            help="Upload your portfolio transactions in CSV format"
        )
        with st.expander("See sample data format"):
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
            
            # Mark results available in session state
            st.session_state['has_results'] = (results_df is not None and not results_df.empty)
            
            # Display results with ultra-modern design
            if not results_df.empty:
                st.markdown("<a id=\"results\"></a>", unsafe_allow_html=True)
                # Success banner (clean)
                st.markdown("""
                <div style="background: #e0f2fe; padding: 1.25rem; border-radius: 14px; color: #0c4a6e; text-align: center; margin: 1.25rem 0; border:1px solid #bae6fd;">
                    <h2 style="margin: 0 0 0.25rem 0; font-size: 1.5rem; font-weight: 700;">✨ Portfolio analysis complete</h2>
                    <p style="margin: 0; opacity: 0.9; font-size: 0.95rem;">Your tax calculations are ready</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Simplified Calculator Preview Section
                st.markdown("---")
                st.markdown("### 📊 Quick Calculator Preview")
                
                # Create tabs for ITR and GST calculators
                tab1, tab2 = st.tabs(["📈 ITR Calculator", "🧮 GST Calculator"])
                
                with tab1:
                    st.markdown("""
                    <div style="background: #f8fafc; padding: 1.25rem; border-radius: 12px; margin: 0.75rem 0; border: 1px solid #e2e8f0;">
                        <h4 style="color: #0f172a; margin: 0 0 0.75rem 0; font-weight: 700; font-size: 1.05rem;">Capital Gains & Dividends</h4>
                        <p style="color: #475569; margin: 0; font-size: 0.9rem;">Tax liability on capital gains and dividend income</p>
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
                            <div style=\"background:#ecfeff;padding:1rem;border-radius:10px;text-align:center;border:1px solid #bae6fd;\">
                                <h3 style=\"margin:0 0 0.25rem 0;color:{gain_color};font-size:1.4rem;font-weight:800;\">{gain_symbol}₹{total_gains:,.0f}</h3>
                                <p style=\"margin:0;color:#0f172a;font-weight:600;\">Total Gains/Loss</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            stcg_amount = summary['Total STCG']
                            st.markdown(f"""
                            <div style=\"background:#fff7ed;padding:1rem;border-radius:10px;text-align:center;border:1px solid #fed7aa;\">
                                <h3 style=\"margin:0 0 0.25rem 0;color:#c2410c;font-size:1.4rem;font-weight:800;\">₹{stcg_amount:,.0f}</h3>
                                <p style=\"margin:0;color:#9a3412;font-weight:600;\">STCG (≤ 12m)</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            ltcg_amount = summary['Total LTCG']
                            st.markdown(f"""
                            <div style=\"background:#eff6ff;padding:1rem;border-radius:10px;text-align:center;border:1px solid #bfdbfe;\">
                                <h3 style=\"margin:0 0 0.25rem 0;color:#1d4ed8;font-size:1.4rem;font-weight:800;\">₹{ltcg_amount:,.0f}</h3>
                                <p style=\"margin:0;color:#1e40af;font-weight:600;\">LTCG (> 12m)</p>
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
                        .stDataFrame { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; }
                        .stDataFrame td { padding: 0.6rem !important; border-bottom: 1px solid #f1f5f9 !important; }
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
                            <div style=\"background:#1d4ed8;padding:1rem;border-radius:12px;text-align:center;color:#fff;border:1px solid #1e40af;\">
                                <h4 style=\"margin:0 0 0.25rem 0;font-weight:700;\">Total Taxable Income</h4>
                                <h2 style=\"margin:0;font-size:1.8rem;font-weight:900;\">₹{total_taxable:,.0f}</h2>
                            </div>
                            """, unsafe_allow_html=True)
                    
                with tab2:
                    st.markdown("""
                    <div style="background:#ecfeff;padding:1.25rem;border-radius:12px;margin:0.75rem 0;border:1px solid #bae6fd;">
                        <h4 style="color:#0f172a;margin:0 0 0.75rem 0;font-weight:700;font-size:1.05rem;">GST Calculator</h4>
                        <p style="color:#475569;margin:0;font-size:0.9rem;">GST on brokerage charges (18%)</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if not results_df.empty:
                        # GST Summary Cards
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"""
                            <div style=\"background:#f8fafc;padding:1rem;border-radius:10px;text-align:center;border:1px solid #e2e8f0;\">
                                <h3 style=\"margin:0 0 0.25rem 0;color:#0f172a;font-size:1.4rem;font-weight:800;\">₹{summary['Total Brokerage']:,.0f}</h3>
                                <p style=\"margin:0;color:#334155;font-weight:600;\">Total Brokerage</p>
                                <small style=\"color:#64748b;opacity:0.9;\">Before GST</small>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div style=\"background:#fff7ed;padding:1rem;border-radius:10px;text-align:center;border:1px solid #fed7aa;\">
                                <h3 style=\"margin:0 0 0.25rem 0;color:#c2410c;font-size:1.4rem;font-weight:800;\">₹{summary['Total GST on Brokerage']:,.0f}</h3>
                                <p style=\"margin:0;color:#9a3412;font-weight:600;\">Total GST (18%)</p>
                                <small style=\"color:#9a3412;opacity:0.9;\">On brokerage</small>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            total_with_gst = summary['Total Brokerage'] + summary['Total GST on Brokerage']
                            st.markdown(f"""
                            <div style=\"background:#f5f3ff;padding:1rem;border-radius:10px;text-align:center;border:1px solid #ddd6fe;\">
                                <h3 style=\"margin:0 0 0.25rem 0;color:#5b21b6;font-size:1.4rem;font-weight:800;\">₹{total_with_gst:,.0f}</h3>
                                <p style=\"margin:0;color:#6d28d9;font-weight:600;\">Total with GST</p>
                                <small style=\"color:#6d28d9;opacity:0.9;\">Brokerage + GST</small>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # GST Breakdown Table by Stock
                        st.markdown("""
                        <h5 style="color: #0f172a; margin: 1rem 0; font-weight: 700;">GST Breakdown by Stock</h5>
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
                        .gst-dataframe { background:white;border-radius:12px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,0.06);border:1px solid #e2e8f0; }
                        .gst-dataframe th { background:#0ea5a4 !important;color:#fff !important;text-align:center !important; }
                        .gst-dataframe td { text-align:center !important; padding:0.6rem !important; border-bottom:1px solid #f1f5f9 !important; }
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
                st.markdown("<a id=\"download\"></a>", unsafe_allow_html=True)
                st.markdown("""
                <div style="text-align: center; margin: 1.5rem 0;">
                    <h3 style="color: #0f172a; font-weight: 700; margin-bottom: 0.75rem;">📥 Download Detailed Results</h3>
                    <p style="color: #475569; margin-bottom: 1rem; font-size: 0.95rem;">Export trade-by-trade analysis for tax filing</p>
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

                # Required CSV format section moved to last (as text)
                st.markdown("---")
                st.markdown("""
                <div class="glass-card">
                    <h3 style="margin:0 0 0.5rem 0; color: var(--text);">📋 Required CSV Format</h3>
                    <ul style="margin:.25rem 0 0 1rem; color:#334155; line-height:1.8;">
                        <li><code>Date</code> — YYYY-MM-DD</li>
                        <li><code>Type</code> — BUY or SELL</li>
                        <li><code>Stock</code> — Security name</li>
                        <li><code>Qty</code> — Quantity</li>
                        <li><code>Price</code> — Price per unit</li>
                        <li><code>Brokerage</code> — Brokerage charges</li>
                    </ul>
                    <p style="margin:.5rem 0 0 0; color:#64748b;">Optional: <code>Dividend</code></p>
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
        # Enhanced landing page with better instructions
        st.markdown("---")
        st.markdown("### 🚀 How to Get Started")
        st.markdown("""
        <div>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:1rem;">
                <div class="material-card">
                    <div class="material-icon mat-blue">🏆</div>
                    <div>
                        <div class="material-title">Goal: Prepare your data</div>
                        <p class="material-sub">Add required columns and ensure date format is YYYY-MM-DD. Keep stock names consistent.</p>
                    </div>
                </div>
                <div class="material-card">
                    <div class="material-icon mat-green">🔔</div>
                    <div>
                        <div class="material-title">Upload & process</div>
                        <p class="material-sub">Upload your CSV; we compute FIFO matches, classify STCG/LTCG, and apply brokerage GST.</p>
                    </div>
                </div>
                <div class="material-card">
                    <div class="material-icon mat-amber">📈</div>
                    <div>
                        <div class="material-title">Review summaries</div>
                        <p class="material-sub">Check per-stock gains, total taxable income, and GST breakdown before download.</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Required CSV Format as text list (no cards)
        st.markdown("""
        <div class="glass-card" style="margin-top:1rem;">
            <h3 style="margin:0 0 .5rem 0;">📋 Required CSV Format</h3>
            <p style="margin:0 0 .5rem 0; color:#64748b;">Your CSV must include these columns:</p>
            <ul style="margin:.25rem 0 0 1rem; color:#334155; line-height:1.8;">
                <li><code>Date</code> — YYYY-MM-DD</li>
                <li><code>Type</code> — BUY or SELL</li>
                <li><code>Stock</code> — Security name</li>
                <li><code>Qty</code> — Quantity</li>
                <li><code>Price</code> — Price per unit</li>
                <li><code>Brokerage</code> — Brokerage charges</li>
            </ul>
            <p style="margin:.5rem 0 0 0; color:#64748b;">Optional: <code>Dividend</code></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Remove extra marketing cards to keep the landing minimal
        
        # CTA removed for a leaner look
    
    # Benefits section at the end
    st.markdown("""
    <div class="benefits-wrap">
        <div class="benefits-title">🌟 Why Choose Our Calculator?</div>
        <div class="benefit-grid">
            <div class="benefit-card">
                <div style="text-align:center;font-size:2rem;">🔥</div>
                <h4>Core Features</h4>
                <div class="benefit-item"><span class="benefit-bullet">✅</span><strong>FIFO Method</strong> - Industry standard calculation</div>
                <div class="benefit-item"><span class="benefit-bullet">✅</span><strong>Auto Classification</strong> - STCG/LTCG detection</div>
                <div class="benefit-item"><span class="benefit-bullet">✅</span><strong>GST Calculation</strong> - 18% on brokerage</div>
                <div class="benefit-item"><span class="benefit-bullet">✅</span><strong>Dividend Tracking</strong> - Complete income analysis</div>
                </div>
            <div class="benefit-card">
                <div style="text-align:center;font-size:2rem;">📈</div>
                <h4>Supported Transactions</h4>
                <div class="benefit-item">📊 <strong>Equity Trading</strong> - All stock transactions</div>
                <div class="benefit-item">📊 <strong>Multiple Stocks</strong> - Portfolio-wide analysis</div>
                <div class="benefit-item">📊 <strong>Partial Matching</strong> - Precise quantity handling</div>
                <div class="benefit-item">📊 <strong>Date Intelligence</strong> - Holding period</div>
            </div>
            <div class="benefit-card">
                <div style="text-align:center;font-size:2rem;">💾</div>
                <h4>Professional Reports</h4>
                <div class="benefit-item">🧾 <strong>Detailed Analysis</strong> - Trade-by-trade</div>
                <div class="benefit-item">🧾 <strong>Tax Summary</strong> - CA-ready</div>
                <div class="benefit-item">🧾 <strong>ITR Ready</strong> - Formatted for filing</div>
                <div class="benefit-item">🧾 <strong>CSV Export</strong> - Professional formatting</div>
            </div>
        </div>
        <div class="cta">
            <h3>👆 Ready to Calculate Your Taxes?</h3>
            <p style="margin:0;opacity:.95;">Scroll to the upload section and start your portfolio analysis.</p>
            <div class="cta-bar">⬆️ Upload your CSV in the section above to begin</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced footer with better formatting
    st.markdown("---")
    
    # Remove post-content marketing highlights for professionalism
    
    # Simple footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; border-top: 1px solid #e5e7eb; margin-top: 2rem;">
        <p style="color: #6b7280; margin: 0; font-size: 0.9rem;">©  Investor ITR & GST Calculator | Powered by Advanced FIFO Algorithm</p>
        <p style="color: #9ca3af; margin: 0.5rem 0 0 0; font-size: 0.8rem;">Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
