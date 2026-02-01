
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
        
        # Create a map of existing chapters
        db_map = {c['day']: c for c in chapters}
        
        chapter_titles = []
        day_map = {}
        
        for day in range(1, 180): # 1 to 179
            ch = db_map.get(day, {'status': 'pending', 'title': f"Day {day}"})
            status = ch.get('status', 'pending')
            
            # If title is generic "Day X Content", make it shorter or keep it? 
            # Ideally fetch topic from PyDaily if possible, but that's expensive here.
            # Just show what we have.
            title_text = ch.get('title', f"Day {day}")
            
            icon = status_icons.get(status, "⚪")
            display_title = f"{icon} Day {day}: {title_text}"
            
            chapter_titles.append(display_title)
            day_map[display_title] = day
            
        if chapter_titles:
            selected_title = st.sidebar.selectbox("Jump to Chapter", chapter_titles)
            selected_day = day_map[selected_title]
        else:
            st.sidebar.text("No chapters found.") # Should not happen now
            
    return mode, selected_day
