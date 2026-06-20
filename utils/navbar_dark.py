import streamlit as st

def render_navbar(active_page="home"):
    # Generate active classes
    def is_active(page):
        return 'class="active"' if active_page == page else ''

    css = """
    <style>
    :root {
      --nav-h: 64px;
      --font-head: 'DM Serif Display', serif;
    }
    
    /* Hide Streamlit chrome so navbar works and is clickable */
    header[data-testid="stHeader"] { 
        background: transparent !important; 
        pointer-events: none !important; 
        z-index: -1 !important;
    }
    
    /* Ensure content is pushed down below the fixed navbar */
    .block-container { 
        padding-top: calc(var(--nav-h) + 1rem) !important; 
    }

    nav#mainNav {
      --nav-brand:      #c9a84c;
      --nav-brand-2:    #a8852c;
      --nav-surface:    rgba(201,168,76,.14);
      --nav-ink:        #f0ede6;
      --nav-border:     rgba(201,168,76,.2);
      --nav-bg:         rgba(5, 10, 5, 0.96); /* Darker than the page backgrounds */
      --nav-shadow:     0 4px 20px rgba(0,0,0,.4);
      
      position: fixed; top: 0; left: 0; right: 0; z-index: 99999;
      height: var(--nav-h);
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 clamp(20px,5vw,60px);
      background: var(--nav-bg);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--nav-border);
      box-shadow: var(--nav-shadow);
      transition: background .3s;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }
    nav#mainNav .nav-logo {
      display: flex; align-items: center; gap: 10px;
      font-family: var(--font-head); font-weight: 400; font-size: 1.25rem;
      color: var(--nav-brand); cursor: pointer; text-decoration: none;
    }
    nav#mainNav .nav-logo-dot {
      width: 32px; height: 32px; border-radius: 8px;
      background: linear-gradient(135deg, var(--nav-brand), var(--nav-brand-2));
      display: flex; align-items: center; justify-content: center;
      color: #0f1a0f; font-size: 1rem; font-weight: 800; font-family: 'Plus Jakarta Sans', sans-serif;
    }
    nav#mainNav .nav-links {
      display: flex; align-items: center; gap: 4px;
      list-style: none; margin: 0; padding: 0;
    }
    nav#mainNav .nav-links a {
      padding: 8px 16px; border-radius: 8px;
      font-weight: 600; font-size: .85rem; color: var(--nav-ink);
      transition: all .2s; cursor: pointer; text-decoration: none;
    }
    nav#mainNav .nav-links a:hover, nav#mainNav .nav-links a.active {
      background: var(--nav-surface); color: var(--nav-brand);
    }
    nav#mainNav .nav-cta {
      background: linear-gradient(135deg, var(--nav-brand), var(--nav-brand-2)) !important;
      color: #0f1a0f !important; padding: 9px 20px !important;
      border-radius: 10px !important; font-weight: 700 !important;
      box-shadow: 0 4px 12px rgba(201,168,76,.25);
      transition: transform .15s, box-shadow .15s !important;
      margin-left: 10px;
    }
    nav#mainNav .nav-cta:hover { 
      transform: translateY(-1px); 
      box-shadow: 0 6px 16px rgba(201,168,76,.4) !important; 
    }
    
    @media (max-width: 768px) {
      nav#mainNav .nav-links { display: none; }
    }
    </style>
    """

    html = f"""
    {css}
    <nav id="mainNav">
      <a href="/home" target="_self" class="nav-logo">
        <div class="nav-logo-dot">D</div>
        DonasiCare
      </a>
      <ul class="nav-links" id="navLinks">
        <li><a href="/home" target="_self" {is_active('home')}>Beranda</a></li>
        <li><a href="/programdonasi" target="_self" {is_active('programdonasi')}>Program</a></li>
        <li><a href="/transparansi" target="_self" {is_active('transparansi')}>Transparansi</a></li>
        <li><a href="/volunteer" target="_self" {is_active('volunteer')}>Volunteer</a></li>
        <li><a href="/tentangkami" target="_self" {is_active('tentangkami')}>Tentang</a></li>
        <li><a href="/aichatbot" target="_self" class="nav-cta">AI Assistant &rarr;</a></li>
      </ul>
    </nav>
    """
    st.html(html)
