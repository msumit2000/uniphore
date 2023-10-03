from psycopg2.extras import RealDictCursor
import json
from udops.src.dep.Common.Constants import Constants
from udops.src.dep.config.Connection import *
from collections import Counter
connection = Connection()


class DatasetMetadatamanager:
    def list_corpus_names(self, filterValue):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            if not filterValue:
                cursor.execute(Constants.select_query)
                rows = cursor.fetchall()
                conn.commit()
                return rows
            else:
                mydict = self._filter(filterValue)
                counter = len(mydict)
                final_resp = []
                cursor.execute(
                    Constants.select_query_create+ mydict)
                rows = cursor.fetchall()
                final_resp.extend(rows)
                conn.commit()
                return final_resp

        except Exception as e:
            raise e

    def corpus_custom_fields(self , corpusname, kv_pairs):
        conn = connection.get_connection()
        cur = conn.cursor()
        cur.execute("select dataset_id from dataset_metadata where dataset_name = %s",(corpusname,))
        rows = cur.fetchall()
        for i in rows:
            c = i[0]
        for key, value in kv_pairs.items():
           cur.execute("insert into dataset_custom_fields(dataset_id, field_name, field_value) values (%s , %s , %s)",(c,key,value))
           print(key,":",value,"\n")

        conn.commit()
        cur.close()
        conn.close()

    def list_dataset_by_name(self, dataset_name, list_corpus1):
        try:
            conn = connection.get_connection()
            query = self._list_filter(list_corpus1)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(Constants.select_query_create + query)
            row = cursor.fetchall()
            return row
        except Exception as e:
            raise e

    def create_dataset(self, dataset_name, result_list, list_corpus, custom_field_file,training_corpus):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            data=()
            for each_data in result_list:
                data = (dataset_name,each_data['corpus_type'], list_corpus,training_corpus)
                
            cursor.execute(Constants.insert_query_dataset_metadata, data)
            conn.commit()
            cursor.execute(Constants.select_dataset_with_name + dataset_name + "'")
            corpus_details = cursor.fetchone()
            if custom_field_file != None:
                for row in custom_field_file:
                    key_list = list(row.keys())
                    value_list = list(row.values())
                    for key in key_list:
                        param_list = corpus_details["dataset_id"], key
                        cursor.execute("insert into dataset_custom_fields (dataset_id,field_name) values(%s,%s)",
                                       param_list)
                        conn.commit()
                    for value in value_list:
                        data1 = value, corpus_details["dataset_id"]
                        cursor.execute("update dataset_custom_fields set field_value =%s where dataset_id =%s", data1)
                        conn.commit()
            else:
                print("No Custom field ")
            for rows in range(0, len(result_list)):
                data = (corpus_details["dataset_id"], result_list[rows]["corpus_id"], result_list[rows]["corpus_name"])
                cursor.execute(Constants.insert_query_dataset_corpora, data)
                conn.commit()
        except Exception as e:
            raise e

    def create_dataset_by_filter_ds(self, corpus_list, dataset_name, filter_value, corpus_type, file,training_corpus):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            data = dataset_name, corpus_type, filter_value,training_corpus
            cursor.execute(Constants.insert_query_dataset_metadata, data)

            conn.commit()
            cursor.execute(Constants.select_dataset_with_name + dataset_name + "'")
            corpus_details = cursor.fetchone()

            if file != None:
                for r in file:
                    key_list = list(r.keys())
                    value_list = list(r.values())
                    for i in key_list:
                        param_list = corpus_details["dataset_id"], i
                        cursor.execute("insert into dataset_custom_fields (dataset_id,field_name) values(%s,%s)",
                                       param_list)
                        conn.commit()
                    for j in value_list:
                        data1 = j, corpus_details["dataset_id"]
                        cursor.execute("update dataset_custom_fields set field_value =%s where dataset_id =%s", data1)
                        conn.commit()
            else:
                print("No Custom field ")
            for row in corpus_list:
                cursor.execute(Constants.select_dataset_with_name + dataset_name + "'")
                corpus_details = cursor.fetchone()
                data = corpus_details["dataset_id"], row["corpus_id"], row["corpus_name"]
                cursor.execute(Constants.insert_query_dataset_corpora, data)
                conn.commit()
        except Exception as e:
            raise e

    def list_dataset_names_ds(self, corpus_type, json_loader, detailed_flag):
        conn = connection.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            for dict1 in json_loader:
                if len(json_loader) == 1 or dict1["filter_type"] == "custom_field":
                    data = (json_loader["filter_type"], json_loader["filter_value"])

                    query = Constants.select_dataset_query + json_loader[0]["filter_type"] + "='" + \
                            json_loader[
                                "filter_value"] + "'"
                
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    return rows
                elif len(json_loader) == 2 or dict1["filter_type"] == "custom_field":
                    query = Constants.select_dataset_query + json_loader[0]["filter_type"] + "='" + \
                            json_loader[0][
                                "filter_value"] + "' AND " + json_loader[1]["filter_type"] + "='" + json_loader[1][
                                "filter_value"] + "'"
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    print(rows)

                    return rows
                elif len(json_loader) == 3 or dict1["filter_type"] == "custom_field":

                    query = Constants.select_dataset_query + json_loader[0]["filter_type"] + "='" + \
                            json_loader[0][
                                "filter_value"] + "' AND " + json_loader[1]["filter_type"] + "='" + json_loader[1][
                                "filter_value"] + "' AND " + json_loader[2]["filter_type"] + "='" + json_loader[2][
                                "filter_value"] + "'"

                    cursor.execute(query)
                    rows = cursor.fetchall()

                    print(rows)

                    return rows
                elif len(json_loader) == 4:

                    query = Constants.select_dataset_query + json_loader[0]["filter_type"] + "='" + \
                            json_loader[0][
                                "filter_value"] + "' AND " + json_loader[1]["filter_type"] + "='" + json_loader[1][
                                "filter_value"] + "' AND " + json_loader[2]["filter_type"] + "='" + json_loader[2][
                                "filter_value"] + "' AND " + json_loader[3]["filter_type"] + "='" + json_loader[3][
                                "filter_value"] + "'"
                    
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    return rows

                elif dict1["filter_type"] == "custom_field":

                    pass
        except Exception as e:
            raise e

    def get_dataset_metadata(self, dataset_name):
        conn = connection.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(Constants.select_dataset_with_name+ dataset_name + "'")
        row = cursor.fetchall()
        return row

    def get_dataset_corpora(self, dataset_name):
        
        conn = connection.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(Constants.select_dataset_with_name+str(dataset_name)+"'")
        resp=cursor.fetchone()

        cursor.execute(Constants.select_datasetcorpora + str(resp["dataset_id"]) + "'")
        row = cursor.fetchall()

        return row

    def list_corpora(self, conn, dataset_name):
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(Constants.select_dataset_with_name + dataset_name + "'")
        row = cursor.fetchall()
        
        cursor.execute(Constants.select_datasetcorpora+ str(row[0]["dataset_id"]) + "'")
        resp = cursor.fetchall()
        r1 = []
        for row1 in resp:
            cursor.execute(Constants.metadata_select_query + str(row1["corpus_id"]) + "'")
            r1.append(cursor.fetchall())
        return r1

    def _filter(self, filterValue):
        sql = " where"
        for condition in str(filterValue).split(","):
            corpus_type, filter_condition_string = condition.split("::", 2)
            filter_condition_lst = filter_condition_string.split(":")
            filter_condition_flag = True if len(filter_condition_lst) % 2 == 0 else False
            if not filter_condition_flag:
                return "error"
            else:
                fiter_len = int(len(filter_condition_lst) / 2)
            index = 0
            sql += "( corpus_type = '"+ corpus_type+"' "
            for i in range(fiter_len):
                sql += " AND "+filter_condition_lst[index] + "='" + filter_condition_lst[index + 1] + "'"
                index += 2
            sql += ") OR "
        sql = sql[0:len(sql) - 4]
        return sql

    def _list_filter(self, filterValue):
        sql = " where"
        for condition in str(filterValue).split(","):
            corpus_type, filter_condition_string = condition.split("::", 2)
            filter_condition_lst = filter_condition_string.split(":")
        
            fiter_len = int(len(filter_condition_lst))
            index = 0
            sql += "( corpus_type = '" + corpus_type + "' and "
            for i in range(fiter_len):
                sql += "corpus_name='" + filter_condition_lst[index]+"' or "
                index += 1
            sql = sql[0:len(sql) - 4]
            sql += ") or "
        sql = sql[0:len(sql) - 4]
    #    print(sql)
        return sql

############## function for dataset api####### def get_summary(self,dataset_name,property):


    def get_summary(self,dataset_name):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"select dataset_corpus_list.corpus_name from dataset_metadata JOIN dataset_corpus_list \
                     ON dataset_metadata.dataset_id = dataset_corpus_list.dataset_id \
                     where dataset_metadata.dataset_name = '{dataset_name}';"
            cursor.execute(query)
            conn.commit()
            rows = cursor.fetchall()
            corpus_name =[]
            for row in rows:
                corpus_name.append(row["corpus_name"])
            final_dict ={}
            result =[]
            pro = ["language","corpus_type","source_type"]
            for property in pro:
                for name  in corpus_name:
                     q = f"select {property} from corpus_metadata where corpus_name ='{name}';"
                     cursor.execute(q)
                     r =cursor.fetchall()
                     a=f"{property}"
                     if len(r)==0 :
                          pass
                     else:
                        value = r[0][a]
                        result.append(value)
                counts = Counter(result)
                dict={}
                for letter, count in counts.items():
                    final_result = {letter: count}
                    dict.update(final_result)
                json_list = [{'key': k, 'value': v} for k, v in dict.items()]
                json_string = json.dumps(json_list)
                final_dict[property]=json_string
                result.clear()
            dataset=[]
            for key, value in final_dict.items():
                array_data = json.loads(value)
                data={}
                data["corpus_property"]=key
                data["countSummary"]=array_data
                dataset.append(data)
            conn.commit()
            cursor.close()
            return dataset
        except Exception as e:
            raise e

    def get_list(self):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = "select * from dataset_metadata"
            cursor.execute(query)
            rows= cursor.fetchall()
            conn.commit()
            cursor.close()
            return rows
        except Exception as e:
            raise e

    def search_dataset(self,property):
        try:
            if property=="":
                conn = connection.get_connection()
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                query = "select * from dataset_metadata"
                cursor.execute(query)
                rows= cursor.fetchall()
                conn.commit()
                cursor.close()
                return rows
            else:
                conn = connection.get_connection()
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                query = f"select dataset_id, dataset_name,corpus_type,corpus_filter from dataset_metadata where corpus_type='{property}';"
                cursor.execute(query)
                rows = cursor.fetchall()
                conn.commit()
                cursor.close()
                return rows
        except Exception as e:
            raise e

    def update(self,name,value):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"UPDATE dataset_metadata SET corpus_filter= '{value}'where dataset_name ='{name}';"
            cursor.execute(query)
            conn.commit()
            cursor.close()
            return 1
        except Exception as e:
            raise e
        
    def get_Counts(self):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("select count(*) from dataset_metadata ")
            count = cursor.fetchall()
            conn.commit()
            cursor.close()
            return count
        except Exception as e:
            print(e)

    def dataset_corpus_list(self,dataset_name):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"select dataset_corpus_list.corpus_name from dataset_corpus_list join dataset_metadata on dataset_corpus_list.dataset_id= dataset_metadata.dataset_id where dataset_metadata.dataset_name ='{dataset_name}';"
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            print(rows)
            return rows
        except Exception as e:
            raise e
