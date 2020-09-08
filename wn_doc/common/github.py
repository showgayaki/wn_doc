import os
import requests


class Github:
    def __init__(self, gh_config):
        self.api_url = gh_config['api_url']
        self.user = gh_config['user']
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '\
             'AppleWebKit/537.36 (KHTML, like Gecko) '\
             'Chrome/55.0.2883.95 Safari/537.36'
        api_key = os.environ.get('GITHUB_API_KEY')
        self.headers = {'User-Agent': ua, 'Authorization': api_key}

    def fetch_repositories(self):
        query = """
                query{
                    viewer{
                        repositories(last:30){
                            totalCount
                            nodes{
                                name
                                url
                                description
                                createdAt
                                languages(last:5){
                                    nodes{
                                        name
                                        color
                                    }
                                }
                            }
                        }
                    }
                }
                """
        repos = {}
        try:
            res = requests.post(
                self.api_url,
                timeout=(3, 6),
                headers=self.headers,
                json={'query': query}
            )
            repos = res.json()
            repos_dict = {}
            for repo in repos['data']['viewer']['repositories']['nodes']:
                repos_dict[repo['name']] = {}
                repos_dict[repo['name']]['url'] = '/repositories/{}'.format(repo['name'])
                repos_dict[repo['name']]['description'] = repo['description']
                repos_dict[repo['name']]['languages'] = repo['languages']
                repos_dict[repo['name']]['created_at'] = repo['createdAt'].replace('T', ' ').replace('Z', ' ')

            # リポジトリ作成日時でソート
            repos_sorted = sorted(repos_dict.items(), key=lambda x: x[1]['created_at'], reverse=True)
        except Exception as e:
            repos['Error'] = e
            return repos
        else:
            res.close()

        return dict(repos_sorted)

    def fetch_trees(self, repo, directory):
        query = '''
                query{
                    repository(owner:"%s", name:"%s"){
                        object(expression: "master:%s") {
                            ... on Tree{
                                entries{
                                    name
                                    type
                                }
                            }
                        }
                    }
                }
                ''' % (self.user, repo, directory)
        try:
            res = requests.post(
                self.api_url,
                timeout=(3, 6),
                headers=self.headers,
                json={'query': query}
            )
            res_json = res.json()

            if res_json['data']['repository'] is None:
                return 404

            tree = res_json['data']['repository']['object']['entries']
            tree_sorted = sorted(tree, key=lambda x: x['type'], reverse=True)
        except Exception as e:
            tree_sorted = [{'name': f'Error: {e}'}]
        else:
            res.close()
        return tree_sorted
