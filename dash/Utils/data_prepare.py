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
       
class Author:
    
    def f(self, df):
        df_filtered = df
        return df_filtered.value_counts().idxmax()
    
    def page_df(self, df):
        grouped_teg = df.groupby('Автор').agg(
            Читателей=pd.NamedAgg(column='Читатели', aggfunc='sum'),
            кол_во_статей=pd.NamedAgg(column='post_id', aggfunc='count'),
            лучшая_тема=pd.NamedAgg(column='post_tag', aggfunc=self.f)
            
            )
        grouped_teg['Автор'] = grouped_teg.index
        grouped_teg = grouped_teg[['Автор','Читателей','кол_во_статей','лучшая_тема']]
        
        return grouped_teg
    
    def bar_data(self, df, head):
        df = df.sort_values(by='Читатели', ascending=False)
        return df.head(head)