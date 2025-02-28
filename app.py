import streamlit as st
import pandas as pd

# Streamlit app
st.title("Excel Duplicate Finder & Arranger")

# File upload
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.write("### Preview of Uploaded Data")
    st.dataframe(df.head())

    # Select columns for finding duplicates
    columns = st.multiselect("Select columns to identify duplicates", df.columns.tolist())

    if columns:
        # Identify duplicate rows based on selected columns
        df["is_duplicate"] = df.duplicated(subset=columns, keep=False)

        # Separate duplicates and non-duplicates
        df_duplicates = df[df["is_duplicate"]].drop(columns=["is_duplicate"])
        df_non_duplicates = df[~df["is_duplicate"]].drop(columns=["is_duplicate"])

        # Sort duplicates to arrange them together
        df_duplicates = df_duplicates.sort_values(by=columns)

        # Combine the sorted duplicates with non-duplicates
        df_final = pd.concat([df_duplicates, df_non_duplicates], ignore_index=True)

        st.write("### Processed Data")
        st.dataframe(df_final)

        # Provide option to download
        @st.cache_data
        def convert_df(df):
            return df.to_excel(index=False, engine='openpyxl')

        st.download_button(
            label="Download Processed Excel",
            data=convert_df(df_final),
            file_name="sorted_duplicates.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
