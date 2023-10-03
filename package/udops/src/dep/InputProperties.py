import os
class properties:
  #  path1 = os.getcwd()
    def input_properties(self,path,corpus_name,output,result):
        path1=os.getcwd()
        dir_path = os.path.dirname(os.path.realpath(__file__))

        for resp in result:
            #output["data_dir_path"].append(os.getcwd()+"/hinglish")
            if resp["field_name"] == "template_file_path":
                output["template_file_path"].append(path+"/" + resp["field_value"])
                output["data_dir_path"].append(path+"/"+corpus_name)
            elif resp["field_name"] == "native_schema":
                output["native_schema"].append(path+"/" + resp["field_value"])
            elif resp["field_name"] == "common_schema":
                output["common_schema"].append(dir_path + resp["field_value"])
        return output
