from typing import Dict, List

from .pull_request import PullRequest
from .comment import Comment
from .file import File
from .developer import Developer
from .contribution import Contribution


class Manager:
    files: Dict[str, File]
    developers: Dict[str, Developer]
    contributions: Dict[str, List[Contribution]]
    comments: Dict[str, List[Comment]]
    pull_requests: Dict[int, PullRequest]

    def __init__(self):
        self.files = {}
        self.developers = {}
        self.contributions = {}
        self.comments = {}
        self.pull_requests = {}

    @property
    def developers_list(self):
        return list(self.developers.values())

    @property
    def files_list(self):
        return list(self.files.values())

    @property
    def comments_list(self):
        return list(self.comments.values())

    @property
    def pull_requests_list(self):
        return list(self.pull_requests.values())

    def add_comment(self, comment: Comment):
        k = comment.filename
        if k not in self.comments:
            self.comments[k] = []
        self.comments[k].append(comment)

    def add_file(self, file: File):
        self.files[file.filepath] = file

    def add_developer(self, developer: Developer):
        self.developers[developer.username] = developer

    def add_contribution(self, contribution: Contribution):
        k = contribution.filename
        if k not in self.contributions:
            self.contributions[k] = []
        self.contributions[k].append(contribution)

    def add_pull_request(self, pr: PullRequest):
        self.pull_requests[pr.number] = pr
