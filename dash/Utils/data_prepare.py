import pandas as pd

class Publication:

    def page_df(self, df):
        cl_df = df[['post_id','Ссылка','Автор','date','Читатели','Глубина просмотра']]
        df['post_id'] = df['post_id'].astype(str)
        cl_df['трафик с ТГ']= 0
        cl_df['трафик с ВК']= 0
        cl_df['трафик с home']= 0
        
        return cl_df
    
    def bar_data(self, df, head):
        df = df.sort_values(by='Читатели', ascending=False)
        return df.head(head)
       