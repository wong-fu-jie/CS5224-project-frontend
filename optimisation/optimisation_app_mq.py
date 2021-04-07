import psycopg2
import pandas.io.sql as sqlio
import folium
import pandas as pd
import numpy as np
import json
from itertools import combinations, permutations
import requests
from datetime import datetime, timedelta
from python_tsp.exact import solve_tsp_dynamic_programming
import geojson
from geojson import Feature, FeatureCollection, MultiLineString
from flask import Flask, request, render_template

import pika

def db_init(poi_list):
    engine = psycopg2.connect(
    database="demo_1",
    user="postgres",
    password="Huxjoffer2021!",
    host="database-1-test.ctpfk8jpyqbl.us-east-1.rds.amazonaws.com",
    port='5432')
    postgreSQL_select_Query = ''
    for i in range(len(poi_list)):
        if i == 0:
            postgreSQL_select_Query += "select * from poi where poi_name='" + \
                poi_list[i]+"'"
        else:
            postgreSQL_select_Query += "union all select * from poi where poi_name='" + \
                poi_list[i]+"'"
    df = sqlio.read_sql_query(postgreSQL_select_Query, engine)
    df.drop(columns=['id'], inplace=True)
    return df


def map_db_init():
    engine = psycopg2.connect(
    database="database_map",
    user="postgres",
    password="Huxjoffer2021!",
    host="database-map.ctpfk8jpyqbl.us-east-1.rds.amazonaws.com",
    port='5432')
    return engine


def greedy(poi_list, mydf, avail_time):
    candidate_num = len(poi_list)
    final_poi_list = None
    for i in range(candidate_num, 0, -1):
        comb = combinations(poi_list, i)
        comb_list = list(comb)
        for j in comb_list:
            time_thres = 0
            for k in range(i):
                time_thres += mydf.loc[(mydf['poi_name']
                                        == j[k]), ['time']].values[0][0]
                if time_thres > avail_time:
                    break
            if time_thres <= avail_time:
                return j

# for each place combination, query onemap


def construct_matrix(combination_list, mydf):
    distance_matrix = np.zeros((len(mydf), len(mydf)))
    iti_matrix = np.empty((len(mydf), len(mydf)), dtype='object')

    for i in combination_list:
        start = str(mydf.loc[(mydf['poi_name'] == i[0]), ['latitude']].values[0][0]) + \
                    ','+str(mydf.loc[(mydf['poi_name'] == i[0]),
                            ['longitude']].values[0][0])
        end = str(mydf.loc[(mydf['poi_name'] == i[1]), ['latitude']].values[0][0]) + \
                  ','+str(mydf.loc[(mydf['poi_name'] == i[1]),
                          ['longitude']].values[0][0])

        duration_list = []
        min_dur = 1000000
        response_list = []
        num_iti = []
        selected_iti = None

        om_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjcyMjIsInVzZXJfaWQiOjcyMjIsImVtYWlsIjoiZTA1NTQwNTZAdS5udXMuZWR1IiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Imh0dHA6XC9cL29tMi5kZmUub25lbWFwLnNnXC9hcGlcL3YyXC91c2VyXC9zZXNzaW9uIiwiaWF0IjoxNjE3MzU0OTEyLCJleHAiOjE2MTc3ODY5MTIsIm5iZiI6MTYxNzM1NDkxMiwianRpIjoiNjNlYWQ5NTliZTk1NTQ3OTMyMTFlYzE4N2QyNWRjYmEifQ.aIKS_YiyD6BG-YMigniabKU7PyYoBKfab_TN1FsqD-0'
        routeType = 'pt'
        mode = ['TRANSIT', 'BUS']
        head = 'https://developers.onemap.sg/privateapi/routingsvc/route?'
        dt = datetime.now().strftime("%Y-%m-%d")
        tm = datetime.now().strftime('%H:%M:%S')

        for j in mode:  # each mode
            url = head+'start='+start+'&end='+end+'&routeType='+routeType+'&token=' + \
                om_token+'&date='+str(dt)+'&time='+str(tm) + \
                                      '&mode='+j+'&numItineraries='+str(3)
            temp_rp = requests.get(url=url)
            # how to handle bad request? (500, 504 etc.) One way is to slightly change the coordinates of the location
            temp_response_json = temp_rp.json()
            response_list.append(temp_response_json)

            # ranges from 1 to 3
            temp_num_iti = len(temp_response_json['plan']['itineraries'])
            num_iti.append(temp_num_iti)
            for k in range(temp_num_iti):  # each possible itinerary
                temp_dur = temp_response_json['plan']['itineraries'][k]['duration']
                duration_list.append(temp_dur)
                min_dur = min(min_dur, temp_dur)
        best_dur_index = duration_list.index(min_dur)  # ranges from 0 to 5
        if best_dur_index <= num_iti[0]-1:  # belongs to transit
            selected_iti = response_list[0]['plan']['itineraries'][best_dur_index]
        else:  # belongs to bus
            selected_iti = response_list[1]['plan']['itineraries'][best_dur_index-num_iti[0]]

        # min_dur write into matrix
        x = mydf.loc[(mydf['poi_name'] == i[0])].index.values[0]
        y = mydf.loc[(mydf['poi_name'] == i[1])].index.values[0]
        distance_matrix[x][y] = min_dur
        distance_matrix[y][x] = min_dur
        iti_matrix[x][y] = selected_iti
        iti_matrix[y][x] = selected_iti
    return distance_matrix, iti_matrix

# find shortest path


def shortest_path(distance_matrix):
    distance_matrix[:, 0] = 0
    permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
    return permutation, distance


def visualisation(permutation, iti_matrix, mydf,j_piece):
    j_list = []
    # draw folium graph
    str_fea_list = []
    tooltip = 'Click For More Info'
    des_dict = {'WALK': 'Walk to ',
        'SUBWAY': 'Take subway to ', 'BUS': 'Take bus to '}
    m = folium.Map(location=[1.2791, 103.8154], zoom_start=12)
    for i in range(len(permutation)-1):  # for one itinerary
        sta_plc_idx = permutation[i]
        end_plc_idx = permutation[i+1]
        itinerary = iti_matrix[sta_plc_idx][end_plc_idx]

        true_sta_pt = np.array((mydf._get_value(
            sta_plc_idx, 'latitude'), mydf._get_value(sta_plc_idx, 'longitude')))
        true_end_pt = np.array((mydf._get_value(
            end_plc_idx, 'latitude'), mydf._get_value(end_plc_idx, 'longitude')))

        temp_num_legs = len(itinerary['legs'])  # num of legs
        pt_lat = []
        pt_lon = []
        tpl_list = []
        pt_name = []
        mode_list = []
        dist_list = []
        for k in range(temp_num_legs):  # for each leg
            pt_lon.append(itinerary['legs'][k]['from']['lon'])
            pt_lat.append(itinerary['legs'][k]['from']['lat'])
            tpl_list.append(
                (itinerary['legs'][k]['from']['lon'], itinerary['legs'][k]['from']['lat']))
            pt_name.append(itinerary['legs'][k]['to']['name'])
            mode_list.append(des_dict[itinerary['legs'][k]['mode']])
            dist_list.append(
                str(round(float(itinerary['legs'][k]['distance'])/1000, 2))+' km.')
            if k == temp_num_legs-1:
                pt_lon.append(itinerary['legs'][k]['to']['lon'])
                pt_lat.append(itinerary['legs'][k]['to']['lat'])
                tpl_list.append(
                    (itinerary['legs'][k]['to']['lon'], itinerary['legs'][k]['to']['lat']))
        temp_feature = Feature(geometry=MultiLineString(
            [tpl_list]), properties={'stroke': '#AF4646'})
        str_fea_list.append(temp_feature)
        first_point = np.array((pt_lat[0], pt_lon[0]))

        distance1 = np.linalg.norm(first_point-true_sta_pt)
        distance2 = np.linalg.norm(first_point-true_end_pt)

        start_point = [pt_lat[0], pt_lon[0]]
        end_point = [pt_lat[-1], pt_lon[-1]]
        iterator = range(len(mode_list))
        # only affect formatting the text
        string = ''
        if distance1 > distance2:
            iterator = range(len(mode_list)-1, -1, -1)
            start_point = [pt_lat[-1], pt_lon[-1]]
            end_point = [pt_lat[0], pt_lon[0]]
        counter = 0
        for j in iterator:
            string += str(counter+1)+'. ' + \
                          mode_list[j]+pt_name[j] + \
                              '. Estimated distance is '+dist_list[j]+'\n'
            counter += 1

        folium.Marker(start_point,
                  popup='<strong>'+string+'</strong>',
                  tooltip=tooltip,
                  icon=folium.Icon(icon='trophy' if i != 0 else 'flag')).add_to(m),
        folium.Marker(end_point, icon=folium.Icon(
            icon='trophy' if i != len(permutation)-2 else 'star')).add_to(m)

        temp_j_ele = {}
        temp_j_ele['order'] = i+1
        temp_j_ele['poi_name'] = mydf._get_value(end_plc_idx, 'poi_name')
        temp_j_ele['time_to_spend'] = mydf._get_value(end_plc_idx, 'time')
        temp_j_ele['time_to_travelhere'] = str(
            timedelta(seconds=int(itinerary['duration'])))
        temp_j_ele['description'] = mydf._get_value(end_plc_idx, 'description')
        j_list.append(temp_j_ele)

    j = {'basics': j_piece,'itinerary': j_list}
    j_file = json.dumps(j)

    feature_collection = FeatureCollection(str_fea_list)
    ms = geojson.dumps(feature_collection)
    folium.GeoJson(ms, name='multistring').add_to(m)

    # Generate map
    render_m = m.get_root().render()

    # insert value into map_database
    map_engine = map_db_init()
    insert_req = "INSERT INTO map_db (id,map_html) VALUES (default," + \
                                      "'"+render_m+"')"
    cursor = map_engine.cursor()
    cursor.execute(insert_req)
    map_engine.commit()

    return j_file


# initialise app
app = Flask(__name__)


@app.route("/optimisation", methods=['GET', 'POST'])
def optimisation(rec_output_dict):
    # poi_list=['COM1, NUS','Hort Park','Telok Blangah Market','Mount Faber Park','Chinatown','Chinatown Complex Food Centre',
    #      'National Museum', 'Wild Wild Wet', 'Jewel Changi Airport Manulife Sky Nets - Walking', 'Jewel Changi Airport Canopy Park',
    #     'Pulau Ubin and Chek Jawa']
    # avail_time=8

    # # to chun han: rec_output is the input of this module
    # with open(r'C:\Users\I544708\Desktop\CC\project\location_list.json') as f:
    #     rec_output_dict = json.load(f)

    avail_time=int(rec_output_dict['time_stay'])
    poi_seg=rec_output_dict.popitem()
    poi_list=poi_seg[1]
    mydf2=db_init(poi_list)
    final_poi_list=list(greedy(poi_list[1:],mydf2,avail_time))
    final_poi_list.insert(0,poi_list[0])
    # this function: input: list of coordinate of each POI, return matrix
    comb = combinations(final_poi_list, 2)  
    comb_list=list(comb)
    mydf=db_init(final_poi_list)
    distance_matrix,iti_matrix=construct_matrix(comb_list,mydf)
    permutation,distance=shortest_path(distance_matrix)
    j_file=visualisation(permutation,iti_matrix,mydf,rec_output_dict)
    return j_file

@app.route("/map",methods=['GET','POST'])
def map():
    map_engine=map_db_init()
    postgreSQL_select_Query = "select map_html from map_db order by id desc limit 1"
    cursor = map_engine.cursor()
    cursor.execute(postgreSQL_select_Query)
    html = cursor.fetchall()
    return html[0][0]

@app.route("/")
def home():
    return "<h1>Hello World</h1>"

def on_request(ch, method, props, body):

    msg = eval(body.decode())

    # print(" [.] fib(%s)" % n)
    response = optimisation(msg)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

# entrance
if __name__=='__main__':
    # app.run(host='0.0.0.0',port=8080)

    parameters = pika.URLParameters('amqps://Administrator:administrator12345@b-92f0f3f3-0fa2-4e56-b884-b2bce26b0222.mq.us-east-1.amazonaws.com:5671/%2f')
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue='optimisation_recommendation')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='optimisation_recommendation', on_message_callback=on_request)

    print(" [x] Awaiting RPC requests")
    channel.start_consuming()  

    app.run(debug=True)


    # host='0.0.0.0',port=8080