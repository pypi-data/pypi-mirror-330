from github import Github, Auth
from filelean import constants
from typing import List 
import re

GITHUB_INFO_REGEX = re.compile(r"github\.com[:|/](?P<user>.+)/(?P<repo>.+)(\.git)?")

def github_url_to_repo_name(github_url:str) -> str:
    """Convert the github url to repo."""
    matchs = GITHUB_INFO_REGEX.findall(github_url)
    assert len(matchs) == 1, f"Invalid github url: {github_url}"
    match = matchs[0]
    return f"{match[0]}/{match[1]}"

def get_github_object() -> Github:
    token = constants.GITHUB_ACCESS_TOKEN
    if token is not None:
        g = Github(auth=Auth.Token(token))
        g.get_user().login
    else:
        g = Github()
    return g

def get_repo_versions(github_url:str, max_num:int=10) -> List[str]:
    """Get the valid versions of the repository."""
    g = get_github_object()
    repo = g.get_repo(github_url_to_repo_name(github_url))
    versions = []
    for tag in repo.get_tags():
        if len(versions) >= max_num:
            break
        versions.append(tag.name)
    return versions