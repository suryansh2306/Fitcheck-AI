def css(theme: str) -> str:
    dark = theme == "Dark"
    bg = "#0f172a" if dark else "#f8fafc"
    surface = "#111c33" if dark else "#ffffff"
    surface_2 = "#17233f" if dark else "#f1f5f9"
    text = "#e5edf9" if dark else "#0f172a"
    muted = "#94a3b8" if dark else "#64748b"
    border = "rgba(148, 163, 184, 0.22)" if dark else "rgba(15, 23, 42, 0.08)"
    shadow = "0 18px 45px rgba(0,0,0,0.28)" if dark else "0 16px 40px rgba(15,23,42,0.08)"
    accent = "#8b5cf6" if dark else "#2563eb"
    accent_2 = "#22d3ee" if dark else "#7c3aed"

    return f"""
    <style>
    :root {{
        --fit-bg: {bg};
        --fit-surface: {surface};
        --fit-surface-2: {surface_2};
        --fit-text: {text};
        --fit-muted: {muted};
        --fit-border: {border};
        --fit-shadow: {shadow};
        --fit-accent: {accent};
        --fit-accent-2: {accent_2};
    }}
    .stApp {{
        background: var(--fit-bg);
        color: var(--fit-text);
        transition: background 250ms ease, color 250ms ease;
    }}
    [data-testid="stSidebar"] {{
        background: var(--fit-surface);
        border-right: 1px solid var(--fit-border);
    }}
    [data-testid="stSidebar"] * {{ color: var(--fit-text); }}
    .block-container {{
        padding-top: 1.8rem;
        max-width: 1280px;
    }}
    h1, h2, h3, h4, h5, h6, p, span, label {{ color: var(--fit-text); }}
    .muted {{ color: var(--fit-muted); }}
    .topbar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 1.3rem;
    }}
    .brand-title {{
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: 0;
        margin: 0;
    }}
    .brand-subtitle {{
        color: var(--fit-muted);
        margin-top: .2rem;
        font-size: .98rem;
    }}
    .card {{
        background: var(--fit-surface);
        border: 1px solid var(--fit-border);
        box-shadow: var(--fit-shadow);
        border-radius: 8px;
        padding: 1.2rem;
        transition: transform 180ms ease, border-color 180ms ease, background 250ms ease;
    }}
    .card:hover {{
        transform: translateY(-2px);
        border-color: color-mix(in srgb, var(--fit-accent) 45%, var(--fit-border));
    }}
    .metric-card {{
        background: linear-gradient(135deg, color-mix(in srgb, var(--fit-accent) 22%, var(--fit-surface)), var(--fit-surface));
        border: 1px solid color-mix(in srgb, var(--fit-accent) 36%, var(--fit-border));
        border-radius: 8px;
        padding: 1rem;
    }}
    .score-wrap {{
        width: 230px;
        height: 230px;
        margin: 0 auto;
        border-radius: 50%;
        display: grid;
        place-items: center;
        background: conic-gradient(var(--fit-accent-2) var(--score), var(--fit-surface-2) 0);
        box-shadow: 0 0 42px color-mix(in srgb, var(--fit-accent) 45%, transparent);
    }}
    .score-inner {{
        width: 170px;
        height: 170px;
        border-radius: 50%;
        background: var(--fit-surface);
        display: grid;
        place-items: center;
        border: 1px solid var(--fit-border);
    }}
    .score-number {{
        font-size: 3.1rem;
        font-weight: 900;
        background: linear-gradient(135deg, var(--fit-accent-2), var(--fit-accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .pill-grid {{
        display: flex;
        flex-wrap: wrap;
        gap: .55rem;
        margin-top: .7rem;
    }}
    .pill {{
        border-radius: 999px;
        padding: .5rem .72rem;
        border: 1px solid var(--fit-border);
        background: var(--fit-surface-2);
        color: var(--fit-text);
        font-size: .9rem;
    }}
    .pill.missing {{
        border-color: rgba(239, 68, 68, .35);
        background: rgba(239, 68, 68, .12);
    }}
    .pill.good {{
        border-color: rgba(34, 197, 94, .35);
        background: rgba(34, 197, 94, .12);
    }}
    .item-card {{
        border: 1px solid var(--fit-border);
        background: var(--fit-surface-2);
        border-radius: 8px;
        padding: .75rem .85rem;
        margin: .55rem 0;
        color: var(--fit-text);
    }}
    div.stButton > button, div.stDownloadButton > button {{
        border-radius: 8px;
        border: 0;
        background: linear-gradient(135deg, var(--fit-accent), var(--fit-accent-2));
        color: white;
        font-weight: 800;
        min-height: 2.8rem;
        box-shadow: 0 14px 30px color-mix(in srgb, var(--fit-accent) 28%, transparent);
    }}
    div.stButton > button:hover, div.stDownloadButton > button:hover {{
        transform: translateY(-1px);
        color: white;
    }}
    .stTextArea textarea, .stFileUploader, .stSelectbox, .stTextInput input {{
        color: var(--fit-text);
    }}
    [data-testid="stExpander"] {{
        background: var(--fit-surface);
        border: 1px solid var(--fit-border);
        border-radius: 8px;
    }}
    </style>
    """


def card(title: str, icon: str, body: str) -> str:
    return f"""<div class="card"><h3>{icon} {title}</h3>{body}</div>"""
