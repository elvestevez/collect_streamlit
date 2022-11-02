import streamlit as st
from PIL import Image
import time
from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


ICON_PATH = './img/icon.png'
CONFIG_FILE = 'datatype.properties'
OPTION_YES = 'Yes'
OPTION_NO = 'No'
ENCODE = 'utf-8'
#URL_API = 'http://localhost:9080'
URL_API = 'https://datacollect-api.herokuapp.com'
type_income_aeat = 'income_aeat'
type_income_ine = 'income_ine'
type_population_ine = 'population_ine'


# get dimensions
def get_api_cities():
    #df = pd.read_json(URL_API + '/cities')
    response = urlopen(URL_API + '/cities')
    data_json = json.loads(response.read())
    df = pd.DataFrame(data_json['data'])
    data = df['City']
    metadata = df = pd.DataFrame(data_json['metadata'])
    return data, metadata

def get_api_provinces():
    #df = pd.read_json(URL_API + '/provinces')
    response = urlopen(URL_API + '/provinces')
    data_json = json.loads(response.read())
    df = pd.DataFrame(data_json['data'])
    data = df['Province']
    metadata = df = pd.DataFrame(data_json['metadata'])
    return data, metadata

def get_api_regions():
    #df = pd.read_json(URL_API + '/regions')
    response = urlopen(URL_API + '/regions')
    data_json = json.loads(response.read())
    df = pd.DataFrame(data_json['data'])
    data = df['Region']
    metadata = df = pd.DataFrame(data_json['metadata'])
    return data, metadata

def get_api_indicators_incomes():
    #df = pd.read_json(URL_API + '/indicators-income-ine')
    response = urlopen(URL_API + '/indicator-income-ine')
    data_json = json.loads(response.read())
    df = pd.DataFrame(data_json['data'])
    data = df['Name_indicator']
    metadata = df = pd.DataFrame(data_json['metadata'])
    return data, metadata

# get population INE
#@st.cache(show_spinner=False)
def get_api_population_ine(year, age='yes'):
    if age == OPTION_NO:
        age = 'no'
    if age == OPTION_YES:
        age = 'yes'
    url = URL_API + f'/population-ine/cities/year/{year}?age={age}'
    #df = pd.read_json(url)
    response = urlopen(url)
    data_json = json.loads(response.read())
    data = pd.DataFrame(data_json['data'])
    metadata = df = pd.DataFrame(data_json['metadata'])
    return data, metadata

# get incomes INE
#@st.cache(show_spinner=False)
def get_api_incomes_ine(year):
    url = URL_API + f'/income-ine/cities/year/{year}'
    #df = pd.read_json(url)
    response = urlopen(url)
    data_json = json.loads(response.read())
    data = pd.DataFrame(data_json['data'])
    metadata = df = pd.DataFrame(data_json['metadata'])
    return data, metadata

# get incomes AEAT
#@st.cache(show_spinner=False)
def get_api_incomes_aeat(year):
    url = URL_API + f'/income-aeat/cities/year/{year}'
    #df = pd.read_json(url)
    response = urlopen(url)
    data_json = json.loads(response.read())
    data = pd.DataFrame(data_json['data'])
    metadata = df = pd.DataFrame(data_json['metadata'])
    return data, metadata

# get years incomes AEAT
def get_api_incomes_aeat_years():
    url = URL_API + f'/income-aeat/years'
    #df = pd.read_json(url)
    response = urlopen(url)
    data_json = json.loads(response.read())
    df = pd.DataFrame(data_json['data'])
    if df.empty:
        #return 0, 1
        return []
    else:
        list_years = list(df['Year'])
        #min_y = min(list_years)
        #max_y = max(list_years)
        #return min_y, max_y
        list_years.sort(reverse=True)
        return list_years

# get years incomes INE
def get_api_incomes_ine_years():
    url = URL_API + f'/income-ine/years'
    #df = pd.read_json(url)
    response = urlopen(url)
    data_json = json.loads(response.read())
    df = pd.DataFrame(data_json['data'])
    if df.empty:
        #return 0, 1
        return []
    else:
        list_years = list(df['Year'])
        #min_y = min(list_years)
        #max_y = max(list_years)
        #return min_y, max_y
        list_years.sort(reverse=True)
        return list_years

# get years population INE
def get_api_population_ine_years():
    url = URL_API + f'/population-ine/years'
    #df = pd.read_json(url)
    response = urlopen(url)
    data_json = json.loads(response.read())
    df = pd.DataFrame(data_json['data'])
    if df.empty:
        #return 0, 1
        return []
    else:
        list_years = list(df['Year'])
        #min_y = min(list_years)
        #max_y = max(list_years)
        #return min_y, max_y
        list_years.sort(reverse=True)
        return list_years



# export to csv
def export_to_csv(df, encode):
    return df.to_csv(index=False, sep=";").encode(encode)



# build graph income aeat
def build_graph_incomes_aeat(df):
    list_fig = []
    # graph 1
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Top 5 cities',  'Bottom 5 cities'))
    fig.add_trace(go.Bar(x=df.nlargest(5, 'Avg_gross_income')['City'], y=df.nlargest(5, 'Avg_gross_income')['Avg_gross_income']),
                  row=1, col=1
    )
    fig.add_trace(go.Bar(x=df.nsmallest(5, 'Avg_gross_income')['City'], y=df.nsmallest(5, 'Avg_gross_income')['Avg_gross_income']),
                  row=1, col=2
    )
    fig.update_layout(height=400, width=800, showlegend=False)
    fig.update_xaxes(tickangle=45)
    list_fig.append(fig)

    return list_fig

# calculate age groups population
def gr_age_population(df):
    df_out = df.copy()
    # gr 0-18 years
    df_out['0_18'] = df_out['Female_0'] + df_out['Female_1'] + df_out['Female_2'] + df_out['Female_3'] + \
                 df_out['Female_4'] + df_out['Female_5'] + df_out['Female_6'] + df_out['Female_7'] + \
                 df_out['Female_8'] + df_out['Female_9'] + df_out['Female_10'] + df_out['Female_11'] + \
                 df_out['Female_12'] + df_out['Female_13'] + df_out['Female_14'] + df_out['Female_15'] + \
                 df_out['Female_16'] + df_out['Female_17'] + df_out['Female_18'] + \
                 df_out['Male_0'] + df_out['Male_1'] + df_out['Male_2'] + df_out['Male_3'] + \
                 df_out['Male_4'] + df_out['Male_5'] + df_out['Male_6'] + df_out['Male_7'] + \
                 df_out['Male_8'] + df_out['Male_9'] + df_out['Male_10'] + df_out['Male_11'] + \
                 df_out['Male_12'] + df_out['Male_13'] + df_out['Male_14'] + df_out['Male_15'] + \
                 df_out['Male_16'] + df_out['Male_17'] + df_out['Male_18']
    df_out['0-18 years'] = df_out['0_18'] / df_out['Total'] * 100
    # gr 19-30 years
    df_out['19_30'] = df_out['Female_19'] + df_out['Female_20'] + df_out['Female_21'] + df_out['Female_22'] + \
                  df_out['Female_23'] + df_out['Female_24'] + df_out['Female_25'] + df_out['Female_26'] + \
                  df_out['Female_27'] + df_out['Female_28'] + df_out['Female_29'] + df_out['Female_30'] + \
                  df_out['Male_19'] + df_out['Male_20'] + df_out['Male_21'] + df_out['Male_22'] + \
                  df_out['Male_23'] + df_out['Male_24'] + df_out['Male_25'] + df_out['Male_26'] + \
                  df_out['Male_27'] + df_out['Male_28'] + df_out['Male_29'] + df_out['Male_30'] 
    df_out['19-30 years'] = df_out['19_30'] / df_out['Total'] * 100
    # gr 31-65 years
    df_out['31_65'] = df_out['Female_31'] + df_out['Female_32'] + df_out['Female_33'] + df_out['Female_34'] + \
                  df_out['Female_35'] + df_out['Female_36'] + df_out['Female_37'] + df_out['Female_38'] + \
                  df_out['Female_39'] + df_out['Female_40'] + df_out['Female_41'] + df_out['Female_42'] + \
                  df_out['Female_43'] + df_out['Female_44'] + df_out['Female_45'] + df_out['Female_46'] + \
                  df_out['Female_47'] + df_out['Female_48'] + df_out['Female_49'] + df_out['Female_50'] + \
                  df_out['Female_51'] + df_out['Female_52'] + df_out['Female_53'] + df_out['Female_54'] + \
                  df_out['Female_55'] + df_out['Female_56'] + df_out['Female_57'] + df_out['Female_58'] + \
                  df_out['Female_59'] + df_out['Female_60'] + df_out['Female_61'] + df_out['Female_62'] + \
                  df_out['Female_63'] + df_out['Female_64'] + df_out['Female_65'] + \
                  df_out['Male_31'] + df_out['Male_32'] + df_out['Male_33'] + df_out['Male_34'] + \
                  df_out['Male_35'] + df_out['Male_36'] + df_out['Male_37'] + df_out['Male_38'] + \
                  df_out['Male_39'] + df_out['Male_40'] + df_out['Male_41'] + df_out['Male_42'] + \
                  df_out['Male_43'] + df_out['Male_44'] + df_out['Male_45'] + df_out['Male_46'] + \
                  df_out['Male_47'] + df_out['Male_48'] + df_out['Male_49'] + df_out['Male_50'] + \
                  df_out['Male_51'] + df_out['Male_52'] + df_out['Male_53'] + df_out['Male_54'] + \
                  df_out['Male_55'] + df_out['Male_56'] + df_out['Male_57'] + df_out['Male_58'] + \
                  df_out['Male_59'] + df_out['Male_60'] + df_out['Male_61'] + df_out['Male_62'] + \
                  df_out['Male_63'] + df_out['Male_64'] + df_out['Male_65']                  
    df_out['31-65 years'] = df_out['31_65'] / df_out['Total'] * 100
    # gr 66-100 years
    df_out['66_100'] = df_out['Female_66'] + df_out['Female_67'] + df_out['Female_68'] + df_out['Female_69'] + \
                   df_out['Female_70'] + df_out['Female_71'] + df_out['Female_72'] + df_out['Female_73'] + \
                   df_out['Female_74'] + df_out['Female_75'] + df_out['Female_76'] + df_out['Female_77'] + \
                   df_out['Female_78'] + df_out['Female_79'] + df_out['Female_80'] + df_out['Female_81'] + \
                   df_out['Female_82'] + df_out['Female_83'] + df_out['Female_84'] + df_out['Female_85'] + \
                   df_out['Female_86'] + df_out['Female_87'] + df_out['Female_88'] + df_out['Female_89'] + \
                   df_out['Female_90'] + df_out['Female_91'] + df_out['Female_92'] + df_out['Female_93'] + \
                   df_out['Female_94'] + df_out['Female_95'] + df_out['Female_96'] + df_out['Female_97'] + \
                   df_out['Female_98'] + df_out['Female_99'] + df_out['Female_100'] + \
                   df_out['Male_66'] + df_out['Male_67'] + df_out['Male_68'] + df_out['Male_69'] + \
                   df_out['Male_70'] + df_out['Male_71'] + df_out['Male_72'] + df_out['Male_73'] + \
                   df_out['Male_74'] + df_out['Male_75'] + df_out['Male_76'] + df_out['Male_77'] + \
                   df_out['Male_78'] + df_out['Male_79'] + df_out['Male_80'] + df_out['Male_81'] + \
                   df_out['Male_82'] + df_out['Male_83'] + df_out['Male_84'] + df_out['Male_85'] + \
                   df_out['Male_86'] + df_out['Male_87'] + df_out['Male_88'] + df_out['Male_89'] + \
                   df_out['Male_90'] + df_out['Male_91'] + df_out['Male_92'] + df_out['Male_93'] + \
                   df_out['Male_94'] + df_out['Male_95'] + df_out['Male_96'] + df_out['Male_97'] + \
                   df_out['Male_98'] + df_out['Male_99'] + df_out['Male_100']                  
    df_out['66-100+ years'] = df_out['66_100'] / df_out['Total'] * 100

    return df_out

# calculate avg age population
def avg_age_population(df):
    df_out = df.copy()
    df_out['Total_age'] = df_out['Female_0'] * 0 + df_out['Male_0'] * 0 + \
                    df_out['Female_1'] * 1 + df_out['Male_1'] * 1 + \
                    df_out['Female_2'] * 2 + df_out['Male_2'] * 2 + \
                    df_out['Female_3'] * 3 + df_out['Male_3'] * 3 + \
                    df_out['Female_4'] * 4 + df_out['Male_4'] * 4 + \
                    df_out['Female_5'] * 5 + df_out['Male_5'] * 5 + \
                    df_out['Female_6'] * 6 + df_out['Male_6'] * 6 + \
                    df_out['Female_7'] * 7 + df_out['Male_7'] * 7 + \
                    df_out['Female_8'] * 8 + df_out['Male_8'] * 8 + \
                    df_out['Female_9'] * 9 + df_out['Male_9'] * 9 + \
                    df_out['Female_10'] * 10 + df_out['Male_10'] * 10 + \
                    df_out['Female_11'] * 11 + df_out['Male_11'] * 11 + \
                    df_out['Female_12'] * 12 + df_out['Male_12'] * 12 + \
                    df_out['Female_13'] * 13 + df_out['Male_13'] * 13 + \
                    df_out['Female_14'] * 14 + df_out['Male_14'] * 14 + \
                    df_out['Female_15'] * 15 + df_out['Male_15'] * 15 + \
                    df_out['Female_16'] * 16 + df_out['Male_16'] * 16 + \
                    df_out['Female_17'] * 17 + df_out['Male_17'] * 17 + \
                    df_out['Female_18'] * 18 + df_out['Male_18'] * 18 + \
                    df_out['Female_19'] * 19 + df_out['Male_19'] * 19 + \
                    df_out['Female_20'] * 20 + df_out['Male_20'] * 20 + \
                    df_out['Female_21'] * 21 + df_out['Male_21'] * 21 + \
                    df_out['Female_22'] * 22 + df_out['Male_22'] * 22 + \
                    df_out['Female_23'] * 23 + df_out['Male_23'] * 23 + \
                    df_out['Female_24'] * 24 + df_out['Male_24'] * 24 + \
                    df_out['Female_25'] * 25 + df_out['Male_25'] * 25 + \
                    df_out['Female_26'] * 26 + df_out['Male_26'] * 26 + \
                    df_out['Female_27'] * 27 + df_out['Male_27'] * 27 + \
                    df_out['Female_28'] * 28 + df_out['Male_28'] * 28 + \
                    df_out['Female_29'] * 29 + df_out['Male_29'] * 29 + \
                    df_out['Female_30'] * 30 + df_out['Male_30'] * 30 + \
                    df_out['Female_31'] * 31 + df_out['Male_31'] * 31 + \
                    df_out['Female_32'] * 32 + df_out['Male_32'] * 32 + \
                    df_out['Female_33'] * 33 + df_out['Male_33'] * 33 + \
                    df_out['Female_34'] * 34 + df_out['Male_34'] * 34 + \
                    df_out['Female_35'] * 35 + df_out['Male_35'] * 35 + \
                    df_out['Female_36'] * 36 + df_out['Male_36'] * 36 + \
                    df_out['Female_37'] * 37 + df_out['Male_37'] * 37 + \
                    df_out['Female_38'] * 38 + df_out['Male_38'] * 38 + \
                    df_out['Female_39'] * 39 + df_out['Male_39'] * 39 + \
                    df_out['Female_40'] * 40 + df_out['Male_40'] * 40 + \
                    df_out['Female_41'] * 41 + df_out['Male_41'] * 41 + \
                    df_out['Female_42'] * 42 + df_out['Male_42'] * 42 + \
                    df_out['Female_43'] * 43 + df_out['Male_43'] * 43 + \
                    df_out['Female_44'] * 44 + df_out['Male_44'] * 44 + \
                    df_out['Female_45'] * 45 + df_out['Male_45'] * 45 + \
                    df_out['Female_46'] * 46 + df_out['Male_46'] * 46 + \
                    df_out['Female_47'] * 47 + df_out['Male_47'] * 47 + \
                    df_out['Female_48'] * 48 + df_out['Male_48'] * 48 + \
                    df_out['Female_49'] * 49 + df_out['Male_49'] * 49 + \
                    df_out['Female_50'] * 50 + df_out['Male_50'] * 50 + \
                    df_out['Female_51'] * 51 + df_out['Male_51'] * 51 + \
                    df_out['Female_52'] * 52 + df_out['Male_52'] * 52 + \
                    df_out['Female_53'] * 53 + df_out['Male_53'] * 53 + \
                    df_out['Female_54'] * 54 + df_out['Male_54'] * 54 + \
                    df_out['Female_55'] * 55 + df_out['Male_55'] * 55 + \
                    df_out['Female_56'] * 56 + df_out['Male_56'] * 56 + \
                    df_out['Female_57'] * 57 + df_out['Male_57'] * 57 + \
                    df_out['Female_58'] * 58 + df_out['Male_58'] * 58 + \
                    df_out['Female_59'] * 59 + df_out['Male_59'] * 59 + \
                    df_out['Female_60'] * 60 + df_out['Male_60'] * 60 + \
                    df_out['Female_61'] * 61 + df_out['Male_61'] * 61 + \
                    df_out['Female_62'] * 62 + df_out['Male_62'] * 62 + \
                    df_out['Female_63'] * 63 + df_out['Male_63'] * 63 + \
                    df_out['Female_64'] * 64 + df_out['Male_64'] * 64 + \
                    df_out['Female_65'] * 65 + df_out['Male_65'] * 65 + \
                    df_out['Female_66'] * 66 + df_out['Male_66'] * 66 + \
                    df_out['Female_67'] * 67 + df_out['Male_67'] * 67 + \
                    df_out['Female_68'] * 68 + df_out['Male_68'] * 68 + \
                    df_out['Female_69'] * 69 + df_out['Male_69'] * 69 + \
                    df_out['Female_70'] * 70 + df_out['Male_70'] * 70 + \
                    df_out['Female_71'] * 71 + df_out['Male_71'] * 71 + \
                    df_out['Female_72'] * 72 + df_out['Male_72'] * 72 + \
                    df_out['Female_73'] * 73 + df_out['Male_73'] * 73 + \
                    df_out['Female_74'] * 74 + df_out['Male_74'] * 74 + \
                    df_out['Female_75'] * 75 + df_out['Male_75'] * 75 + \
                    df_out['Female_76'] * 76 + df_out['Male_76'] * 76 + \
                    df_out['Female_77'] * 77 + df_out['Male_77'] * 77 + \
                    df_out['Female_78'] * 78 + df_out['Male_78'] * 78 + \
                    df_out['Female_79'] * 79 + df_out['Male_79'] * 79 + \
                    df_out['Female_80'] * 80 + df_out['Male_80'] * 80 + \
                    df_out['Female_81'] * 81 + df_out['Male_81'] * 81 + \
                    df_out['Female_82'] * 82 + df_out['Male_82'] * 82 + \
                    df_out['Female_83'] * 83 + df_out['Male_83'] * 83 + \
                    df_out['Female_84'] * 84 + df_out['Male_84'] * 84 + \
                    df_out['Female_85'] * 85 + df_out['Male_85'] * 85 + \
                    df_out['Female_86'] * 86 + df_out['Male_86'] * 86 + \
                    df_out['Female_87'] * 87 + df_out['Male_87'] * 87 + \
                    df_out['Female_88'] * 88 + df_out['Male_88'] * 88 + \
                    df_out['Female_89'] * 89 + df_out['Male_89'] * 89 + \
                    df_out['Female_90'] * 90 + df_out['Male_90'] * 90 + \
                    df_out['Female_91'] * 91 + df_out['Male_91'] * 91 + \
                    df_out['Female_92'] * 92 + df_out['Male_92'] * 92 + \
                    df_out['Female_93'] * 93 + df_out['Male_93'] * 93 + \
                    df_out['Female_94'] * 94 + df_out['Male_94'] * 94 + \
                    df_out['Female_95'] * 95 + df_out['Male_95'] * 95 + \
                    df_out['Female_96'] * 96 + df_out['Male_96'] * 96 + \
                    df_out['Female_97'] * 97 + df_out['Male_97'] * 97 + \
                    df_out['Female_98'] * 98 + df_out['Male_98'] * 98 + \
                    df_out['Female_99'] * 99 + df_out['Male_99'] * 99 + \
                    df_out['Female_100'] * 100 + df_out['Male_100'] * 100 
    df_out['Avg_age'] = df_out['Total_age'] / df_out['Total']

    return df_out

# build graph pop ine
def build_graph_population_ine(df, selected_age=OPTION_YES):
    list_fig = []
    # graph 1
    data = df.sort_values(by='Total', ascending=False).head(10).rename(columns={'Total_F': 'Female', 'Total_M': 'Male'})
    fig = px.bar(data,
                 x='City', 
                 y=['Total', 'Female', 'Male'])
    fig.update_layout(height=500, 
                      width=800, 
                      title_text='Top cities population', title_x=0.5, 
                      barmode='group',
                      legend_title_text='Gender')
    ###data = df.groupby('Province')[['Total', 'Total_F', 'Total_M']].sum().reset_index()
    ###data = data.sort_values(by='Total', ascending=False).head(10).rename(columns={'Total_F': 'Female', 'Total_M': 'Male'})
    ###fig = px.bar(data,
    ###             x='Province', 
    ###             y=['Total', 'Female', 'Male'])
    ###fig.update_layout(height=400, 
    ###                  width=800, 
    ###                  title_text='Top provinces population', title_x=0.5, 
    ###                  barmode='group',
    ###                  legend_title_text='Gender')    
    fig.update_xaxes(tickangle=45)
    list_fig.append(fig)
    if selected_age == OPTION_YES:
        # graph 2
        data = avg_age_population(df)
        data = data.groupby('Province')[['Avg_age']].mean().reset_index()
        fig = make_subplots(rows=1, 
                            cols=2,
                            subplot_titles=('Youngest provinces', 'Oldest provinces'))
        fig.add_trace(go.Bar(x=data.sort_values(by='Avg_age').head(5)['Province'], 
                            y=data.sort_values(by='Avg_age').head(5)['Avg_age']),
                            row=1, col=1)
        fig.add_trace(go.Bar(x=data.sort_values(by='Avg_age').tail(5)['Province'], 
                            y=data.sort_values(by='Avg_age').tail(5)['Avg_age']),
                            row=1, col=2)
        fig.update_layout(height=400, 
                        width=800, 
                        showlegend=False, 
                        title_text='Average age', title_x=0.5)
        ###data = avg_age_population(df)
        ###data = data.loc[(data['Total'] > 1000)]
        ###fig = make_subplots(rows=1, 
        ###                    cols=2,
        ###                    subplot_titles=('Youngest cities (population >1000)', 'Oldest cities (population >1000)'))
        ###fig.add_trace(go.Bar(x=data.sort_values(by='Avg_age').head(5)['City'], 
        ###                    y=data.sort_values(by='Avg_age').head(5)['Avg_age']),
        ###                    row=1, col=1)
        ###fig.add_trace(go.Bar(x=data.sort_values(by='Avg_age').tail(5)['City'], 
        ###                    y=data.sort_values(by='Avg_age').tail(5)['Avg_age']),
        ###                    row=1, col=2)
        ###fig.update_layout(height=400, 
        ###                width=800, 
        ###                showlegend=False, 
        ###                title_text='Average age', title_x=0.5)
        fig.update_yaxes(range=[0, 70]) 
        fig.update_xaxes(tickangle=45)       
        list_fig.append(fig)
        # graph 3
        data = gr_age_population(df)
        data = data.groupby('Year')[['0-18 years', '19-30 years', '31-65 years', '66-100+ years']].mean().reset_index()
        fig = px.bar(data,
             x='Year',
             y=['0-18 years', '19-30 years', '31-65 years', '66-100+ years'],
             barmode='group')
        fig.update_layout(height=350, 
                        width=300, 
                        title_text='Population distribution by age group', title_x=0.5, 
                        legend_title_text='Age groups')
        fig.update_yaxes(title='% population')
    
        list_fig.append(fig)
        
    return list_fig

# build graph income ine
def build_graph_incomes_ine(df):
    list_fig = []
    # graph 1
    data = df.loc[(df['Id_indicator'] == 'RNMP') &
                  (df['Total_pop'] > 1000)]
    fig = make_subplots(rows=1, 
                        cols=2,
                        subplot_titles=('Top cities (population >1000)', 'Bottom cities (population >1000)'))
    fig.add_trace(go.Bar(x=data.sort_values(by='Total', ascending=False).head(5)['City'], 
                         y=data.sort_values(by='Total', ascending=False).head(5)['Total']),
                         row=1, col=1)
    fig.add_trace(go.Bar(x=data.sort_values(by='Total', ascending=False).tail(5)['City'], 
                         y=data.sort_values(by='Total', ascending=False).tail(5)['Total']),
                         row=1, col=2)
    fig.update_layout(height=400, 
                      width=800, 
                      showlegend=False, 
                      title_text='Average net income per person (EUR)', title_x=0.5)
    fig.update_yaxes(range=[0, 35000])
    fig.update_xaxes(tickangle=45)
    list_fig.append(fig)
    
    # graph 2
    data = df.loc[df['Id_city'] == data.nlargest(1, 'Total').iloc[0]['Id_city']]
    fig = px.bar(data,
                 x='City', 
                 y='Total',
                 color='Name_indicator',
                 barmode='group')
    fig.update_layout(height=400, 
                      width=800, 
                      title_text='Top city (population >1000)', 
                      legend_title_text='Indicator income (EUR)')
    list_fig.append(fig)

    return list_fig

# get graph
def get_plot(type, df, selected_age=OPTION_YES):
    list_fig = []
    if df.empty:
        fig = make_subplots(rows=1, cols=1)
        list_fig.append(fig)
    else:
        if type == type_population_ine:
            list_fig = build_graph_population_ine(df, selected_age)
        elif type ==type_income_ine:
            list_fig = build_graph_incomes_ine(df)
        elif type ==type_income_aeat:
            list_fig = build_graph_incomes_aeat(df)
        else:
            fig = make_subplots(rows=1, cols=1)
            list_fig.append(fig)
    return list_fig



# get url tableau
def get_url_tableau(type):
    if type == type_income_aeat:
        url = ''
    elif type == type_income_ine:
        url = 'https://public.tableau.com/app/profile/elvira8700/viz/IncomeINE/IncomeINE'
    elif type == type_population_ine:
        url = 'https://public.tableau.com/app/profile/elvira8700/viz/populationINE/Population'
    else:
        url = ''
    return url

# get html tableau
#def get_html_tableau(type):
#    if type == type_income_ine:
#        #get content from tableau (share)
#        html_tab = """<div class='tableauPlaceholder' id='viz1666686443128' style='position: relative'><noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;In&#47;IncomesINE&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='IncomesINE&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;In&#47;IncomesINE&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1666686443128');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='420px';vizElement.style.maxWidth='650px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='887px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='420px';vizElement.style.maxWidth='650px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='887px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='877px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
#    else:
#        html_tab = ''
#    return html_tab



# Home
def play_home():
    pass

# display datatype
def write_datatype(df):
    text = ""
    for index, row in df.iterrows():
        if row['type'] == 'string':
            st.markdown(f"&emsp;🇹 ({row['type']}) {row['id']}: {row['description']}")
            #text = text + f"&emsp;🇹 {row['id']}: {row['text']}"
        if row['type'] == 'integer':
            st.markdown(f"&emsp;🔢 ({row['type']}) {row['id']}: {row['description']}")
            #text = text + f"&emsp;🔢 {row['id']}: {row['text']}"
        if row['type'] == 'float':
            st.markdown(f"&emsp;🔢 ({row['type']}) {row['id']}: {row['description']}")
            #text = text + f"&emsp;🔢 {row['id']}: {row['text']}"
        if row['type'] == 'date':
            st.markdown(f"&emsp;🗓️ ({row['type']}) {row['id']}: {row['description']}")
            #text = text + f"&emsp;D {row['id']}: {row['text']}"

# Population INE collect
def play_population_ine():
    # header
    st.header('Population in Spain')
    st.write('Get population distribution by city')
    st.markdown('Source data [Instituto Nacional de Estadística](https://www.ine.es/)')


    # options
    #min_y_p, max_y_p = get_api_population_ine_years()
    #selected_year_p = st.slider('Year: ', min_value=min_y_p, max_value=max_y_p, key='year_pop_ine')
    list_years_pop_i = get_api_population_ine_years()
    selected_year_p = st.radio('Year: ', list_years_pop_i, key='year_pop_ine', horizontal=True)
    #selected_age = st.radio('By age:', [OPTION_NO, OPTION_YES])
    #select_cities = st.selectbox('City: ', get_api_cities())
    
    # get data
    with st.spinner('Loading...'):
        df_pop, metadata_pop = get_api_population_ine(selected_year_p)
        
        f_csv = export_to_csv(df_pop, ENCODE)

        # download
        st.download_button(
            label="Download data as CSV",
            data=f_csv,
            file_name=f'population_INE_{selected_year_p}.csv',
            mime='text/csv'
        )

        # description of data
        st.subheader('Data description')
        st.write(f'Number of rows: ', len(df_pop))
        st.write(f'Number of columns: ', len(df_pop.columns))
        write_datatype(metadata_pop)
        #st.markdown(text_datatype)

        # data sample
        st.subheader('Data sample')
        st.write('First 5 rows')
        st.write(df_pop.head(5))

        # dashboard
        st.subheader('Data overview')
        # plot
        plots_pop = get_plot(type_population_ine, df_pop)
        for gr_pop in plots_pop:
            st.plotly_chart(gr_pop, use_container_width=True)
        # url tableau
        url_tab_p = get_url_tableau(type_population_ine)
        st.write(f'For more visualizations, you can view the [Tableau Dashboard]({url_tab_p})')
        # component tableau
        #html_tab_p = get_html_tableau(type_population_ine)
        #components.html(html_tab_p)


# Income INE collect
def play_income_ine():
    # header
    st.header('Income in Spain')
    st.write('Get income distribution by city')
    st.markdown('Source data [Instituto Nacional de Estadística](https://www.ine.es/)')
    
    # options
    #min_y_i, max_y_i = get_api_incomes_ine_years()
    #selected_year_i = st.slider('Year: ', min_value=min_y_i, max_value=max_y_i, key='year_incomes_ine')
    list_years_in_i = get_api_incomes_ine_years()
    selected_year_i = st.radio('Year: ', list_years_in_i, key='year_in_ine', horizontal=True)
    
    # get data
    with st.spinner('Loading...'):
        df_incomes_ine, metadata_incomes_ine = get_api_incomes_ine(selected_year_i)

        f_csv = export_to_csv(df_incomes_ine, ENCODE)

        # download
        st.download_button(
            label="Download data as CSV",
            data=f_csv,
            file_name=f'incomes_INE_{selected_year_i}.csv',
            mime='text/csv'
        )

        # datatype
        st.subheader('Data description')
        st.write(f'Number of rows: ', len(df_incomes_ine))
        st.write(f'Number of columns: ', len(df_incomes_ine.columns))
        write_datatype(metadata_incomes_ine)
        #st.markdown(text_datatype)

        # data
        st.subheader('Data sample')
        st.write('First 5 rows')
        st.write(df_incomes_ine.head(5))

        # dashboard
        st.subheader('Data overview')
        # plot
        plots_in_i = get_plot(type_income_ine, df_incomes_ine)
        for gr_in_i in plots_in_i:
            st.plotly_chart(gr_in_i, use_container_width=True)
        # url tableau
        url_tab_i = get_url_tableau(type_income_ine)
        st.write(f'For more visualizations, you can view the [Tableau Dashboard]({url_tab_i})')
        # component tableau
        #html_tab_i = get_html_tableau(type_income_ine)
        #components.html(html_tab_i)
    
# Income AEAT collect
def play_income_aeat():
    # header
    st.header('Income in Spain')
    st.write('Get income distribution by city')
    st.markdown('Source data [Agencia Estatal de Administración Tributaria](https://sede.agenciatributaria.gob.es/)')

    # options
    #min_y_i_aeat, max_y_i_aeat = get_api_incomes_aeat_years()
    #selected_year_i_aeat = st.slider('Year: ', min_value=min_y_i_aeat, max_value=max_y_i_aeat, key='year_incomes_aeat')
    list_years_in_aeat = get_api_incomes_aeat_years()
    selected_year_i_aeat = st.radio('Year: ', list_years_in_aeat, key='year_in_aeat', horizontal=True)
    
    # get data
    with st.spinner('Loading...'):
        df_incomes_aeat, metadata_incomes_aeat = get_api_incomes_aeat(selected_year_i_aeat)

        f_csv = export_to_csv(df_incomes_aeat, ENCODE)

        # download
        st.download_button(
            label="Download data as CSV",
            data=f_csv,
            file_name=f'incomes_AEAT_{selected_year_i_aeat}.csv',
            mime='text/csv'
        )

        # datatype
        st.subheader('Data description')
        st.write(f'Number of rows: ', len(df_incomes_aeat))
        st.write(f'Number of columns: ', len(df_incomes_aeat.columns))
        write_datatype(metadata_incomes_aeat)
        #st.markdown(text_datatype)

        # data
        st.subheader('Data sample')
        st.write('First 5 rows')
        st.write(df_incomes_aeat.head(5))

        # dashboard
        st.subheader('Data overview')
        # plot
        plots_in_a = get_plot(type_income_aeat, df_incomes_aeat)
        for gr_in_a in plots_in_a:
            st.plotly_chart(gr_in_a, use_container_width=True)
        # url tableau
        url_tab_ia = get_url_tableau(type_income_aeat)
        st.write(f'For more visualizations, you can view the [Tableau Dashboard]({url_tab_ia})')
        # component tableau
        #html_tab_ia = get_html_tableau(type_income_aeat)
        #components.html(html_tab_ia)



# page config
st.set_page_config(
    page_title='collect'#,
    #page_icon='',
    #layout="wide"
)



# page
st.image(Image.open(ICON_PATH), width=60)
st.title('Collects')
st.text('Datasets ready for use!')
st.text('')



tab_pop_ine, tab_income_ine, tab_income_aeat = st.tabs(['Population INE', 'Income INE', 'Income AEAT'])

with tab_pop_ine:
   play_population_ine()

with tab_income_ine:
   play_income_ine()

with tab_income_aeat:
   play_income_aeat()
