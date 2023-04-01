import streamlit as st
import spacy
import pandas as pd
from spacy import displacy
import streamlit.components.v1 as stc
from textblob import TextBlob
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")
import altair as alt
from collections import Counter

HTML_RANDOM_TEMPLATE = """
<div style='padding:10px;background-color:#E1E2E1;
			border-radius: 8px 34px 9px 26px;
-moz-border-radius: 8px 34px 9px 26px;
-webkit-border-radius: 8px 34px 9px 26px;
border: 2px ridge #000000;'>
<h5>Verse of the Day</h5>
<p>{}</p></div>
"""

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Streamlit HOLY QURAN APP </h1>
    </div>
    """


nlp = spacy.load("en_core_web_sm")


def render_entities(raw_text):
    docx = nlp(raw_text)
    html = displacy.render(docx, style="ent")
    html = html.replace("\n\n", "\n")
    result = HTML_WRAPPER.format(html)
    stc.html(result, height=500, scrolling=True)


def get_tags(docx):
    tagged_docx = TextBlob(docx).tags
    return tagged_docx


def plot_mendelhall_curve(docx):
    word_len = [len(token) for token in docx.split()]
    word_len_count = Counter(word_len)
    sorted_word_len_count = sorted(dict(word_len_count).items())
    x, y = zip(*sorted_word_len_count)
    fig = plt.figure(figsize=(20, 10))
    plt.plot(x, y)
    plt.title("plot of word length distribution")
    # plt.show()
    st.pyplot(fig)


def get_most_common_tokkens(docx, num=2):
    word_freq = Counter(docx.split())
    most_common_tokens = word_freq.most_common(num)
    return dict(most_common_tokens)


def plot_word_frequency_with_altair(docx, num=10):
    word_freq = Counter(docx.split())
    most_common_tokkens = dict(word_freq.most_common(num))
    word_freq_df = pd.DataFrame(
        {"Tokens": most_common_tokkens.keys(), "Count": most_common_tokkens.values()}
    )
    c = alt.Chart(word_freq_df).mark_bar().encode(x="Tokens", y="Count")
    st.altair_chart(c, use_container_width=True)


TAGS = {
    "NN": "green",
    "NNS": "green",
    "NNP": "green",
    "NNPS": "green",
    "VB": "blue",
    "VBD": "blue",
    "VBG": "blue",
    "VBN": "blue",
    "VBP": "blue",
    "VBZ": "blue",
    "JJ": "red",
    "JJR": "red",
    "JJS": "red",
    "RB": "cyan",
    "RBR": "cyan",
    "RBS": "cyan",
    "IN": "darkwhite",
    "POS": "darkyellow",
    "PRP$": "magenta",
    "PRP$": "magenta",
    "DET": "black",
    "CC": "black",
    "CD": "black",
    "WDT": "black",
    "WP": "black",
    "WP$": "black",
    "WRB": "black",
    "EX": "yellow",
    "FW": "yellow",
    "LS": "yellow",
    "MD": "yellow",
    "PDT": "yellow",
    "RP": "yellow",
    "SYM": "yellow",
    "TO": "yellow",
    "None": "off",
}


def mytag_visualizer(tagged_docx):
    colored_text = []
    for i in tagged_docx:
        if i[1] in TAGS.keys():
            token = i[0]
            # print(token)
            color_for_tag = TAGS.get(i[1])
            result = '<span style="color:{}">{}</span>'.format(color_for_tag, token)
            colored_text.append(result)
    result = " ".join(colored_text)
    # print(result)
    return result
