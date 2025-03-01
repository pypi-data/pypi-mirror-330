from .config import Config
from .github import GithubRepoProvider

class Repo:
    def factory_repo_provider(self):
        if self.config.get_repo_provider() == "github":
            return GithubRepoProvider()

    def __init__(self):
        self.config = Config()
        self.repo_provider = self.factory_repo_provider()

    def request(self, endpoint: str, params=None, method='GET', data=None):
        return self.repo_provider.request(endpoint, params, method, data)

    def update_pull_request(self, pull_request_number = None, title = None, body = None, assignees = None, labels = None, state = None, maintainer_can_modify = None, target_branch = None):
        self.repo_provider.update_pull_request(pull_request_number = pull_request_number, title = title, body = body, assignees = assignees, labels = labels, state = state, maintainer_can_modify = maintainer_can_modify, target_branch = target_branch)

    def update_issue(self, issue_number = None, title = None, body = None, assignees = None, labels = None, state = None, state_reason = None, milestone = None):
        self.repo_provider.update_issue(issue_number = issue_number, title = title, body = body, assignees = assignees, labels = labels, state = state, state_reason = state_reason, milestone = milestone)

    def create_issue(self, title = None, body = None, assignees = None, labels = None, milestone = None):
        self.repo_provider.create_issue(title, body, assignees, labels, milestone)

    def create_pull_request(self, source_branch = None, target_branch = None, title = None, body = None, draft = False, issue_number = None, owner = None, repo = None):
        self.repo_provider.create_pull_request(source_branch = source_branch, target_branch = target_branch, title = title, body = body, draft = draft, issue_number = issue_number, owner = owner, repo = repo)

    def comment_on_pull_request(self, pull_request_number = None, body = None):
        self.repo_provider.comment_on_pull_request(pull_request_number = pull_request_number, body = body)

    def update_pull_request_comment(self, comment_id = None, body = None):
        self.repo_provider.update_pull_request_comment(comment_id = comment_id, body = body)

    def delete_pull_request_comment(self, comment_id = None):
        self.repo_provider.delete_pull_request_comment(comment_id = comment_id)

    def comment_on_pull_request_file(self, commit_id = None, file_path = None, pull_request_number = None, body = None, line = None, delete_existing = True, position = None, side = None, start_line = None, start_side = None, reply_to_id = None, subject_type = None):
        self.repo_provider.comment_on_pull_request_file(commit_id = commit_id, file_path = file_path, pull_request_number = pull_request_number, body = body, line = line, delete_existing = delete_existing, position = position, side = side, start_line = start_line, start_side = start_side, reply_to_id = reply_to_id, subject_type = subject_type)

    def update_issue_comment(self, comment_id = None, body = None):
        self.repo_provider.update_issue_comment(comment_id = comment_id, body = body)

    def delete_issue_comment(self, comment_id = None):
        self.repo_provider.delete_issue_comment(comment_id = comment_id)

    def comment_on_issue(self, issue_number = None, body = None):
        self.repo_provider.comment_on_issue(issue_number = issue_number, body = body)

    def reply_to_pull_request_comment(self, reply_to_id = None, pull_request_number = None, body = None):
        self.repo_provider.reply_to_pull_request_comment(reply_to_id = reply_to_id, pull_request_number = pull_request_number, body = body)

    def review_pull_request(self, pull_request_number = None, body = None, commit_id = None, comments = None):
        self.repo_provider.review_pull_request(pull_request_number = pull_request_number, body = body, commit_id = commit_id, comments = comments)