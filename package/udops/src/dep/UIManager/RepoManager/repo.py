import os.path
from dvc.repo import Repo
import git
import os
from udops.src.dep.Common.Constants import Constants
from psycopg2.extras import RealDictCursor


class repomanager:
    def init(self,location):
        try:
            os.chdir(location)
            git.Repo.init(location)
            print("git initialized")
            Repo.init(
                location,
                force=True,
            )
            return 1

        except Exception as e:
            error = str(e)
            print(error)
            return error

    # def get_url(self, target,location):
    #     try:ls
    #         os.chdir(location)
    #         git.Repo.init(location)
    #         #s = Repo(location)
    #        # s.get_url(target)
    #         return 1
    #     except Exception as e:
    #         error = str(e)
    #         return error

    def create_corpus(self, json_loader, conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(Constants.create_metadata_table)
            cursor.execute(Constants.create_custom_table)

            data = json_loader["corpus_name"], json_loader["corpus_type"], json_loader["language"], json_loader[
                "source_type"], \
                json_loader["vendor"], json_loader["domain"], json_loader["description"], json_loader["lang_code"], \
                json_loader["acquisition_date"], json_loader["migration_date"], json_loader["flag"]

            corpus_name = json_loader["corpus_name"]
            cursor.execute(Constants.select_query3 + f"'{corpus_name}'")
            rows = cursor.fetchall()
            if len(rows) == 0:
                cursor.execute(
                    Constants.insert_query_metadata,
                    data)
                cursor.execute(Constants.query_metadata + json_loader["corpus_name"] + "'")
                conn.commit()
                cursor.close()
                return 1
            else:
                return 2

        except Exception as e:
            error = str(e)
            return error

    def add_(self, target,location):
        try:
            os.chdir(location)
            s = Repo(location)
            g = git.Repo(location)
            s.add(
                targets=target,
               # recursive=False,
                no_commit=False,
                #fname=None,
                to_remote=False,
            )
            g.git.add('--all')
            return 1
        except Exception as e:
            error = str(e)
            return error

    def remote(self, name: str, data: str, gita: str, location):
        try:
            s = Repo(location)
            g = git.Repo(location)
            with s.config.edit() as conf:
                conf["core"] = {"remote": "data"}
                conf["remote"]["data"] = {"url": str(data) + 'remote/' + name}
            g.create_remote('origin', str(gita))
            g.git.add('--all')
            return 1
        except Exception as e:
            error = str(e)
            return error

    def commit(self, message, location):
        try:

            g = git.Repo(location)
            g.git.add('--all')
            g.git.commit('-m', message)
            return 1
        except Exception as e:
            error = str(e)
            return error

    def push(self,location):
        try:
            s = Repo(location)
            g = git.Repo(location)
            s.push(remote='data')
            g.git.push("--set-upstream", "origin", "master")
            return 1
        except Exception as e:
            error = str(e)
            return error

    def clone(self,args,location):
        try:
            git.Git(location).clone(args)
            return 1
        except Exception as e:
            error = str(e)
            return error

    def pull(self, file,location):
        try:
            s = Repo(location)
            s.pull(remote="data", targets=file)
            return 1
        except Exception as e:
            error = str(e)
            return error
