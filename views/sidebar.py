
import streamlit as st

def render_sidebar(chapters):
    """Render the sidebar navigation."""
    st.sidebar.title("📚 PyTextbook")
    
    # Mode Selection
    mode = st.sidebar.radio(
        "Mode",
        ["📖 Read Book", "🖼️ Manage Images", "📊 Dashboard"]
    )
    
    selected_day = None
    
    if mode == "📖 Read Book":
        st.sidebar.subheader("Table of Contents")
        
        # Group by week (implied by day / 7)
        # For efficiency, we just list days with status colors
        # 🟢 = Complete, 🟡 = Generating, 🔴 = Error, ⚪ = Pending
        
        status_icons = {
            "pending": "⚪",
            "part1_done": "🟡",
            "part2_done": "🟡",
            "complete": "🟢",
            "failed": "🔴"
        }
        
        chapter_titles = []
        day_map = {}
        
        for ch in chapters:
            icon = status_icons.get(ch.get('status', 'pending'), "⚪")
            title = f"{icon} Day {ch['day']}: {ch['title']}"
            chapter_titles.append(title)
            day_map[title] = ch['day']
            
        if chapter_titles:
            selected_title = st.sidebar.selectbox("Jump to Chapter", chapter_titles)
            selected_day = day_map[selected_title]
        else:
            st.sidebar.text("No chapters found.")
            
    return mode, selected_day
