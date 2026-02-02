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

    # ---------------------------------------------------------
    # 🛠️ SELF-REPAIR: Fix Generic Titles using Generated Content
    # ---------------------------------------------------------
    current_title = chapter.get('title', '')
    # Check if title looks generic (e.g. "Day 1 Content") AND we have content
    # Regex checks for "Day \d+ Content" or exact match
    import re
    is_generic = re.match(r'^Day\s*\d+\s*Content$', current_title, re.IGNORECASE) or current_title == f"Day {day} Content"
    
    if is_generic and chapter.get('content_part1_theory'):
        # Extract real title from Markdown
        # Look for first level header: "# Something"
        content = chapter.get('content_part1_theory')
        match = re.search(r'(?m)^#\s+(?:Chapter\s*\d+:?)?\s*(.*)', content)
        
        if match:
            new_title = match.group(1).strip()
            # Clean up potential "Day 1:" inside the extracted title if it existed
            new_title = re.sub(r'^Day\s*\d+[:\-\s]*', '', new_title, flags=re.IGNORECASE).strip()
            
            if new_title and new_title != current_title:
                try:
                    # Update DB
                    db.client.table("textbook_chapters").update({"title": new_title}).eq("day", day).execute()
                    # Trigger Refresh so UI picks it up immediately
                    st.rerun() 
                except Exception as e:
                    print(f"Failed to auto-update title: {e}")

    # ---------------------------------------------------------

    # 1. Navigation & Header Clean Setup
    valid_days = db.get_non_quiz_days()
    # Debug removed
    # Cache mapping for efficiency (could be passed in, but this is fine)
    # We need to build the dropdown list
    # Format: "Day X: Topic"
    
    # We need to find the title for the current day from the DB if possible, 
    # but 'chapter' variable already has it for *this* day.
    # We need titles for *all* days for the dropdown? 
    # Fetching all titles might be expensive if many chapters.
    # Sidebar used 'get_all_chapters_metadata' in streamlit_app.py.
    # Ideally satisfy dropdown with just "Day X" if needed, but User likes topics.
    # Let's assume we fetch metadata efficiently or just show "Day X" in dropdown if simple.
    # Let's try to get metadata for all valid days.
    all_ch_meta = db.get_all_chapters_metadata()
    meta_map = {c['day']: c['title'] for c in all_ch_meta}
    
    options = []
    current_index = 0
    for i, d in enumerate(valid_days):
        t = meta_map.get(d, f"Day {d}")
        label = f"Day {d}: {t}"
        options.append(label)
        if d == day:
            current_index = i
            
    # Layout: Title (Left) - Dropdown (Right)
    # Layout: Title (Left) - Dropdown (Right)
    # User wants dropdown "Green Circle" (Far Right). 
    # Current [3, 1] might be crowding it. Let's try [6, 2] to keep proportions but push right?
    # Or [1, 1] split?
    # Let's try to align it better.
    col_header, col_nav = st.columns([7, 3])

    with col_header:
        # User requested filtering "Day X" entirely.
        # "Delete the Main Page Title: It's redundant." -> DONE. (We output nothing)
        pass

    with col_nav:
        # Smart Labeling for Dropdown
        # If title is "Day X Content" (Generic), just show "Day X"
        # If title is "Variables" (Specific), show "Day X: Variables" or just "Variables"?
        # User said: "replace the Day x with the title name"
        # So "Variables".
        
        display_options = []
        option_map = {} # label -> day
        
        for i, d in enumerate(valid_days):
            raw_t = meta_map.get(d, f"Day {d}")
            # Clean "Day X" prefix from title
            t_clean = re.sub(r'^Day\s*\d+[:\-\s]*', '', raw_t, flags=re.IGNORECASE).strip()
            
            # If title was generic "Content" or empty, fallback to Day X
            if d == 0:
                label = "Preface"
            elif t_clean.lower() in ["content", ""]:
                label = f"Day {d}"
            else:
                label = f"Day {d}: {t_clean}" # Keep Day X for context in list, but clean content
                
            display_options.append(label)
            option_map[label] = d
            
            # if d == day: current_index = i (Moved logic after loop)
            pass

        # Determine current_index safely
        current_index = 0
        for idx, opt in enumerate(display_options):
            if option_map.get(opt) == day:
                current_index = idx
                break

        # st.write(f"DEBUG: Calculated Index={current_index} for Day {day}")
        
        selected_option = st.selectbox(
            "Navigation", 
            display_options, 
            index=current_index, 
            label_visibility="collapsed",
            key="nav_dropdown_v2"
        )
        
        # Handle Selection
        try:
            # We use the map now
            new_day = option_map[selected_option]
            if new_day != day:
                st.session_state['current_day'] = new_day
                st.rerun()
        except Exception as e:
            st.error(f"Navigation Error: {e}")

    # Clean Content Logic (Regex for later rendering)
    # Status Banner
    status = chapter.get('status', 'pending')
    if status == 'pending':
        st.info("⚠️ This chapter has not been generated yet. Use buttons below to start.")
        
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

    # Admin Zone
    st.markdown("---")
    with st.expander("⚠️ Danger Zone (Admin)"):
        st.warning("Deleting a chapter removes all parts and images. Use with caution.")
        if st.button(f"🗑️ Delete Chapter {day}", type="primary"):
            try:
                # Delete images first (if not cascade)
                # content is cascade, but let's be safe
                db.client.table("textbook_chapters").delete().eq("day", day).execute()
                st.success(f"Chapter {day} deleted.")
                st.rerun()
            except Exception as e:
                st.error(f"Deletion failed: {e}")
def _render_markdown_with_images(content, day, db):
    """
    Custom renderer to replace <!-- IMAGE_PLACEHOLDER --> with actual images or warnings.
    """
    import re
    
    # Split content by image placeholders
    # Regex to match the whole block <!-- IMAGE... --> ... -->
    # This is tricky in markdown.
    # Simpler approach: Split by lines and process.
    
    # 0. Clean Content (Remove Day X prefixes from headers)
    # E.g. "### Day 1: Variables" -> "### Variables"
    content = re.sub(r'(?m)^(#{1,6})\s*Day\s*\d+:\s*', r'\1 ', content)

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
