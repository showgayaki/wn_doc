from django.shortcuts import render
from django.http import Http404
from wn_doc.common.github import Github
from wn_doc.common.config import github_config, nav


def repository(request, directory):
    global_nav = nav()
    active_page = 'Repositories'

    gh_config = github_config()
    git = Github(gh_config)

    repository = directory.split('/')[0]
    sub_direcroty = '/'.join(directory.split('/')[1:])
    trees = git.fetch_trees(repository, sub_direcroty)

    if trees == 404:
        raise Http404
    else:
        code = ''
        codes = {}
        for tree in trees:
            if tree['type'] == 'blob':
                codes[tree['name']] = {}
                codes[tree['name']]['id'] = tree['name'].replace('.', '')
                file_name = '{}/{}'.format(sub_direcroty, tree['name']) if sub_direcroty != '' else tree['name']
                code = (
                    'https://gist-it.appspot.com/'
                    'https://github.com/{}/{}/blob/master/{}?footer=no'
                ).format(
                    gh_config['user'],
                    repository,
                    file_name
                )
                codes[tree['name']]['code'] = code

    return render(
        request,
        'repository.html',
        {
            'active_page': active_page,
            'global_nav': global_nav,
            'directory': directory,
            'trees': trees,
            'codes': codes
        }
    )
