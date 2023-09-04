from udops.src.dep.UIManager.RepoManager.repo import repomanager
from udops.src.dep.config.Connection import *
from udops.src.dep.InputProperties import *
from psycopg2.extras import RealDictCursor
prop = properties()
connection = Connection()
conn = connection.get_connection()



class uimanager:

    def update_flag(self,corpus_name):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"update corpus_metadata set flag = 1 where corpus_name = '{corpus_name}'"
            cursor.execute(query)
            conn.commit()
            cursor.close()
            return 1
        except Exception as e:
            error = str(e)
            return error

    def create_corpus(self, json_loader, location):
        try:
            repo = repomanager()
            print(f"location--{location}")
            in_it = repo.init(location)
            if in_it == 1:
                #url_get = repo.get_url(target, location)
                #if url_get == 1:
                corpus_create = repo.create_corpus(json_loader, conn)
                print(f"create_corpus--->{corpus_create}")
                if corpus_create == 1:
                    return 1
                elif corpus_create == 2:
                    return 2
                else:
                    return corpus_create
                # else:
                #     return url_get
            else:
                return in_it
        except Exception as e:
            error = str(e)
            return error

    def add(self, target,location):
        try:
            repo = repomanager()
            return repo.add_(target,location)
        except Exception as e:
            error = str(e)
            return error

    def remote(self,name,data,gita,location):
        try:
            repo = repomanager()
            return repo.remote(name,data,gita, location)
        except Exception as e:
            error = str(e)
            return error

    def commit(self,message,location):
        try:
            repo = repomanager()
            return repo.commit(message,location)
        except Exception as e:
            error = str(e)
            return error

    def push(self,location):
        try:
            repo = repomanager()
            return repo.push(location)
        except Exception as e:
            error = str(e)
            return error

    def clone(self,arg,location):
        try:
            repo = repomanager()
            return repo.clone(arg,location)
        except Exception as e:
            error = str(e)
            return error

    def pull(self,file,location):
        try:
            repo = repomanager()
            repo.pull(file,location)
            return 1
        except Exception as e:
            error = str(e)
            return error

    
