import time
from transformers import pipeline
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import nlp as nlp
import pandas as pd
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
import streamlit.components.v1 as html
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import streamlit.components.v1 as stc
# File Processing Pkgs
import docx2txt
from PIL import Image
from PyPDF2 import PdfFileReader
import pdfplumber
#import cv2
import cv
from PIL import Image
import  numpy as np
import base64
import plotly.express as px
from streamlit_option_menu import option_menu
import requests
import neattext.functions as nfx
import torch
import streamlit as st
from transformers import BartTokenizer, BartForConditionalGeneration
from transformers import T5Tokenizer, T5ForConditionalGeneration
import warnings
import   gensim
#from gensim.summarization import  summarize
import sqlite3

st.set_page_config( page_title ="论 文 帮 助 A p p" , layout="wide",initial_sidebar_state='expanded', page_icon="🌎" )

# Warnings ignore
#warnings.filterwarnings(action='ignore')
st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('deprecation.showPyplotGlobalUse', False)


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def local_css(file_name):
    with open(file_name) as f:
      st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html= True)
local_css("style.css")

#html_temp = """
 #       <div style = "background-color:none;padding:5px;border-radius:30px;width :auto;">
  #      <h1 style = "color:white;text-align:center;font-size:20px;">检测并聊 </h1>
   #     </div>
    #    """
#royalblue
#components.html(html_temp)

#############DB##########
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate,DATE)')

def add_data(author, title, article, postdate):
    c.execute('INSERT INTO blogtable(author,title,article,postdate) VALUES (?,?,?,?)',
              (author, title, article, postdate))
    conn.commit()

def view_all_notes():
    c.execute('SELECT * FROM blogtable')
    data = c.fetchall()
    # for row in data:
    # 	print(row)
    return data

def view_all_titles():
    c.execute('SELECT DISTINCT title FROM blogtable')
    data = c.fetchall()
    # for row in data:
    # 	print(row)
    return data

def get_single_blog(title):
    c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
    data = c.fetchall()
    return data

def get_blog_by_title(title):
    c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
    data = c.fetchall()
    return data

def get_blog_by_author(author):
    c.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
    data = c.fetchall()
    return data

def get_blog_by_msg(article):
    c.execute("SELECT * FROM blogtable WHERE article like '%{}%'".format(article))
    data = c.fetchall()
    return data

def edit_blog_author(author, new_author):
    c.execute('UPDATE blogtable SET author ="{}" WHERE author="{}"'.format(new_author, author))
    conn.commit()
    data = c.fetchall()
    return data

def edit_blog_title(title, new_title):
    c.execute('UPDATE blogtable SET title ="{}" WHERE title="{}"'.format(new_title, title))
    conn.commit()
    data = c.fetchall()
    return data

def edit_blog_article(article, new_article):
    c.execute('UPDATE blogtable SET title ="{}" WHERE title="{}"'.format(new_article, article
                                                                         ))
    conn.commit()
    data = c.fetchall()
    return data

def delete_data(title):
    c.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
    conn.commit()

# Avatar Image using a url
avatar1 = "https://www.w3schools.com/howto/img_avatar1.png"
avatar2 = "https://www.w3schools.com/howto/img_avatar2.png"


# Reading Time
def readingTime(mytext):
    total_words = len([token for token in mytext.split(" ")])
    estimatedTime = total_words / 200.0
    return estimatedTime

def analyze_text(text):
    return nlp(text)

# Layout Templates
title_temp = """
	<div style="background-color:silver;padding:6px;border-radius:8px;margin:6px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 40px;border-radius: 50%;" >
	<h6 style="color:white;">Author:{}</h6>
	<br/>
	<br/>	
	<p style="text-align:justify">{}</p>
	</div>
	"""
article_temp = """
	<div style="background-color:#464e5f;padding:7px;border-radius:5px;margin:7px;color:white;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<h6 style="color:white;">Author:{}</h6> 
	<h6 style="color:white;">共享日期: {}</h6>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
	<br/>
	<br/>
	<p style="text-align:justify;color:white;">{}</p>
	</div>
	"""
head_message_temp = """
	<div style="background-color:gray;padding:7px;border-radius:5px;margin:7px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;">
	<h6 style = "color:white;">Author:{}</h6> 		
	<h6 styles = color:white;">共享日期: {}</h6>		
	</div>
	"""
full_message_temp = """
	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<p style="text-align:justify;color:black;padding:10px">{}</p>
	</div>
	"""

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

def main():
 #   """A Simple CRUD Blog App"""
  #  html_temp = """
	#	<div style="background-color:{};padding:5px;border-radius:5px">
	#	<h1 style="color:{};text-align:center;line-height:25px;">学生科学团总支<br><small>(遵义师范学院)</small> <br><small>论文和项目执行</small> </h1>
	#	</div>
	#	"""
    custom_title = """
     <div style="font-size:60px;font-weight:bolder;background-color:#fff;padding:10px;
     border-radius:10px;border:5px solid royalblue;text-align:center;line-height:60px;">
     		<span style='color:blue'>学</span>
     		<span style='color:black'>生</span>
     		<span style='color:red'>科</span>
     		<span style='color:green'>学</span>
     		<span style='color:purple'>团</span>
     		<span style='color:blue'>总</span>
     		<span style='color:red'>支</span><br>
     		<span style='color:blue'>(</span>
     		<span style='color:red'><small>论</small></span>
     		<span style='color:black'><small>文</small></span>
     		<span style='color:red'><small>帮</small></span>
     		<span style='color:green'><small>助</small></span>
     		<span style='color:yellow'>A</span>
     		<span style='color:black'>p</span>
     		<span style='color:blue'>p</span>
     		<span style='color:blue'>)</span>
     </div>
     """
    #st.markdown(html_temp.format('royalblue', 'white'), unsafe_allow_html=True)
    st.markdown(custom_title.format('royalblue', 'white'), unsafe_allow_html=True)

    with st.sidebar:
        image_lottie_animation = Image.open(r"C:\Users\ADMIN\Desktop\MachieLearnig APP\images\logozunyi.jpg")
        st.image(image_lottie_animation, output_format="auto", width=300)

    with st.sidebar:
        selected = option_menu(menu_title="遵义师范学院:论文和项目执行", options=["首页", "查看摘要", "分享摘要", "搜索", "摘要词云图关键字","总结论文摘要","分享文件","分享设计和实现结果的截图","技术","学习编程语言","看视频","关于我们","联系我们"],
                               icons=['bank', 'bookmark-check', 'share', 'search','cloud','check-all','share-fill','card-image','gear-wide-connected','braces','tv-fill','file-earmark-person-fill','person-lines-fill'],
                               default_index=0
                               )

        styles = {
              "container ": {"padding": "0!important", "background-color": "white"},
              "icon": {"color": "blue", "font-size": "25px"},
              "nav-link": {
              "font-size": "25px",
               "text-align": "left",
             "margin": "0px",
             "--hover-color": "blue",

              },
           "nav-link-selected": {"background-color": "blue"},

           }

    if selected == "首页":
        st.subheader("首页:")
        st.write("这里只显示了主题及其作者，如果你想要详细信息，请搜索！")
        result = view_all_notes()
        for i in result:
            # short_article = str(i[2])[0:int(len(i[2])/2)]
            short_article = str(i[2])[0:50]
            st.write(title_temp.format(i[1], i[0], short_article), unsafe_allow_html=True)

    # st.write(result)
    elif selected == "查看摘要":
        st.subheader("查看摘要或者研究项目:")
        st.write("这里只显示了一个摘要，如果你想要更多，请搜索!")

        all_titles = [i[0] for i in view_all_titles()]
        postlist = st.sidebar.selectbox("共享摘要和项目", all_titles)
        post_result = get_blog_by_title(postlist)
        for i in post_result:
            st.text("阅读时间:{} minutes".format(readingTime(str(i[2]))))
            st.markdown(head_message_temp.format(i[1], i[0], i[3]), unsafe_allow_html=True)
            st.markdown(full_message_temp.format(i[2]), unsafe_allow_html=True)

        # if st.button("Analyze"):
        # 	docx = analyze_text(i[2])
        # 	html = displacy.render(docx,style="ent")
        # 	html = html.replace("\n\n","\n")
        # 	st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)

    elif selected == "分享摘要":
        st.subheader("上传论文摘要或者项目研究:")
        create_table()
        blog_title = st.text_input('输入研究标题:')
        blog_author = st.text_input("输入作者姓名:", max_chars=50)
        blog_article = st.text_area("输入摘要或研究项目:", height=200)
        blog_post_date = st.date_input("共享日期")
        if st.button("分享"):
            add_data(blog_author, blog_title, blog_article, blog_post_date)
            st.success("Post::'{}' 摘要已分享".format(blog_title))

    elif selected == "搜索":
        st.subheader("搜索论文摘要和导言:")
        search_term = st.text_input("输入标题或作者姓名")
        search_choice = st.radio("搜索字段:", ("title", "author"))
        if st.button('搜索'):
            if search_choice == "title":
                article_result = get_blog_by_title(search_term)
            elif search_choice == "author":
                article_result = get_blog_by_author(search_term)

            # Preview Articles
            for i in article_result:
                st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
                #st.write(article_temp.format(i[1],i[0],i[3],i[2]),unsafe_allow_html=True)
                st.write(head_message_temp.format(i[1], i[0],i[3]),unsafe_allow_html=True)
                st.write(full_message_temp.format(i[2]), unsafe_allow_html=True)


    elif selected == "摘要词云图关键字":
        st.subheader("管理论文摘要和项目:")
        st.write("找关键字")
        result = view_all_notes()
        clean_db = pd.DataFrame(result, columns=["Author", "Title", "Article", "Date", "Index"])
        st.dataframe(clean_db)
        unique_list = [i[0] for i in view_all_titles()]
        delete_by_title = st.selectbox("选择适合你研究方向的主题", unique_list)
        if st.button("删除"):
            delete_data(delete_by_title)
            st.warning("Deleted: '{}'".format(delete_by_title))

        if st.checkbox("Metrics"):
            new_df = clean_db
            new_df['Length'] = new_df['Article'].str.len()

            st.dataframe(new_df)
           # st.dataframe(new_df['Author'].value_counts())
            st.subheader("作者统计信息:")
            new_df['Author'].value_counts().plot(kind='bar')
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()

            new_df['Author'].value_counts().plot.pie(autopct="%1.1f%%")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()

        if st.checkbox("WordCloud"):
                # text = clean_db['Article'].iloc[0]
                st.subheader("Word Cloud:画出来摘要的关键字:")
                text = ', '.join(clean_db['Article'])
                # Create and generate a word cloud image:
                wordcloud = WordCloud().generate(text)
                # Display the generated image:
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()

        if st.checkbox("BarH Plot"):
                st.subheader("摘要长度:")
                new_df = clean_db
                new_df['Length'] = new_df['Article'].str.len()
                barh_plot = new_df.plot.barh(x='Author', y='Length', figsize=(10, 10))
                st.write(barh_plot)
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()

    elif selected == "总结论文摘要":
        st.subheader("使用TLDR-izer's NLP Algorithm:总结你的摘要: ")
        warnings.filterwarnings(action='ignore')
        st.set_option('deprecation.showfileUploaderEncoding', False)
        st.set_option('deprecation.showPyplotGlobalUse', False)

        os.environ["TOKENIZERS_PARALLELISM"] = "true"

        st.write("# 以更高的英语语法效率和准确性，总结你的论文简介、摘要、文章等等!")
        article = st.text_area('Enter your Text:', height=200,max_chars=100000)

        if st.button("Summarize"):
            st.write("Your summary:")
            summarizer = pipeline("summarization")
            output = summarizer(article, min_length=50, max_length=150)
            st.write(output[0]['summary_text'])

    elif selected == "分享文件":
        st.subheader("上传文件:")
        if "photo" not in st.session_state:
            st.session_state["photo"]= "not done"

        col1,col2,col3 = st.columns([1,2,1])

        col1.markdown(" # Welcome to  论 文 帮 助 A p p ")
        col1.markdown(" Here is some information my project ")

        def change_photo_state():
            st.session_state["photo"]="done"

        uploaded_photo = col2.file_uploader("Upload a Photo",on_change=change_photo_state)
        camera_photo = col2.camera_input("Take a photo",on_change=change_photo_state)

        if st.session_state["photo"] == "done":
            progress_bar = col2.progress(0)

            for perc_completed in range(100):
                time.sleep(0.05)
                progress_bar.progress(perc_completed+1)

            col2.success("photo successfully uploaded")

            col3.metric(label= "Temp",value = "60 'C",delta = "3 'c")

            with st.expander("click to read and see my projects "):
                st.write("hello,here is some info you are looking for")

                if uploaded_photo is None:
                    st.image(camera_photo)

                else:
                    st.image(uploaded_photo)

    elif selected == "分享设计和实现结果的截图":
        st.subheader("上传项目截图:")
        if "photo" not in st.session_state:
            st.session_state["photo"]= "not done"

        col1,col2,col3 = st.columns([1,2,1])

        col1.markdown(" # Welcome to  论 文 帮 助 A p p ")
        col1.markdown(" Here is some information about my project ")

        def change_photo_state():
            st.session_state["photo"]="done"

        uploaded_photo = col2.file_uploader("Upload a Photo",on_change=change_photo_state)
        camera_photo = col2.camera_input("Take a photo",on_change=change_photo_state)

        if st.session_state["photo"] == "done":
            progress_bar = col2.progress(0)

            for perc_completed in range(100):
                time.sleep(0.05)
                progress_bar.progress(perc_completed+1)

            col2.success("photo successfully uploaded")

            col3.metric(label= "Temp",value = "60 'C",delta = "3 'c")

            with st.expander("click to read and see my projects "):
                st.write("hello,here is some info you are looking for")

                if uploaded_photo is None:
                    st.image(camera_photo)

                else:
                    st.image(uploaded_photo)

    elif  selected == "技术":
        st.subheader("遵义师范学院科学:")

    elif selected == "学习编程语言":
        st.subheader("理解这些编程语言的不同:")
        a,b,d,e,f,g = st.columns(6)
        with a:
            st.write("大数据")
            lottie_coding = load_lottieurl("https://assets1.lottiefiles.com/private_files/lf30_ajzyv37m.json")
            st_lottie(lottie_coding, height=110, key="data science")
            st.write("---")
            st.write("基本代码")
            st.code("""
            from pandas import DataFrame
            from pandas import Series

            #造数据
            df=DataFrame({'age':Series([26,85,85]),'name':Series(['xiaoqiang1','xiaoqiang2','xiaoqiang2'])})
            df

            #判断是否有重复行
            df.duplicated()

            #移除重复行
             df.drop_duplicates()
            """)
            st.write("""
            
            大数据是指无法在一定时间内用常规软件工具对其内容进行抓取、管理和处理的数据集合。大数据技术，是指从各种各样类型的数据中，快速获得有价值信息的能力。适用于大数据的技术，包括大规模并行处理（MPP）数据库，数据挖掘电网，分布式文件系统，分布式数据库，云计算平台，互联网，和可扩展的存储系统。
             大数据的特点.

　　         具体来说，大数据具有4个基本特征：

　　         一 是数据体量巨大。百度资料表明，其新首页导航每天需要提供的数据超过1.5PB（1PB=1024TB），这些数据如果打印出来将超过5千亿张A4纸。有资料证实，到目前为止，人类生产的所有印刷材料的数据量仅为200PB。

　　         二 是数据类型多样。现在的数据类型不仅是文本形式，更多的是图片、视频、音频、地理位置信息等多类型的数据，个性化数据占绝对多数。

　　         三 是处理速度快。数据处理遵循“1秒定律”，可从各种类型的数据中快速获得高价值的信息。

　　         四 是价值密度低。以视频为例，一小时的视频，在不间断的监控过程中，可能有用的数据仅仅只有一两秒。

            - 浅谈数据科学
              数据科学（Data Science）这一概念自大数据崛起也随之成为数据领域的讨论热点，从去年开始，“数据科学家”便成为了一个工作职位出现在各种招聘信息上。那么究竟什么是数据科学？大数据和数据科学又是什么关系？大数据在数据科学中起到怎样的作用？欢迎进入大数据学习扣群522189307，一起学习交流，本文主要是想起到科普作用，使即将或正在从事数据工作的朋友对数据科学工作有一个全概貌了解，也使各有想法进入大数据领域的朋友在真正从事大数据工作之前对行业的情况有所知晓。数据科学是一个混合交叉学科（如下图所示），要完整的成为一个数据科学家，就需要具备较好的数学和计算机知识，以及某一个专业领域的知识。所做的工作都是围绕数据打转转，在数据量爆发之后，大数据被看做是数据科学中的一个分支。

            - 浅谈大数据

            大数据（Big Data）其实已经兴起好些年了，只是随着无处不在的传感器、无处不在的数据埋点，获取数据变得越来越容易、量越来越大、内容越来越多样化，于是原来传统的数据领域不得不思考重新换一个平台可以处理和使用逐渐庞大数据量的新平台。用以下两点进一步阐述：

             吴军博士提出的一个观点：现有产业+新技术=新产业，大数据也符合这个原则，只是催生出来的不仅仅是一个新产业，而是一个完整的产业链：原有的数据领域+新的大数据技术=大数据产业链；

             数据使用的范围，原来的数据应用主要是从现有数据中的数据中进行采样，再做数据挖掘和分析，发掘出数据中的潜在规则用以预测或决策，然而采样始终会舍弃一部分数据，即会丢失一部分潜在规则和价值，随着数据量和内容的不断累积，企业越来越重视在数据应用时可以使用全量数据，可以尽可能的覆盖所有潜在规则从而发掘出可能想到或从未想到的价值。

             如下图所示，大数据领域可以分为以下几个主要方向：

            - 数据平台
             Data Platform，构建、维护稳定、安全的大数据平台，按需设计大数据架构，调研选型大数据技术产品、方案，实施部署上线。对于大数据领域涉及到的大多数技术都需要求有所了解，并精通给一部分，具备分布式系统的只是背景。

            - 2数据采集
              Data Collecting，从Web/Sensor/RDBMS等渠道获取数据，为大数据平台提供数据来源，如Apache Nutch是开源的分布式数据采集组件，大家熟知的Python爬虫框架ScraPy等。

           - 数据仓库
              Data Warehouse，有点类似于传统的数据仓库工作内容：设计数仓层级结构、ETL、进行数据建模，但基于的平台不一样，在大数据时代，数据仓库大多基于大数据技术实现，例如Hive就是基于Hadoop的数据仓库。

           - 数据处理
              Data Processing，完成某些特定需求中的处理或数据清洗，在小团队中是结合在数据仓库中一起做的，以前做ETL或许是利用工具直接配置处理一些过滤项，写代码部分会比较少，如今在大数据平台上做数据处理可以利用更多的代码方式做更多样化的处理，所需技术有Hive、Hadoop、Spark等。BTW，千万不要小看数据处理，后续的数据分析、数据挖掘等工作都是基于数据处理的质量，可以说数据处理在整个流程中有特别重要的位置。

            -  数据分析
              Data Analysis，基于统计分析方法做数据分析：例如回归分析、方差分析等。大数据分析例如Ad-Hoc交互式分析、SQL on Hadoop的技术有：Hive 、Impala、Presto、Spark SQL，支持OLAP的技术有：Kylin。

            - 数据挖掘
              Data Mining，是一个比较宽泛的概念，可以直接理解为从大量数据中发现有用的信息。大数据中的数据挖掘，主要是设计并在大数据平台上实现数据挖掘算法：分类算法、聚类算法、关联分析等。

            - 机器学习
             Machine Learning，与数据挖掘经常一起讨论，甚至被认为是同一事物。机器学习是一个计算机与统计学交叉的学科，基本目标是学习一个x->y的函数（映射），来做分类或者回归的工作。之所以经常和数据挖掘合在一起讲是因为现在好多数据挖掘的工作是通过机器学习提供的算法工具实现的，例如个性化推荐，是通过机器学习的一些算法分析平台上的各种购买，浏览和收藏日志，得到一个推荐模型，来预测你喜欢的商品。

            - 深度学习
              Deep Learning，是机器学习里面的一个topic（非常火的Topic），从深度学习的内容来看其本身是神经网络算法的衍生，在图像、语音、自然语言等分类和识别上取得了非常好的效果，大部分的工作是在调参。不知道大家有否发现现在的Google 翻译比以前的要准确很多，因为Google在去年底将其Google 翻译的核心从原来基于统计的方法换成了基于神经网络的方法~So~

            - 数据可视化
              Data Visualization，将分析、挖掘后的高价值数据用比较优美、灵活的方式展现在老板、客户、用户面前，更多的是一些前端的东西，maybe要求一定的美学知识。结合使用者的喜好，以最恰当的方式呈现数据价值。

            -  数据应用
              Data Application，从以上的每个部分可以衍生出的应用，例如广告精准投放、个性化推荐、用户画像等。

            """)
        with b:
            st.write("Java")
            lottie_coding = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_c8ktt5et.json")
            st_lottie(lottie_coding, height=110, key="java")
            st.write("---")
            st.write("基本代码")
            st.code("""
            public class Prog1{

       public static void main(String[] args){

              int n = 10;

              System.out.println("第"+n+"个月兔子总数为"+fun(n));

       }

       private static int fun(int n){

              if(n==1 || n==2)

                 return 1;

              else

                 return fun(n-1)+fun(n-2);

       }

}
""")
            st.write("""
            
            Java是一门面向对象编程语言，不仅吸收了C++语言的各种优点，还摒弃了C++里难以理解的多继承、指针等概念，因此Java语言具有功能强大和简单易用两个特征。Java语言作为静态面向对象编程语言的代表，极好地实现了面向对象理论，允许程序员以优雅的思维方式进行复杂的编程。

            Java是一个强类型语言，它允许扩展编译时检查潜在类型不匹配问题的功能。Java要求显式的方法声明，它不支持C风格的隐式声明。

            Java可以编写桌面应用程序、Web应用程序、分布式系统和嵌入式系统应用程序等。

            Java的特点：

            Java具有简单性、面向对象、分布式、健壮性、安全性、平台独立与可移植性、多线程、动态性等特点；下面我们来具体介绍一下：

            1、简单性

            Java看起来设计得很像C++，但是为了使语言小和容易熟悉，设计者们把C++语言中许多可用的特征去掉了，这些特征是一般程序员很少使用的。例如，Java不支持go to语句，代之以提供break和continue语句以及异常处理。Java还剔除了C++的操作符过载（overload）和多继承特征，并且不使用主文件，免去了预处理程序。因为Java没有结构，数组和串都是对象，所以不需要指针。Java能够自动处理对象的引用和间接引用，实现自动的无用单元收集，使用户不必为存储管理问题烦恼，能更多的时间和精力花在研发上。

            2、面向对象

            Java语言提供类、接口和继承等面向对象的特性，为了简单起见，只支持类之间的单继承，但支持接口之间的多继承，并支持类与接口之间的实现机制（关键字为implements）。Java语言全面支持动态绑定，而C++语言只对虚函数使用动态绑定。总之，Java语言是一个纯的面向对象程序设计语言。

            3、分布性

            Java设计成支持在网络上应用，它是分布式语言。Java既支持各种层次的网络连接，又以Socket类支持可靠的流（stream）网络连接，所以用户可以产生分布式的客户机和服务器。

            网络变成软件应用的分布运载工具。Java程序只要编写一次，就可到处运行。

            4、编译和解释性

            Java编译程序生成字节码（byte-code），而不是通常的机器码。Java字节码提供对体系结构中性的目标文件格式，代码设计成可有效地传送程序到多个平台。Java程序可以在任何实现了Java解释程序和运行系统（run-time system）的系统上运行。

            在一个解释性的环境中，程序开发的标准“链接”阶段大大消失了。如果说Java还有一个链接阶段，它只是把新类装进环境的过程，它是增量式的、轻量级的过程。因此，Java支持快速原型和容易试验，它将导致快速程序开发。这是一个与传统的、耗时的“编译、链接和测试”形成鲜明对比的精巧的开发过程。

            5、稳健性

            Java原来是用作编写消费类家用电子产品软件的语言，所以它是被设计成写高可靠和稳健软件的。Java消除了某些编程错误，使得用它写可靠软件相当容易。

            Java的强类型机制、异常处理、垃圾的自动收集等是Java程序健壮性的重要保证。对指针的丢弃是Java的明智选择。Java的安全检查机制使得Java更具健壮性。

            6、安全性

            Java的存储分配模型是它防御恶意代码的主要方法之一。Java没有指针，所以程序员不能得到隐蔽起来的内幕和伪造指针去指向存储器。更重要的是，Java编译程序不处理存储安排决策，所以程序员不能通过查看声明去猜测类的实际存储安排。编译的Java代码中的存储引用在运行时由Java解释程序决定实际存储地址。

            Java运行系统使用字节码验证过程来保证装载到网络上的代码不违背任何Java语言限制。这个安全机制部分包括类如何从网上装载。例如，装载的类是放在分开的名字空间而不是局部类，预防恶意的小应用程序用它自己的版本来代替标准Java类。

            7、可移植性

            Java使得语言声明不依赖于实现的方面。例如，Java显式说明每个基本数据类型的大小和它的运算行为（这些数据类型由Java语法描述）。

            Java环境本身对新的硬件平台和操作系统是可移植的。Java编译程序也用Java编写，而Java运行系统用ANSIC语言编写。

            8、高性能

            Java是一种先编译后解释的语言，所以它不如全编译性语言快。但是有些情况下性能是很要紧的，为了支持这些情况，Java设计者制作了“及时”编译程序，它能在运行时把Java字节码翻译成特定CPU（中央处理器）的机器代码，也就是实现全编译了。

            Java字节码格式设计时考虑到这些“及时”编译程序的需要，所以生成机器代码的过程相当简单，它能产生相当好的代码。

            9、多线程

            在Java语言中，线程是一种特殊的对象，它必须由Thread类或其子（孙）类来创建。通常有两种方法来创建线程：

            1）、使用型构为Thread(Runnable)的构造子类将一个实现了Runnable接口的对象包装成一个线程，

            2）、从Thread类派生出子类并重写run方法，使用该子类创建的对象即为线程。值得注意的是Thread类已经实现了Runnable接口，因此，任何一个线程均有它的run方法，而run方法中包含了线程所要运行的代码。线程的活动由一组方法来控制。Java语言支持多个线程的同时执行，并提供多线程之间的同步机制（关键字为synchronized）。

            10、动态性

            Java语言的设计目标之一是适应于动态变化的环境。Java程序需要的类能够动态地被载入到运行环境，也可以通过网络来载入所需要的类。这也有利于软件的升级。另外，Java中的类有一个运行时刻的表示，能进行运行时刻的类型检查。

            11、平台独立性

            Java程序（后缀为java的文件）在Java平台上被编译为体系结构中立的字节码格式（后缀为class的文件），然后可以在实现这个Java平台的任何系统中运行。这种途径适合于异构的网络环境和软件的分发。

            相关视频教程推荐：《Java教程》

            以上就是java是一种什么语言？的详细内容，更多请关注php中文网其它相关文章！
            
            """)
        with d:
            st.write("Python")
            lottie_coding = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_2znxgjyt.json")
            st_lottie(lottie_coding, height=110, key="python")
            st.write("---")
            st.write("基本代码")
            st.code("""
            
           #方法1
           strl = "hello world"
           print(strl[::-1])
           #方法2
           from functools import reduce
           print(reduce(lambda x,y:y+x,strl))
            
            
            """)
            st.write("""
            
            Python是世界上最流行的解释型编程语言之一。Python 由 Guido van Rossum 设计，作为“ABC”编程语言的继承者，于 1991 年首次发布。它是一种高级通用语言，其设计理念是通过使用缩进来强调代码的可读性。Python 的语言结构旨在帮助程序员为小型和大型项目编写逻辑代码。

            该语言是动态类型的，支持多种编程范式。它完全支持面向对象和结构化编程，它的一些特性支持函数式和面向方面的编程。

            Python 被设计为一种高度可扩展的语言。这种模块化使得它作为一种向已经存在的应用程序添加接口的方式非常流行。由于其全面的标准库，它通常被描述为“包含电池”的语言。我们需要感谢 ABC 提供的这个特性，因为 Python 的设计者对于一个拥有大型标准库的小型核心语言的愿景源于他对 ABC 语言的挫败感，而 ABC 语言是基于相反的方法。

             - 语法
            Python 的格式在视觉上很整洁，并且经常使用关键字；然而，许多其他语言依赖于标点符号。Python 的另一个显着区别是它不使用大括号来分隔块。与 C 等其他语言相比，它的语法异常和特殊情况要少得多。

            - 缩进
            Python 使用空格缩进来分隔块。在某些语句之后可能会增加缩进，但缩进的减少意味着程序段的结束。这使得程序的视觉结构准确地表示了程序的语义结构。

            此功能称为“越位规则”。它可能不是python独有的，而是带有语义的；另一方面，大多数语言的缩进没有任何语义意义。

            - 变量
            在 Python 中，变量名是一个引用持有者，没有与之关联的固定数据类型。它们可以随时反弹到任何物体上。尽管在给定时间，变量将引用某个对象，该对象本身具有类型。这称为动态类型。

            这与 Java、C++、FORTRAN、Scala 和 Pascal 等语言完全相反，因为它们是静态类型的编程语言，其中每个变量只能包含特定类型的值。

            - 表达式
            表达式是编程语言中的语法实体，可以对其进行评估以确定其值。它是编程语言解释和计算以产生值的常量、变量、函数和运算符的组合。

            在 Python 中，表达式和语句是有区别的。也就是说，语句不能是表达式的组成部分。这个特性并不常见，因为它在一些主要语言中没有，比如 Scheme、Common Lisp 或 Ruby。但是这会导致重复某些功能。

            - 类型
            Python 使用鸭子类型，这是一种用于确定对象是否可以用于特定目的的应用程序。在这种语言中，编译时不检查类型约束。对对象执行操作失败意味着给定的对象不是合适的类型。

            Python 是一种强类型语言，因此它不允许定义不明确的操作，而不是默默地尝试理解它们。

            它允许程序员使用类定义自己的类型。可以通过调用类来构造类的新实例。

            - 方法
            这里的“方法”是与消息和对象相关联的过程。一个对象由数据和行为组成；这些包括一个接口，该接口指定对象如何被其任何消费者使用。

            Python 方法有一个显式的 self 参数来访问实例数据。Python 还提供了方法，通常称为 dunder 方法，允许用户定义的类修改它们如何被本地操作处理，例如长度、比较、算术运算、类型转换等。

            - 库
            Python 有一个很大的标准库。它能够提供适用于许多任务的工具。它包括用于创建图形用户界面 (GUI)、连接到关系数据库、生成伪随机数、操作正则表达式、单元测试等的模块。

            大多数标准库是跨平台的 Python 代码，因此只有少数模块需要更改或重写以进行变体实现。

            - Python的应用
            Python 可以作为 Web 应用程序的脚本语言。有了 Web 服务器网关接口，标准 API 已经发展到可以促进这些应用程序。

            NumPy、SciPy 和 Matplotlib 等库允许在科学计算中有效地使用 Python。Biopython 和 Astropy 等库提供特定领域的功能。SageMath 是一个计算机代数系统，带有可在 Python 中编程的笔记本界面。它的库可以涵盖数学的各个方面，例如代数、组合、数值数学、数论和微积分。

            在 TensorFlow、Keras、Pytorch 和 Scikit-learn 等库的帮助下，Python 常用于人工智能项目和机器学习项目。Python 因其模块化架构、简单的语法和富文本处理工具而常用于自然语言处理。

            Python 也可以用来创建游戏，使用 Pygame 等库可以制作 2D 游戏。

            GNU Debugger 使用 Python 作为漂亮的打印机来显示复杂的结构，例如 C++ 容器。Esri 将 Python 推广为在 ArcGIS 中编写脚本的最佳选择。它已被用作 Google App Engine 中三种可用编程语言中的第一种。

            许多操作系统都将 Python 作为标准组件。它随大多数 Linux 发行版一起提供，并且可以从命令行终端使用。许多 Linux 发行版使用用 Python 编写的安装程序。例如，Ubuntu 使用 Ubiquity 安装程序，而 Red Hat Linux 和 Fedora 使用 Anaconda 安装程序。

            Python 还广泛用于信息安全行业，包括漏洞利用开发。
            
            """)
        with e:
            st.write("Matlab")
            lottie_coding = load_lottieurl("https://assets8.lottiefiles.com/private_files/lf30_8npirptd.json")
            st_lottie(lottie_coding, height=110, key="matlab")
            st.write("---")
            st.write("基本代码")
            st.code("""
            
            % 生成矩阵
            % 直接法
            a = [1,2,3;4,5,6;7,8,9];
            % 冒号一维矩阵 a = 开始：步长：结束，步长为1可省略
            b = 1:1:10;  % 1,2,...10
            b = 1:10;  %与上一个等价
            % 函数生成
            % linspace(开始，结束，元素个数)，等差生成指定元素数的一维矩阵，省略个数则生成100个
            c = linspace(0,10,5);
            % 特殊矩阵
            e = eye(4);  % eye(维数)单位阵
            z = zeros(1,4);  % zeros(维数)全零阵
            o = ones(4,1);  % ones(维数)全1阵
            r = rand(4);  % rand(维数)0~1分布随机阵
            rn = randn(4);  % randn(维数)0均值Gaussian分布随机阵
                      
            %%
            % 矩阵运算
            diag_a = diag(a,1);  % diag(行向量，主对角线上方第k条斜线)用行向量生成对角阵
            tril_a = tril(a,1);  % tril(矩阵，主对角线上方第k条斜线)生成矩阵的下三角阵，triu上三角阵
            % 加、减、乘、乘方
            a*a
            % 点运算
            % a.*b , a./b , a.\b , a.^b  对应元素的*,/,\,^运算
            a.*a
            % 逆矩阵
            pinv(a)  % 伪逆矩阵，当a不是方阵，求广义逆矩阵；当a是可逆方阵，结果与逆矩阵相同
            % 特征值，特征向量
            [v,D] = eig(a);  % 输出v为特征向量，D为特征值对角阵
            % *行列式
            det(a)
            % *秩
            rank(a)
            % *伴随
            compan(b)
        
            %%
            % 矩阵的修改
            %部分替换
           chg_a = a;
           chg_a(2,3) = 4;  % (行，列)元素替换
           chg_a(1,:) = [2,2,2];  % (行,:)替换行，为[]删除该行
           chg_a(:,1) = [];  % (:,列)替换列，为[]删除该列
           % 转置
           T_a = a';
           % 指定维数拼接
           c1_a = cat(1,a,a);  % 垂直拼接
           c2_a = cat(2,a,a);  % 水平拼接
           % *变维
           rs_a = reshape(a,1,9);  % 元素个数不变，矩阵变为m*n

           %%
           % 信息获取
           % 矩阵的行列数
           [row_a, col_a] = size(a);  % [行数，列数]
           % 行列中最大的
           len_a = length(a);
        
           %%
           % 多维数组
           % 创建
           % 直接法
            mul_1(:,:,1) = [1,2,3;2,3,4];
            mul_1(:,:,2) = [3,4,5;4,5,6];
            % *扩展法
            mul_2 = [1,2,3;2,3,4];
            mul_2(:,:,2) = [3,4,5;4,5,6];  % 若不赋值第一页，第一页全为0
            % cat法
            mul_31 = [1,2,3;2,3,4];
            mul_32 = [3,4,5;4,5,6];
            mul_3 = cat(3,mul_31,mul_32);  % 把a1a2按照“3”维连接

            %%
            % *字符串
            % 创建
            str0 = 'hello world';  % 单引号引起
            str1 = 'I''m a student';  % 字符串中单引号写两遍
            str3 = ['I''m' 'a' 'student'];  % 方括号链接多字符串
            str4 = strcat(str0, str1);  % strcat连接字符串函数
            str5 = strvcat(str0, str1);  % strvcat连接产生多行字符串
            str6 = double(str0);  % 取str0的ASCII值，也可用abs函数
            str7 = char(str6);  % 把ASCII转为字符串
            % 操作
            % 比较
            strcmp(str0, str1);  % 相等为1，不等为0
            strncmp(str0, str1, 3);  % 比较前3个是否相等(n)
            strcmpi(str0, str1);  % 忽略大小写比较(i)
            strncmpi(str0, str1, 3);  % 忽略大小写比较前3个是否相等
            % 查找替换
            strfind(str0, str1);  % 在str0找到str1的位置
            strmatch(str1, str0);  % 在str0字符串数组中找到str1开头的行数
            strtok(str0);  % 截取str0第一个分隔符（空格，tab，回车）前的部分
            strrep(str0, str1, str2);  % 在str0中用str2替换str1
            % 其他
            upper(str0);  % 转大写，lower转小写
            strjust(str0, 'right');  % 将str0右对齐，left左对齐，center中间对齐
            strtrim(str0);  % 删除str0开头结尾空格
            eval(str0);  % 将str0作为代码执行
            
            %%
            %转换
            % ___2___  -->  如num2str，将数字转字符串； dec2hex，将十进制转十六进制
            str_b = num2str(b);
            % abs，double取ASCII码；char把ASCII转字符串
            abs_str = abs('aAaA');  

            
            """)
            st.write("""
            一、matlab定义
　　         The MathWorks公司的MATLAB 是一种用于算法开发、数据可视化、数据分析以及数值计算的高级技术计算语言和交互式环境。使用 MATLAB，您可以较使用传统的编程语言（如 C++、C++ 和 Fortran）更快地解决技术计算问题。MATLAB 是美国MathWorks公司出品的商业数学软件，用于算法开发、数据可视化、数据分析以及数值计算的高级技术计算语言和交互式环境，主要包括MATLAB和Simulink两大部分。

　　         MATLAB是矩阵实验室（Matrix Laboratory）的简称，和MathemaTIca、Maple并称为三大数学软件。它在数学类科技应用软件中在数值计算方面首屈一指。MATLAB可以进行矩阵运算、绘制函数和数据、实现算法、创建用户界面、连接其他编程语言的程序等，主要应用于工程计算、控制设计、信号处理与通讯、图像处理、信号检测、金融建模设计与分析等领域。
            
            MATLAB的基本数据单位是矩阵，它的指令表达式与数学、工程中常用的形式十分相似，故用MATLAB来解算问题要比用C，FORTRAN等语言完相同的事情简捷得多，并且mathwork也吸收了像Maple等软件的优点，使MATLAB成为一个强大的数学软件。在新的版本中也加入了对C，FORTRAN，C++ ，JAVA的支持。可以直接调用，用户也可以将自己编写的实用程序导入到MATLAB函数库中方便自己以后调用，此外许多的MATLAB爱好者都编写了一些经典的程序，用户可以直接进行下载就可以用。

　　         二、matlab是编程语言吗？
　　         严格的来说matlab不算是编程语言。只有你有C语言的基础，Matlab就很容易。Matlab是边解释边执行。另外Matlab集成了大量的自带函数，比如矩阵计算，画图，谱分析。这就不符合标准编程语言的特点。你如果明白类和对象的概念，对用好Matlab很有帮助。所以Matlab属于科学计算工具，而不是严格的一门编程语言。

　　         三、MATLAB优势特点
　　         1） 高效的数值计算及符号计算功能，能使用户从繁杂的数学运算分析中解脱出来；

　　         2） 具有完备的图形处理功能，实现计算结果和编程的可视化；

　　        3） 友好的用户界面及接近数学表达式的自然化语言，使学者易于学习和掌握；

　　        4） 功能丰富的应用工具箱（如信号处理工具箱、通信工具箱等） ，为用户提供了大量方便实用的处理工具。

　　        编程环境

　　        MATLAB由一系列工具组成。这些工具方便用户使用MATLAB的函数和文件，其中许多工具采用的是图形用户界面。包括MATLAB桌面和命令窗口、历史命令窗口、编辑器和调试器、路径搜索和用于用户浏览帮助、工作空间、文件的浏览器。随着MATLAB的商业化以及软件本身的不断升级，MATLAB的用户界面也越来越精致，更加接近Windows的标准界面，人机交互性更强，操作更简单。而且新版本的MATLAB提供了完整的联机查询、帮助系统，极大的方便了用户的使用。简单的编程环境提供了比较完备的调试系统，程序不必经过编译就可以直接运行，而且能够及时地报告出现的错误及进行出错原因分析。

　　        简单易用

　　        Matlab是一个高级的矩阵/阵列语言，它包含控制语句、函数、数据结构、输入和输出和面向对象编程特点。用户可以在命令窗口中将输入语句与执行命令同步，也可以先编写好一个较大的复杂的应用程序（M文件）后再一起运行。新版本的MATLAB语言是基于最为流行的C++语言基础上的，因此语法特征与C++语言极为相似，而且更加简单，更加符合科技人员对数学表达式的书写格式。使之更利于非计算机专业的科技人员使用。而且这种语言可移植性好、可拓展性极强，这也是MATLAB能够深入到科学研究及工程计算各个领域的重要原因。

　　        强大处理

　　        MATLAB是一个包含大量计算算法的集合。其拥有600多个工程中要用到的数学运算函数，可以方便的实现用户所需的各种计算功能。函数中所使用的算法都是科研和工程计算中的最新研究成果，而且经过了各种优化和容错处理。在通常情况下，可以用它来代替底层编程语言，如C和C++ 。在计算要求相同的情况下，使用MATLAB的编程工作量会大大减少。MATLAB的这些函数集包括从最简单最基本的函数到诸如矩阵，特征向量、快速傅立叶变换的复杂函数。函数所能解决的问题其大致包括矩阵运算和线性方程组的求解、微分方程及偏微分方程的组的求解、符号运算、傅立叶变换和数据的统计分析、工程中的优化问题、稀疏矩阵运算、复数的各种运算、三角函数和其他初等数学运算、多维数组操作以及建模动态仿真等。

　　        图形处理

　　        MATLAB自产生之日起就具有方便的数据可视化功能，以将向量和矩阵用图形表现出来，并且可以对图形进行标注和打印。高层次的作图包括二维和三维的可视化、图象处理、动画和表达式作图。可用于科学计算和工程绘图。新版本的MATLAB对整个图形处理功能作了很大的改进和完善，使它不仅在一般数据可视化软件都具有的功能（例如二维曲线和三维曲面的绘制和处理等）方面更加完善，而且对于一些其他软件所没有的功能（例如图形的光照处理、色度处理以及四维数据的表现等），MATLAB同样表现了出色的处理能力。同时对一些特殊的可视化要求，例如图形对话等，MATLAB也有相应的功能函数，保证了用户不同层次的要求。另外新版本的MATLAB还着重在图形用户界面（GUI）的制作上作了很大的改善，对这方面有特殊要求的用户也可以得到满足。

　　        模块工具

　　       MATLAB对许多专门的领域都开发了功能强大的模块集和工具箱。一般来说，它们都是由特定领域的专家开发的，用户可以直接使用工具箱学习、应用和评估不同的方法而不需要自己编写代码。领域，诸如数据采集、数据库接口、概率统计、样条拟合、优化算法、偏微分方程求解、神经网络、小波分析、信号处理、图像处理、系统辨识、控制系统设计、LMI控制、鲁棒控制、模型预测、模糊逻辑、金融分析、地图工具、非线性控制设计、实时快速原型及半物理仿真、嵌入式系统开发、定点仿真、DSP与通讯、电力系统仿真等，都在工具箱（Toolbox）家族中有了自己的一席之地。

　　       程序接口

　　       新版本的MATLAB可以利用MATLAB编译器和C/C++数学库和图形库，将自己的MATLAB程序自动转换为独立于MATLAB运行的C和C++代码。允许用户编写可以和MATLAB进行交互的C或C++语言程序。另外，MATLAB网页服务程序还容许在Web应用中使用自己的MATLAB数学和图形程序。MATLAB的一个重要特色就是具有一套程序扩展系统和一组称之为工具箱的特殊应用子程序。工具箱是MATLAB函数的子程序库，每一个工具箱都是为某一类学科专业和应用而定制的，主要包括信号处理、控制系统、神经网络、模糊逻辑、小波分析和系统仿真等方面的应用。

　　       软件开发

　　       在开发环境中，使用户更方便地控制多个文件和图形窗口；在编程方面支持了函数嵌套，有条件中断等；在图形化方面，有了更强大的图形标注和处理功能，包括对性对起连接注释等；在输入输出方面，可以直接向Excel和HDF5进行连接。

　　       四、matlab的应用
　　       MATLAB®是一种对技术计算高性能的语言。它集成了计算，可视化和编程于一个易用的环境中，在此环境下，问题和解答都表达为我们熟悉的数学符号。典型的应用有：

　　       数学和计算

　　       算法开发

　　       建模，模拟和原形化

　　       数据分析，探索和可视化

　　       科学与工程制图

　　       应用开发，包括图形用户界面的建立

　　       MATLAB是一个交互式的系统，其基本数据元素是无须定义维数的数组。这让你能解决很多技术计算的问题，尤其是那些要用到矩阵和向量表达式的问题。而要花的时间则只是用一种标量非交互语言（例如C或Fortran）写一个程序的时间的一小部分。

　　       名称“MATLAB”代表matrix laboratory（矩阵实验室）。MATLAB最初是编写来提供给对由LINPACK和EINPACK工程开发的矩阵软件简易访问的。今天，MATLAB使用由LAPACK和ARPACK工程开发的软件，这些工程共同表现了矩阵计算的软件中的技术发展。

　　       MATLAB已经与许多用户输入一同发展了多年。在大学环境中，它是很多数学类、工程和科学类的初等和高等课程的标准指导工具。在工业上，MATLAB是高产研究、开发和分析所选择的工具。 MATLAB以一系列称为工具箱的应用指定解答为特征。对多数用户十分重要的是，工具箱使你能学习和应用专门的技术。工具箱是是MATLAB函数（M-文件）的全面的综合，这些文件把MATLAB的环境扩展到解决特殊类型问题上。具有可用工具箱的领域有：信号处理，控制系统神经网络，模糊逻辑，小波分析，模拟等等。
            
        
            """)
        with f:
            st.write("C++")
            lottie_coding = load_lottieurl("https://assets3.lottiefiles.com/private_files/lf30_WVVTq8.json")
            st_lottie(lottie_coding, height=110, key="C++")
            st.write("---")
            st.write("基本代码")
            st.code("""
            #include <fstream>
            #include <iostream>
            using namespace std;
 
 
            int main(){
            string filename = "test.txt";
 
            ifstream file;
            file.open(filename.data());
            // assert(file.is_open());
 
            string image_path;
	        while(getline(file, image_path)){
		    cout << image_path <<endl;
    }
            return 0;
}
            """)
            st.write("""
            
            C++是一种计算机高级程序设计语言，由C语言扩展升级而产生 [17]  ，最早于1979年由本贾尼·斯特劳斯特卢普在AT&T贝尔工作室研发。 [2] 
            C++既可以进行C语言的过程化程序设计，又可以进行以抽象数据类型为特点的基于对象的程序设计，还可以进行以继承和多态为特点的面向对象的程序设计。C++擅长面向对象程序设计的同时，还可以进行基于过程的程序设计。
            C++拥有计算机运行的实用性特征，同时还致力于提高大规模程序的编程质量与程序设计语言的问题描述能力。 [1] 
            
             - 发展历程
            1970年，AT&T贝尔实验室的工作人员D.Ritchie和K.Thompson共同研发了C语言。研制C语言的初衷是用它编写UNIX系统程序，因此，实际上C语言是UNIX的“副产品”。
            1971年，瑞士联邦技术学院N.Wirth教授发明了第一个结构化的编程语言Pascal。
            20世纪70年代中期，本贾尼·斯特劳斯特卢普在剑桥大学计算机中心工作。斯特劳斯特卢普希望开发一个既要编程简单、正确可靠，又要运行高效、可移植的计算机程序设计语言。而以C语言为背景，以Simula思想为基础的语言，正好符合斯特劳斯特卢普的初衷和设想。
            1979年，本贾尼·斯特劳斯特卢普到了AT&T贝尔实验室，开始从事将C改良为带类的C（C with classes）的工作。、1983年，该语言被正式命名为C++。 [2] 
            C++代码
            C++代码(3张)
            1985年、1990年和1994年，C++先后进行3次主要修订。
            C++的标准化工作于1989年开始 [21]  ，并成立了一个ANSI和ISO（International Standards Organization）国际标准化组织的联合标准化委员会。
            1994年1月25曰，联合标准化委员会提出了第一个标准化草案。在该草案中，委员会在保持斯特劳斯特卢普最初定义的所有特征的同时，还增加了部分新特征。 [3] 
            在完成C++标准化的第一个草案后不久，亚历山大·斯特潘诺夫（Alexander Stepanov）创建了标准模板库（Standard Template Library，STL）。在通过了标准化第一个草案之后，联合标准化委员会投票并通过了将STL包含到C++标准中的提议。STL对C++的扩展超出了C++的最初定义范围。虽然在标准中增加STL是个很重要的决定，但也因此延缓了C++标准化的进程。
            1997年11月14日，联合标准化委员会通过了该标准的最终草案，
            1998年，C++的ANSI/IS0标准被投入使用。 [4] 
            
            语言特点
            - 与C语言的兼容性
            C++与C语言完全兼容，C语言的绝大部分内容可以直接用于C++的程序设计，用C语言编写的程序可以不加修改地用于C++。 [22] 
            - 数据封装和数据隐藏
            在C++中，类是支持数据封装的工具，对象则是数据封装的实现。C++通过建立用户定义类支持数据封装和数据隐藏。
            在面向对象的程序设计中，将数据和对该数据进行合法操作的函数封装在一起作为一个类的定义。对象被说明为具有一个给定类的变量。每个给定类的对象包含这个类所规定的若干私有成员、公有成员及保护成员。完好定义的类一旦建立，就可看成完全封装的实体，可以作为一个整体单元使用。类的实际内部工作隐藏起来，使用完好定义的类的用户不需要知道类的工作原理，只要知道如何使用它即可。
            - 支持继承和重用
            在C++现有类的基础上可以声明新类型，这就是继承和重用的思想。通过继承和重用可以更有效地组织程序结构，明确类间关系，并且充分利用已有的类来完成更复杂、深入的开发。新定义的类为子类，成为派生类。它可以从父类那里继承所有非私有的属性和方法，作为自己的成员。
            - 多态性
            采用多态性为每个类指定表现行为。多态性形成由父类和它们的子类组成的一个树型结构。在这个树中的每个子类可以接收一个或多个具有相同名字的消息。当一个消息被这个树中一个类的一个对象接收时，这个对象动态地决定给予子类对象的消息的某种用法。多态性的这一特性允许使用高级抽象。
            继承性和多态性的组合，可以轻易地生成一系列虽然类似但独一无二的对象。由于继承性，这些对象共享许多相似的特征。由于多态性，一个对象可有独特的表现方式，而另一个对象有另一种表现方式。 [8] 
            
            工作原理
            C++语言的程序开发环境，为了方便测试，将调试环境做成了解释型。即开发过程中，以解释型的逐条语句执行方式来进行调试，以编译型的脱离开发环境而启动运行的方式来生成程序最终的执行代码。 [7] 
            开发C++应用程序，需要经过编写源程序、编译、连接程序生成可执行程序、运行程序四个步骤 [23]  。生成程序是指将源码（C++语句）转换成一个可以运行的应用程序的过程。如果程序编写正确，那么通常只需按一个功能键，即可完成该过程。
            第一步对程序进行编译，这需要用到编译器（compiler）。编译器将C++语句转换成机器码（也称为目标码）；如果该步骤成功执行，下一步就是对程序进行链接，这需要用到链接器（linker）。链接器将编译获得机器码与C++库中的代码进行合并。C++库包含了执行某些常见任务的函数（“函数”是子程序的另一种称呼）。例如，一个C++库中包含标准的平方根函数sqrt，所以不必亲自计算平方根。C++库中还包含一些子程序，它们把数据发送到显示器，并知道如何读写硬盘上的数据文件。 [9] 
            
            语言基础
            - 基本类型
            C++语言数    据类型可以分为两大类：基本类型和引用类型。基本类型是指不能再分解的数据类型，其数据在函数的调用中是以传值方式工作的；引用类型有时也称复合类型，它是可以分解为基本类型的数据类型，其数据在函数调用中是以传址方式来工作的。 [10] 
            - 整型
            1、整数常量
            整数常量是不带小数的数值，用来表示正负数。例2—2中Ox55、0x55ff、1000000都是c++语言的整数常量。
            c++语言的整数常量有三种形式：十进制、八进制、十六进制。
           （1）十进制整数是由不以0开头的0～9的数字组成的数据。
           （2）八进制整数是由以0开头的0～7的数字组成的数据。
           （3）十六进制整数是由以0x或0x开头的0～9的数字及A～F的字母(大小写字母均可)组成的数据。
            例如：
            0，63，83是十进制数。
            00，077，0123是八进制数。
            0x0，Ox0，0x53，0x53，0x3f，0x3f是十六进制数。
            整数常量的取值范围是有限的，它的大小取决于此类整型数的类型，与所使用的进制形式无关。
            2、整型变量类型
            整型变量类型有byte，short，int，long四种说明符，它们都是有符号整型变量类型。
           （1）byte类型
            byte类型说明一个带符号的8位整型变量。由于不同的机器对多字节数据的存储方式不同，可能是从低字节向高字节存储，也可能是从高字节向低字节存储。这样，在分析网络协议或文件格式时，为了解决不同机器上的字节存储顺序问题，用byte类型来表示数据是合适的。
           （2）short类型
            short类型说明一个带符号的16位整型变量。short类型限制了数据的存储应为先高字节，后低字节。
           （3）int类型
            int类型说明一个带符号的32位整型变量。int类型是一种最丰富、最有效的类型。它最常用于计数、数组访问和整数运算。
           （4）long类型
            long类型说明一个带符号的64位整型变量。对于大型计算，常常会遇到很大的整数，并超出int所表示的范围，这时要使用long类型。
            浮点型
            1、浮点数常量
            浮点数是带有小数的十进制数，可用一般表示法或科学记数法表示。0.23f、0.7e-3都是c++语言的浮点数常量。
           （1）一般表示法：十进制整数+小数点+十进制小数。
           （2）科学记数法：十进制整数+小数点+十进制小数+E（或e）+正负号+指数。
            例如：3.14159，0.567，9777.12是一般表示法形式，1.234e5，4.90867e-2是科学记数法形式。
            c++语言的浮点数常量在机器中有单精度和双精度之分。单精度以32位形式存放，用f/F做后缀标记(可以省略)；双精度则以64位形式存放。当一个浮点数常量没有特别指定精度时，则它为双精度浮点数常量。
            2、浮点变量类型
            浮点变量也称实数变量，用于需要精确到小数的函数运算中，有float和double两种类型说明符。
           （1）float类型
            float类型是一个位数为32位的单精度浮点数。它具有运行速度较快，占用空间较少的特点。
           （2）double类型
            double类型是一个位数为64的双精度浮点数。双精度数在某些具有优化和高速运算能力的现代处理机上运算比单精度数快。双精度类型double比单精度类型float具有更高的精度和更大表示范围，常常使用。
            字符型
            1、字符型常量
            字符型常量是指由单引号括起来的单个字符。
            例如：’a’，’A’，’z’，‘$’，’?’。
            注意：’a’和’A’是两个不同的字符常量。
            除了以上形式的字符常量外，c++语言还允许使用一种以“\”开头的特殊形式的字符常量。这种字符常量称为转义字符，用来表示一些不可显示的或有特殊意义的字符。
            2、字符型变量
            字符型变量的类型说明符为char，它在机器中占8位，其范围为0～255。
            注意：字符型变量只能存放一个字符，不能存放多个字符，例如：
            1
            char a='am';
            这样定义赋值是错误的。
            布尔型
            布尔常量只有两个值：“true”和“false”，表示“真”和“假”，均为关键词，在机器中位长为8位。
            布尔型变量的类型说明符为booI，用来表示逻辑值。 [10] 
            运算符与表达式
            C++语言中定义了丰富的运算符，如算术运算符、关系运算符、逻辑运算符等等，有些运算符需要两个操作数，使用形式为：<操作数1>运算符<操作数2>，这样的运算符称为二元运算符（或二目运算符）。另一些运算符只需要一个操作数，称为一元运算符（或单目运算符）。
            运算符具有优先级与结合性。当一个表达式包含多个运算符时，先进行优先级高的运算，再进行优先级低的运算。如果表达式中出现了多个相同优先级的运算，运算顺序就要看运算符的结合性了。所谓结合性，是指当一个操作数左右两边的运算符优先级相同时，按什么样的顺序进行运算，是自左向右，还是自右向左。例如，我们熟悉的算术表达式6+5-2中,“+”、 “-”是同级运算符，那么是先算5-2，还是先算6+5？这就取决于算术运算符的结合性。由于算术运算符的结合性为自左向右，所以应先算6+5，然后再算11-2。
            算术运算符与算术表达式
            C++中的算术运算符包括基本的算术运算符和自增、自减运算符。由算术运算符、操作数和括号构成的表达式称为算术表达式。
            基本算术运算符有：+（加）、-（减或负号）、*（乘）、/（除）、%（取余）。其中“-”作为负号时为一元运算符，其余都为二元运算符。这些基本算术运算符的意义与数学中相应符号的意义是一致的。它们之间的相对优先级关系与数学中的也是一致的，即先乘除、后加减，同级运算自左向右进行。使用算术运算符要注意以下几点：
            1、“%”是取余运算，只能用于整型操作数。表达式a%b的结果为a/b的余数。 “%”的优先级与“/”相同。
            2、当“/”用于两整型操作数相除时，其结果取商的整数部分，小数部分被自动舍弃。因此，表达式1/2的结果为0，这一点需要特别注意。
            3、C++中的“++” （自增）、 “--” （自减）运算符是使用方便且效率很高的两个运算符，它们都是一元运算符。
            这两个运算符都有前置和后置两种使用形式，无论写成前置或后置的形式，它们的作用都是将操作数的值增1（减1）后，重新写回该操作数在内存中的原有位置。所以，如果变量i原来的值是1，计算表达式i++后，表达式的结果为2，并且i的值也被改变为2。但是，当自增、自减运算的结果要被用于继续参与其它操作时，前置与后置时的情况就完全不同。例如，如果i的值为l，则下列两条语句的执行结果不同：
            1
            2
            cout<<i++；
            cout<<++i；
            第一条语句首先输出i当前的值1，然后i自增，其值变为2；第二条语句首先使i自增为2，然后输出i的值2。
            赋值运算符与赋值表达式
            C++提供了几个赋值运算符，最简单的赋值运算符就是“=”。带有赋值运算符的表达式被称为赋值表达式。例如，m=m+6就是一个赋值表达式。赋值表达式的作用就是将等号右边表达式的值赋给等号左边的对象。赋值表达式的类型为等号左边对象的类型，表达式的结果为等号左边对象被赋值后的值，运算的结合性为自右向左。请看下列赋值表达式的例子。
            1
            n=1
            表达式值为1。
            1
            a=b=c=2
            这个表达式从右向左运算，在c被更新为2后，表达式c=2的值为2，接着b的值被更新为2，最后a被赋值为2。
            1
            a=3+(c=4)
            表达式值为7，a的值为7，c为4。
            除了“=”以外，C++还提供了10种复合的赋值运算符：+=，-=，*=，/=，%=，<<=，>>=，&=，“=，|=。其中，前五个运算符是赋值运算符与算术运算符复合而成的，后五个是赋值运算符与位运算符复合而成的。关于位运算，稍后再做介绍。这里10种运算符的优先级与“=”相同，结合性也是自右向左。现在举例说明复合赋值运算符的功能。
            1
            2
            b+=2;//等价于b=b+2
            x*=y+3;//等价于x=x*(y+3)
            1
            如果在赋值表达式后面加上分号，便成为了赋值语句。例如：
            b=b+2：便是一个赋值语句，它实现的功能与赋值表达式相同。赋值表达式与赋值语句的不同点在于：赋值表达式可以作为一个更复杂表达式的一部分，继续参与运算；而赋值语句不能。
            逗号运算符与逗号表达式
            在C++中，逗号也是一个运算符，它的使用形式为：
            <表达式1>，<表达式2>，…，<表达式n>求解顺序为，先求解表达式1，再求解表达式2，最后求解表达式n的值。逗号表达式的最终结果为表达式n的值。例如：
            1
            x=2*5,x*4
            表达式的结果为40。
            关系运算符和关系表达式
            关系运算符即比较符。
            用关系运算符将两个表达式连接起来就是关系表达式。关系表达式是一种最简单的逻辑表达式。例如：
            1
            2
            3
            x>5
            x+y<=20
            c==a+b
            注：“==”（等于）是连续的两个等号，勿误写为赋值运算符“=”。
            关系表达式一般用于判断是否符合某一条件。关系表达式的结果类型为bool，值只能是true或false。条件满足为true，条件不满足为false。例如，当x=t时，x>5的结果就为false。
            逻辑运算符与逻辑表达式
            用逻辑运算符将简单的关系表达式连接起来构成较复杂的逻辑表达式。逻辑表达式的结果类型也为bool，值只能为true或false。
            “!”是一元运算符，使用形式是： !操作数。非运算的作用是对操作数取反。如果操作数a的值为true，则表达式!a的值为false：如果操作数a的值为false，则表达式!a的值为true。
            “&&”是二元运算符。“&&”运算的作用是求两个操作数的逻辑与。只有当两个操作数的值都为true时，与运算的结果才为true，其它情况下与运算的结果均为false。
            “||”也是二元运算符。 “||”运算的作用是求两个操作数的逻辑或。只有当两个操作数的值都为false时，或运算的结果才为false，其它情况下或运算的结果均为true。 [11] 
            类和对象
            类所表示的一组对象十分相似，可以作为模板来有效的创建对象，利用类可以产生很多的对象类所代表的事物或者概念都是抽象的。在存取Private类型数据或者函数的时候，只有类本身声明的函数才是被允许的。类在与外部连接时，利用的就是Public共有类型函数，任何外部函数的访问都是运行的。
            对象主要是对客观事物的某个实体进行描述，它作为一个单位，共同组成了系统，它的组成是一组属性和一组服务，这组服务操作于这组属性。属性和服务是对象构成众多要素中的两种，属性的实质是一个数据项，主要是对对象静态特性进行描述，服务的实质是一个操作序列，主要是对对象动态特征进行描述。 [12] 
            关键字
            关键字（keyword）是整个语言范围内预先保留的标识符，每个C++关键字都有特殊的含义。经过预处理后，关键字从预处理记号（preprocessing-token）中区出来，剩下的标识符作为记号（token），用于声明对象、函数、类型、命名空间等。不能声明与关键字同名的标识符。
            各个版本的ISO C++都规定以下划线接大写字母起始的标识符保留给实现。编译器可以用这些保留标识符作为扩展关键字，这不保证可移植性。以下讨论ISO C++所保留的关键字。
            
            """)
        with g:
            st.write("AI")
            lottie_coding = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_zrqthn6o.json")
            st_lottie(lottie_coding, height=110, key="AI")
            st.write("---")
            st.write("基本代码")
            st.code("""
            
            import sklearn
            from sklearn.feature_extraction import DictVectorizer
 
            dv = DictVectorizer()
            instances = [{'city': '北京','temperature':100},{'city': '上海','temperature':60}, {'city': '深圳','temperature':150}]
            data = dv.fit_transform(instances).toarray()
            print(data)
            print(dv.get_feature_names())
            print(dv.inverse_transform(data))
            """)
            st.write("""
            人工智能 (AI)
            人工智能利用计算机和机器模仿人类思维的问题解决和决策制定能力。
            
            什么是人工智能？
            虽然在过去数十年中，人工智能 (AI) 的一些定义不断出现，但 John McCarthy 在 2004 年的论文 (PDF, 106 KB) (链接位于 IBM 外部 ) 中给出了以下定义：“这是制造智能机器，特别是智能计算机程序的科学和工程。 它与使用计算机了解人类智能的类似任务有关，但 AI 不必局限于生物可观察的方法”。

            然而，在这个定义出现之前数十年，人工智能对话的诞生要追溯到艾伦·图灵 (Alan Turing) 于 1950 年发表的开创性工作：“计算机械和智能” (PDF，89.8 KB)（链接位于 IBM 外部）。 在这篇论文中，通常被誉为“计算机科学之父”的图灵提出了以下问题：“机器能思考吗？”由此出发，他提出了著名的“图灵测试”，由人类审查员尝试区分计算机和人类的文本响应。 虽然该测试自发表之后经过了大量的审查，但它仍然是 AI 历史的重要组成部分，也是一种在哲学中不断发展的概念，因为它利用了有关语言学的想法。

            Stuart Russell 和 Peter Norvig 随后发表了“人工智能：现代方法”（链接位于 IBM 外部），成为 AI 研究的主要教科书之一。 在该书中，他们探讨了 AI 的四个潜在目标或定义，按照理性以及思维与行动将 AI 与计算机系统区分开来：

           人类方法：

           像人类一样思考的系统
           像人类一样行动的系统
           理想方法：

           理性思考的系统
           理性行动的系统
           艾伦·图灵的定义可归入“像人类一样行动的系统”类别。

           以最简单的形式而言，人工智能是结合了计算机科学和强大数据集的领域，能够实现问题解决。 它还包括机器学习和深度学习等子领域，这些子领域经常与人工智能一起提及。 这些学科由 AI 算法组成，这些算法旨在创建基于输入数据进行预测或分类的专家系统。

           目前，仍有许多围绕 AI 发展的炒作，市场上任何新技术的出现都会引发热议。 正如Gartner 的炒作周期（链接位于 IBM 外部）中所指出的，包括自动驾驶汽车和个人助理在内的产品创新遵循：“创新的典型发展进程，从超高热情到幻想破灭期，最终了解创新在市场或领域中的相关性和作用”。正如 Lex Fridman 在其 2019 年的 MIT 讲座（链接位于 IBM 外部）中所指出的那样，我们正处于泡沫式期望的颠峰，逐渐接近幻灭槽。

           随着对话围绕 AI 的伦理道德展开，我们可以开始看到幻灭槽初见端倪。 要了解有关 IBM 在 AI 伦理道德对话中的立场的更多信息，请在此阅读详细内容。

           人工智能的类型 - 弱 AI 与强 AI
           弱 AI 也称为狭义的 AI 或人工狭义智能 (ANI)，是经过训练的 AI，专注于执行特定任务。 弱 AI 推动了目前我们周围的大部分 AI。“范围窄”可能是此类 AI 更准确的描述符，因为它其实并不弱，支持一些非常强大的应用，如 Apple 的 Siri、Amazon 的 Alexa 以及 IBM Watson 和自主车辆。

           强 AI 由人工常规智能 (AGI) 和人工超级智能 (ASI) 组成。 人工常规智能 (AGI) 是 AI 的一种理论形式，机器拥有与人类等同的智能；它具有自我意识，能够解决问题、学习和规划未来。 人工超级智能 (ASI) 也称为超级智能，将超越人类大脑的智力和能力。 虽然强 AI 仍完全处于理论阶段，还没有实际应用的例子，但这并不意味着 AI 研究人员不在探索它的发展。 ASI 的最佳例子可能来自科幻小说，如 HAL、超人以及《2001 太空漫游》电影中的无赖电脑助手。

           深度学习与机器学习
           由于深度学习和机器学习这两个术语往往可互换使用，因此必须注两者之间的细微差别。 如上所述，深度学习和机器学习都是人工智能的子领域，深度学习实际上是机器学习的一个子领域。
           
           
           深度学习实际上由神经网络组成。深度学习中的“深度”是指由三层以上组成的神经网络（包括输入和输出）可被视为深度学习算法.
           
           深度学习和机器学习的不同之处在于每个算法如何学习。 深度学习可以自动执行过程中的大部分特征提取，消除某些必需的人工干预，并能够使用更大的数据集。 可将深度学习视为“可扩展的机器学习”，正如 Lex Fridman 在同一 MIT 讲座中所指出的那样。 常规的机器学习，或叫做"非深度"机器学习，更依赖于人工干预进行学习。 人类专家确定特征的层次结构，以了解数据输入之间的差异，通常需要更多结构化数据以用于学习。

           "深度"机器学习则可以利用标签化的数据集，也称为监督式学习，以确定算法，但不一定必须使用标签化的数据集。 它可以原始格式（例如文本、图像）采集非结构化数据，并且可以自动确定区分不同类别数据的特征的层次结构。 与机器学习不同，它不需要人工干预数据的处理，使我们能够以更有趣的方式扩展机器学习。
           
           
           人工智能应用
           目前，AI 系统存在大量的现实应用。 下面是一些最常见的示例：

           语音识别：也称为自动语音识别 (ASR)、计算机语音识别或语音到文本，能够使用自然语言处理 (NLP)，将人类语音处理为书面格式。许多移动设备将语音识别结合到系统中以进行语音搜索，例如： Siri，或提供有关文本的更多辅助功能。
           客户服务：在线聊天机器人正逐步取代客户互动中的人工客服。 他们回答各种主题的常见问题 (FAQ) ，例如送货，或为用户提供个性化建议，交叉销售产品，提供用户尺寸建议，改变了我们对网站和社交媒体中客户互动的看法。 示例包括具有虚拟客服的电子商务站点上的聊天机器人、消息传递应用（例如 Slack 和 Facebook Messenger）以及虚拟助理和语音助手通常执行的任务。
           计算机视觉：该 AI 技术使计算机和系统能够从数字图像、视频和其他可视输入中获取有意义的信息，并基于这些输入采取行动。 这种提供建议的能力将其与图像识别任务区分开来。 计算机视觉由卷积神经网络提供支持，应用在社交媒体的照片标记、医疗保健中的放射成像以及汽车工业中的自动驾驶汽车等领域。
           推荐引擎：AI 算法使用过去的消费行为数据，帮助发现可用于制定更有效的交叉销售策略的数据趋势。 这用于在在线零售商的结帐流程中向客户提供相关的附加建议。
           自动股票交易：旨在用于优化股票投资组合，AI 驱动的高频交易平台每天可产生成千上万个甚至数以百万计的交易，无需人工干预。
           人工智能的发展历史： 大事记
           “一台会思考的机器”这一构想最早可以追溯到古希腊时期。 而自从电子计算技术问世以来（相对于本文中讨论的某些主题而言），人工智能进化过程中的重要事件和里程碑包括以下内容：

           1950：艾伦·图灵发表了论文“计算机械和智能”。图灵因为在二战期间破译纳粹德国的 ENIGMA 码而闻名于世。在这篇论文中，他提出了问题“机器是否可以思考？”并进行回答，推出了图灵测试，用于确定计算机是否能证明具有与人类相同的智能（或相同智能的结果）。 自此之后，人们就图灵测试的价值一直争论不休。
           1956：John McCarthy 在达特茅斯学院举办的首届 AI 会议上创造了“人工智能”一词。（McCarthy 继续发明了 Lisp 语言。）同年晚些时候，Allen Newell、J.C.Shaw 和 Herbert Simon 创建了 Logic Theorist，这是有史以来第一个运行的 AI 软件程序。
           1967：Frank Rosenblatt 构建了 Mark 1 Perceptron，这是第一台基于神经网络的计算机，它可以通过试错法不断学习。 就在一年后，Marvin Minsky 和 Seymour Papert 出版了一本名为《感知器》的书，这本书既成为神经网络领域的标志性作品，同时至少在一段时间内，成为反对未来神经网络研究项目的论据。
           1980 年代：使用反向传播算法训练自己的神经网络在 AI 应用中广泛使用。
           1997：IBM 的深蓝计算机在国际象棋比赛（和复赛）中击败国际象棋世界冠军 Garry Kasparov。
           2011：IBM Watson 在《危险边缘！》节目中战胜冠军 Ken Jennings 和 Brad Rutter。
           2015：百度的 Minwa 超级计算机使用一种称为卷积神经网络的特殊深度神经网络来识别图像并进行分类，其准确率高于一般的人类。
           2016：由深度神经网络支持的 DeepMind 的 AlphaGo 程序在五轮比赛中击败了围棋世界冠军 Lee Sodol。 考虑到随着游戏的进行，可能的走法非常之多，这一胜利具有重要意义（仅走了四步之后走法就超过 14.5 万亿种！）。 后来，谷歌以四亿美元的报价收购了 DeepMind。
           人工智能和 IBM Cloud
           在为企业推进 AI 驱动技术方面，IBM 一直是领导者，它已率先为多种行业开创了机器学习系统的未来。 立足于数十年的 AI 研究成果、多年来与各种规模企业合作积累的经验，以及从 30000 多次 IBM Watson 参与中汲取的知识，IBM 为成功部署人工智能搭建了 AI 之梯：

           收集：简化数据收集和可访问性。
           整理：创建面向业务的分析基础。
           分析：构建可扩展而且值得信赖的 AI 驱动的系统。
           融入：在整个业务框架中集成和优化系统。
           现代化： 将 AI 应用和系统引入云。
           IBM Watson 为企业提供彻底改造业务系统和工作流程所需的 AI 工具，同时显著提高自动化水平和效率。 有关 IBM 如何帮助您完成 AI 之旅的更多信息，请浏览 IBM 产品服务组合：托管服务和解决方案

           注册 IBMid 并创建 IBM Cloud 帐户。
            
            """)

    elif selected == "看视频":
        row1,row2 = st.columns(2)
        with row1:

         row1.markdown(" # Enjoy All AI Tutorial Vedios")
         row1.markdown("Explore as you Learn")
         with row2:
           st.write("###")

           st.video("https://youtu.be/yVV_t_Tewvs")
        #st.subheader("看怎么做:")
        # VEDIO SECTION:
        #video_file = open(
         #  r'C:\Users\ADMIN\Videos\Captures\GoDays Landing Page – Figma and 2 more pages - Personal - Microsoft​ Edge 2022-09-11 15-42-24.mp4',
          # 'rb')
        #video_bytes = video_file.read()
        #st.video(video_bytes)
        # st.video(video_file)
        #st.snow()
           st.button("感谢你观看视频")

    elif selected == "关于我们":
        st.subheader("目的")

        def load_css():
            with open("style.css") as f:
                st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
            st.markdown(
                '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
                unsafe_allow_html=True)

        def st_button(icon, url, label, iconsize):
            if icon == 'youtube':
                button_code = f'''
                <p>
                    <a href={url} class="btn btn-outline-primary btn-lg btn-block" type="button" aria-pressed="true">
                        <svg xmlns="http://www.w3.org/2000/svg" width={iconsize} height={iconsize} fill="currentColor" class="bi bi-youtube" viewBox="0 0 16 16">
                            <path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.009.104c-.05.572-.124 1.14-.235 1.558a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.052.008-.104.022-.26.01-.104c.048-.519.119-1.023.22-1.402a2.007 2.007 0 0 1 1.415-1.42c.487-.13 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z"/>
                        </svg>  
                        {label}
                    </a>
                </p>'''
            elif icon == 'twitter':
                button_code = f'''
                <p>
                <a href={url} class="btn btn-outline-primary btn-lg btn-block" type="button" aria-pressed="true">
                    <svg xmlns="http://www.w3.org/2000/svg" width={iconsize} height={iconsize} fill="currentColor" class="bi bi-twitter" viewBox="0 0 16 16">
                        <path d="M5.026 15c6.038 0 9.341-5.003 9.341-9.334 0-.14 0-.282-.006-.422A6.685 6.685 0 0 0 16 3.542a6.658 6.658 0 0 1-1.889.518 3.301 3.301 0 0 0 1.447-1.817 6.533 6.533 0 0 1-2.087.793A3.286 3.286 0 0 0 7.875 6.03a9.325 9.325 0 0 1-6.767-3.429 3.289 3.289 0 0 0 1.018 4.382A3.323 3.323 0 0 1 .64 6.575v.045a3.288 3.288 0 0 0 2.632 3.218 3.203 3.203 0 0 1-.865.115 3.23 3.23 0 0 1-.614-.057 3.283 3.283 0 0 0 3.067 2.277A6.588 6.588 0 0 1 .78 13.58a6.32 6.32 0 0 1-.78-.045A9.344 9.344 0 0 0 5.026 15z"/>
                    </svg>
                    {label}
                </a>
                </p>'''
            elif icon == 'linkedin':
                button_code = f'''
                <p>
                    <a href={url} class="btn btn-outline-primary btn-lg btn-block" type="button" aria-pressed="true">
                        <svg xmlns="http://www.w3.org/2000/svg" width={iconsize} height={iconsize} fill="currentColor" class="bi bi-linkedin" viewBox="0 0 16 16">
                            <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
                        </svg>
                        {label}
                    </a>
                </p>'''
            elif icon == 'medium':
                button_code = f'''
                <p>
                    <a href={url} class="btn btn-outline-primary btn-lg btn-block" type="button" aria-pressed="true">
                        <svg xmlns="http://www.w3.org/2000/svg" width={iconsize} height={iconsize} fill="currentColor" class="bi bi-medium" viewBox="0 0 16 16">
                            <path d="M9.025 8c0 2.485-2.02 4.5-4.513 4.5A4.506 4.506 0 0 1 0 8c0-2.486 2.02-4.5 4.512-4.5A4.506 4.506 0 0 1 9.025 8zm4.95 0c0 2.34-1.01 4.236-2.256 4.236-1.246 0-2.256-1.897-2.256-4.236 0-2.34 1.01-4.236 2.256-4.236 1.246 0 2.256 1.897 2.256 4.236zM16 8c0 2.096-.355 3.795-.794 3.795-.438 0-.793-1.7-.793-3.795 0-2.096.355-3.795.794-3.795.438 0 .793 1.699.793 3.795z"/>
                        </svg>
                        {label}
                    </a>
                </p>'''
            elif icon == 'newsletter':
                button_code = f'''
                <p>
                    <a href={url} class="btn btn-outline-primary btn-lg btn-block" type="button" aria-pressed="true">
                        <svg xmlns="http://www.w3.org/2000/svg" width={iconsize} height={iconsize} fill="currentColor" class="bi bi-envelope" viewBox="0 0 16 16">
                            <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4Zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2Zm13 2.383-4.708 2.825L15 11.105V5.383Zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.741ZM1 11.105l4.708-2.897L1 5.383v5.722Z"/>
                        </svg>
                        {label}
                    </a>
                </p>'''
            elif icon == 'cup':
                button_code = f'''
                <p>
                    <a href={url} class="btn btn-outline-primary btn-lg btn-block" type="button" aria-pressed="true">
                        <svg xmlns="http://www.w3.org/2000/svg" width={iconsize} height={iconsize} fill="currentColor" class="bi bi-cup-fill" viewBox="0 0 16 16">
                            <path d="M1 2a1 1 0 0 1 1-1h11a1 1 0 0 1 1 1v1h.5A1.5 1.5 0 0 1 16 4.5v7a1.5 1.5 0 0 1-1.5 1.5h-.55a2.5 2.5 0 0 1-2.45 2h-8A2.5 2.5 0 0 1 1 12.5V2zm13 10h.5a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.5-.5H14v8z"/>
                        </svg>
                        {label}
                    </a>
                </p>'''
            elif icon == '':
                button_code = f'''
                <p>
                    <a href={url} class="btn btn-outline-primary btn-lg btn-block" type="button" aria-pressed="true">
                        {label}
                    </a>
                </p>'''
            return st.markdown(button_code,unsafe_allow_html=True)

        load_css()

        st.write(
            "[![Star](https://img.shields.io/github/stars/Gershom- Taku/links.svg?logo=github&style=social)](https://gitHub.com/Gershom- Taku/links)")

        col1, col2, col3 = st.columns(3)
        col2.image(Image.open(r"C:\Users\ADMIN\Desktop\MachieLearnig APP\images\logozunyi.jpg"))

        st.header('Takudzwa Choto')

        st.info(
            'Developer ,with an interest in Data Science,Machine Learning,Deep Learning and AI')

        icon_size = 30

        st_button('youtube', '#https://gershom-taku-check-and-chat-main-rftzu7.streamlitapp.com/', 'Takudzwa', icon_size)
        st_button('medium', 'https://gershom-taku-check-and-chat-main-rftzu7.streamlitapp.com/', 'Read my Blogs', icon_size)
        st_button('twitter', 'https://twitter.com/Takudzwa_Choto', 'Follow me on Twitter', icon_size)
        st_button('linkedin', '#https://gershom-taku-check-and-chat-main-rftzu7.streamlitapp.com/', 'Follow me on LinkedIn', icon_size)
        st_button('newsletter', '#https://gershom-taku-check-and-chat-main-rftzu7.streamlitapp.com/', 'Sign up for my Newsletter', icon_size)
        st_button('cup', 'https://twitter.com/Takudzwa_Choto', 'Buy me a Coffee', icon_size)


        st.subheader("Amazing Projects:")
        #VEDIO SECTION:
        video_file = open(
          r'C:\Users\ADMIN\Videos\Captures\GoDays Landing Page – Figma and 2 more pages - Personal - Microsoft​ Edge 2022-09-11 15-42-24.mp4',
         'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
        st.snow()
        st.button("感谢你观看视频")


    elif selected == "联系我们":
        st.subheader("发邮件")

        st.markdown(""" <style> .font {
                               font-size:35px ; font-family: 'Cooper Black'; color: blue;} 
                               </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">联系我们:</p>', unsafe_allow_html=True)
        contact_form = """
                            <input type = "hidden" name = " _capture" value = "false">
                            <form action="https://formsubmit.co/chototakudzwa8@gmail.com" method="POST">
                            <input type="text" name="name" placeholder = "Your name" required>
                            <input type="email" name="email" placeholder = "Your email" required>
                            <input type = "text" name = "company" placeholder = "Your company" required >
                            <textarea  name = "message" placeholder = "Enter message" required></textarea>
                            <button type="submit">Send</button>
                       </form>

                            """

        st.markdown(contact_form, unsafe_allow_html=True)

###################ADDING THE FOOTER#####################

if __name__ == '__main__':
    main()

st.write("---")
footer = """<style>
   a:link , a:visited{
   color: white;
   background-color: transparent;
   text-decoration: none;
   }

   a:hover,  a:active {
   color: red;
   background-color: transparent;
   text-decoration: none;
   }

   .footer {
   position: fixed;
   left: 0;
   bottom: 0;
   width: 100%;
   background-color:#5486ea ;
   color: white;
   text-align: center;
   }
   </style>
   <div class="footer">
   <p>DEVELOPED BY <a style='display: block; text-align: center;'" target="_blank">遵义师范学院学生科学团总支</a></p>
   </div>
   """
st.markdown(footer, unsafe_allow_html=True)

st.markdown("""
<style>
 .css-1iyw2u1 {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

#########END OF THE FOOTER#############

##################################ADDING BACKGROUND PICTURE#############################################################
#def add_bg_from_local(image_file):
 #   with open(image_file, "rb") as image_file:
 #       st.markdown(
 #           f"""
 #   <style>
 #   .stApp {{
 #       background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
 #       background-size: cover
 #}}
 #   </style>
  #  """,
 #           unsafe_allow_html=True

 #       )

#add_bg_from_local(r"C:\Users\ADMIN\Desktop\MachieLearnig APP\images\logozunyi.jpg")

#with st.sidebar:
 #   selected = option_menu(menu_title = None,options =["home","school","contacts"],
  #                         default_index = 0
   #                        )

#if selected == "home":
 #         st.title(f"helo")