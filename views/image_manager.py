"""
Admin view for managing missing images.
"""
import streamlit as st
import pandas as pd
from backend.db_textbook import TextbookDB

def render_image_manager(db: TextbookDB):
    st.title("🖼️ Image Manager")
    
    # 1. Fetch pending images
    pending_images = db.get_pending_images()
    
    if not pending_images:
        st.success("✅ No pending images! All diagrams are covered.")
        return

    st.write(f"Found {len(pending_images)} images needing attention.")
    
    # Convert to DataFrame for easier display
    df = pd.DataFrame(pending_images)
    
    # Display table
    for i, row in df.iterrows():
        with st.expander(f"{row['id']} - {row['description']}", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {row['description']}")
                st.markdown("**Suggested URLs:**")
                urls = row.get('suggested_urls', [])
                if urls:
                    for url in urls:
                        st.markdown(f"- [{url}]({url})")
                else:
                    st.write("No AI suggestions.")
            
            with col2:
                # Upload Form
                uploaded_file = st.file_uploader(f"Upload for {row['id']}", type=['png', 'jpg', 'jpeg'], key=row['id'])
                
                if uploaded_file:
                    # TODO: Implement actual Supabase Storage upload
                    # For now, we simulate success
                    st.success(f"Ready to upload {uploaded_file.name}")
                    
                    if st.button("Confirm Upload", key=f"btn_{row['id']}"):
                        # Dummy URL for now until Step 3
                        public_url = f"https://placeholder.com/{row['id']}.png"
                        if db.update_image_url(row['id'], public_url):
                            st.success("Updated DB!")
                            st.rerun()
                        else:
                            st.error("Failed to update.")
