import pandas as pd
import altair as alt

def pop_and_delta(country):
    
    flatten = lambda l: [item for sublist in l for item in sublist] # itertools.chain is better. 
    
    src_pop = "../data/base_pops/API_SP.POP.TOTL_DS2_en_csv_v2_10224786.csv"
    src_delta = "../data/delta_pops/API_SP.POP.GROW_DS2_en_csv_v2_10182032.csv"
    
    columns_to_drop = ['Country Code', 'Indicator Name', 'Indicator Code']
    column_names = ['year', 'pop', 'delta_pop']
    
    df_pop = pd.read_csv(src_pop, header=2).drop(columns=columns_to_drop)
    df_delta = pd.read_csv(src_delta, header=2).drop(columns=columns_to_drop)
    
    df_pop.rename(columns={'Country Name': 'country'}, inplace=True)
    df_delta.rename(columns={'Country Name': 'country'}, inplace=True)
    
    country_pop =  df_pop[df_pop['country']==country].T
    country_delta =  df_delta[df_delta['country']==country].T
    
    years = pd.DataFrame(country_pop.iloc[1:]).index.values
    
    country_pop = flatten(pd.DataFrame(country_pop.iloc[1:]).values)
    country_delta = flatten(pd.DataFrame(country_delta.iloc[1:]).values)
    
    # country_delta.map(lambda x: x * 0.01, inplace=True)
    country_delta = [x * 0.01 for x in country_delta]
    # print(country_delta.values)
    
    country_df = pd.DataFrame({column_names[0]: years, 
                              column_names[1]: country_pop, 
                              column_names[2]: country_delta})
    
    return country_df

def show_pop_w_delta(country_df):
    '''take a dataframe and return two charts, vconcat'd. 
    
    TODO: make sure its renderer is right for http with django, add call to .serve() somewhere. 
    '''
    w=800 # width
    
    interval = alt.selection_interval(encodings=['x'])
    column_names = ['year', 'pop', 'delta_pop']
    
    chart_pop = alt.Chart(country_df, width=w).mark_bar(color='orange').encode(
        #x=alt.X('pop',  scale=alt.Scale(domain=(country_df[column_names[1]].min(), country_df[column_names[1]].max()))),
        x=alt.X('pop',  scale=alt.Scale(domain=(0, country_df[column_names[1]].max()))),
        y=alt.Y('year', axis=alt.Axis(title='Year')),
        #y='year'
        tooltip='delta_pop'
        ).transform_filter(
            interval
        )
        
    chart_delta = alt.Chart(country_df, width=w).mark_line(color='purple').encode(
        x=alt.X('year', axis=alt.Axis(title='Year')),
        y=alt.Y('delta_pop', axis=alt.Axis(format='%', title='Change in Population'))
        # y='delta_pop'
        # tooltip='pop'
        ).properties(
            selection=interval
        )
    
    return chart_delta & chart_pop
