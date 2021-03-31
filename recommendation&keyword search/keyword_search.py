import pandas as pd

'''
sample record from front-end:
{
'keywords': 'orchard'
'min_rating': 4/None
'max_price': 20/None
}
'''

def compare_rating(x,min_rating):
    try:
        is_larger_min_rating = (float(x)>min_rating)
    except Exception as e:
        is_larger_min_rating = False
    return is_larger_min_rating

def filter_attraction(attraction_df, max_price, min_rating):
    if max_price:
        attraction_df = attraction_df[(attraction_df['max_price']<2) | (attraction_df['max_price'].isnull())]

    if min_rating:
        attraction_df = attraction_df[attraction_df['rating'].apply(lambda x: compare_rating(x,min_rating))]

    return attraction_df

def search_by_keywords(keywords, max_price, min_rating):
    keywords = keywords.lower()
    attraction_df = pd.read_csv('attraction.csv')
    attraction_df = filter_attraction(attraction_df, max_price, min_rating)
    attraction_to_return = attraction_df[attraction_df['name'].str.lower().str.contains(keywords)]
    attraction_to_return = attraction_to_return[['name','rating','address','pricing']]
    return attraction_to_return

if __name__ == '__main__':
    max_price = 20
    min_rating = 4
    keywords = 'Gallery'
    attraction_to_return = search_by_keywords(keywords,max_price,min_rating)
    print(attraction_to_return)