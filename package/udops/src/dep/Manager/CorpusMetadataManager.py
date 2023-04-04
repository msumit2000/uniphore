from udops.src.dep.Common.Constants import Constants
import json
from psycopg2.extras import RealDictCursor

    
class CorpusMetadataManager:
    def list_corpus_names1(self, filterValue, conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            if not filterValue:
                cursor.execute(Constants.select_query)
                rows = cursor.fetchall()
                conn.commit()
                return rows
            else:
                print("*************************")
                mydict = json.loads(filterValue)
                if len(mydict) == 1:
                    cursor.execute(
                        Constants.select_query1 + list(mydict.keys())[0] + "= '" + list(mydict.values())[
                            0] + "'")
                    rows = cursor.fetchall()
                    conn.commit()
                    return rows
                elif len(mydict) == 2:
                    cursor.execute(
                        Constants.select_query1 + list(mydict.keys())[0] + "= '" + list(mydict.values())[
                            0] + "' AND " + list(mydict.keys())[1] + "= '" + list(mydict.values())[1] + "'")
                    rows = cursor.fetchall()
                    conn.commit()
                    conn.close()
                    cursor.close()
                    return rows
                elif len(mydict) == 3:
                    cursor.execute(
                        Constants.select_query1 + list(mydict.keys())[0] + "= '" + list(mydict.values())[
                            0] + "' AND " + list(mydict.keys())[1] + "= '" + list(mydict.values())[1] + "' AND " +
                        list(mydict.keys())[
                            2] + "= '" + list(mydict.values())[2] + "'")
                    rows = cursor.fetchall()
                    conn.commit()
                    return rows
                elif len(mydict) == 4:
                    cursor.execute(
                        Constants.select_query1 + list(mydict.keys())[0] + "= '" + list(mydict.values())[
                            0] + "' AND " + list(mydict.keys())[1] + "= '" + list(mydict.values())[1] + "' AND " +
                        list(mydict.keys())[
                            2] + "= '" + list(mydict.values())[2] + "' AND " + list(mydict.keys())[
                            3] + "= '" + list(mydict.values())[3] + "'")
                    rows = cursor.fetchall()
                    conn.commit()
                    conn.close()
                    cursor.close()
                    return rows
                elif len(mydict) == 5:
                    cursor.execute(
                        Constants.select_query1 + list(mydict.keys())[0] + "= '" + list(mydict.values())[
                            0] + "' AND " + list(mydict.keys())[1] + "= '" + list(mydict.values())[1] + "' AND " +
                        list(mydict.keys())[
                            2] + "= '" + list(mydict.values())[2] + "' AND " + list(mydict.keys())[
                            3] + "= '" + list(mydict.values())[3] + "' AND" + list(mydict.keys())[4] + "= '" +
                        list(mydict.values())[4] + "'")
                    rows = cursor.fetchall()
                    conn.commit()
                    conn.close()
                    cursor.close()
                    return rows
                else:
                    return Constants.corpus_error
        except Exception as e:
            print(e)

    def get_corpus_metadata_by_id(self, corpus_id, conn):
        try:
            print(corpus_id)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                Constants.query_metadta + corpus_id + "'")
            rows = cursor.fetchone()
            cursor.execute(Constants.query_metadta + corpus_id + "'")
            rows1 = cursor.fetchall()  # for corpus_custom_field
         #   conn.commit()
        #    conn.close()
          #  cursor.close()
            return rows1
        except Exception as e:
            print(e)

    def get_corpus_metadata_by_type(self, corpus_type, conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(Constants.metadata_select_query_type + corpus_type + "'")
            rows = cursor.fetchall()
            conn.commit()
            conn.close()
            cursor.close()
      #      print(rows)
            return rows
        except Exception as e:
            print(e)
    
    def list_corpus_names(self, filterValue, conn):
        try:

            cursor = conn.cursor(cursor_factory=RealDictCursor)
            if not filterValue:
                cursor.execute(Constants.select_query)
                rows = cursor.fetchall()
                conn.commit()
                return rows
            else:
                mydict = self._filter(filterValue)
                # mydict = json.loads(filterValue)
                counter = len(mydict)

                while len(mydict) >= counter:
                    final_resp = []
                    for condition_list in mydict:
                        if len(condition_list) == 3:
                            cursor.execute(
                                "select * from corpus_metadata where corpus_type='" + condition_list[0] + "' AND " +
                                condition_list[1] + "='" + condition_list[2] + "'")
                            rows = cursor.fetchall()
                            final_resp.extend(rows)
                            conn.commit()
                            counter = counter - 1
                        else:
                            raise Exception("Please validate filter Condition!!")
                    # print(final_resp)
                    return final_resp

        except Exception as e:
            print(e)


    def create_corpus(self, json_loader, conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(Constants.create_metadata_table)
            cursor.execute(Constants.create_custom_table)
            data = json_loader["corpus_name"], json_loader["corpus_type"], json_loader["language"], json_loader[
                "source_type"], \
                   json_loader["vendor"], json_loader["domain"],json_loader["description"],json_loader["lang_code"],json_loader["acquisition_date"], json_loader["migration_date"]

            cursor.execute(
                Constants.insert_query_metadata,
                data)
            cursor.execute(Constants.query_metadta + json_loader["corpus_name"] + "'")
            corpus_details = cursor.fetchone()
            for row in json_loader["custom_fields"]:
                param_list = corpus_details["corpus_id"], row["field_name"], row["field_value"]

                cursor.execute(Constants.insert_query_custom_field,
                               param_list)
            print("success")
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(e)

    def update_corpus(self, json_loader, conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(Constants.metadata_select_query + json_loader["corpus_id"] + "'")
            rows = cursor.fetchall()
            if len(rows) == 0:
                return Constants.corpus_error
            else:
                for row in rows:
                    if row["corpus_name"] != json_loader["corpus_name"] and row["corpus_type"] != json_loader[
                        "corpus_type"] \
                            and row["language"] != json_loader["language"]:
                        return Constants.corpus_error
                    elif json_loader["source_type"] != row["source_type"] or json_loader["customer_name"] != row[
                        "customer_name"] or json_loader["data_domain_name"] != row["data_domain_name"]:

                        data1 = json_loader["source_type"], json_loader["customer_name"], json_loader[
                            "data_domain_name"], \
                                json_loader["corpus_id"]
                        cursor.execute(Constants.update_query, data1)  # corpus_id update condition
                        conn.commit()
                        cursor.close()
                        conn.close()
        except Exception as e:
            print(e)

    def update_timestamp(self, conn, args):
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(Constants.update_ts_query, args)
        conn.commit()
        conn.close()
        cursor.close()
    
    def update_corpus_remote(self,name,args1,args2,conn):
        cursor=conn.cursor()
        input_remote_tuple=(args2,args1,name)
        cursor.execute("update corpus_metadata set git_remote = %s, remote_location = %s where corpus_name=%s",input_remote_tuple)
        conn.commit()
        conn.close()
        cursor.close()
   
    def corpus_custom_fields(self ,corpusname,kv_pairs, conn):
        cur = conn.cursor()
        cur.execute("select corpus_id from corpus_metadata where corpus_name = %s",(corpusname,))
        rows = cur.fetchall()
        for i in rows:
            c = i[0]
        print(c)
        for key, value in kv_pairs.items():
           cur.execute("insert into corpus_custom_fields(corpus_id, field_name, field_value) values (%s , %s , %s)",(c,key,value))
           print(key,":",value,"\n")
           
        conn.commit()
        cur.close()
        conn.close()

    def delete_corpus(self, corpusname,conn):
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("DELETE FROM corpus_metadata WHERE corpus_name = %s",(corpusname,))
        print("Deleted corpus ",corpusname)
        conn.commit()
        cur.close()
        conn.close()
    
    def _filter(self, filterValue):
        filters = filterValue.split(",")
        resp = []
        for filter_con in filters:
            condition = filter_con.split(":")
            resp.append(condition)

        return resp

