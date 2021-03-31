import pandas as pd
import numpy as np

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
    review_df = pd.read_excel('review.xlsx')
    profile_df = pd.read_excel('user_profile.xlsx')
    user_item = pd.pivot_table(review_df, values='rating', index=['UserID'],columns=['uuid'])
    profile_df['occupation'] = 'occ_'+profile_df['occupation']
    profile_df['nationality'] = 'nation_'+profile_df['nationality']
    occupation_df = pd.get_dummies(profile_df.occupation)
    nation_df = pd.get_dummies(profile_df.nationality)
    profile_onehot = pd.concat([occupation_df,nation_df],axis=1)
    profile_onehot['age'] = profile_df['age']
    profile_onehot['UserID'] = profile_df['UserID']
    profile_onehot = profile_onehot.set_index('UserID')
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
    if len(recommended_places)>10:
        recommended_places = recommended_places[:10]
        recommended_places = [i[0] for i in recommended_places]
    else:
        recommended_places = [i[0] for i in recommended_places]
    attraction_df = pd.read_csv('attraction.csv')
    recommended_places_info = attraction_df[attraction_df['uuid'].isin(recommended_places)][['name','latitude','latitude']]
    return recommended_places_info

if __name__ == '__main__':
    location_list = get_recommendation(1)
    print(location_list)