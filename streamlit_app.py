"""Browse the published August 2026 AHU–VAV diagnostic evidence."""

import csv
from pathlib import Path

import streamlit as st


REPORT_DIR = Path(__file__).resolve().parent
VIEWS = {
    "Full-month timeline": ("01_month", "Read the signal panels at the same timestamp to relate temperature, airflow, damper indication, fan status, and sustained screening conditions."),
    "Signal relationships": ("02_relationships", "Each point represents one timestamp. Use the timeline to establish duration; scatter plots alone do not confirm a fault."),
    "Detailed event window": ("03_detail", "Inspect the selected window at the original 15-minute resolution, with surrounding context where available."),
}


def main():
    st.set_page_config(page_title="VAV Diagnostic Explorer", page_icon="📊", layout="wide")
    st.title("AHU–VAV Diagnostic Explorer")
    st.caption("August 2026 data · Report prepared 28 September 2026")
    st.write("Explore temperature, airflow, and damper evidence for ten VAV units served by AHU-3.")

    if not REPORT_DIR.is_dir():
        st.error("The diagnostic report folder is missing.")
        st.stop()

    with st.sidebar:
        st.header("Explore the report")
        vav = st.selectbox("VAV unit", [f"VAV{number:02d}" for number in range(1, 11)])
        view = st.radio("Plot", list(VIEWS))
        st.caption("Choose a unit and plot to explore the existing evidence. Plots show the recorded August dataset.")

    st.subheader(f"{vav} · {view}")
    suffix, description = VIEWS[view]
    st.write(description)
    if vav == "VAV09":
        st.info("VAV09 has no eligible samples: its three signals are constant across the dataset. The detail window helps inspect the frozen readings.")

    if view == "Detailed event window":
        windows_path = REPORT_DIR / "detail_window_selection.csv"
        if windows_path.is_file():
            with windows_path.open(encoding="utf-8-sig", newline="") as handle:
                window = next((row for row in csv.DictReader(handle) if row["vav"] == vav), None)
            if window:
                st.caption(f"Displayed window: {window['start']} to {window['end']}")
                st.write(window["reason"])

    image_path = REPORT_DIR / f"{vav}_{suffix}.png"
    if image_path.is_file():
        st.image(str(image_path), width="stretch")
        st.download_button("Download this plot at full resolution", image_path.read_bytes(), file_name=image_path.name, mime="image/png")
    else:
        st.error(f"The plot {image_path.name} is missing from the report folder.")

    guide_path = REPORT_DIR / "HOW_TO_READ_PLOTS.txt"
    with st.expander("How to read the plots"):
        if guide_path.is_file():
            st.text(guide_path.read_text(encoding="utf-8-sig"))
        else:
            st.warning("The reading guide is missing from the report folder.")

    st.subheader("Complete report")
    for label, filename, mime in (
        ("Download complete PDF", "All_VAV_diagnostic_plots.pdf", "application/pdf"),
        ("Download HTML gallery", "All_VAV_diagnostic_plots.html", "text/html"),
        ("Download reading guide", "HOW_TO_READ_PLOTS.txt", "text/plain"),
    ):
        path = REPORT_DIR / filename
        if path.is_file():
            st.download_button(label, path.read_bytes(), file_name=filename, mime=mime)

    st.caption("Screening conditions are investigation leads. Interpret them with the reading guide and supporting timeline evidence.")


if __name__ == "__main__":
    main()
