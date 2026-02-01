"""
Viewer module for rendering textbook chapters.
"""
import streamlit as st
from backend.db_textbook import TextbookDB
import streamlit as st

def _run_generation(day, part):
    """Helper to trigger generation."""
    with st.spinner(f"Generating {part}..."):
        from backend.generator import TextbookGenerator
        gen = TextbookGenerator()
        res = gen.generate_day(day, part)
        if res['success']:
            st.success("Generated!")
            return True
        else:
            st.error(f"Failed: {res['message']}")
            return False

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
        st.info("⚠️ This chapter has not been generated yet. Use buttons below to start.")
        # Do not return, continue to tabs
        
    # Tabs for Parts
    tab1, tab2, tab3 = st.tabs(["📘 Part 1: Theory", "🧪 Part 2: Practice", "🎓 Part 3: Mentor"])
    
    with tab1:
        content = chapter.get('content_part1_theory')
        if content:
            _render_markdown_with_images(content, day, db)
            with st.expander("⚙️ Admin: Regenerate Part 1"):
                if st.button("🔄 Regenerate Theory", key="regen_p1"):
                     _run_generation(day, 'part1')
                     st.rerun()
        else:
            st.warning("Part 1 generation pending.")
            if st.button("🚀 Generate Theory", key="gen_p1"):
                with st.spinner("Generating Theory part..."):
                    from backend.generator import TextbookGenerator
                    gen = TextbookGenerator()
                    res = gen.generate_day(day, 'part1')
                    if res['success']:
                        st.success("Generated!")
                        st.rerun()
                    else:
                        st.error(f"Failed: {res['message']}")

    with tab2:
        content = chapter.get('content_part2_practice')
        if content:
            _render_markdown_with_images(content, day, db)
            with st.expander("⚙️ Admin: Regenerate Part 2"):
                if st.button("🔄 Regenerate Practice", key="regen_p2"):
                     _run_generation(day, 'part2')
                     st.rerun()
        else:
            st.info("Part 2 generation pending.")
            if st.button("🚀 Generate Practice", key="gen_p2"):
                with st.spinner("Generating Practice part..."):
                    from backend.generator import TextbookGenerator
                    gen = TextbookGenerator()
                    res = gen.generate_day(day, 'part2')
                    if res['success']:
                        st.success("Generated!")
                        st.rerun()
                    else:
                        st.error(f"Failed: {res['message']}")

    with tab3:
        content = chapter.get('content_part3_mentor')
        if content:
            _render_markdown_with_images(content, day, db)
            with st.expander("⚙️ Admin: Regenerate Part 3"):
                if st.button("🔄 Regenerate Mentor", key="regen_p3"):
                     _run_generation(day, 'part3')
                     st.rerun()
        else:
            st.info("Part 3 generation pending.")
            if st.button("🚀 Generate Mentor", key="gen_p3"):
                with st.spinner("Generating Mentor part..."):
                    from backend.generator import TextbookGenerator
                    gen = TextbookGenerator()
                    res = gen.generate_day(day, 'part3')
                    if res['success']:
                        st.success("Generated!")
                        st.rerun()
                    else:
                        st.error(f"Failed: {res['message']}")

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
    in_ignore_block = False # Generic ignore
    current_image_id = None
    
    for line in lines:
        # 1. Image Block Start
        if '<!-- IMAGE_PLACEHOLDER:' in line:
            # Flush buffer
            if buffer:
                st.markdown('\n'.join(buffer))
                buffer = []
            
            # Extract ID
            match = re.search(r'IMAGE_PLACEHOLDER:\s*(.*?)\s*-->', line)
            if match:
                current_image_id = match.group(1).strip()
            in_image_block = True
            
        # 2. Block End (Generic)
        elif (in_image_block or in_ignore_block) and '-->' in line:
            in_ignore_block = False
            
            # If leaving image block, render widget
            if in_image_block:
                in_image_block = False
                if current_image_id:
                    _render_image_widget(current_image_id, day, db)
                current_image_id = None
        
        # 3. Swallow Image Block Content
        elif in_image_block:
            pass 
            
        # 4. Detect Suggested URLs or Description outside block (Legacy/Gemini quirks)
        elif '<!-- SUGGESTED_URLS:' in line or '<!-- DESCRIPTION:' in line:
            in_ignore_block = True
            
        # 5. Generic Ignore Swallow
        elif in_ignore_block:
            pass
            
        # 6. Normal Content
        else:
            buffer.append(line)
            
    # Flush remaining
    if buffer:
        st.markdown('\n'.join(buffer))

def _render_image_widget(image_id, day, db):
    """Render the image or a placeholder warning."""
    try:
        response = db.client.table("textbook_images").select("*").eq("id", image_id).execute()
        img_data = response.data[0] if response.data else None
    except:
        img_data = None
        
    if img_data and img_data.get('status') == 'uploaded' and img_data.get('selected_url'):
        st.image(img_data['selected_url'], caption=img_data.get('description', ''))
    else:
        # Render Warning Box with Description for Manual Gen
        desc = img_data.get('description', 'No description available.') if img_data else "No data."
        
        st.warning(
            f"🖼️ **Diagram Missing:** `{image_id}`\n\n"
            f"**AI Prompt:**\n> {desc}\n\n"
            f"Go to 'Manage Images' to upload this."
        )
