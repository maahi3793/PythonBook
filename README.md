# 📚 PythonBook: The PyDaily Companion Textbook

## Project Overview

**PythonBook** is an AI-generated CS-graduate-level Python textbook that transforms PyDaily's micro-lessons into comprehensive deep-dive chapters. It runs as a parallel daily process, generating textbook content from existing PyDaily lessons, quizzes, boss battles, and nuggets.

### Quick Facts

| Attribute | Value |
|-----------|-------|
| **GitHub Repo** | [github.com/maahi3793/PythonBook](https://github.com/maahi3793/PythonBook) |
| **Local Path** | `c:\Users\reach\.gemini\antigravity\scratch\relaunchpython\PythonBook` |
| **Database** | Reuses PyDaily's Supabase (same project, new tables) |
| **Hosting** | Streamlit Cloud (free) |
| **AI Model** | Google Gemini 1.5 Pro |
| **Output Formats** | PDF, ePub, HTML (via Pandoc) |

---

## Relationship to PyDaily

```
PyDaily (Parent Project)                  PythonBook (This Project)
════════════════════════                  ════════════════════════
📧 Daily 15-min lessons via email   →→→   📖 Deep-dive textbook chapters
🧠 Quizzes (20 questions)           →→→   🧪 Explained quiz solutions
⚔️ Boss Battles                     →→→   💪 Challenge walkthroughs
🎰 Nuggets (memes, tips, facts)     →→→   💡 Pro tips sections

Both share:
- Same Supabase database
- Same Gemini API
- Same GitHub account
```

---

## The Two Tones

### Tone 1: Academic Textbook (For Theory)
> "A Python list is implemented as a **dynamic array**. Unlike fixed-size arrays in C, Python lists automatically resize when elements are added..."

### Tone 2: Senior Mentor (For Tips/Advice)
> "Hey, quick tip from someone who learned this the hard way — never modify a list while iterating over it. I once spent 3 hours debugging a production issue..."

---

## Content Structure

Each chapter (one per PyDaily day) has 3 parts:

### Part 1: Theory (Generated at Call #1)
- What You'll Learn
- Expanded theory with diagrams (Mermaid code)
- "Under the Hood" technical explanation

### Part 2: Practice (Generated at Call #2)
- Real-World Use Case
- Quiz Questions with full explanations
- Boss Challenge + Solution walkthrough

### Part 3: Mentor (Generated at Call #3)
- Pro Tips (from nuggets)
- "Mentor Moment" (common pitfalls, career advice)
- Exercises (Easy/Medium/Hard)
- Further Reading (CPython links, PEPs)

### "Think Like a Dev" Content
- Weekly summaries after each 7 days
- Final consolidated chapter after Day 179

---

## Image Placeholder System

AI cannot generate images, but it suggests URLs from the internet:

```markdown
## Memory Layout

When Python allocates a list...

<!-- IMAGE_PLACEHOLDER: IMG_CH05_01 -->
<!-- DESCRIPTION: Python list memory diagram showing heap allocation -->
<!-- SUGGESTED_URLS:
  - https://realpython.com/images/list-internals.png
  - https://pythontutor.com/visualize/heap.png
-->

As shown above...
```

The web UI (PyTextbook Studio) shows:
1. All pending image placeholders
2. AI-suggested URLs (clickable)
3. Upload button for manual image selection
4. Preview before confirming

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SYSTEM ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────┐         ┌─────────────────────────┐   │
│  │    GitHub Actions       │         │      Supabase           │   │
│  │    (Daily Bot)          │         │   (Shared with PyDaily) │   │
│  │                         │         │                         │   │
│  │  08:00 IST: Part 1      │────────▶│  Tables:                │   │
│  │  10:00 IST: Part 2      │         │  - textbook_chapters    │   │
│  │  12:00 IST: Part 3      │         │  - textbook_images      │   │
│  │  14:00 IST: Weekly      │         │  - textbook_craft       │   │
│  │                         │         │                         │   │
│  │  Reads from:            │◀────────│  Existing PyDaily:      │   │
│  │  - daily_content        │         │  - daily_content        │   │
│  │  - quiz_questions       │         │  - quiz_questions       │   │
│  │  - boss_battles         │         │  - boss_battles         │   │
│  │  - feed (nuggets)       │         │  - feed                 │   │
│  └─────────────────────────┘         └─────────────────────────┘   │
│              │                                   │                  │
│              └───────────────┬───────────────────┘                  │
│                              ▼                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              PyTextbook Studio (Streamlit)                   │  │
│  │              https://pythonbook.streamlit.app                │  │
│  │                                                              │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌───────────┐ │  │
│  │  │  Chapter   │ │   Image    │ │   Export   │ │  Weekly   │ │  │
│  │  │  Browser   │ │  Manager   │ │   Tool     │ │  Summary  │ │  │
│  │  └────────────┘ └────────────┘ └────────────┘ └───────────┘ │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    OUTPUT (via Pandoc)                        │  │
│  │  📄 PDF  │  📱 ePub  │  🌐 HTML  │  📝 DOCX                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Daily Generation Schedule

| Time (IST) | UTC Cron | Action |
|------------|----------|--------|
| 08:00 | `30 2 * * *` | Generate Part 1: Theory |
| 10:00 | `30 4 * * *` | Generate Part 2: Practice |
| 12:00 | `30 6 * * *` | Generate Part 3: Mentor |
| 14:00 | `30 8 * * *` | Generate Weekly Summary (Saturdays only) |

---

## Database Schema (Add to Existing PyDaily Supabase)

```sql
-- ============================================
-- PYTHONBOOK TABLES (Add to PyDaily's Supabase)
-- ============================================

-- Main chapters table
CREATE TABLE textbook_chapters (
    id SERIAL PRIMARY KEY,
    day INTEGER UNIQUE NOT NULL,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'pending',  -- pending, part1_done, part2_done, complete, reviewed
    
    -- Content parts (generated separately)
    content_part1_theory TEXT,      -- What You'll Learn + Theory
    content_part2_practice TEXT,    -- Real-world + Quiz + Boss
    content_part3_mentor TEXT,      -- Pro Tips + Mentor + Exercises
    
    -- Timestamps
    generated_at TIMESTAMP,
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
CREATE TABLE textbook_images (
    id TEXT PRIMARY KEY,            -- e.g., 'IMG_CH05_01'
    chapter_day INTEGER REFERENCES textbook_chapters(day),
    description TEXT NOT NULL,
    suggested_urls JSONB,           -- ["url1", "url2", ...]
    selected_url TEXT,              -- What user chose
    storage_path TEXT,              -- Supabase Storage path after upload
    status TEXT DEFAULT 'pending',  -- pending, selected, uploaded
    created_at TIMESTAMP DEFAULT NOW()
);

-- "Think Like a Dev" content
CREATE TABLE textbook_craft (
    id SERIAL PRIMARY KEY,
    week INTEGER,                   -- 1, 2, 3, ... 26
    type TEXT NOT NULL,             -- 'weekly_summary' or 'final_chapter'
    content TEXT NOT NULL,
    status TEXT DEFAULT 'pending',  -- pending, generated, reviewed
    generated_at TIMESTAMP DEFAULT NOW()
);

-- Generation log (for debugging)
CREATE TABLE textbook_generation_log (
    id SERIAL PRIMARY KEY,
    day INTEGER,
    part TEXT,                      -- 'part1', 'part2', 'part3', 'weekly'
    status TEXT,                    -- 'started', 'completed', 'failed'
    error_message TEXT,
    tokens_used INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Project File Structure

```bash
PythonBook/
├── .github/
│   └── workflows/
│       └── textbook_scheduler.yml     # Daily content generation
│
├── backend/
│   ├── __init__.py
│   ├── db_textbook.py                 # Supabase CRUD for textbook tables
│   ├── gemini_textbook.py             # AI prompts for textbook generation
│   ├── image_extractor.py             # Parse and save image placeholders
│   └── export_service.py              # Pandoc PDF/ePub generation
│
├── prompts/
│   ├── part1_theory.md                # Prompt template for theory
│   ├── part2_practice.md              # Prompt template for practice
│   ├── part3_mentor.md                # Prompt template for mentor
│   └── weekly_summary.md              # Prompt template for weekly
│
├── views/
│   ├── chapter_browser.py             # Browse/view generated chapters
│   ├── image_manager.py               # Manage image placeholders
│   ├── export_tool.py                 # Generate PDF/ePub
│   └── weekly_view.py                 # View weekly summaries
│
├── assets/
│   ├── styles.css                     # Streamlit custom styles
│   └── setup_tables.sql               # Database setup script
│
├── output/                            # Generated files (gitignored)
│   ├── chapters/                      # Compiled markdown per day
│   └── exports/                       # PDF, ePub, HTML
│
├── run_textbook_bot.py                # CLI entry point for GitHub Actions
├── streamlit_app.py                   # Web UI entry point
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
└── .env.example                       # Environment variables template
```

---

## Environment Variables

```bash
# Reuse from PyDaily (same values)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key
GEMINI_API_KEY=your-gemini-key

# New (optional)
PANDOC_PATH=/usr/bin/pandoc    # For local PDF generation
```

---

## API Reference: Existing PyDaily Tables

The textbook bot reads from these **existing PyDaily tables**:

| Table | What We Read | Purpose |
|-------|--------------|---------|
| `daily_content` | `day`, `content` | Base lesson to expand |
| `quiz_questions` | `day`, `questions` | Quiz explanations |
| `boss_battles` | `day_range`, `challenge` | Boss challenge content |
| `feed` | `day`, `type`, `content` | Nuggets for pro tips |

**Important:** These tables already exist in PyDaily's Supabase. The textbook bot only READS from them, never writes.

---

## Implementation Phases

### Phase 1: Project Setup (Day 1-2)
- [ ] Create GitHub repo: `github.com/maahi3793/PythonBook`
- [ ] Initialize project structure locally
- [ ] Add Supabase tables (run `setup_tables.sql`)
- [ ] Create `.env` with existing PyDaily credentials
- [ ] Test Supabase connection

### Phase 2: Content Generation Bot (Day 2-3)
- [ ] Create `gemini_textbook.py` with prompts for Part 1/2/3
- [ ] Create `db_textbook.py` for CRUD operations
- [ ] Create `image_extractor.py` to parse placeholders
- [ ] Create `run_textbook_bot.py` CLI entry point
- [ ] Test with Day 1 content

### Phase 3: GitHub Actions (Day 3-4)
- [ ] Create `textbook_scheduler.yml`
- [ ] Set up secrets in GitHub repo
- [ ] Test scheduled runs

### Phase 4: Web UI - Chapter Browser (Day 4-5)
- [ ] Create Streamlit app structure
- [ ] Build chapter list view
- [ ] Build chapter detail view (rendered markdown)
- [ ] Add status indicators (pending/complete)

### Phase 5: Web UI - Image Manager (Day 5-6)
- [ ] Build image placeholder list
- [ ] Show AI-suggested URLs
- [ ] Implement image upload to Supabase Storage
- [ ] Preview uploaded images

### Phase 6: Export Tool (Day 6-7)
- [ ] Install Pandoc in GitHub Actions
- [ ] Create export service (PDF, ePub, HTML)
- [ ] Add export UI in Streamlit
- [ ] Test output quality

### Phase 7: Deploy & Monitor (Day 7)
- [ ] Deploy Streamlit app to Streamlit Cloud
- [ ] Verify daily generation is working
- [ ] Set up basic monitoring

### Phase 8: Daily Generation (Days 8-186)
- [ ] Let it run daily alongside PyDaily
- [ ] Periodically review image placeholders
- [ ] Fix any generation issues

### Phase 9: Final Compilation (Day 187+)
- [ ] Generate final "What's Next" chapter
- [ ] Review all content
- [ ] Compile complete PDF/ePub
- [ ] Upload to PyDaily portal (future paywall)

---

## Prompt Templates

### Part 1: Theory Prompt
```
You are writing a computer science textbook chapter.

CONTEXT:
- Topic: {topic}
- Day: {day}
- PyDaily Lesson Content: {lesson_content}

TASK:
Write a comprehensive theory section with:

1. "What You'll Learn" (3-5 bullet points)
2. Expanded Theory (800-1200 words)
   - Start with a real-world analogy
   - Explain the concept thoroughly
   - Include "Under the Hood" section about Python internals
3. Diagrams (as Mermaid code blocks where helpful)

TONE: Academic but approachable. Like MIT OpenCourseWare.

FORMAT: Return as Markdown. Use proper headings (##, ###).

For images, use this exact format:
<!-- IMAGE_PLACEHOLDER: IMG_CH{day:02d}_01 -->
<!-- DESCRIPTION: What the image should show -->
<!-- SUGGESTED_URLS:
  - https://example1.com/image.png
  - https://example2.com/diagram.png
-->
```

### Part 2: Practice Prompt
```
You are writing practice exercises for a Python textbook.

CONTEXT:
- Topic: {topic}
- Day: {day}
- Related Quiz Questions: {quiz_questions}
- Boss Battle Challenge: {boss_challenge}

TASK:
Write practice content:

1. "Real-World Use Case" (300-500 words)
   - Concrete scenario (e.g., "Imagine you're building a playlist app...")
   - Full code walkthrough with comments
   
2. "From the Quiz" (3-4 selected questions)
   - Show the question
   - Explain WHY the correct answer is correct
   - Common mistakes students make
   
3. "Boss Challenge Walkthrough"
   - Show the challenge
   - Step-by-step solution
   - Alternative approaches

TONE: Practical, hands-on. Like a workshop instructor.
FORMAT: Return as Markdown.
```

### Part 3: Mentor Prompt
```
You are a senior software engineer mentoring a junior developer.

CONTEXT:
- Topic: {topic}
- Day: {day}
- Related Nuggets: {nuggets}

TASK:
Write mentorship content:

1. "Pro Tips" (2-3 short tips)
   - From the nuggets, expand with practical advice
   
2. "Mentor Moment" (300-500 words)
   - Start with "Hey," or "Quick tip —"
   - Share a story or common mistake
   - Give career-relevant advice
   - Include interview gotchas for this topic
   
3. "Exercises"
   - 1 Easy (for practice)
   - 1 Medium (for understanding)
   - 1 Hard (interview-level)
   
4. "Further Reading"
   - Link to relevant CPython source code
   - Link to relevant PEPs
   - Link to official Python docs

TONE: Friendly, wise, like a cool senior at work.
FORMAT: Return as Markdown.
```

---

## Dependencies

```txt
# requirements.txt
streamlit>=1.30.0
supabase>=2.0.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
markdown>=3.5.0
Pillow>=10.0.0
```

For PDF generation (install separately):
```bash
# Ubuntu/Debian (GitHub Actions)
sudo apt-get install pandoc wkhtmltopdf

# Windows (local)
choco install pandoc wkhtmltopdf
```

---

## Getting Started (For New Chat)

1. Clone the repo:
   ```bash
   git clone https://github.com/maahi3793/PythonBook.git
   cd PythonBook
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment:
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase + Gemini credentials (same as PyDaily)
   ```

4. Create database tables:
   ```bash
   # Run the SQL in assets/setup_tables.sql in your Supabase SQL editor
   ```

5. Run locally:
   ```bash
   streamlit run streamlit_app.py
   ```

6. Generate Day 1 content manually:
   ```bash
   python run_textbook_bot.py --day 1 --part all
   ```

---

## Links

| Resource | URL |
|----------|-----|
| GitHub Repo | https://github.com/maahi3793/PythonBook |
| PyDaily Repo | https://github.com/maahi3793/PyDaily |
| Streamlit App | https://pythonbook.streamlit.app (after deploy) |
| Supabase Dashboard | (same as PyDaily) |

---

## License

MIT License - Same as PyDaily
