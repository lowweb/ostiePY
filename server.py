from flask import Flask, request
from  get_imdb_nm_films import get_media_info
from flask_cors import CORS
from db_request import sql_request

app = Flask (__name__)
CORS(app)
app.debug = True



# @app.route('/')
# def main_view():
#     return "Yep"
#

@app.route("/search")
def messages_view():

    """
    'media': movie song
    'artist'
    'song
    """

    # пустой result
    data = {
        'resultsCount':'0',
        'results': []
    }

    artist = request.args.get('artist')
    song = request.args.get('song')
    media = request.args.get('media')

    # если нет артиста и типа запроса то заворачиваем
    if not artist or not media:
        return {'results': []}
    # пустая песня?значить ищем всего артиста
    if not song:
        song = ''
    if media == 'movie':
        # чекаем по базе артста
        artist_list = sql_request(f"Select fullname,nconst from artists where fullname='{artist}'")
        if len(artist_list)>0:
            for item in artist_list:
                data['resultsCount'] = len(artist_list)
                data['results'].append({'artist' : item['fullname'], 'artistData': get_media_info(item['nconst'], song)})
        else:
            return { 'resultsCount':'0',
                     'results': []}

        return  data



app.run(host='192.168.1.54',port='5000')