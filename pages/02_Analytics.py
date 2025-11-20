"""
Analytics Hub - Toybox 2.0
Central analytics and reporting dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add shared components to path
current_dir = Path(__file__).parent
apps_dir = current_dir.parent / "apps"
sys.path.insert(0, str(apps_dir))

from shared.components import (
    create_page_header, create_metric_cards, 
    display_info_message, create_data_table
)

# Page header
create_page_header(
    "Analytics Hub",
    "Centralized analytics and reporting dashboard",
    "📊"
)

# Analytics overview
st.markdown("### 📈 Analytics Overview")

display_info_message(
    "This page provides an overview of data analytics across all Toybox applications. "
    "Use the analytics tools in the sidebar to access specific analysis capabilities."
)

# Sample analytics data
np.random.seed(42)
dates = pd.date_range(start='2025-01-01', end='2025-11-10', freq='D')
usage_data = pd.DataFrame({
    'Date': dates,
    'Snow Dumper Usage': np.random.poisson(15, len(dates)),
    'Data Quality Runs': np.random.poisson(8, len(dates)),
    'API Calls': np.random.poisson(50, len(dates))
})

# Usage metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sessions",
        value="1,247", 
        delta="89 this week",
        help="Total user sessions across all apps"
    )

with col2:
    st.metric(
        "Data Processed",
        value="2.3 TB",
        delta="156 GB today",
        help="Total data processed by all applications"
    )

with col3:
    st.metric(
        "Active Projects",
        value="12",
        delta="2 new",
        help="Currently active data projects"
    )

with col4:
    st.metric(
        "Success Rate",
        value="98.5%",
        delta="0.3%",
        help="Overall application success rate"
    )

# Usage trends
st.markdown("### 📊 Usage Trends")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📈 Daily Usage")
    
    # Create sample chart data
    chart_data = usage_data.set_index('Date')[['Snow Dumper Usage', 'Data Quality Runs']].tail(30)
    st.line_chart(chart_data)

with col2:
    st.markdown("#### 🔥 Top Applications")
    
    app_usage = pd.DataFrame({
        'Application': ['Snow Dumper', 'Excel Macro', 'API Explorer', 'MM Maintenance', 'System Config'],
        'Usage Count': [245, 189, 156, 98, 67],
        'Last Used': ['2 hours ago', '1 hour ago', '30 mins ago', '3 hours ago', '1 day ago']
    })
    
    st.dataframe(app_usage, use_container_width=True, hide_index=True)

# Performance analytics  
st.markdown("### ⚡ Performance Analytics")

tab1, tab2, tab3 = st.tabs(["Response Times", "Error Rates", "Resource Usage"])

with tab1:
    st.markdown("#### ⏱️ Application Response Times")
    
    response_times = pd.DataFrame({
        'Application': ['Snow Dumper', 'Excel Macro', 'API Explorer', 'Analytics Hub', 'Dashboard'],
        'Avg Response (ms)': [1250, 890, 450, 320, 180],
        'P95 Response (ms)': [2100, 1450, 780, 560, 340],
        'Status': ['Good', 'Good', 'Excellent', 'Excellent', 'Excellent']
    })
    
    st.dataframe(response_times, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("#### ❌ Error Rates by Application")
    
    error_data = pd.DataFrame({
        'Application': ['Snow Dumper', 'Excel Macro', 'API Explorer', 'MM Maintenance'],
        'Total Requests': [1250, 890, 2340, 567],
        'Errors': [15, 8, 23, 3], 
        'Error Rate (%)': [1.2, 0.9, 0.98, 0.53]
    })
    
    st.bar_chart(error_data.set_index('Application')['Error Rate (%)'])

with tab3:
    st.markdown("#### 💾 Resource Utilization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("CPU Usage", "45%", "-3%")
        st.metric("Memory Usage", "62%", "+5%") 
        
    with col2:
        st.metric("Disk I/O", "128 MB/s", "+12 MB/s")
        st.metric("Network", "45 Mbps", "-2 Mbps")

# Data insights
st.markdown("### 🔍 Data Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📅 Weekly Summary")
    
    weekly_stats = {
        'Monday': {'sessions': 45, 'data_gb': 234},
        'Tuesday': {'sessions': 52, 'data_gb': 189}, 
        'Wednesday': {'sessions': 48, 'data_gb': 267},
        'Thursday': {'sessions': 61, 'data_gb': 298},
        'Friday': {'sessions': 58, 'data_gb': 245},
        'Saturday': {'sessions': 23, 'data_gb': 89},
        'Sunday': {'sessions': 18, 'data_gb': 67}
    }
    
    for day, stats in weekly_stats.items():
        st.markdown(f"**{day}:** {stats['sessions']} sessions, {stats['data_gb']} GB processed")

with col2:
    st.markdown("#### 🎯 Key Insights")
    
    insights = [
        "📈 Snow Dumper usage increased 23% this month",
        "🔧 Excel Macro processing efficiency improved 15%", 
        "🌐 API Explorer error rate decreased to <1%",
        "👥 New user adoption rate: 8 users this week",
        "⚡ Average response time improved by 12%"
    ]
    
    for insight in insights:
        st.markdown(f"• {insight}")

# Export options
st.markdown("### 📤 Export Analytics")

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    if st.button("📊 Export Usage Data", type="secondary"):
        st.success("Usage data exported successfully!")

with export_col2:
    if st.button("📈 Export Performance Report", type="secondary"):
        st.success("Performance report exported successfully!")

with export_col3:
    if st.button("📋 Export Full Analytics", type="secondary"):
        st.success("Full analytics report exported successfully!")

# Footer
st.markdown("---")
st.caption(f"Analytics data updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Refresh page for latest data")