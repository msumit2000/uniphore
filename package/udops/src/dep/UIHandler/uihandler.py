from udops.src.dep.UIManager.uimanager import uimanager


class uihandler:

    def update_flag(self, corpus_name):
        uim = uimanager()
        return uim.update_flag(corpus_name)

    def init(self, file, target,location):
        uim = uimanager()
        corpus_properties = file
        return uim.create_corpus(corpus_properties, target, location)

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

    def clone(self,corpus_name,args:str,location):
        uim = uimanager()
        return uim.clone(corpus_name,args,location)

    def pull(self,audio,location):
        uim = uimanager()
        return uim.pull(audio,location)

