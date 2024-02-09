import streamlit as st
from gensim.summarization import summarize


from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def sumy_summarizer(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result


def main():
    st.title("Summary and Text Preprocessing")
    activity1 = ["Summarize", "Text Preprocessing"]
    choice = st.sidebar.selectbox("Select Function", activity1)
    if choice == 'Summarize':
        st.subheader("Summary with NLP")
        raw_text = st.text_area("Enter Text Here")
        summary_choice = st.selectbox("Summary Choice", ["Genism", "Sumy Lex Rank"])

        if st.button("Summarize"):
            if summary_choice == "Genism":
                summary_result = summarize(raw_text)
            elif summary_choice == "Sumy Lex Rank":
                summary_result = sumy_summarizer(raw_text)

            st.write(summary_result)

    if choice == 'Text Preprocessing':
        st.subheader("Text Preprocessing")
        raw_text = st.text_area("Enter Text Here")
        choice2 = ["Convert to Lower Case", "Remove Punctuation", "Convert sentence into words"]
        choiceOperations = []
        choiceOperations = st.multiselect("Operations", choice2)

        out, flag = '', True
        if st.button("Process"):
            if "Convert to Lower Case" in choiceOperations:
                if flag:
                    out = raw_text.lower()
                    flag = False
                else:
                    out = out.lower()
            if "Remove Punctuation" in choiceOperations:
                punctuations = '''!()-[]{};:'"\,>./?@#$%^&*_~'''
                if flag:
                    for x in raw_text:
                        if x in punctuations:
                            out = raw_text.replace(x, "")
                            flag = False
                else:
                    for x in out:
                        if x in punctuations:
                            out = out.replace(x, "")
            if "Convert sentence into words" in choiceOperations:
                if flag:
                    out = raw_text.split()
                    flag = False
                else:
                    out = out.split()

        st.write(out)

if __name__ == '__main__':
    main()