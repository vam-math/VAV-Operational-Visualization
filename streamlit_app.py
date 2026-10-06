"""Present the original HTML gallery inside a minimal Streamlit shell."""

import base64
from pathlib import Path

import streamlit as st

REPORT_DIR = Path(__file__).resolve().parent


def gallery_html():
    """Preserve the gallery and make its relative file links downloadable."""
    html = (REPORT_DIR / "All_VAV_diagnostic_plots.html").read_text(encoding="utf-8-sig")
    for filename, mime in (
        ("HOW_TO_READ_PLOTS.txt", "text/plain;charset=utf-8"),
        ("All_VAV_diagnostic_plots.pdf", "application/pdf"),
    ):
        encoded = base64.b64encode((REPORT_DIR / filename).read_bytes()).decode("ascii")
        html = html.replace(
            f'href="{filename}"',
            f'href="data:{mime};base64,{encoded}" download="{filename}"',
        )
    if 'name="viewport"' not in html:
        html = html.replace("<head>", '<head><meta name="viewport" content="width=device-width, initial-scale=1">', 1)
    return html


def main():
    st.set_page_config(
        page_title="All VAV diagnostic evidence",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    # The iframe owns scrolling so the original sticky navigation still works.
    st.html("""
        <style>
        [data-testid="stHeader"], [data-testid="stToolbar"],
        [data-testid="stDecoration"], footer { display: none !important; }
        [data-testid="stAppViewContainer"], [data-testid="stMain"] {
            background: #edf1f5;
        }
        [data-testid="stMainBlockContainer"] {
            max-width: none;
            padding: 0;
        }
        [data-testid="stVerticalBlock"] { gap: 0; }
        iframe {
            display: block;
            width: 100%;
            height: 100dvh !important;
            border: 0;
        }
        </style>
    """)
    try:
        html = gallery_html()
    except FileNotFoundError as error:
        st.error(f"A required report file is missing: {Path(error.filename).name}")
        st.stop()
    st.iframe(html, height=900, alt="AHU–VAV diagnostic plots for August 2026")


if __name__ == "__main__":
    main()
