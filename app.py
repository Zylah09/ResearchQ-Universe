#!/usr/bin/env python3
"""
ResearchQ.id Validity & Reliability Analysis Tool
Streamlit Web App - Real-time Data Validation & Analysis

Features:
- Upload raw data (Excel/CSV)
- Auto-calculate: Pearson correlation, KMO, Bartlett, Cronbach's Alpha, Item-total
- Input SmartPLS outer loading for validation
- Interactive visualizations (heatmaps, charts)
- Export PDF + Excel reports
- Bahasa Indonesia support

Author: ResearchQ.id
Version: 1.0
Date: 2026-05-28
"""

import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import f_oneway, chi2
from scipy.spatial.distance import pdist, squareform
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="ResearchQ - Validity & Reliability Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 0rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
    .success-box {
        padding: 1rem;
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        border-radius: 0.5rem;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        border-radius: 0.5rem;
    }
    .danger-box {
        padding: 1rem;
        background-color: #fee2e2;
        border-left: 4px solid #dc2626;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_data(file):
    """Load data from Excel or CSV"""
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def calculate_pearson_correlation(df):
    """Calculate Pearson correlation matrix"""
    return df.corr()

def calculate_kmo(df):
    """Calculate Kaiser-Meyer-Olkin (KMO) measure"""
    # KMO formula: sum(r^2) / (sum(r^2) + sum(1/(1-r^2)))
    corr_matrix = df.corr().values
    n_vars = corr_matrix.shape[0]
    
    # Get partial correlations
    inv_corr = np.linalg.inv(corr_matrix)
    partial_corr = -inv_corr / np.sqrt(np.outer(np.diag(inv_corr), np.diag(inv_corr)))
    np.fill_diagonal(partial_corr, 0)
    
    # Calculate KMO
    numerator = np.sum(corr_matrix**2) - np.trace(corr_matrix**2)
    denominator = numerator + np.sum(partial_corr**2)
    
    kmo = numerator / denominator if denominator != 0 else 0
    return kmo

def calculate_bartlett(df):
    """Calculate Bartlett's sphericity test"""
    n = len(df)
    corr_matrix = df.corr()
    det_corr = np.linalg.det(corr_matrix)
    
    # Bartlett test statistic
    chi_sq = -((n - 1) - (2 * df.shape[1] + 5) / 6) * np.log(det_corr)
    df_chi = df.shape[1] * (df.shape[1] - 1) / 2
    
    # P-value
    p_value = 1 - chi2.cdf(chi_sq, int(df_chi))
    
    return chi_sq, p_value, df_chi

def calculate_cronbach_alpha(df):
    """Calculate Cronbach's Alpha"""
    n_items = df.shape[1]
    variances = df.var()
    total_var = df.sum(axis=1).var()
    
    alpha = (n_items / (n_items - 1)) * (1 - (variances.sum() / total_var))
    return alpha

def calculate_item_total_correlation(df):
    """Calculate item-total correlation"""
    total_score = df.sum(axis=1)
    item_total = {}
    
    for col in df.columns:
        remaining = df.drop(col, axis=1).sum(axis=1)
        correlation = total_score.corr(remaining)
        item_total[col] = correlation
    
    return pd.Series(item_total)

def interpret_alpha(alpha):
    """Interpret Cronbach's Alpha value"""
    if alpha >= 0.80:
        return "Excellent", "🟢"
    elif alpha >= 0.70:
        return "Acceptable", "🟡"
    else:
        return "Weak", "🔴"

def interpret_kmo(kmo):
    """Interpret KMO value"""
    if kmo >= 0.70:
        return "Excellent", "🟢"
    elif kmo >= 0.50:
        return "Acceptable", "🟡"
    else:
        return "Poor", "🔴"

def interpret_loading(loading):
    """Interpret SmartPLS outer loading"""
    if loading >= 0.70:
        return "Excellent", "🟢"
    elif loading >= 0.50:
        return "Good", "🟢"
    elif loading >= 0.40:
        return "Marginal", "🟡"
    else:
        return "Invalid", "🔴"

def create_correlation_heatmap(corr_matrix):
    """Create correlation heatmap"""
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        zmin=-1,
        zmax=1,
        text=np.round(corr_matrix.values, 3),
        texttemplate='%{text}',
        textfont={"size": 9},
        colorbar=dict(title="Correlation")
    ))
    fig.update_layout(
        height=600,
        title="Pearson Correlation Matrix",
        xaxis_title="Items",
        yaxis_title="Items"
    )
    return fig

def create_item_total_chart(item_total):
    """Create item-total correlation bar chart"""
    fig = px.bar(
        x=item_total.index,
        y=item_total.values,
        title="Item-Total Correlation",
        labels={'x': 'Items', 'y': 'Correlation'},
        color=item_total.values,
        color_continuous_scale=['#dc2626', '#fbbf24', '#10b981'],
        range_color=[0.2, 0.8]
    )
    fig.add_hline(y=0.30, line_dash="dash", line_color="red", 
                  annotation_text="Minimum threshold (0.30)")
    fig.update_layout(height=400, showlegend=False)
    return fig

def export_to_pdf(data_analysis, smarpls_results=None):
    """Export results to PDF"""
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("<b>VALIDITY & RELIABILITY ANALYSIS REPORT</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.5*cm))
    
    # Generated date
    date_text = Paragraph(f"<i>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>", styles['Normal'])
    elements.append(date_text)
    elements.append(Spacer(1, 0.5*cm))
    
    # Section 1: Data Summary
    elements.append(Paragraph("<b>1. Data Summary</b>", styles['Heading2']))
    summary_data = [
        ['Metric', 'Value'],
        ['Sample Size', str(data_analysis['n_samples'])],
        ['Number of Items', str(data_analysis['n_items'])],
        ['Number of Constructs', str(len(data_analysis['cronbach_alpha']))],
    ]
    summary_table = Table(summary_data, colWidths=[3*cm, 3*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Section 2: KMO & Bartlett
    elements.append(Paragraph("<b>2. KMO & Bartlett's Test</b>", styles['Heading2']))
    kmo_data = [
        ['Test', 'Value', 'Status'],
        ['KMO Measure', f"{data_analysis['kmo']:.4f}", data_analysis['kmo_status']],
        ['Bartlett Chi-Square', f"{data_analysis['bartlett_chi2']:.4f}", data_analysis['bartlett_status']],
        ['Bartlett p-value', f"{data_analysis['bartlett_p']:.6f}", 'Significant' if data_analysis['bartlett_p'] < 0.05 else 'Not Significant'],
    ]
    kmo_table = Table(kmo_data, colWidths=[4*cm, 4*cm, 4*cm])
    kmo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(kmo_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Section 3: Cronbach's Alpha
    elements.append(Paragraph("<b>3. Cronbach's Alpha (Reliability)</b>", styles['Heading2']))
    alpha_data = [['Construct', 'Alpha', 'Status']]
    for construct, alpha in data_analysis['cronbach_alpha'].items():
        status, emoji = interpret_alpha(alpha)
        alpha_data.append([construct, f"{alpha:.4f}", status])
    
    alpha_table = Table(alpha_data, colWidths=[4*cm, 3*cm, 4*cm])
    alpha_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(alpha_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Section 4: SmartPLS Outer Loading
    if smarpls_results:
        elements.append(PageBreak())
        elements.append(Paragraph("<b>4. SmartPLS Outer Loading Validation</b>", styles['Heading2']))
        
        loading_data = [['Item', 'Loading', 'Status', 'Recommendation']]
        for item, loading, status, rec in smarpls_results:
            loading_data.append([item, f"{loading:.4f}", status, rec])
        
        loading_table = Table(loading_data, colWidths=[2*cm, 2.5*cm, 3*cm, 4*cm])
        loading_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(loading_table)
        elements.append(Spacer(1, 0.5*cm))
    
    # Footer
    elements.append(Spacer(1, 1*cm))
    footer = Paragraph("<i>ResearchQ.id - Validity & Reliability Analysis Tool</i>", styles['Normal'])
    elements.append(footer)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Header
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("## 📊")
    with col2:
        st.markdown("## ResearchQ - Validity & Reliability Analysis Tool")
    
    st.markdown("---")
    st.markdown("**Analisis validitas & reliabilitas data research Anda secara instant**")
    st.markdown("Upload data → Get results → Export PDF/Excel")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Analyze", "📈 SmartPLS Validation", "📄 Reports"])
    
    # ====== TAB 1: UPLOAD & ANALYZE ======
    with tab1:
        st.subheader("Step 1: Upload Data")
        
        uploaded_file = st.file_uploader(
            "Upload your data (Excel or CSV)",
            type=['xlsx', 'xls', 'csv'],
            help="File harus berisi data responden dengan items sebagai kolom"
        )
        
        if uploaded_file:
            df = load_data(uploaded_file)
            
            if df is not None:
                st.success(f"✅ File loaded successfully: {df.shape[0]} rows × {df.shape[1]} columns")
                
                # Data preview
                with st.expander("📋 Data Preview", expanded=False):
                    st.dataframe(df.head(10), use_container_width=True)
                
                st.markdown("---")
                st.subheader("Step 2: Specify Constructs")
                
                # Allow user to group items by construct
                st.write("Group items into constructs (untuk Cronbach's Alpha per construct)")
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    construct_input = st.text_area(
                        "Enter construct groups (format: 'Construct_Name: item1, item2, item3')",
                        value="X1: X1.1, X1.2, X1.3, X1.4, X1.5, X1.6\nX2: X2.1, X2.2, X2.3, X2.4, X2.5, X2.6, X2.7\nY: Y.1, Y.2, Y.3, Y.4, Y.5, Y.6, Y.7",
                        height=150,
                        help="Pisahkan construct dengan baris baru"
                    )
                
                # Parse constructs
                constructs = {}
                try:
                    for line in construct_input.strip().split('\n'):
                        if ':' in line:
                            name, items = line.split(':')
                            items_list = [i.strip() for i in items.split(',')]
                            constructs[name.strip()] = items_list
                except:
                    st.error("❌ Format error. Gunakan format: Construct_Name: item1, item2, item3")
                
                if constructs and st.button("🚀 Run Analysis", type="primary"):
                    st.session_state.df = df
                    st.session_state.constructs = constructs
                    
                    # Run analysis
                    with st.spinner("Analyzing..."):
                        # Overall analysis
                        corr_matrix = calculate_pearson_correlation(df)
                        kmo = calculate_kmo(df)
                        bartlett_chi2, bartlett_p, bartlett_df = calculate_bartlett(df)
                        item_total = calculate_item_total_correlation(df)
                        
                        # Per-construct analysis
                        cronbach_alphas = {}
                        for construct_name, items in constructs.items():
                            construct_df = df[[col for col in items if col in df.columns]]
                            if len(construct_df.columns) > 0:
                                cronbach_alphas[construct_name] = calculate_cronbach_alpha(construct_df)
                        
                        # Store in session
                        st.session_state.analysis = {
                            'correlation': corr_matrix,
                            'kmo': kmo,
                            'bartlett_chi2': bartlett_chi2,
                            'bartlett_p': bartlett_p,
                            'item_total': item_total,
                            'cronbach_alpha': cronbach_alphas,
                            'n_samples': len(df),
                            'n_items': len(df.columns),
                        }
                    
                    st.success("✅ Analysis complete!")
        
        # Display analysis results if available
        if 'analysis' in st.session_state:
            analysis = st.session_state.analysis
            
            st.markdown("---")
            st.subheader("📊 Analysis Results")
            
            # Metrics overview
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                kmo_status, kmo_emoji = interpret_kmo(analysis['kmo'])
                st.metric("KMO Measure", f"{analysis['kmo']:.4f}", kmo_status)
            
            with col2:
                bartlett_status = "✅ Significant" if analysis['bartlett_p'] < 0.05 else "❌ Not Significant"
                st.metric("Bartlett p-value", f"{analysis['bartlett_p']:.6f}", bartlett_status)
            
            with col3:
                avg_alpha = np.mean(list(analysis['cronbach_alpha'].values()))
                alpha_status, alpha_emoji = interpret_alpha(avg_alpha)
                st.metric("Avg Cronbach's α", f"{avg_alpha:.4f}", alpha_status)
            
            with col4:
                avg_itc = analysis['item_total'].mean()
                st.metric("Avg Item-Total", f"{avg_itc:.4f}", "Good" if avg_itc > 0.30 else "Weak")
            
            st.markdown("---")
            
            # Visualizations
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.plotly_chart(create_correlation_heatmap(analysis['correlation']), use_container_width=True)
            
            with col2:
                st.plotly_chart(create_item_total_chart(analysis['item_total']), use_container_width=True)
            
            # Detailed results
            st.markdown("---")
            st.subheader("📋 Detailed Results")
            
            # KMO & Bartlett
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write("**KMO & Bartlett's Test**")
                st.write(f"- KMO: {analysis['kmo']:.4f} ({interpret_kmo(analysis['kmo'])[0]})")
                st.write(f"- Bartlett χ²: {analysis['bartlett_chi2']:.4f}")
                st.write(f"- Bartlett p-value: {analysis['bartlett_p']:.6f}")
                if analysis['kmo'] >= 0.50 and analysis['bartlett_p'] < 0.05:
                    st.markdown('<div class="success-box">✅ Data suitable for factor analysis</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="danger-box">❌ Data may not be suitable for factor analysis</div>', unsafe_allow_html=True)
            
            with col2:
                st.write("**Cronbach's Alpha by Construct**")
                for construct, alpha in analysis['cronbach_alpha'].items():
                    status, emoji = interpret_alpha(alpha)
                    st.write(f"{emoji} {construct}: {alpha:.4f} ({status})")
            
            # Item-Total correlation
            st.write("**Item-Total Correlation**")
            st.dataframe(analysis['item_total'].to_frame('Correlation').sort_values('Correlation', ascending=False), use_container_width=True)
            
            # Interpretation
            st.markdown("---")
            st.subheader("💡 Interpretation")
            
            interpretation = ""
            
            # KMO interpretation
            if analysis['kmo'] >= 0.70:
                interpretation += "✅ **KMO Excellent:** Data sangat cocok untuk factor analysis.\n\n"
            elif analysis['kmo'] >= 0.50:
                interpretation += "⚠️ **KMO Acceptable:** Data cukup cocok untuk factor analysis, tapi bisa lebih baik.\n\n"
            else:
                interpretation += "❌ **KMO Poor:** Data TIDAK cocok untuk factor analysis. Pertimbangkan hapus items dengan MSA rendah.\n\n"
            
            # Bartlett interpretation
            if analysis['bartlett_p'] < 0.05:
                interpretation += "✅ **Bartlett Significant:** Variabel-variabel berkorelasi secara signifikan.\n\n"
            else:
                interpretation += "❌ **Bartlett Not Significant:** Variabel-variabel mungkin tidak berkorelasi.\n\n"
            
            # Cronbach interpretation
            valid_alphas = [a for a in analysis['cronbach_alpha'].values() if a >= 0.70]
            if len(valid_alphas) == len(analysis['cronbach_alpha']):
                interpretation += "✅ **Reliability Excellent:** Semua konstruk memiliki internal consistency yang baik (α > 0.70).\n\n"
            elif len(valid_alphas) > 0:
                interpretation += f"⚠️ **Reliability Acceptable:** {len(valid_alphas)}/{len(analysis['cronbach_alpha'])} constructs reliable. Construct lain perlu revisi.\n\n"
            else:
                interpretation += "❌ **Reliability Weak:** Tidak ada construct dengan α > 0.70. Perlu hapus items lemah dan recalculate.\n\n"
            
            st.markdown(interpretation)
    
    # ====== TAB 2: SMARTPLS VALIDATION ======
    with tab2:
        st.subheader("SmartPLS Outer Loading Validation")
        
        st.write("Paste outer loading values dari SmartPLS untuk validasi measurement model Anda.")
        
        loading_input = st.text_area(
            "Enter outer loading values (format: 'Item_name = loading_value', satu per baris)",
            value="""X1.1 = 0.752
X1.2 = 0.685
X1.3 = 0.541
X1.4 = 0.438
X1.5 = 0.395
X1.6 = 0.620
X2.1 = 0.780
X2.2 = 0.710
X2.3 = 0.620
X2.4 = 0.530
X2.5 = 0.450
X2.6 = 0.680
X2.7 = 0.720
Y.1 = 0.810
Y.2 = 0.750
Y.3 = 0.690
Y.4 = 0.580
Y.5 = 0.520
Y.6 = 0.670
Y.7 = 0.720""",
            height=300,
            help="Copy dari SmartPLS output"
        )
        
        if st.button("📊 Validate Loadings", type="primary"):
            # Parse input
            loadings_dict = {}
            try:
                for line in loading_input.strip().split('\n'):
                    if '=' in line:
                        item, loading = line.split('=')
                        loadings_dict[item.strip()] = float(loading.strip())
            except:
                st.error("❌ Format error. Gunakan format: Item_name = loading_value")
            
            if loadings_dict:
                # Validate
                results = []
                valid_count = 0
                marginal_count = 0
                invalid_count = 0
                
                for item, loading in loadings_dict.items():
                    status, emoji = interpret_loading(loading)
                    
                    if loading >= 0.70:
                        recommendation = "KEEP - Excellent"
                        valid_count += 1
                    elif loading >= 0.50:
                        recommendation = "KEEP - Good"
                        valid_count += 1
                    elif loading >= 0.40:
                        recommendation = "CONSIDER - Marginal"
                        marginal_count += 1
                    else:
                        recommendation = "DELETE - Invalid"
                        invalid_count += 1
                    
                    results.append((item, loading, status, recommendation))
                
                st.session_state.smartpls_results = results
                
                # Display summary
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Valid Items (≥0.50)", valid_count)
                with col2:
                    st.metric("Marginal Items (0.40-0.50)", marginal_count)
                with col3:
                    st.metric("Invalid Items (<0.40)", invalid_count)
                with col4:
                    validity = "✅ Valid" if invalid_count == 0 else "❌ Invalid"
                    st.metric("Model Validity", validity)
                
                st.markdown("---")
                
                # Results table
                st.write("**Detailed Loading Assessment**")
                results_df = pd.DataFrame(results, columns=['Item', 'Loading', 'Status', 'Recommendation'])
                st.dataframe(results_df, use_container_width=True)
                
                # Visualization
                st.write("**Loading Distribution**")
                fig = px.bar(
                    results_df,
                    x='Item',
                    y='Loading',
                    color='Loading',
                    color_continuous_scale=['#dc2626', '#fbbf24', '#10b981'],
                    range_color=[0.3, 0.8]
                )
                fig.add_hline(y=0.70, line_dash="dash", line_color="green", annotation_text="Excellent (0.70)")
                fig.add_hline(y=0.50, line_dash="dash", line_color="orange", annotation_text="Good (0.50)")
                fig.add_hline(y=0.40, line_dash="dash", line_color="red", annotation_text="Marginal (0.40)")
                st.plotly_chart(fig, use_container_width=True)
                
                # Interpretation
                st.markdown("---")
                st.subheader("💡 Interpretation")
                
                if invalid_count == 0 and marginal_count == 0:
                    st.markdown('<div class="success-box">✅ Model measurement VALID. Semua items memiliki loading ≥ 0.50.</div>', unsafe_allow_html=True)
                elif invalid_count == 0:
                    st.markdown(f'<div class="warning-box">⚠️ Model measurement ACCEPTABLE. {marginal_count} items marginal, pertimbangkan untuk dihapus.</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="danger-box">❌ Model measurement INVALID. {invalid_count} items perlu dihapus (loading < 0.40).</div>', unsafe_allow_html=True)
    
    # ====== TAB 3: REPORTS ======
    with tab3:
        st.subheader("Export Results")
        
        if 'analysis' in st.session_state:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("📄 Download PDF Report"):
                    smartpls_results = st.session_state.get('smartpls_results', None)
                    pdf_buffer = export_to_pdf(st.session_state.analysis, smartpls_results)
                    
                    st.download_button(
                        label="📥 Click to Download PDF",
                        data=pdf_buffer,
                        file_name=f"validity_reliability_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
            
            with col2:
                if st.button("📊 Download Excel Report"):
                    # Create Excel with analysis results
                    output = BytesIO()
                    
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        # Sheet 1: Summary
                        summary_df = pd.DataFrame({
                            'Metric': ['Sample Size', 'Number of Items', 'KMO', 'Bartlett p-value'],
                            'Value': [
                                st.session_state.analysis['n_samples'],
                                st.session_state.analysis['n_items'],
                                f"{st.session_state.analysis['kmo']:.4f}",
                                f"{st.session_state.analysis['bartlett_p']:.6f}"
                            ]
                        })
                        summary_df.to_excel(writer, sheet_name='Summary', index=False)
                        
                        # Sheet 2: Correlation Matrix
                        st.session_state.analysis['correlation'].to_excel(writer, sheet_name='Correlation')
                        
                        # Sheet 3: Item-Total Correlation
                        st.session_state.analysis['item_total'].to_frame('Item_Total_Correlation').to_excel(writer, sheet_name='Item_Total')
                        
                        # Sheet 4: Cronbach Alpha
                        alpha_df = pd.DataFrame(list(st.session_state.analysis['cronbach_alpha'].items()), columns=['Construct', 'Cronbach_Alpha'])
                        alpha_df.to_excel(writer, sheet_name='Cronbach_Alpha', index=False)
                        
                        # Sheet 5: SmartPLS results
                        if 'smartpls_results' in st.session_state:
                            smartpls_df = pd.DataFrame(
                                st.session_state.smartpls_results,
                                columns=['Item', 'Loading', 'Status', 'Recommendation']
                            )
                            smartpls_df.to_excel(writer, sheet_name='SmartPLS_Loading', index=False)
                    
                    output.seek(0)
                    st.download_button(
                        label="📥 Click to Download Excel",
                        data=output,
                        file_name=f"validity_reliability_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        else:
            st.info("ℹ️ Jalankan analisis di tab 'Upload & Analyze' terlebih dahulu")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; font-size: 0.9rem;">
    <p>ResearchQ.id - Validity & Reliability Analysis Tool</p>
    <p>📱 WhatsApp: 0899-1077-795 | 🔗 Lynk.id: lynk.id/resq | 🎥 YouTube: NotYourLecture</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    # Initialize session state
    if 'analysis' not in st.session_state:
        st.session_state.analysis = None
    if 'smartpls_results' not in st.session_state:
        st.session_state.smartpls_results = None
    
    main()
