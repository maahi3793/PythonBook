def get_book_styles():
    return """
    <style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,300;1,400&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Fira+Code:wght@400;500&display=swap');

    /* =========================================
       TYPOGRAPHY
       ========================================= */
       
    /* Body Text */
    html, body, [class*="css"] {
        font-family: 'Merriweather', serif;
    }
    
    p, li, .stMarkdown, .stText {
        font-family: 'Merriweather', serif !important;
        color: #2C2C2C !important;
        font-size: 16px !important; /* Standard Book Size */
        line-height: 1.6 !important; /* Tighter */
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif !important;
        color: #1A1A1A !important;
        margin-top: 1.5em !important;
        margin-bottom: 0.5em !important;
    }
    
    h1 { font-size: 2.2rem !important; font-weight: 700 !important; border-bottom: 2px solid #F0EBE3; padding-bottom: 0.5rem; }
    h2 { font-size: 1.8rem !important; font-weight: 600 !important; }
    h3 { font-size: 1.4rem !important; font-weight: 600 !important; font-style: italic; }
    
    /* Code Blocks */
    code, .stCodeBlock {
        font-family: 'Fira Code', monospace !important;
        font-size: 13px !important; /* Smaller code */
        border-radius: 4px;
    }
    
    /* =========================================
       LAYOUT - THE "PAPER PAGE"
       ========================================= */
       
    /* Main Background */
    .stApp {
        background-color: #FDFBF7; 
        background-image: radial-gradient(#E8E4DD 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* The Content Page */
    .block-container {
        padding-top: 2rem !important; /* Reduced from 6rem */
        padding-bottom: 5rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        
        max-width: 750px !important; /* Tighter reading width */
        
        background-color: #FFFFFF;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08); /* Soft Shadow */
        margin-top: 2rem;
        border-radius: 2px;
        border: 1px solid #F2F0EB;
    }
    
    /* Mobile Responsiveness for Page */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            margin-top: 0rem;
            box-shadow: none;
        }
    }

    /* =========================================
       UI ELEMENTS cleanup
       ========================================= */
       
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #F7F5F0 !important;
        border-right: 1px solid #E6E2DC;
    }
    
    /* Hide Streamlit Header/Footer */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Buttons - Literary Style */
    .stButton>button {
        font-family: 'Merriweather', serif !important;
        font-weight: 700;
        background-color: white !important;
        border: 2px solid #8D6E63 !important;
        color: #8D6E63 !important;
        border-radius: 4px !important;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #8D6E63 !important;
        color: white !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Alerts/Info Boxes */
    .stAlert {
        font-family: 'Merriweather', serif !important;
        border-radius: 4px;
        border: 1px solid rgba(0,0,0,0.1);
    }
    
    </style>
    """
