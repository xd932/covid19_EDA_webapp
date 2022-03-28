import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go




ind_states_22=pd.read_csv('covid_status.csv')
no_vir_dea=pd.read_csv('no_vir_dea.csv')
oxy_dea=pd.read_csv('oxy_dea.csv')
#kitne ko covid huva world mein
world_cases=pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_cases.csv')
#countrwise Confirmed	Deaths	Active	Deaths / 100 Cases	Population	Cases / Million People	Confirmed last week
country=pd.read_csv('countrywise.csv')
#vaccination active	positive	cured	death	new_active	new_positive	new_cured	new_death	death_reconsille	total	state_code
india=pd.read_json('https://raw.githubusercontent.com/datameet/covid19/master/downloads/mohfw-backup/data_json/2022-03-22T08%3A00%3A00.00%2B05%3A30_md5_1b9a533cf03e6d9d3b942fcd5796fd45.json')

#vaccination
vax=pd.read_csv('vax.csv',index_col=False)
vaxind=pd.read_csv('vax_ind_tot.csv')



st.sidebar.title('EDA on COVID-19')
st.sidebar.image('http://www.nits.ac.in/images%20of%20site/covid-19-image.png')










user_menu=st.sidebar.radio(
    'Selectan Option',
    ('None Covid Death','Oxygen Shortage','World Yearly Cases','Indian States Cases','Vaccination Status')
)

if user_menu == 'None Covid Death':
    st.title('NON COVID DEATHS:')
    no_vir_dea=no_vir_dea.drop(['DB_LASTUPDATED_SET','Name(s) and age','Source','Link','Category','Date of publication','District','Incident Location','S. No'],axis=1)


    st.dataframe(no_vir_dea)
    st.subheader('No of death per State')
    fig = px.pie(no_vir_dea, values='No. of deaths', names='State/UT')
    st.plotly_chart(fig)
     
    st.subheader('Cause:')
    lst=[]
    lst=no_vir_dea['Reason of death'].value_counts()
    lst
     
    st.subheader('Categorizing')
    lst1=[]
    lst1=no_vir_dea['Occupation\nCategory'].value_counts()
    lst1

     




if user_menu=='Oxygen Shortage':
    st.header('Death Due to Oxygen Shortage')
    oxy_dea=oxy_dea.drop(['s_no','district','category','source','date_of_report','reference'],axis=1)
    st.dataframe(oxy_dea)


    st.subheader('Statewise Death')
    grouped=oxy_dea.groupby(['state'], as_index=False)['no_of_deaths'].sum()
    grouped=grouped.sort_values('no_of_deaths', ascending=False)
    grouped.reset_index(drop=True, inplace=True)
    grouped

    st.subheader('Statewise Contribution')
    fig = px.line(grouped, x='state', y='no_of_deaths',width=900,height=700)
    st.plotly_chart(fig)






if user_menu=='World Yearly Cases':
    st.header('Worldwide Cases')
    world_cases = world_cases.fillna(0).round(2)
    st.dataframe(world_cases)

    st.subheader('Countries Wise Cases:')
    x= st.text_input('','India')
    z= st.text_input('','Africa')
    w= st.text_input('','United Kingdom')
    a= st.text_input('','United States')
    b= st.text_input('','Italy')
    c= st.text_input('','World')
    st.subheader('Checking waves timing, there number')
    fig = px.line(world_cases, x='date', y=[x,z,w,a,b,c],width=900,height=700)
    st.plotly_chart(fig)

    lst2=[]
    lst2=world_cases.columns
    st.subheader('Total cases of Countries')
    fig=px.line(world_cases,x='date',y=lst2,width=1000,height=500)
    st.plotly_chart(fig)



if user_menu=='Indian States Cases':
    st.header('Indian Cases')
    ind_states_22['State/UTs']=ind_states_22['State/UTs'].str[:4].str.upper()
    ind_states_22['Severity%']=(ind_states_22['Total Cases']/ind_states_22['Population'])*100
    ind_states_22['Deaths%']=(ind_states_22['Deaths']/ind_states_22['Population'])*100
    ind_states_22=ind_states_22.round(2)
    ind_states_22

    st.subheader('Comparing total death, cases till date ')
    fig = px.line(ind_states_22, x='State/UTs', y=['Total Cases','Deaths'],width=900,height=700)
    st.plotly_chart(fig)
    st.subheader('Analyzing ratios')
    fig = px.line(ind_states_22, x='State/UTs', y=['Active Ratio','Discharge Ratio','Death Ratio'],width=900,height=700)
    st.plotly_chart(fig)
    st.subheader('Comparing all datas')
    fig = px.line(ind_states_22, x='State/UTs', y=['Total Cases','Active','Discharged','Deaths'],width=900,height=700)
    st.plotly_chart(fig)




     








if user_menu=='Vaccination Status':
    st.header("India's Vaccination Status")
    vax = vax.iloc[:-1 , :]
    vax
    st.subheader('Doses administered Statwise')
    fig=px.line(vax,x='STATE/UT',y=['1st18+','2nd18+','1st15-18','2nd15-18','1st12-14','Precaution DOSE'],width=1000,height=700)
    st.plotly_chart(fig)


    st.subheader('Group-wise Distribution :')
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=vax['STATE/UT'],y=vax['Total DOSE']))
    st.plotly_chart(fig)

    vaxind['DOSES']=vaxind['DOSES'].str.replace(',', '').astype(int)
    st.subheader('Total dose administrated')
    fig = px.bar(vaxind, x="DOSES", y="CATEGORY", orientation='h',width=800,height=700)
    st.plotly_chart(fig)    

    vax['Total DOSE']=vax['Total DOSE'].str.replace(',', '').astype(int)
    lstate=[]
    lstate=vax['STATE/UT']
    ldoses=[]
    ldoses=vax['Total DOSE']


    st.subheader(' % share of doses Statewise')
    fig = px.pie(no_vir_dea, values=ldoses, names=lstate,width=700,height=700)
    st.plotly_chart(fig)




     