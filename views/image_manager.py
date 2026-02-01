"""
Admin view for managing missing images.
"""
import streamlit as st
import pandas as pd
from backend.db_textbook import TextbookDB

def render_image_manager(db: TextbookDB):
    st.title("🖼️ Image Manager")
    
    # Toggle to show all
    show_all = st.sidebar.checkbox("Show All Images (Including Uploaded)")
    
    # 1. Fetch images
    if show_all:
        try:
            res = db.client.table("textbook_images").select("*").order("chapter_day").execute()
            images = res.data
        except: images = []
    else:
        images = db.get_pending_images()
    
    if not images:
        st.success("✅ No images found.")
        return

    st.write(f"Found {len(images)} images.")
    
    # Convert to DataFrame for easier display
    df = pd.DataFrame(images)
    
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
                    st.info(f"Uploading {uploaded_file.name}...")
                    
                    if st.button("Confirm Upload", key=f"btn_{row['id']}"):
                        try:
                            # 1. Determine Path
                            # Use ID as filename to correspond to placeholder
                            ext = uploaded_file.name.split('.')[-1]
                            path = f"{row['id']}.{ext}" # e.g. IMG_CH01_01.png
                            
                            # 2. Upload to Storage
                            file_bytes = uploaded_file.getvalue()
                            size_kb = len(file_bytes) / 1024
                            st.write(f"📝 File Size: {size_kb:.2f} KB")
                            
                            content_type = f"image/{ext}" if ext != 'jpg' else 'image/jpeg'
                            
                            # Log attempt
                            st.write(f"🚀 Uploading to path: `{path}`...")
                            
                            res = db.client.storage.from_("textbook-images").upload(
                                path=path,
                                file=file_bytes,
                                file_options={"content-type": content_type, "upsert": "true"}
                            )
                            st.write(f"✅ Supabase Response: `{res}`")
                            
                            # 3. Get Public URL
                            public_url = db.client.storage.from_("textbook-images").get_public_url(path)
                            st.write(f"🔗 URL: `{public_url}`")
                            
                            # 4. Update DB
                            if db.update_image_url(row['id'], public_url):
                                st.success(f"✅ Upload Complete! Image saved to DB.")
                                if st.button("Reload Page", key=f"reload_{row['id']}"):
                                    st.rerun()
                            else:
                                st.error("❌ Failed to update database record.")
                                
                        except Exception as e:
                            st.error(f"❌ Upload Failed Details: {e}")
                            logging.error(f"Upload failed: {e}")
