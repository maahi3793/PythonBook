"""
Dashboard view for statistics and PDF export.
"""
import streamlit as st
import pandas as pd
from backend.db_textbook import TextbookDB

def render_dashboard(db: TextbookDB):
    st.title("📊 Textbook Dashboard")
    
    # Fetch Data
    # We can reuse get_all_chapters_metadata for basic stats
    chapters = db.get_all_chapters_metadata()
    
    if not chapters:
        st.info("No chapters data available.")
        return

    # 1. Progress Stats
    total = 179
    generated = len([c for c in chapters if c.get('status') in ['part1_done', 'part2_done', 'complete']])
    complete = len([c for c in chapters if c.get('status') == 'complete'])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Generated Days", f"{generated}/{total}")
    col2.metric("Fully Complete", f"{complete}/{total}")
    col3.metric("Completion Rate", f"{int(generated/total*100)}%")
    
    st.progress(generated/total)
    
    st.markdown("---")

    # 2. Bulk Actions (Phase 3.5)
    st.subheader("🛠️ Control Room")
    
    with st.expander("Batch Generation", expanded=True):
        c1, c2, c3 = st.columns([1, 1, 2])
        start_day = c1.number_input("Start Day", min_value=1, max_value=179, value=1)
        end_day = c2.number_input("End Day", min_value=1, max_value=179, value=5)
        
        if c3.button("🚀 Generate Range", use_container_width=True):
            if start_day > end_day:
                st.error("Start day must be <= End day")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                logs = st.empty()
                
                from backend.generator import TextbookGenerator
                gen = TextbookGenerator()
                
                total_days = end_day - start_day + 1
                
                for i, day in enumerate(range(start_day, end_day + 1)):
                    status_text.text(f"Processing Day {day}...")
                    # Generate all parts
                    res = gen.generate_day(day, 'all')
                    
                    logs.write(f"Day {day}: {res.get('message', 'Unknown')}")
                    progress_bar.progress((i + 1) / total_days)
                    
                st.success("Batch Complete!")
                st.rerun()

    st.markdown("---")
    
    # 3. PDF Export
    st.subheader("📤 Export Textbook")
    
    export_range = st.selectbox(
        "Select Range",
        ["Full Textbook (All Generated)", "First 10 Days (Preview)", "Specific Week"]
    )
    
    if st.button("Generate PDF 📄"):
        with st.spinner("Generating PDF... this may take a moment."):
            # 1. Filter chapters based on selection
            if "Full Textbook" in export_range:
                # Get all completed/generated chapters
                all_ch = db.client.table("textbook_chapters").select("*").order("day").execute()
                export_chapters = [c for c in all_ch.data if c.get('status') in ['part1_done', 'part2_done', 'complete']]
            elif "First 10" in export_range:
                # Preview
                all_ch = db.client.table("textbook_chapters").select("*").lte("day", 10).order("day").execute()
                export_chapters = [c for c in all_ch.data if c.get('status') in ['part1_done', 'part2_done', 'complete']]
            else:
                export_chapters = []
                st.warning("Selection not implemented.")
                return

            if not export_chapters:
                st.error("No valid chapters found to export.")
                return
                
            # 2. Call Exporter
            from backend.pdf_exporter import generate_pdf
            pdf_path = generate_pdf(export_chapters)
            
            # 3. Download Button
            if pdf_path:
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=f,
                        file_name="PythonBook_Complete.pdf",
                        mime="application/pdf"
                    )
                st.success("✅ PDF Generated successfully!")
            else:
                st.error("Failed to generate PDF. Check logs.")

    st.markdown("---")
    
    # 3. Recent Activity Table
    st.subheader("Recent Activity")
    df = pd.DataFrame(chapters)
    # Simple table of status
    st.dataframe(df[['day', 'title', 'status']].sort_values('day', ascending=False).head(10))
