import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import os

# ----------------------------- #
# ✅ Streamlit page setup
# ----------------------------- #
st.set_page_config(page_title="Student Exam Dashboard", layout="wide")
sns.set_style("whitegrid")

# Ensure uploads folder exists
os.makedirs("uploads", exist_ok=True)

st.title("🎓 Student Exam Performance Dashboard")
st.write("Upload a semicolon-separated student CSV file (e.g., `student-mat.csv` from UCI).")

# ----------------------------- #
# 📁 File Upload
# ----------------------------- #
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, sep=';')
        st.success("✅ File uploaded and loaded successfully!")
        st.write("### Preview of Data")
        st.dataframe(df.head(10), height=250)

        with st.expander("🔍 Show full dataset"):
            st.dataframe(df, height=400)

        # Data cleaning
        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)
        df["TotalScore"] = df["G1"] + df["G2"] + df["G3"]

        # ----------------------------- #
        # 🧩 Visualization Options
        # ----------------------------- #
        st.subheader("📊 Select Visualizations to Display:")
        plot_gender = st.checkbox("Count plot of gender (sex)")
        plot_hist = st.checkbox("Histogram of final grades (G3)")
        plot_box = st.checkbox("Box plot of grades by sex")
        plot_heatmap = st.checkbox("Correlation heatmap")

        # ----------------------------- #
        # 📊 Count Plot
        # ----------------------------- #
        if plot_gender:
            st.markdown("### 🧑‍🤝‍🧑 Count Plot of Gender")
            fig, ax = plt.subplots()
            sns.countplot(x='sex', data=df, ax=ax)
            ax.set_xlabel("Sex")
            ax.set_ylabel("Count")
            plt.tight_layout()
            st.pyplot(fig)

            fig.savefig("uploads/gender_count_plot.png")
            buf = BytesIO()
            fig.savefig(buf, format='png')
            st.download_button("📥 Download Gender Plot", data=buf.getvalue(),
                               file_name="gender_count_plot.png", mime="image/png")

        # ----------------------------- #
        # 📊 Histogram
        # ----------------------------- #
        if plot_hist:
            st.markdown("### 📈 Histogram of Final Grades (G3)")
            fig, ax = plt.subplots()
            ax.hist(df['G3'], bins=10, color='skyblue', edgecolor='black')
            ax.set_xlabel("Final Grade G3")
            ax.set_ylabel("Number of Students")
            plt.tight_layout()
            st.pyplot(fig)

            fig.savefig("uploads/grade_histogram.png")
            buf = BytesIO()
            fig.savefig(buf, format='png')
            st.download_button("📥 Download Grade Histogram", data=buf.getvalue(),
                               file_name="grade_histogram.png", mime="image/png")

        # ----------------------------- #
        # 📊 Box Plot
        # ----------------------------- #
        if plot_box:
            st.markdown("### 📦 Box Plot of Final Grades by Sex")
            fig, ax = plt.subplots()
            sns.boxplot(x='sex', y='G3', data=df, ax=ax)
            ax.set_xlabel("Sex")
            ax.set_ylabel("Final Grade G3")
            plt.tight_layout()
            st.pyplot(fig)

            fig.savefig("uploads/boxplot_by_sex.png")
            buf = BytesIO()
            fig.savefig(buf, format='png')
            st.download_button("📥 Download Box Plot", data=buf.getvalue(),
                               file_name="boxplot_by_sex.png", mime="image/png")

        # ----------------------------- #
        # 📊 Correlation Heatmap
        # ----------------------------- #
        if plot_heatmap:
            st.markdown("### 🌡️ Correlation Heatmap")
            corr_matrix = df.select_dtypes(include='number').corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, fmt=".2f",
                        annot_kws={"fontsize": 8}, cmap='coolwarm', ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.yticks(rotation=0)
            plt.title("Correlation Heatmap")
            plt.tight_layout()
            st.pyplot(fig)

            fig.savefig("uploads/correlation_heatmap.png")
            buf = BytesIO()
            fig.savefig(buf, format='png')
            st.download_button("📥 Download Heatmap", data=buf.getvalue(),
                               file_name="correlation_heatmap.png", mime="image/png")

    except Exception as e:
        st.error(f"❌ Failed to load the file: {e}")

else:
    st.info("📤 Please upload a `.csv` file to start.")
