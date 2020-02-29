import requests
# from lxml import html
from bs4 import BeautifulSoup
# import json
# from get_movie_poster import get_movie_poster

def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    input_file.close()
    return text

def get_media_info (ARTIST_ID,SEARCH_SONG):
    """
      input: код артиста из базы, песня(возможно null)
      если песня не заданы ищем все саундтреки по исполнителю
      """

    url = f'https://www.imdb.com/name/{ARTIST_ID}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text,'html.parser')

    # print(ARTIST_ID)
    # print(SEARCH_SONG)
    m_results = []

    # тестовый парсинг по файлу потом убрать
    # text = read_file('data/sound.html')
    # soup = BeautifulSoup(text,'html.parser')

    films_list = soup.find('div', {'id': 'filmography'}).find('div', {'class': 'filmo-category-section'}).find_all('div', {'class': 'filmo-row'})
    for item in films_list:
        # id фильма
        m_id=item.get('id')[11:]
        m_episodes=[]
        # ссылка на фильм
        m_href=item.find('a').get('href')
        m_name=item.find('a').text
        # print(m_name)
        # может быть пустым
        m_year=item.find('span',{'class': 'year_column'}).text.strip()
        m_year = m_year if m_year !='' else 'None'

        episodes = item.find_all('div',{'class': 'filmo-episodes'})
        # если это сериал или передача
        if episodes:
            # print('episode')
            # сколько эпизодов в принципе не надо тк не все эпизоды будут в выдаче а там кол-во
            # print(item.contents[4].strip())
            for episode in episodes:
                # m_episodes.append({'epName': episode.find('a').text,
                #                     'epLink': episode.find('a').get('href')})
                # получаем песню эпизода
                songs = episode.contents[2].strip().split(',')
                # print(f'songs: {songs}')
                # если ищем не пустую песню
                if len(SEARCH_SONG) != 0:
                    for song in songs:
                        # находим левые и правые кавычки, все что без "" откидываем
                        lf_pos = song.find('"') + 1
                        rgh_pos = song[lf_pos:].find('"') + lf_pos
                        if lf_pos and rgh_pos:
                            # print
                            song = song[lf_pos:rgh_pos].strip()
                            # print (len(song))
                            if SEARCH_SONG.upper() == song.upper():
                                m_episodes.append({'epName': episode.find('a').text,
                                                   'epLink': episode.find('a').get('href')})
                                # m_results['mEpisodes'] = m_episodes
                                # m_results.append({'mId': m_id,
                                #                   'mLink': m_href,
                                #                  'mName': m_name,
                                #                  'mYear': m_year,
                                #                   'mEpisodes': m_episodes})
                # добавляем все песни по исполнителю
                else:
                    m_episodes.append({'epName': episode.find('a').text,
                                       'epLink': episode.find('a').get('href')})
                    # print(m_results)
                    # m_results['mEpisodes'] = m_episodes
                    # m_results.append({'mId': m_id,
                    #                   'mLink': m_href,
                    #                   'mName': m_name,
                    #                   'mYear': m_year,
                    #                   'mEpisodes': m_episodes})
            if m_episodes:
                m_poster = ""
                m_results.append({'mId': m_id,
                                  'mLink': m_href,
                                  'mName': m_name,
                                  'mYear': m_year,
                                  'mPoster': m_poster,
                                  'mEpisodes': m_episodes})
        # вариант медиа без эпизодов
        else:
            m_episodes=[]
            # если ищем по песни иначе по всему артисту
            if len(SEARCH_SONG) != 0:
                songs = item.contents[4].strip().split (',')
                for song in songs:
                    lf_pos = song.find('"') + 1
                    rgh_pos = song[lf_pos:].find('"') + lf_pos
                    song = song[lf_pos:rgh_pos].strip()
                    # print(len(song))
                    # если ищем по артисту и песне
                    if SEARCH_SONG.upper() == song.upper():
                        # print('Y')
                        m_poster = ""
                        m_results.append({'mId': m_id,
                                          'mLink': m_href,
                                          'mName': m_name,
                                          'mYear': m_year,
                                          'mPoster': m_poster,
                                          'mEpisodes': m_episodes})
                    # print('film')
            # если ищем по артисту  в целом
            else:
                m_poster = ""
                m_results.append({'mId': m_id,
                                  'mLink': m_href,
                                  'mName': m_name,
                                  'mYear': m_year,
                                  'mPoster': m_poster,
                                  'mEpisodes': m_episodes})


        # print('==================================================')

    return m_results

    # for result in m_results:
    #     print(f"id фильма: {result['m_id']}")
    #     print(f"Название: {result['m_name']}")
    #     if result['m_episodes']:
    #         print(f"Эпизоды: {result['m_episodes']}")
    #     print()

if __name__== "__main__":
    get_media_info('','dust')