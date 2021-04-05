import numpy as np
from flask import Flask
import json
import psycopg2
import pandas.io.sql as sqlio
import pandas as pd

def db_init():
    engine = psycopg2.connect(
    database="demo_1",
    user="postgres",
    password="Huxjoffer2021!",
    host="database-1-test.ctpfk8jpyqbl.us-east-1.rds.amazonaws.com",
    port='5432')
    return engine


def get_similarity(vector1, vector2):
    avg1 = np.nanmean(vector1)
    avg2 = np.nanmean(vector2)
    sqrt1 = np.sqrt(np.nansum((vector1-avg1)**2))
    sqrt2 = np.sqrt(np.nansum((vector2-avg2)**2))
    common_index = [i[0] for i in np.argwhere((~np.isnan(vector1)) & (~np.isnan(vector2)))]
    common_value1 = np.array(vector1)[common_index]
    common_value2 = np.array(vector2)[common_index]
    cov = np.sum([(i-avg1)*(j-avg2) for (i,j) in zip(common_value1,common_value2)])
    pearson_sim = cov/(sqrt1*sqrt2)
    return pearson_sim

def get_sim_list(vector,user_item_list):
    sim_list = []
    for user_profile in user_item_list:
        pearson_sim = get_similarity(vector,user_profile)
        sim_list.append(pearson_sim)
    return sim_list

def get_user_feature_matrix(userid):
    engine = db_init()
    postgreSQL_select_Query = 'select * from review'
    review_df = sqlio.read_sql_query(postgreSQL_select_Query, engine)
    postgreSQL_select_Query = 'select * from user_profile'
    profile_df = sqlio.read_sql_query(postgreSQL_select_Query, engine)
    user_item = pd.pivot_table(review_df, values='rating', index=['userid'],columns=['uuid'])
    profile_df['occupation'] = 'occ_'+profile_df['occupation']
    profile_df['nationality'] = 'nation_'+profile_df['nationality']
    occupation_df = pd.get_dummies(profile_df.occupation)
    nation_df = pd.get_dummies(profile_df.nationality)
    profile_onehot = pd.concat([occupation_df,nation_df],axis=1)
    profile_onehot['age'] = profile_df['age']
    profile_onehot['userid'] = profile_df['userid']
    profile_onehot = profile_onehot.set_index('userid')
    user_item = user_item.join(profile_onehot)
    user_item['age'] = (user_item['age']-user_item['age'].mean())/user_item['age'].std()
    return user_item

def get_recommendation(userid):
    user_item = get_user_feature_matrix(userid)
    current_user_feature = user_item.loc[userid].tolist()
    user_item = user_item.loc[[i for i in user_item.index if i!=userid]]
    user_item_list = user_item.values.tolist()
    sim_list = get_sim_list(current_user_feature,user_item_list)
    user_item['similarity'] = sim_list
    similar_users = user_item.sort_values('similarity',ascending=False).head(50)
    similar_users = similar_users.dropna(axis=1,how='all')
    candidate_movies = [i for i in similar_users.columns if i.startswith('002')]
    movie_rating = {}
    for movie in candidate_movies:
        current_movie_df = similar_users[[movie,'similarity']].dropna()
        current_rating = (current_movie_df[movie]*current_movie_df['similarity']).sum()/current_movie_df['similarity'].sum()
        movie_rating[movie] = current_rating
    recommended_places = [(k, v) for k, v in sorted(movie_rating.items(), key=lambda item: -item[1])]
    if len(recommended_places)>6:
        recommended_places = recommended_places[:6]
        recommended_places = [i[0] for i in recommended_places]
    else:
        recommended_places = [i[0] for i in recommended_places]
    engine = db_init()
    postgreSQL_select_Query = 'select * from attraction'
    attraction_df = sqlio.read_sql_query(postgreSQL_select_Query, engine)
    recommended_df = pd.DataFrame()
    for place in recommended_places:
        current_df = attraction_df[attraction_df['uuid']==place]
        recommended_df = recommended_df.append(current_df)
    recommended_df['rank'] = np.arange(len(recommended_df))
    recommended_df['pace'] = pd.cut(recommended_df['rank'],3,labels=[1.5,1,0.75])
    recommended_df['pace'] = recommended_df['pace'].astype(float)
    recommended_df['recommended time stay (h)'] = recommended_df['avg_stay_time']*recommended_df['pace']
    recommended_df = recommended_df[['name','description','recommended time stay (h)']]
    return recommended_df

# initialise app
app=Flask(__name__)

@app.route("/recommendation",methods=['GET','POST'])
def recommend():
    location_list = get_recommendation(1)
    j_file = json.dumps(location_list.to_dict())
    return j_file

@app.route("/")
def home():
    return "<h1>Hello World</h1>"

# entrance
if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)

# if __name__=='__main__':
#     app.run(debug=True)

# if __name__ == '__main__':
#     location_list = get_recommendation(1)
#     print(location_list)