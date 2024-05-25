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

        # print(grouped_teg)

        return grouped_teg

    def top_authors_df(self, df):
        grouped_author = df.groupby('Автор').agg(
        total_readers=pd.NamedAgg(column='Читатели', aggfunc='sum'),
        total_posts=pd.NamedAgg(column='post_tag', aggfunc='count'),
        avg_depth=pd.NamedAgg(column='Глубина просмотра', aggfunc='mean'),
        best_topic=pd.NamedAgg(column='post_tag', aggfunc=lambda x: df.loc[x.index, 'Читатели'].idxmax())).reset_index()
        grouped_author['best_topic'] = grouped_author['best_topic'].apply(lambda x: df.loc[x, 'post_tag'])

        # print(grouped_author.columns)

        grouped_author.columns = ['Автор', 'Количество просмотров', 'Количество статей', 'Глубина', 'Лучшая тема (По просмотрам)']

        # print(grouped_author)

        return(grouped_author.sort_values(by='Количество просмотров', ascending=False))

    def bar_data(self, df, head):
        df = df.sort_values(by='Читатели', ascending=False)
        return df.iloc[:head]
    

class Theme:

    def f(self, df):
        df_filtered = df
        return df_filtered.value_counts().idxmax()

    def page_df(self, df):
        grouped_teg = df.groupby('post_tag').agg(
            Читатели=pd.NamedAgg(column='Читатели', aggfunc='sum'),
            кол_во_статей=pd.NamedAgg(column='post_id', aggfunc='count'),
            лучший_автор=pd.NamedAgg(column='Автор', aggfunc=self.f),
            
            )
        grouped_teg['Тема'] = grouped_teg.index
        grouped_teg = grouped_teg[['Тема','Читатели','кол_во_статей','лучший_автор']]

        # print(grouped_teg)

        return grouped_teg


    def bar_data(self, df, head=-1):
        df = df.sort_values(by='Читатели', ascending=False)
        return df.iloc[:head]