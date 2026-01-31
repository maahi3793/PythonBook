-- ============================================
-- PYTHONBOOK DATABASE SETUP
-- Run this in your Supabase SQL Editor
-- (Same Supabase project as PyDaily)
-- ============================================

-- Main chapters table
CREATE TABLE IF NOT EXISTS textbook_chapters (
    id SERIAL PRIMARY KEY,
    day INTEGER UNIQUE NOT NULL,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'pending',  -- pending, part1_done, part2_done, complete, reviewed
    
    -- Content parts (generated separately)
    content_part1_theory TEXT,      -- What You'll Learn + Theory
    content_part2_practice TEXT,    -- Real-world + Quiz + Boss
    content_part3_mentor TEXT,      -- Pro Tips + Mentor + Exercises
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    part1_at TIMESTAMP,
    part2_at TIMESTAMP,
    part3_at TIMESTAMP,
    reviewed_at TIMESTAMP,
    
    -- Source references (for traceability)
    source_lesson_id TEXT,
    source_quiz_id TEXT,
    source_boss_id TEXT
);

-- Image placeholders
CREATE TABLE IF NOT EXISTS textbook_images (
    id TEXT PRIMARY KEY,            -- e.g., 'IMG_CH05_01'
    chapter_day INTEGER REFERENCES textbook_chapters(day) ON DELETE CASCADE,
    description TEXT NOT NULL,
    suggested_urls JSONB DEFAULT '[]',  -- ["url1", "url2", ...]
    selected_url TEXT,              -- What user chose
    storage_path TEXT,              -- Supabase Storage path after upload
    status TEXT DEFAULT 'pending',  -- pending, selected, uploaded
    created_at TIMESTAMP DEFAULT NOW()
);

-- "Think Like a Dev" content
CREATE TABLE IF NOT EXISTS textbook_craft (
    id SERIAL PRIMARY KEY,
    week INTEGER,                   -- 1, 2, 3, ... 26 (NULL for final)
    type TEXT NOT NULL,             -- 'weekly_summary' or 'final_chapter'
    title TEXT,
    content TEXT NOT NULL,
    status TEXT DEFAULT 'pending',  -- pending, generated, reviewed
    created_at TIMESTAMP DEFAULT NOW()
);

-- Generation log (for debugging and monitoring)
CREATE TABLE IF NOT EXISTS textbook_generation_log (
    id SERIAL PRIMARY KEY,
    day INTEGER,
    part TEXT,                      -- 'part1', 'part2', 'part3', 'weekly', 'final'
    status TEXT,                    -- 'started', 'completed', 'failed'
    error_message TEXT,
    tokens_used INTEGER,
    duration_seconds FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- INDEXES for performance
-- ============================================
CREATE INDEX IF NOT EXISTS idx_chapters_day ON textbook_chapters(day);
CREATE INDEX IF NOT EXISTS idx_chapters_status ON textbook_chapters(status);
CREATE INDEX IF NOT EXISTS idx_images_chapter ON textbook_images(chapter_day);
CREATE INDEX IF NOT EXISTS idx_images_status ON textbook_images(status);
CREATE INDEX IF NOT EXISTS idx_craft_week ON textbook_craft(week);
CREATE INDEX IF NOT EXISTS idx_log_day ON textbook_generation_log(day);

-- ============================================
-- ROW LEVEL SECURITY (Optional - for Streamlit)
-- Allows read/write for authenticated service key
-- ============================================
ALTER TABLE textbook_chapters ENABLE ROW LEVEL SECURITY;
ALTER TABLE textbook_images ENABLE ROW LEVEL SECURITY;
ALTER TABLE textbook_craft ENABLE ROW LEVEL SECURITY;
ALTER TABLE textbook_generation_log ENABLE ROW LEVEL SECURITY;

-- Policy: Allow all operations for service key
CREATE POLICY "Service key full access" ON textbook_chapters FOR ALL USING (true);
CREATE POLICY "Service key full access" ON textbook_images FOR ALL USING (true);
CREATE POLICY "Service key full access" ON textbook_craft FOR ALL USING (true);
CREATE POLICY "Service key full access" ON textbook_generation_log FOR ALL USING (true);

-- ============================================
-- STORAGE BUCKET for images
-- Run this in Supabase Dashboard > Storage
-- ============================================
-- Create bucket: textbook-images
-- Make it public (or use signed URLs)
