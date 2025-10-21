import streamlit as st
import pandas as pd
import fitz  # PyMuPDF

st.title("CV Skill Matching Assistant")

# Upload Excel file
excel_file = st.file_uploader("Upload Excel file with job skills", type=["xlsx"])
if excel_file:
    # Read the Excel file using openpyxl engine
    df_skills = pd.read_excel(excel_file, sheet_name="Skills Master JIE", engine="openpyxl")

    # Use actual column names from the Excel file
    if "Unnamed: 1" in df_skills.columns and "Unnamed: 3" in df_skills.columns:
        job_titles = df_skills["Unnamed: 1"].dropna().unique()
        selected_job = st.selectbox("Select a job title", sorted(job_titles))

        # Filter skills for selected job
        job_skills = df_skills[df_skills["Unnamed: 1"] == selected_job]["Unnamed: 3"].dropna().str.lower().unique()
        st.write(f"Found {len(job_skills)} skills for '{selected_job}'")

        # Upload CV PDFs
        uploaded_cvs = st.file_uploader("Upload CV PDFs", type=["pdf"], accept_multiple_files=True)
        if uploaded_cvs:
            results = []
            for cv_file in uploaded_cvs:
                doc = fitz.open(stream=cv_file.read(), filetype="pdf")
                text = ""
                for page in doc:
                    text += page.get_text()
                text = text.lower()

                matched = [skill for skill in job_skills if skill in text]
                results.append({
                    "CV Name": cv_file.name,
                    "Match Count": len(matched),
                    "Matched Skills": ", ".join(matched)
                })

            # Display results
            st.subheader("CV Match Results")
            st.dataframe(pd.DataFrame(results))
    else:
        st.error("Excel file must contain columns 'Unnamed: 1' for job titles and 'Unnamed: 3' for skill names.")