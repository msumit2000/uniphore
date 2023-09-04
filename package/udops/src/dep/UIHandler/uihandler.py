from udops.src.dep.UIManager.uimanager import uimanager


class uihandler:

    def update_flag(self, corpus_name):
        uim = uimanager()
        return uim.update_flag(corpus_name)

    def init(self,file, location):
        uim = uimanager()
        corpus_properties = file
        return uim.create_corpus(corpus_properties, location)

    def add(self,target: str,location):
        uim = uimanager()
        return uim.add(target,location)

    def remote(self,name:str,data: str, gita: str, location):
        uim = uimanager()
        return uim.remote(name,data,gita,location)

    def commit(self,message: str, location):
        uim = uimanager()
        return uim.commit(message, location)

    def push(self, location):
        uim = uimanager()
        return uim.push(location)

    def clone(self,args:str,location):
        uim = uimanager()
        return uim.clone(args,location)

    def pull(self,audio,location):
        uim = uimanager()
        return uim.pull(audio,location)

    def get_s3_path(self,teamname,username):
        uim = uimanager()
        return uim.get_s3_path(teamname,username)

