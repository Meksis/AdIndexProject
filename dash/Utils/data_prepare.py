import pandas as pd

def publication(df):
    cl_df = df[['Ссылка','Автор','Читатели','Глубина просмотра']]
    cl_df['трафик с ТГ']= 0
    cl_df['трафик с ВК']= 0
    cl_df['трафик с home']= 0
    
    return cl_df