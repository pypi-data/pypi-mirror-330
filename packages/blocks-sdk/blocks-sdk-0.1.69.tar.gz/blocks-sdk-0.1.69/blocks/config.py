import os

class Config:
    def __init__(self):
        self.github_api_url = "https://api.github.com"
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_repository_path = os.getenv("GITHUB_REPOSITORY_PATH")
        self.repo_provider = os.getenv("REPO_PROVIDER")

    def get_github_api_url(self):
        return self.github_api_url

    def get_github_token(self):
        return self.github_token

    def get_github_repository_path(self):
        return self.github_repository_path
    
    def get_github_repository_owner(self):
        repository_path = self.get_github_repository_path()
        slug_parts = repository_path.split("/") if repository_path else []
        if len(slug_parts) == 2:
            return slug_parts[0]
        else:
            return None

    def get_github_repository_name(self):
        repository_path = self.get_github_repository_path()
        slug_parts = repository_path.split("/") if repository_path else []
        if len(slug_parts) == 2:
            return slug_parts[1]
        else:
            return None

    def get_repo_provider(self):
        return self.repo_provider
