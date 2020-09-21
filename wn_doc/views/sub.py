from django.shortcuts import render
from django.http import Http404
from wn_doc.common.github import Github
from wn_doc.common.config import github_config, nav, view_contents


def sub(request, page):
    global_nav = nav()

    if page.capitalize() in global_nav.keys():
        active_page = page.capitalize()
    else:
        raise Http404

    if page == 'repositories':
        git = Github(github_config())
        contents = git.fetch_repositories()
        contents.update(view_contents(page))
    else:
        contents = view_contents(page)

    return render(
        request,
        'sub.html',
        {
            'active_page': active_page,
            'global_nav': global_nav,
            'contents': contents
        }
    )
