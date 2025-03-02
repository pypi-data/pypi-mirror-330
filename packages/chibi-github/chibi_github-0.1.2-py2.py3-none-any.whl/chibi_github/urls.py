from chibi_github.config import configuration
from chibi_requests import Chibi_url
from chibi_requests.auth import Token


base_url = Chibi_url(
    f"{configuration.github.schema}://{configuration.github.host}" )

base_url += Token( token=configuration.github.personal_token )

issues = base_url + 'issues'

repo_pull = base_url + 'repos/{username}/{repo}/pulls'

user_repos = base_url + 'users/{username}/repos'
