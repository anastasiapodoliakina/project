import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go



df = pd.read_csv('Salary_Data.csv')
df = df.dropna()
lst = []
lst = df[df.Gender=='Other'].index[0:14]
df = df.drop(labels=lst, axis=0)
df['Education Level'] = df['Education Level'].replace("Bachelor's", "Bachelor's Degree")
df['Education Level'] = df['Education Level'].replace("Master's", "Master's Degree")
df['Education Level'] = df['Education Level'].replace("phD", "PhD")

val = []
for i in range(4):
    val.append(df["Education Level"].value_counts()[i])
fig = go.Figure(data=[go.Pie(labels=df["Education Level"].value_counts().index.tolist(), values=val, hole=.3)])

fig1 = px.scatter(df[['Age', 'Salary']].groupby('Age', as_index=False).mean(),
                 x="Age", y="Salary",  marginal_y="rug")
fig2 = px.line(df[['Salary', 'Years of Experience']].groupby('Years of Experience', as_index=False).mean(), x="Years of Experience", y="Salary")

ed_df = df[['Salary', 'Education Level']].groupby('Education Level', as_index=False).mean().sort_values("Education Level")
fig3 = px.bar(ed_df, x="Education Level", y="Salary", color = 'Education Level')

fig4 = px.line(df[['Salary', 'Gender','Age']].groupby(['Gender', 'Age'], as_index=False).mean(), x="Age", y="Salary", color='Gender')

vsd = df[["Age", "Salary", "Years of Experience", "Education Level"]].groupby(["Education Level","Years of Experience"],as_index=False).mean()
fig5 = px.scatter(vsd,
           x="Age", y="Salary",
                size="Years of Experience", color="Education Level",
                  size_max=10,trendline="lowess",hover_data=["Years of Experience"])

st.title('Salary Data')
page_names = ['Dataframe', 'Descriptive statistics', 'Plots']
page = st.radio('Navigation', page_names)
if page == 'Dataframe':
    st.dataframe(df)
    st.write('''
     #### This dataset contains information about some employees. Each row represents a different employee, and the columns include information such as age, gender, education level, job title, years of experience, and salary.
     ''')
elif page == 'Plots':

    pl = st.selectbox("Choose:", ['Most Common Education Level', "Correlation of Salary and Work Experience", "Correlation of Salary and Education", 'Correlation of Age and Salary', 'Correlation of Age and Salary for Men and Women', 'Correlation of Salary and All Other Columns'])
    if pl == 'Most Common Education Level':
        st.plotly_chart(fig)
    elif pl == "Correlation of Salary and Work Experience":
        st.plotly_chart(fig2)
    elif pl == 'Correlation of Salary and Education':
        st.plotly_chart(fig3)
    elif pl == 'Correlation of Age and Salary':
        st.plotly_chart(fig1)
    elif pl == 'Correlation of Age and Salary for Men and Women':
        st.plotly_chart(fig4)
    elif pl == 'Correlation of Salary and All Other Columns':
        st.plotly_chart(fig5)

elif page == 'Descriptive statistics':
    selected_bonus = st.selectbox("Choose:", ['Salary', "Age", "Years of Experience"])
    if selected_bonus == 'Salary':
        st.write('''
                        | mean             | median          | std        | min       | max         |
                        | :--------------: |:---------------:| :---------:| :--------:| :----------:|
                        | 115326.96        | 115000.0        | 52786.18   | 350.0     | 250000.0    |
                        ''')
    elif selected_bonus == 'Age':
        st.write('''
                | mean             | median          | std        | min       | max         |
                | :--------------: |:---------------:| :---------:| :--------:| :----------:|
                | 33.62            | 32.0            | 7.61       | 21.0      | 62.0        |''')
    elif selected_bonus == 'Years of Experience':
        st.write('''
            | mean | median | std | min | max |
            |:--------------: |:---------------: |:---------: |:--------: |:----------: |
            | 8.09 | 7.0 | 6.05 | 0.0 | 34.0 |
            # 
            ''')

