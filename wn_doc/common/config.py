import requests
from bs4 import BeautifulSoup


def github_config():
    github_dict = {
        'api_url': 'https://api.github.com/graphql',
        'user': 'showgayaki'
    }
    return github_dict


def nav():
    nav_dict = {
        'Home': '/',
        'Apps': '/apps',
        'Repositories': '/repositories',
        'Official': '/official'
    }
    return nav_dict


def view_contents(page='index'):
    all_contents = {
        'Apps': {
            'Michopa or Yukipoyo': {
                'url': 'https://my-recog.herokuapp.com/',
                'description': 'みちょぱとゆきぽよ判別機'
            }
        },
        'Official': {
            'Python': {
                'url': 'https://www.python.org/'
            },
            'Django': {
                'url': 'https://www.djangoproject.com/'
            },
            'Flask': {
                'url': 'https://flask.palletsprojects.com/en/1.1.x/'
            },
            'NumPy': {
                'url': 'https://numpy.org/'
            },
            'pandas': {
                'url': 'https://pandas.pydata.org/'
            },
            'matplotlib': {
                'url': 'https://matplotlib.org/'
            },
        }
    }

    for val in all_contents['Official'].values():
        try:
            res = requests.get(val['url'], timeout=(3, 6))
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.find('title').get_text()
        except Exception as e:
            title = str(e)
        else:
            res.close()
        val['description'] = title

    contents = all_contents[page.capitalize()] if page != 'index' else all_contents
    return contents
