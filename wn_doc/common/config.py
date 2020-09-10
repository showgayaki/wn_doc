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
                'url': 'https://www.python.org/',
                'description': 'Pythonはパワフル・・・そして高速'
            },
            'Django': {
                'url': 'https://www.djangoproject.com/',
                'description': 'The Web framework for perfectionists with deadlines | Django'
            },
            'Flask': {
                'url': 'https://flask.palletsprojects.com/en/1.1.x/',
                'description': 'Welcome to Flask — Flask Documentation (1.1.x)'
            },
            'NumPy': {
                'url': 'https://numpy.org/',
                'description': 'NumPy'
            },
            'pandas': {
                'url': 'https://pandas.pydata.org/',
                'description': 'pandas - Python Data Analysis Library'
            },
            'matplotlib': {
                'url': 'https://matplotlib.org/',
                'description': 'Matplotlib: Python plotting'
            },
        }
    }

    contents = all_contents[page.capitalize()] if page != 'index' else all_contents
    return contents
