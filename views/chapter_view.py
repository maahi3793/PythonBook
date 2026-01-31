"""
Viewer module for rendering textbook chapters.
"""
import streamlit as st
from backend.db_textbook import TextbookDB

def render_chapter_view(db: TextbookDB, day: int):
    # Fetch content
    try:
        # We need a method to get specific chapter content
        # db.get_chapter(day) - assuming this exists or I'll add it
        # Wait, get_or_create_chapter returns the row, but we mostly need the content columns
        chapter = db.get_or_create_chapter(day) # This fetches the row
    except Exception as e:
        st.error(f"Error fetching chapter: {e}")
        return

    if not chapter:
        st.error("Chapter not found.")
        return

    st.title(f"Day {day}: {chapter.get('title', 'Unknown Topic')}")
    
    # Status Banner
    status = chapter.get('status', 'pending')
    if status == 'pending':
        st.info("⚠️ This chapter has not been generated yet.")
        return
        
    # Tabs for Parts
    tab1, tab2, tab3 = st.tabs(["📘 Part 1: Theory", "🧪 Part 2: Practice", "🎓 Part 3: Mentor"])
    
    with tab1:
        content = chapter.get('content_part1_theory')
        if content:
            _render_markdown_with_images(content, day, db)
        else:
            st.warning("Part 1 genertion pending.")

    with tab2:
        content = chapter.get('content_part2_practice')
        if content:
            _render_markdown_with_images(content, day, db)
        else:
            st.info("Part 2 generation pending.")

    with tab3:
        content = chapter.get('content_part3_mentor')
        if content:
            _render_markdown_with_images(content, day, db)
        else:
            st.info("Part 3 generation pending.")

def _render_markdown_with_images(content, day, db):
    """
    Custom renderer to replace <!-- IMAGE_PLACEHOLDER --> with actual images or warnings.
    """
    import re
    
    # Split content by image placeholders
    # Regex to match the whole block <!-- IMAGE... --> ... -->
    # This is tricky in markdown.
    # Simpler approach: Split by lines and process.
    
    lines = content.split('\n')
    buffer = []
    
    in_image_block = False
    current_image_id = None
    
    for line in lines:
        if '<!-- IMAGE_PLACEHOLDER:' in line:
            # Flush buffer
            if buffer:
                st.markdown('\n'.join(buffer))
                buffer = []
            
            # Extract ID
            match = re.search(r'ID_PLACEHOLDER:\s*(.*?)\s*-->', line.replace("IMAGE_", "ID_")) # typo in regex logic? 
            # Re-read image_extractor.py: "<!-- IMAGE_PLACEHOLDER: (.*?) -->"
            match = re.search(r'IMAGE_PLACEHOLDER:\s*(.*?)\s*-->', line)
            if match:
                current_image_id = match.group(1).strip()
            in_image_block = True
            
        elif in_image_block and '-->' in line:
            # End of block
            in_image_block = False
            
            # Render Image Widget
            if current_image_id:
                _render_image_widget(current_image_id, day, db)
            current_image_id = None
            
        elif in_image_block:
            pass # Skip description/url lines in the markdown output
            
        else:
            buffer.append(line)
            
    # Flush remaining
    if buffer:
        st.markdown('\n'.join(buffer))

def _render_image_widget(image_id, day, db):
    """Render the image or a placeholder warning."""
    # Fetch image status from DB
    # We need a db method for this, or query directly
    # Ideally db.get_image(image_id)
    
    # For now, let's just query directly via client if we can, or add helper
    # Adding helper to db is better path.
    # checking db_textbook.py...
    
    # Temporary direct query for MVP
    try:
        response = db.client.table("textbook_images").select("*").eq("id", image_id).execute()
        img_data = response.data[0] if response.data else None
    except:
        img_data = None
        
    if img_data and img_data.get('status') == 'uploaded' and img_data.get('selected_url'):
        st.image(img_data['selected_url'], caption=img_data.get('description', ''))
    else:
        # Render Warning Box
        st.warning(f"🖼️ **Diagram Missing:** `{image_id}`\n\nGo to 'Manage Images' to upload this.")
