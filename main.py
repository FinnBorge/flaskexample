from flask import Flask, request, render_template, session
import requests
import logging
import urllib.parse as urlparse

app = Flask(__name__)
app.secret_key = 'demo'
GITHUB_TOKEN = 'f55a7e3d11dca546b1bda5310f549e6aac9e68fe'

# explanatory comments are above the code they explain

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        organization = request.form.get('organization')
        # Collect all of the organization's repositories
        # across multiple pages, if applicable
        get_repo_list_response = requests.get(
            'https://api.github.com/orgs/%s/repos' % organization,
            headers={'Authorization':'token %s' % GITHUB_TOKEN}
        )
        # store list of repos
        repositories = get_repo_list_response.json()
        # iterate until there are no remaining pages
        while 'next' in get_repo_list_response.links.keys():
            get_repo_list_response = requests.get(
                get_repo_list_response.links['next']['url'],
                headers={'Authorization':'token %s' % GITHUB_TOKEN}
            )
            # add new repos to list
            repositories.extend(get_repo_list_response.json())
        # instantiate data dict
        data = {}
        for repo in repositories:
            # pull list of contributors
            get_contributors_list_response = requests.get(
                '%s?anon=1' % repo['contributors_url'],
                headers={'Authorization':'token %s' % GITHUB_TOKEN}
            )
            # check for extra pages of contributors
            if 'last' in get_contributors_list_response.links:
                last_url = get_contributors_list_response.links['last']['url']
                parsed = urlparse.urlparse(last_url)
                # extract final page num
                count_pages = int(urlparse.parse_qs(parsed.query)['page'][0])
                # if more than 1 page, use knowledge that pages contain 30 records
                # to skip requesting every page
                # then add the count on the final page
                last_page_res = requests.get(
                        last_url,
                        headers={'Authorization':'token %s' % GITHUB_TOKEN})
                contributors = 30 * (count_pages - 1) + len(last_page_res.json())
            # if there is no link, its just the single page
            elif 'last' not in get_contributors_list_response.links:
                contributors = len(get_contributors_list_response.json())
            data[repo['name']] = {
                'name': repo['name'],
                'id': repo['id'],
                'html_url': repo['html_url'],
                'description': repo['description'],
                'forks': repo['forks_count'],
                'stars': repo['stargazers_count'],
                'contributors': contributors
            }
        return render_template('index.html', repository_list=data)

    #GET
    return render_template('index.html')
