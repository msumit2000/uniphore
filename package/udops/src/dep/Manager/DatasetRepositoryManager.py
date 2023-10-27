import os.path
from dvc.repo import Repo
import git
import os


class DatasetRepositoryManager:
    def init_dataset(self):
        git.Repo.init(os.getcwd())
        Repo.init(
            ".",
            force=True,
        )

    def add_dataset(self, target):
        s = Repo(os.getcwd())
        g = git.Repo(os.getcwd())
        s.add(
            targets=target,
          recursive=False,
            no_commit=False,
            fname=None,
            to_remote=False,
        )
        g.git.add('--all')

    def commit_dataset(self, args2):
        g = git.Repo(os.getcwd())
        g.git.commit('-m', args2)


    def clone_dataset(self, args):
        git.Git(os.getcwd()).clone(args)

    def remote_dataset(self, args1: str, args2: str):
        s = Repo(os.getcwd())
        g = git .Repo(os.getcwd())
        with s.config.edit() as conf:
            conf["core"] = {"remote": "remote_store"}
            conf["remote"]["remote_store"] = {"url": str(args1)}
        g.create_remote('origin', str(args2))

    def push_dataset(self):
        s = Repo(os.getcwd())
        g = git.Repo(os.getcwd())
        s.push(remote='remote_store')
        g.git.push("--set-upstream", "origin", "master")

    def pull_dataset(self, args):
        s = Repo(os.getcwd())
        s.fetch()
    # s.checkout()
        s.pull(remote="remote_store")
