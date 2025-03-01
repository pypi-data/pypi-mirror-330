import requests

from .base import BaseRepoProvider
from .config import Config

class GithubRepoProvider(BaseRepoProvider):
    def __init__(self):
        self.config = Config()

    def request(self, endpoint: str, params=None, method='GET', data=None):
        """
        Make a request to the GitHub API.

        Args:
            endpoint (str): The endpoint to request.
            params (dict): The parameters to pass to the request.
            method (str): The HTTP method to use.
            data (dict): The data to pass to the request.
        """
        headers = {
            'Authorization': f'token {self.config.get_github_token()}',
            'Accept': 'application/vnd.github.v3+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        url = f'{self.config.get_github_api_url()}{endpoint}'
        response = requests.request(method, url, headers=headers, params=params, json=data)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise

        if (method == "DELETE"):
            return None

        return response.json()

    def update_pull_request(
        self, 
        pull_request_number = None, 
        title = None, 
        body = None, 
        assignees = None, 
        labels = None, 
        state = None, 
        maintainer_can_modify = None,
        target_branch = None,
        owner = Config().get_github_repository_owner(),
        repo = Config().get_github_repository_name()
    ):
        """
        Update a pull request in GitHub.

        Uses the following endpoints:
        - https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#update-a-pull-request

        Args:
            pull_request_number (int): The number of the pull request to update. (required)
            title (str): The title of the pull request. (optional)
            description (str): The description of the pull request. (optional)
            state (str): The state of the pull request. (optional)
            target_branch (str): The target branch of the pull request. (optional)

        Raises:
            ValueError: If the pull_request_number is not provided.
        """

        if pull_request_number is None:
            raise ValueError("update_pull_request: pull_request_number is required")
        
        if owner is None:
            raise ValueError("update_pull_request: owner is required")
        
        if repo is None:
            raise ValueError("update_pull_request: repo is required")

        payload = {
            "owner": owner,
            "repo": repo,
            "pull_number": pull_request_number,
        }

        if title is not None:
            payload["title"] = title

        if body is not None:
            payload["body"] = body

        if assignees is not None:
            payload["assignees"] = assignees

        if labels is not None:
            payload["labels"] = labels

        if state is not None:
            payload["state"] = state

        if target_branch is not None:   
            payload["base"] = target_branch

        if maintainer_can_modify is not None:
            payload["maintainer_can_modify"] = maintainer_can_modify

        self.request(f"/repos/{owner}/{repo}/pulls/{pull_request_number}", method="PATCH", data=payload)

    def update_issue(
            self, 
            issue_number = None, 
            title = None, 
            body = None, 
            assignees = None, 
            labels = None, 
            state = None,
            state_reason = None,
            milestone = None,
            owner = Config().get_github_repository_owner(),
            repo = Config().get_github_repository_name()
    ):
        """
        Update an issue in GitHub.

        Uses the following endpoints:
        - https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#update-an-issue

        Args:
            issue_number (int): The number of the issue to update. (required)
            title (str): The title of the issue. (optional)
            body (str): The body of the issue. (optional)
            assignees (list): A list of assignees to assign to the issue. (optional)
            labels (list): A list of labels to add to the issue. (optional)
            state (str): The state of the issue. (optional)
            owner (str): The owner of the repository. (optional)
            repo (str): The name of the repository. (optional)

        Raises:
            ValueError: If the issue_number is not provided.
        """
        if issue_number is None:
            raise ValueError("update_issue: issue_number is required")
        
        if owner is None:
            raise ValueError("update_issue: owner is required")
        
        if repo is None:
            raise ValueError("update_issue: repo is required")

        payload = {
            "owner": owner,
            "repo": repo,
            "issue_number": issue_number,
        }

        if assignees is not None:
            payload["assignees"] = assignees

        if labels is not None:
            payload["labels"] = labels

        if title is not None:
            payload["title"] = title

        if body is not None:
            payload["body"] = body

        if milestone is not None:
            payload["milestone"] = milestone

        if state is not None:
            payload["state"] = state

        if state_reason is not None:
            payload["state_reason"] = state_reason

        self.request(f"/repos/{owner}/{repo}/issues/{issue_number}", method="PATCH", data=payload)

    def create_issue(
            self, 
            title = None, 
            body = None, 
            milestone = None,
            assignees = None, 
            labels = None,
            owner = Config().get_github_repository_owner(),
            repo = Config().get_github_repository_name()
    ):
        """
        Create an issue in GitHub.

        Uses the following endpoints:
        - https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#create-an-issue

        Args:
            title (str): The title of the issue. (required)
            body (str): The body of the issue. (optional) [default: ""]
            assignees (list): A list of assignees to assign to the issue. (optional) [default: []]
            labels (list): A list of labels to add to the issue. (optional) [default: []]
            owner (str): The owner of the repository. (optional)
            repo (str): The name of the repository. (optional)

        Raises:
            ValueError: If the title is not provided.
        """
        if title is None:
            raise ValueError("create_issue: title is required")
        
        if owner is None:
            raise ValueError("create_issue: owner is required")
        
        if repo is None:
            raise ValueError("create_issue: repo is required")

        payload = {
            "owner": owner,
            "repo": repo,
            "title": title,
        }

        if body is not None:
            payload["body"] = body

        if assignees is not None:
            payload["assignees"] = assignees

        if labels is not None:
            payload["labels"] = labels

        if milestone is not None:
            payload["milestone"] = milestone

        self.request(f"/repos/{owner}/{repo}/issues", method="POST", data=payload)

    def create_pull_request(
            self, 
            source_branch = None, 
            target_branch = None, 
            title = None, 
            body = None, 
            draft = False,
            issue_number = None,
            owner = Config().get_github_repository_owner(),
            repo = Config().get_github_repository_name()
    ):
        """
        Create a pull request in GitHub.

        Uses the following endpoints:
        - https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#create-a-pull-request

        Args:
            source_branch (str): The source branch to create the pull request from. (required)
            target_branch (str): The target branch to create the pull request to. (required)
            title (str): The title of the pull request. (required)
            body (str): The body of the pull request. (optional) [default: ""]
            draft (bool): Whether the pull request is a draft. (optional) [default: False]
            owner (str): The owner of the repository. (optional)
            repo (str): The name of the repository. (optional)

        Raises:
            ValueError: If any of the required arguments are not provided.
        """
        if source_branch is None:
            raise ValueError("create_pull_request: source_branch is required")

        if target_branch is None:
            raise ValueError("create_pull_request: target_branch is required")

        if title is None:
            raise ValueError("create_pull_request: title is required")
        
        if owner is None:
            raise ValueError("create_pull_request: owner is required")
        
        if repo is None:
            raise ValueError("create_pull_request: repo is required")

        payload = {
            "owner": owner,
            "repo": repo,
            "title": title,
            "draft": draft,
            "head": source_branch,
            "base": target_branch,
        }

        if body is not None:
            payload["body"] = body

        if issue_number is not None:
            payload["issue"] = issue_number

        self.request(f"/repos/{owner}/{repo}/pulls", method="POST", data=payload)

    def comment_on_pull_request(
            self, 
            pull_request_number = None, 
            body = None,
            owner = Config().get_github_repository_owner(),
            repo = Config().get_github_repository_name()
    ):
        """
        Comment on a pull request in GitHub.

        Uses the following endpoints:
        - https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#create-an-issue-comment

        Args:
            pull_request_number (int): The number of the pull request to comment on. (required)
            body (str): The body of the comment. (optional) [default: ""]
            owner (str): The owner of the repository. (optional)
            repo (str): The name of the repository. (optional)

        Raises:
            ValueError: If any of the required arguments are not provided.
        """

        if body is None:
            raise ValueError("comment_on_pull_request: body is required")

        if pull_request_number is None:
            raise ValueError("comment_on_pull_request: pull_request_number is required")
        
        if owner is None:
            raise ValueError("comment_on_pull_request: owner is required")
        
        if repo is None:
            raise ValueError("comment_on_pull_request: repo is required")

        payload = {
            "owner": owner,
            "repo": repo,
            "body": body,
            "pull_number": pull_request_number,
        }

        self.request(f"/repos/{owner}/{repo}/issues/{pull_request_number}/comments", method="POST", data=payload)

    def delete_pull_request_comment(
            self, 
            comment_id = None,
            owner = Config().get_github_repository_owner(),
            repo = Config().get_github_repository_name()
    ):
        """
        Delete a pull request comment in GitHub.

        Uses the following endpoints:
        - https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28#delete-a-review-comment-for-a-pull-request

        Args:
            comment_id (int): The ID of the comment to delete. (required)

        Raises:
            ValueError: If the comment_id is not provided.
        """
        if comment_id is None:
            raise ValueError("delete_pull_request_comment: comment_id is required")
        
        if owner is None:
            raise ValueError("delete_pull_request_comment: owner is required")
        
        if repo is None:
            raise ValueError("delete_pull_request_comment: repo is required")

        self.request(f"/repos/{owner}/{repo}/pulls/comments/{comment_id}", method="DELETE")

    def update_pull_request_comment(
            self, 
            comment_id = None, 
            body = None,
            owner = Config().get_github_repository_owner(),
            repo = Config().get_github_repository_name()
    ):
        """
        Update a pull request comment in GitHub.

        Uses the following endpoints:
        - https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28#update-a-review-comment-for-a-pull-request

        Args:
            comment_id (int): The ID of the comment to update. (required)
            body (str): The body of the comment. (required)

        Raises:
            ValueError: If any of the required arguments are not provided.
        """
        if comment_id is None:
            raise ValueError("update_pull_request_comment: comment_id is required")

        if owner is None:
            raise ValueError("update_pull_request_comment: owner is required")
        
        if repo is None:
            raise ValueError("update_pull_request_comment: repo is required")

        if body is None:
            raise ValueError("update_pull_request_comment: body is required")

        payload = {
            "body": body,
        }

        self.request(f"/repos/{self.config.get_github_repository_path()}/pulls/comments/{comment_id}", method="PATCH", data=payload)

    # (verified)
    def comment_on_pull_request_file(
            self, 
            commit_id = None, 
            file_path = None, 
            pull_request_number = None, 
            body = None, 
            line = None, 
            delete_existing = True,
            position = None,
            side = None,
            start_line = None,
            start_side = None,
            reply_to_id = None,
            subject_type = None,
            owner = Config().get_github_repository_owner(),
            repo = Config().get_github_repository_name()
    ):
        """
        Comment on a file in a pull request in GitHub.

        Uses the following endpoints:
        - https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28#create-a-review-comment-for-a-pull-request

        Args:
            commit_id (str): The SHA of the commit to comment on. (required)
            file_path (str): The path of the file to comment on. (required)
            pull_request_number (int): The number of the pull request to comment on. (required)
            body (str): The body of the comment. (optional) [default: ""]
            line (int): The line number to comment on. (optional) [default: None]
            delete_existing (bool): Whether to delete the existing comment on the file. (optional) [default: True]
            owner (str): The owner of the repository. (optional)
            repo (str): The name of the repository. (optional)  

        Raises:
            ValueError: If any of the required arguments are not provided.
        """


        if body is None:
            raise ValueError("comment_on_pull_request_file: body is required")

        if commit_id is None:
            raise ValueError("comment_on_pull_request_file: commit_id is required")

        if file_path is None:
            raise ValueError("comment_on_pull_request_file: file_path is required")

        if pull_request_number is None:
            raise ValueError("comment_on_pull_request_file: pull_request_number is required")
        
        if owner is None:
            raise ValueError("comment_on_pull_request_file: owner is required")
        
        if repo is None:
            raise ValueError("comment_on_pull_request_file: repo is required")

        payload = {
            "body": body,
            "commit_id": commit_id,
            "path": file_path,
            "subject_type": "file",
        }

        if position is not None:
            payload["position"] = position

        if side is not None:
            payload["side"] = side

        if start_line is not None:
            payload["start_line"] = start_line

        if start_side is not None:
            payload["start_side"] = start_side

        if line is not None:
            payload["line"] = line

        if subject_type is not None:
            payload["subject_type"] = subject_type

        if reply_to_id is not None:
            payload["in_reply_to"] = reply_to_id

        self.request(f"/repos/{owner}/{repo}/pulls/{pull_request_number}/comments", method="POST", data=payload)

    def update_issue_comment(
            self, 
            comment_id = None, 
            body = None,
            owner = Config().get_github_repository_owner(),
            repo = Config().get_github_repository_name()
    ):
        """
        Update an issue comment in GitHub.

        Uses the following endpoints:
        - https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#update-an-issue-comment

        Args:
            comment_id (int): The ID of the comment to update. (required)
            body (str): The body of the comment. (required)
            owner (str): The owner of the repository. (optional)
            repo (str): The name of the repository. (optional)

        Raises:
            ValueError: If any of the required arguments are not provided.
        """
        if comment_id is None:
            raise ValueError("update_issue_comment: comment_id is required")

        if body is None:
            raise ValueError("update_issue_comment: body is required")
        
        if owner is None:
            raise ValueError("update_issue_comment: owner is required")
        
        if repo is None:
            raise ValueError("update_issue_comment: repo is required")

        payload = {
            "body": body,
        }

        self.request(f"/repos/{owner}/{repo}/issues/comments/{comment_id}", method="PATCH", data=payload)

    def delete_issue_comment(
            self, 
            comment_id = None,
            owner = Config().get_github_repository_owner(),
            repo = Config().get_github_repository_name()
    ):
        """
        Delete an issue comment in GitHub.

        Uses the following endpoints:
        - https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#delete-an-issue-comment

        Args:
            comment_id (int): The ID of the comment to delete. (required)
            owner (str): The owner of the repository. (optional)
            repo (str): The name of the repository. (optional)

        Raises:
            ValueError: If the comment_id is not provided.
        """

        if comment_id is None:
            raise ValueError("delete_issue_comment: comment_id is required")
        
        if owner is None:
            raise ValueError("delete_issue_comment: owner is required")
        
        if repo is None:
            raise ValueError("delete_issue_comment: repo is required")

        self.request(f"/repos/{owner}/{repo}/issues/comments/{comment_id}", method="DELETE")

    def comment_on_issue(
            self, 
            issue_number = None, 
            body = None,
            owner = Config().get_github_repository_owner(),
            repo = Config().get_github_repository_name()
    ):
        """
        Comment on an issue in GitHub.

        Uses the following endpoints:
        - https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#create-an-issue-comment

        Args:
            issue_number (int): The number of the issue to comment on. (required)
            body (str): The body of the comment. (optional) [default: ""]
            owner (str): The owner of the repository. (optional)
            repo (str): The name of the repository. (optional)

        Raises:
            ValueError: If any of the required arguments are not provided.
        """

        if body is None:
            raise ValueError("comment_on_issue: body is required")

        if issue_number is None:
            raise ValueError("comment_on_issue: issue_number is required")
        
        if owner is None:
            raise ValueError("comment_on_issue: owner is required")
        
        if repo is None:
            raise ValueError("comment_on_issue: repo is required")

        payload = {
            "owner": owner,
            "repo": repo,
            "body": body,
            "issue_number": issue_number,
        }
    
        self.request(f"/repos/{owner}/{repo}/issues/{issue_number}/comments", method="POST", data=payload)

    def reply_to_pull_request_comment(
            self,
            reply_to_id = None, 
            pull_request_number = None, 
            body = None,
            owner = Config().get_github_repository_owner(),
            repo = Config().get_github_repository_name()
    ):
        """
        Reply to a pull request comment in GitHub.

        Uses the following endpoints:
        - https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28#create-a-reply-for-a-review-comment

        Args:
            reply_to_id (int): The ID of the comment to reply to. (required)
            pull_request_number (int): The number of the pull request to reply to. (required)
            body (str): The body of the reply. (optional) [default: ""]
            owner (str): The owner of the repository. (optional)
            repo (str): The name of the repository. (optional)

        Raises:
            ValueError: If any of the required arguments are not provided.
        """

        if body is None:
            raise ValueError("reply_to_pull_request_comment: body is required")

        if reply_to_id is None:
            raise ValueError("reply_to_pull_request_comment: reply_to_id is required")

        if pull_request_number is None:
            raise ValueError("reply_to_pull_request_comment: pull_request_number is required")

        if owner is None:
            raise ValueError("reply_to_pull_request_comment: owner is required")
        
        if repo is None:
            raise ValueError("reply_to_pull_request_comment: repo is required")

        payload = {
            "in_reply_to": reply_to_id,
            "body": body,
        }

        self.request(f"/repos/{owner}/{repo}/pulls/{pull_request_number}/comments", method="POST", data=payload)

    def review_pull_request(
            self, 
            pull_request_number = None, 
            body = None, 
            commit_id = None, 
            comments = None, 
            event = "COMMENT",
            owner = Config().get_github_repository_owner(),
            repo = Config().get_github_repository_name()
    ):
        """
        Review a pull request in GitHub. 
        
        Uses the following endpoints:
        - https://docs.github.com/en/rest/pulls/reviews?apiVersion=2022-11-28#create-a-review-for-a-pull-request

        Args:
            pull_request_number (int): The number of the pull request to review. (required)
            body (str): The body of the review. (optional) [default: ""]
            commit_sha (str): The SHA of the commit to review. (optional) [default: None]
            comments (list): A list of comments to add to the review. (optional) [default: []]
            event (str): The event to trigger on the review. (optional) [default: "COMMENT"]
            owner (str): The owner of the repository. (optional)
            repo (str): The name of the repository. (optional)

        Raises:
            ValueError: If any of the required arguments are not provided.
        """

        if body is None:
            raise ValueError("review_pull_request: body is required")

        if pull_request_number is None:
            raise ValueError("review_pull_request: pull_request_number is required")
        
        if owner is None:
            raise ValueError("review_pull_request: owner is required")
        
        if repo is None:
            raise ValueError("review_pull_request: repo is required")
    
        payload = {
            "owner": owner,
            "repo": repo,
            "pull_number": pull_request_number,
            "event": event,
            "body": body,
        }

        if commit_id is not None:
            payload["commit_id"] = commit_id

        if comments is not None:
            payload["comments"] = comments

        self.request(f"/repos/{owner}/{repo}/pulls/{pull_request_number}/reviews", method="POST", data=payload)
