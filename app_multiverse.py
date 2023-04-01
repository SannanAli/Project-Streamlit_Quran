import streamlit as st
import pandas as pd
import streamlit.components.v1 as stc
from utils import *
import neattext.functions as ntx


@st.cache_data
def load_Quran(file):
    Quran = pd.read_excel(file)
    return Quran


def run_multiverse():
    st.subheader("Multi Verse Search")

    df_Quran = load_Quran("resources\my_Quran.xlsx")
    df_Quran = pd.DataFrame(df_Quran)
    # st.dataframe(df_Quran)
    Sura_Name_list = df_Quran["Sura Name"].unique().tolist()
    Sura_Name = st.sidebar.selectbox("Sura Name", Sura_Name_list)

    para_name_list = df_Quran["Para"].unique().tolist()
    para_name = st.sidebar.selectbox("Para/Chapter", para_name_list)
    Quran_df_para = df_Quran[df_Quran["Para"] == para_name]
    st.dataframe(Quran_df_para)
    all_verses = Quran_df_para["Ayat number"].unique().tolist()
    st.dataframe(all_verses)
    verses = st.sidebar.multiselect("Ayat Number", all_verses)
    selected_verses = Quran_df_para.iloc[verses]
    st.dataframe(selected_verses)

    verse_details = "Sura Name : {} Chapter/Para : {} Ayat Number : {}".format(
        Sura_Name, Quran_df_para["Para"].values[0], verses
    )
    st.info(verse_details)
    c1, c2 = st.columns(2)
    # join all text in a sentence in String
    docx = "".join(selected_verses["Ayat e Quran"].tolist())

    with c1:
        st.info("Details")
        for row in selected_verses.iterrows():
            st.write(row["Ayat e Quran"])

    with c2:
        st.info("Study")
        with st.expander("Visualize Entities"):
            st.warning("Select more then 5 Ayats")
            render_entities(docx)

        with st.expander("Visualize POS Tags"):
            tagged_docx = get_tags(docx)
            processed_tags = mytag_visualizer(tagged_docx)
            stc.html(processed_tags, height=500, scrolling=True)

        with st.expander("Keywords Tokens"):
            processed_keywords = ntx.remove_shortwords(docx)
            keywords_tokens = get_most_common_tokkens(processed_keywords, 4)
            st.write(keywords_tokens)

    with st.expander("Mendelhall Curve of Ayat"):
        try:
            plot_mendelhall_curve(docx)
        except:
            st.warning("Select Atleast 2 Ayats")
    with st.expander("Word Frequency Plot"):
        try:
            plot_word_frequency_with_altair(docx)
        except Exception as e:
            st.write(e)
    with st.expander("POS TAG Plot"):
        tagged_docx = get_tags(docx)
        tagged_docx_df = pd.DataFrame(tagged_docx, columns=["Tokken", "Tags"])
        # st.dataframe(tagged_docx_df)
        df_tag_count = tagged_docx_df["Tags"].value_counts().to_frame("Counts")
        df_tag_count["tag_type"] = df_tag_count.index
        # st.dataframe(df_tag_count)

        c = alt.Chart(df_tag_count).mark_bar().encode(x="tag_type", y="Counts")
        st.altair_chart(c, use_container_width=True)
