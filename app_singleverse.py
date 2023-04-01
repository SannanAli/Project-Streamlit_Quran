import streamlit as st
import pandas as pd
import streamlit.components.v1 as stc
import random
from utils import HTML_RANDOM_TEMPLATE


@st.cache_data
def load_Quran(file):
    Quran = pd.read_excel(file)
    return Quran


def run_singleverse():
    st.subheader("Single Verse Search")

    df_Quran = load_Quran("resources\my_Quran.xlsx")
    df_Quran = pd.DataFrame(df_Quran)
    # st.dataframe(df_Quran)
    Sura_Name_list = df_Quran["Sura Name"].unique().tolist()
    Sura_Name = st.sidebar.selectbox("Sura Name", Sura_Name_list)
    Quran_df_sura = df_Quran[df_Quran["Sura Name"] == Sura_Name]
    st.dataframe(Quran_df_sura)

    chapter = st.sidebar.number_input("sura Number", 1, 114)
    verse = st.sidebar.number_input("Verse", 1, 6349)

    c1, c2 = st.columns([2, 1])

    with c1:  # for Single Verse
        try:
            selected_verse = df_Quran[
                (df_Quran["Sura Number"] == chapter)
                & (df_Quran["Ayat number"] == verse)
            ]
            # st.write(type(selected_verse))
            # st.dataframe(selected_verse,use_container_width=True)

            verse_details = "Sura Name : {} Chapter/Para : {} Sura Number : {}".format(
                selected_verse["Sura Name"].values[0], chapter, verse
            )
            st.success(verse_details)
            Ayat = "{}".format(selected_verse["Ayat e Quran"].values[0])
            st.write(Ayat)
        except:
            st.error("Verse is not included")

    with c2:
        st.success("Verse OF The Day")

        verse_list = range(20)

        verse_choice = random.choice(verse_list)
        random_sura_name = random.choice(Sura_Name_list)

        # st.write('{} {}'.format(random_sura_name,verse_choice))

        random_quran_df = df_Quran[df_Quran["Sura Name"] == random_sura_name]
        random_selected_verse = random_quran_df[
            random_quran_df["Ayat number"] == verse_choice
        ]

        try:
            today_verse = random_selected_verse["Ayat e Quran"].values[0]
        except:
            today_verse = random_selected_verse = random_quran_df[
                random_quran_df["Ayat number"] == 1
            ]["Ayat e Quran"].values[0]

        stc.html(HTML_RANDOM_TEMPLATE.format(today_verse), height=300)
