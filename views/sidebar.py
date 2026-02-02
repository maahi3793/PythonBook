
import streamlit as st

def render_sidebar(chapters: list, db):
    """
    Render the sidebar navigation.
    Returns: (mode, selected_day)
    """
    # Logo & Branding
    st.sidebar.image("assets/logo.png", use_container_width=True)
    # st.sidebar.title("PyTextbook") # User requested to drop the books emoji and title if logo is there
    
    # Mode Selection
    mode = st.sidebar.radio(
        "Mode",
        ["📖 Read Book", "🖼️ Manage Images", "📊 Dashboard"]
    )
    
    selected_day = None
    
    if mode == "📖 Read Book":
        st.sidebar.info("Select a Chapter from the Top-Right dropdown in the main view.")
            
    return mode, selected_day
