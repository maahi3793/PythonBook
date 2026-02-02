"""
PythonBook Streamlit App
========================
Web UI for managing textbook generation.

Features:
- Chapter Browser: View generated chapters
- Image Manager: Handle image placeholders
- Export Tool: Generate PDF
"""

import streamlit as st
import logging

try:
    from backend.db_textbook import TextbookDB
    from views.sidebar import render_sidebar
    from views.chapter_view import render_chapter_view
    from views.image_manager import render_image_manager
    from views.dashboard import render_dashboard
except ImportError as e:
    # Just in case paths are tricky
    import sys, os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from backend.db_textbook import TextbookDB
    from views.sidebar import render_sidebar
    from views.chapter_view import render_chapter_view
    from views.image_manager import render_image_manager
    from views.dashboard import render_dashboard

# Configure Logging
logging.basicConfig(level=logging.INFO)

# Page config
st.set_page_config(
    page_title="PyTextbook Studio",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # 1. Initialize DB
    # We do this once or per run? Streamlit re-runs script often.
    # Ideally use st.cache_resource for connection.
    @st.cache_resource
    def get_db():
        return TextbookDB()
    
    try:
        db = get_db()
    except Exception as e:
        st.error(f"❌ Failed to connect to Database: {e}")
        st.stop()

    # 2. Add Custom CSS
    try:
        from assets.book_style import get_book_styles
        st.markdown(get_book_styles(), unsafe_allow_html=True)
    except ImportError:
        # Fallback if path issue
        st.warning("⚠️ Could not load book styles.")

    # 3. Sidebar Navigation
    # Fetch chapters for sidebar efficiently
    chapters_meta = db.get_all_chapters_metadata()
    mode, selected_day = render_sidebar(chapters_meta, db)
    
    # 4. Main Content Router
    # 4. Main Content Router
    if mode == "📖 Read Book":
        # Initialize Current Day if not set
        if 'current_day' not in st.session_state:
            st.session_state['current_day'] = 1
            
        render_chapter_view(db, st.session_state['current_day'])

            
    elif mode == "🖼️ Manage Images":
        render_image_manager(db)
        
    elif mode == "📊 Dashboard":
        render_dashboard(db)

if __name__ == "__main__":
    main()
