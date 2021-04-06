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
    '''
    compute the pearson similarity given two user's attributes
    input: two users' feature vectors
    return: pearson similarity of the two users
    '''
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
    '''
    generate a list of pearson similarity between a given user and all the other existing users
    input: vector: feature for the given user
           user_item_list: features for all the other existing users
    return: list of pearson similarity
    '''
    sim_list = []
    for user_profile in user_item_list:
        pearson_sim = get_similarity(vector,user_profile)
        sim_list.append(pearson_sim)
    return sim_list

def get_user_feature_matrix(userid):
    '''
    generate user feature matrix containing user's rating for POI and user's profile
    return: dataframe for users' profile and user feature matrix
    '''
    engine = db_init()
    postgreSQL_select_Query = 'select * from review'
    review_df = sqlio.read_sql_query(postgreSQL_select_Query, engine)
    postgreSQL_select_Query = 'select * from user_profile'
    profile_df = sqlio.read_sql_query(postgreSQL_select_Query, engine)
    # profile_df = pd.read_excel('user_profile.xlsx')
    # exclude the user with missing values for preference, pace and foodie
    profile_df = profile_df[~profile_df.isnull().any(axis=1)]
    # convert review_df to pivot table
    user_item = pd.pivot_table(review_df, values='rating', index=['userid'],columns=['uuid'])
    # convert occupation and nationality to one hot
    profile_df['occupation'] = 'occ_'+profile_df['occupation']
    profile_df['nationality'] = 'nation_'+profile_df['nationality']
    occupation_df = pd.get_dummies(profile_df.occupation)
    nation_df = pd.get_dummies(profile_df.nationality)
    profile_onehot = pd.concat([occupation_df,nation_df],axis=1)
    profile_onehot['age'] = profile_df['age']
    profile_onehot['userid'] = profile_df['userid']
    profile_onehot = profile_onehot.set_index('userid')
    # combine users' rating history and profile information
    user_item = user_item.join(profile_onehot)
    user_item['age'] = (user_item['age']-user_item['age'].mean())/user_item['age'].std()
    return profile_df,user_item

def get_recommendation(userid,start_loc,time_stay,start_time):
    '''
    return a list of recommended POIs and the parameters for optimization based on the users' input
    input: userid: id for the user to get recommendation
           start_loc: starting point of tour
           time_stay: total time to stay/travel in Singapore
           start_time: start time of trip
    return: dictionary of containing recommended POIs and the parameters for optimization
    '''
    profile_df, user_item = get_user_feature_matrix(userid)
    # feature for user to get recommendation
    current_user_feature = user_item.loc[userid].tolist()
    # exclude the current user from the user item matrix
    user_item = user_item.loc[[i for i in user_item.index if i!=userid]]
    user_item_list = user_item.values.tolist()
    # get pearson similarity between the user and others
    sim_list = get_sim_list(current_user_feature,user_item_list)
    user_item['similarity'] = sim_list
    # get top 50 similar users
    similar_users = user_item.sort_values('similarity',ascending=False).head(50)
    similar_users = similar_users.dropna(axis=1,how='all')
    similar_users = similar_users.dropna(axis=1,how='all')
    # generate recommendation for POI based on predicted rating
    candidate_poi = [i for i in similar_users.columns if i.startswith('002')]
    poi_rating = {}
    for poi in candidate_poi:
        current_poi_df = similar_users[[poi,'similarity']].dropna()
        current_rating = (current_poi_df[poi]*current_poi_df['similarity']).sum()/current_poi_df['similarity'].sum()
        poi_rating[poi] = current_rating
    recommended_places = [(k, v) for k, v in sorted(poi_rating.items(), key=lambda item: -item[1])]
    # return the 10 recommended places with highest predict rating
    if len(recommended_places)>10:
        recommended_places = recommended_places[:10]
        recommended_places = [i[0] for i in recommended_places]
    else:
        recommended_places = [i[0] for i in recommended_places]
    engine = db_init()
    postgreSQL_select_Query = 'select * from attraction'
    attraction_df = sqlio.read_sql_query(postgreSQL_select_Query, engine)
    recommended_df = attraction_df[attraction_df['uuid'].isin(recommended_places)]
    recommended_df = recommended_df[['name','latitude','longitude','type','description']]
    poi_info = recommended_df.to_dict('records')
    # infer user's POI preference, travel pace and foodie based on the similar users
    similar_user_id = similar_users.index
    similar_user_profile = profile_df[profile_df['userid'].isin(similar_user_id)]
    POI_preference1 = similar_user_profile['poi_preference1'].mode()[0]
    POI_preference2 = similar_user_profile[similar_user_profile['poi_preference1']!=POI_preference1]['poi_preference2'].mode()[0]
    travel_pace = similar_user_profile['pace'].mode()[0]
    foodie = similar_user_profile['foodie'].mode()[0]
    optimization_dict = {'start_loc': start_loc,
                         'time_stay': time_stay,
                         'start_time': start_time,
                         'poi_preference': [POI_preference1,POI_preference2],
                         'travel_pace': travel_pace,
                         'foodie': foodie,
                         'poi_list': poi_info}
    return optimization_dict

def demo_recommendation(userid,start_loc,time_stay,start_time):
    demo_df = pd.read_excel('demo_attraction.xlsx')
    poi_list = demo_df.poi_name.to_list()
    poi_preference = ['park','mall']
    travel_pace = 'leisure'
    foodie = 'leisure'
    optimization_dict = {'start_loc': start_loc,
                         'time_stay': time_stay,
                         'start_time': start_time,
                         'poi_preference':poi_preference,
                         'travel_pace': travel_pace,
                         'foodie': foodie,
                         'poi_list':poi_list}
    return optimization_dict

# initialise app
app=Flask(__name__)

@app.route("/recommendation",methods=['GET','POST'])
def recommend():
    location_list = get_recommendation(1)
    j_file = json.dumps(location_list.to_dict('records'))
    return j_file

@app.route("/")
def home():
    return "<h1>Hello World</h1>"

# # entrance
# if __name__=='__main__':
#     app.run(host='0.0.0.0',port=5001)

# if __name__=='__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    location_list = get_recommendation(1,1,1,1)
    print(location_list)
    # optimization_dict = demo_recommendation(1,'COM3, NUS',8,'2021-4-10')
    # with open('location_list.json','w') as f:
    #     json.dump(optimization_dict,f)