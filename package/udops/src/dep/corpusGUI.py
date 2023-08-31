# commit
from udops.src.dep.UIHandler.uiauthentication import authentication
from udops.src.dep.UIHandler.uihandler import uihandler
import re

try:

    class GUI:

        def create_corpus(self, data):
            try:
                auth = authentication()
                user_id = auth.authenticate_user(data['username'])
                if user_id == 0:
                    return 0
                else:
                    team_id = auth.get_user_team(data['teamname'])
                    if team_id == 0:
                        return 2
                    else:
                        location = auth.get_team_location(data['teamname'])
                        if location == 0:
                            return 3
                        else:
                            corpus_details = {
                                "corpus_name": data['corpus_name'],
                                "corpus_type": data['corpus_type'],
                                "language": data['language'],
                                "source_type": data['source_type'],
                                "vendor": data['vendor'],
                                "domain": data['domain'],
                                "description": data['description'],
                                "lang_code": data['lang_code'],
                                "acquisition_date": data['acquisition_date'],
                                "migration_date": data['migration_date'],
                                "flag":data['flag']
                            }
                            uih = uihandler()
                            create_corpus = uih.init(corpus_details, data['source'],location)
                            if create_corpus == 1:
                                corpus_id = auth.corpus_id(data['corpus_name'])
                                auth.default_acess(corpus_id, user_id)
                                auth.Corpus_team_map(team_id, corpus_id)
                                return 1
                            elif create_corpus == 2:
                                return 4
                            else:
                                return create_corpus
            except Exception as e:
                error = str(e)
                return error

        def add(self, data):
            uih = uihandler()
            auth = authentication()
            location = auth.get_team_location(data["teamname"])
            if location == 0:
                return 2
            else:
                return uih.add(data["target"],location)

        # def remote(self,teamname:str, name: str, data: str, gita: str):
        def remote(self, data):
            uih = uihandler()
            if re.sub(r'^.*/(.*?)(\.git)?$', r'\1', data['gita']) == data['name']:
                auth = authentication()
                location = auth.get_team_location(data["teamname"])
                if location == 0:
                    return 2
                else:
                    return uih.remote(data['name'], data['data'], data['gita'], location)

        # def commit(self, teamname,message: str):
        def commit(self, data):
            uih = uihandler()
            auth = authentication()
            location = auth.get_team_location(data["teamname"])
            if location == 0:
                return 2
            else:
                return uih.commit(data['message'],location)

        def push(self, data):
            try:
                uih = uihandler()
                auth = authentication()
                user_id = auth.authenticate_user(data['username'])
                if user_id == 0:
                    return 0
                else:
                    corpus_id = auth.corpus_id(data['corpus_name'])
                    access_type = "write"
                    access = auth.authorize_user(user_id, corpus_id, access_type)
                    auth = authentication()
                    location = auth.get_team_location(data["teamname"])
                    if location == 0:
                        return 2
                    else:
                        if access == 0:
                            return 3
                        else:
                            if uih.push(location) == 1:
                                return 1
                            else:
                                return uih.push(location)

            except Exception as e:
                return e

        def clone(self, data):
            try:
                uih = uihandler()
                auth = authentication()
                user_id = auth.authenticate_user(data['username'])
                if user_id == 0:
                    return 0
                else:
                    corpus_id = auth.corpus_id(data['corpus_name'])
                    access = auth.authorize_user_clone(user_id, corpus_id)
                    auth = authentication()
                    location = auth.get_team_location(data["teamname"])
                    if location == 0:
                        return 2
                    if access == 0:
                        return 3
                    else:
                        if uih.clone(data['corpus_name'],data['gita'],location) == 1:
                            flag = uih.update_flag(data['corpus_name'])
                            if flag == 1:
                                return 1
                            else:
                                return flag
                        else:
                            return uih.clone(data['corpus_name'],data['gita'],location)
            except Exception as a:
                return a

        def pull(self, data):
            try:
                uih = uihandler()
                auth = authentication()
                user_id = auth.authenticate_user(data['username'])
                if user_id == 0:
                    return 0
                else:
                    corpus_id = auth.corpus_id(data['corpus_name'])
                    access_type = "write"
                    access = auth.authorize_user(user_id, corpus_id, access_type)
                    auth = authentication()
                    location = auth.get_team_location(data["teamname"])
                    if location == 0:
                        return 2
                    else:
                        if access == 0:
                            return 3
                        else:
                            if uih.pull(data['folder'],location) == 1:
                                return 1
                            else:
                                return uih.pull(data['folder'],location)
            except Exception as e:
                return e

except Exception as e:
    raise e