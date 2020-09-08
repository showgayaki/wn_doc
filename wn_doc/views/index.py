from django.shortcuts import render
from wn_doc.common.github import Github
from wn_doc.common.config import github_config, nav, view_contents


def index(request):
    global_nav = nav()
    contents = view_contents()

    git = Github(github_config())
    contents['Repositories'] = git.fetch_repositories()

    return render(
        request,
        'index.html',
        {
            'active_page': 'Home',
            'global_nav': global_nav,
            'contents': contents
        }
    )
