"""
PythonBook Streamlit App
========================
Web UI for managing textbook generation.

Features:
- Chapter Browser: View generated chapters
- Image Manager: Handle image placeholders
- Export Tool: Generate PDF/ePub/HTML
- Weekly View: View "Think Like a Dev" summaries
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="PyTextbook Studio",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("📚 PyTextbook Studio")

page = st.sidebar.radio(
    "Navigate",
    ["📖 Chapter Browser", "🖼️ Image Manager", "📤 Export", "📅 Weekly Summaries", "⚙️ Settings"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Progress")
st.sidebar.metric("Chapters Generated", "0/179")
st.sidebar.metric("Images Pending", "0")

# Main content
if page == "📖 Chapter Browser":
    st.title("📖 Chapter Browser")
    st.info("Chapter browser will be implemented in Phase 4")
    
elif page == "🖼️ Image Manager":
    st.title("🖼️ Image Manager")
    st.info("Image manager will be implemented in Phase 5")
    
elif page == "📤 Export":
    st.title("📤 Export Tool")
    st.info("Export tool will be implemented in Phase 6")
    
elif page == "📅 Weekly Summaries":
    st.title("📅 Weekly Summaries")
    st.info("Weekly view will be implemented in Phase 4")
    
elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.info("Settings will be implemented in Phase 7")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Part of the [PyDaily](https://pydaily.streamlit.app) ecosystem")
