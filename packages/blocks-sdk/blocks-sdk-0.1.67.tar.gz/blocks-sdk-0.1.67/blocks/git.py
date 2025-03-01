import os

from .utils import bash

class Git:

    def __init__(self):
        self.repo_path = os.getenv("GITHUB_REPOSITORY_PATH")
        self.token = os.getenv("GITHUB_TOKEN")
        self.url = f"https://token:{self.token}@github.com/{self.repo_path}"
        
    def configure(self):
        bash("git config --local user.email 'bot@blocksorg.com'")
        bash("git config --local user.name 'BlocksOrg'")

    def checkout(self, target_dir="repo", ref="", new_branch=False):
        url = self.url

        os.makedirs(target_dir, exist_ok=True)

        if ref:
            return bash(f"git clone --branch {ref} {url} {target_dir}")
        return bash(f"git clone {url} {target_dir}")

    def clone(self, target_dir="repo", ref="", new_branch=False):
        return self.checkout(target_dir, ref, new_branch)

    def init(self):
        bash("git init")

    def pull(self):
        bash(f"git pull origin={self.url} HEAD")
    
    def push(self, publish=False):
        if publish:
            bash(f"git push -u origin HEAD")
        else:
            bash(f"git push origin HEAD")

    def commit(self, message):
        bash(f"git commit -m '{message}'")

    def add(self, file, all=False):
        if all:
            bash("git add .")
        else:
            bash(f"git add {file}")

    def branch(self, branch_name, checkout=False):
        if checkout:
            bash(f"git checkout -b {branch_name}")
        else:
            bash(f"git branch {branch_name}")
