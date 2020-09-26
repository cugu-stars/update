import json
import os
import subprocess
import urllib.request

from github import Github

g = Github(os.environ['API_KEY'])
user = g.get_user()

organization = g.get_organization("cugu-stars")
existing = {repo.parent.full_name: repo for repo in organization.get_repos() if repo.fork}

for repo in user.get_starred():
    if repo.full_name not in existing:
        if not repo.private:
            print("Create fork", repo.full_name)
            organization.create_fork(repo)
    else:
        print(repo.full_name, "already exists as", existing[repo.full_name].full_name)
        clone_url = existing[repo.full_name].clone_url.replace("://", "://cugu:" + os.environ['API_KEY'] + "@")
        subprocess.run("git clone %s %s" % (clone_url, repo.full_name), shell=True, check=True)
        subprocess.run("git remote add upstream %s" % existing[repo.full_name].parent.clone_url, shell=True, check=True, cwd=repo.full_name)
        subprocess.run("git fetch upstream", shell=True, check=True, cwd=repo.full_name)
        subprocess.run("git merge upstream/master", shell=True, check=True, cwd=repo.full_name)
        subprocess.run("git push", shell=True, check=True, cwd=repo.full_name)
