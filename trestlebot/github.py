#!/usr/bin/python

#    Copyright 2023 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""GitHub related functions for the Trestle Bot."""

import re
from typing import Optional, Tuple

import github3
from github3.repos.repo import Repository

from trestlebot.provider import GitProvider, GitProviderException


class GitHub(GitProvider):
    """Create GitHub object to interact with the GitHub API"""

    def __init__(self, access_token: str):
        """
        Initialize GitHub Object

        Args:
            access_token: Access token to make authenticated API requests.
        """
        session: github3.GitHub = github3.GitHub()
        session.login(token=access_token)

        self.session = session
        self.pattern = r"^(?:https?://)?github\.com/([^/]+)/([^/.]+)"

    def parse_repository(self, repo_url: str) -> Tuple[str, str]:
        """
        Parse repository url

        Args:
            repo_url: Valid url for GitHub repo

        Returns:
            Owner and repo name in a tuple, respectively
        """

        match = re.match(self.pattern, repo_url)

        if not match:
            raise GitProviderException(f"{repo_url} is an invalid GitHub repo URL")

        owner = match.group(1)
        repo = match.group(2)
        return (owner, repo)

    def create_pull_request(
        self,
        ns: str,
        repo_name: str,
        base_branch: str,
        head_branch: str,
        title: str,
        body: str,
    ) -> int:
        """
        Create a pull request in the repository

        Args:
            ns: Namespace or owner of the repository
            repo_name: Name of the repository
            base_branch: Branch that changes need to be merged into
            head_branch: Branch with changes
            title: Text for the title of the pull_request
            body: Text for the body of the pull request

        Returns:
            Pull request number
        """
        repository: Optional[Repository] = self.session.repository(
            owner=ns, repository=repo_name
        )
        if repository is None:
            raise GitProviderException(
                f"Repository for {ns}/{repo_name} cannot be None"
            )

        pull_request = repository.create_pull(
            title=title, body=body, base=base_branch, head=head_branch
        )

        if pull_request:
            return pull_request.number
        else:
            raise GitProviderException(
                "Failed to create pull request in {ns}/{repo_name} for {head_branch} to {base_branch}"
            )
