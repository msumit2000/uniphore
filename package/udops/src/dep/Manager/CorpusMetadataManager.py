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
                    # conn.close()
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
                    cursor.close()
                    return rows
                else:
                    return Constants.corpus_error
        except Exception as e:
            print(e)

    def get_corpus_metadata_by_id(self, corpus_id, conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                Constants.query_metadta + corpus_id + "'")
            rows = cursor.fetchone()
            cursor.execute(Constants.query_metadta + corpus_id + "'")
            rows1 = cursor.fetchall()  # for corpus_custom_field

            return rows1
        except Exception as e:
            print(e)

    def get_corpus_metadata_by_type(self, corpus_type, conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(Constants.metadata_select_query_type + corpus_type + "'")
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
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
                    return final_resp

        except Exception as e:
            print(e)

    def create_corpus(self, json_loader, conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(Constants.create_metadata_table)
            cursor.execute(Constants.create_custom_table)
            corpus_name = json_loader["corpus_name"]
            query = f"select corpus_id from corpus_metadata where corpus_name = '{corpus_name}'"
            cursor.execute(query)
            row = cursor.fetchone()
            if len(row) == 0:
                return 0
            else:
                data = json_loader["corpus_name"], json_loader["corpus_type"], json_loader["language"], json_loader[
                    "source_type"], \
                    json_loader["vendor"], json_loader["domain"], json_loader["description"], json_loader["lang_code"], \
                    json_loader["acquisition_date"], json_loader["migration_date"]

                cursor.execute(
                    Constants.insert_query_metadata,
                    data)
                cursor.execute(Constants.query_metadata + json_loader["corpus_name"] + "'")
                conn.commit()
                cursor.close()

                return 1
            # conn.close()
        except Exception as e:
            print(e)

    def update_corpus(self, json_loader, conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            corpus_name = json_loader["corpus_name"]
            #           cursor.execute(Constants.query_metadata + json_loader["corpus_name"] + "'")
            query = f"select * from corpus_metadata where corpus_name='{corpus_name}'"
            cursor.execute(query)
            rows = cursor.fetchall()
            #            print(len(rows))
            if len(rows) == 0:
                return 0
            else:
                for key, value in json_loader.items():
                    cursor = conn.cursor(cursor_factory=RealDictCursor)
                    query = f"UPDATE corpus_metadata SET {key}='{value}' where corpus_name ='{corpus_name}'"
                    cursor.execute(query)
                    conn.commit()
                return 1
        except Exception as e:
            print(e)

    def update_timestamp(self, conn, args):
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(Constants.update_ts_query, args)
        conn.commit()
        cursor.close()

    def update_corpus_remote(self, name, args1, args2, conn):
        cursor = conn.cursor()
        input_remote_tuple = (args2, args1, name)
        cursor.execute("update corpus_metadata set git_remote = %s, remote_location = %s where corpus_name=%s",
                       input_remote_tuple)
        conn.commit()
        cursor.close()

    def corpus_custom_fields(self, corpusname, kv_pairs, conn):
        cur = conn.cursor()
        cur.execute("select corpus_id from corpus_metadata where corpus_name = %s", (corpusname,))
        rows = cur.fetchall()
        for i in rows:
            c = i[0]
        for key, value in kv_pairs.items():
            cur.execute("insert into corpus_custom_fields(corpus_id, field_name, field_value) values (%s , %s , %s)",
                        (c, key, value))
            print(key, ":", value, "\n")

        conn.commit()
        cur.close()

    def delete_corpus(self, corpusname, conn):
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            query1 = f"SELECT corpus_id FROM corpus_metadata where corpus_name ='{corpusname}'"
            cur.execute(query1)
            rows = cur.fetchone()
            if rows is None:
                print("Corpus not found")
            else:
                corpus_id = rows['corpus_id']
                #  query2 = f"DELETE FROM cfg_udops_teams_acl WHERE corpus_id ={corpus_id}"

                cur.execute(f"DELETE FROM cfg_udops_teams_acl WHERE corpus_id ={corpus_id}")
                cur.execute(f"DELETE FROM cfg_udops_acl WHERE corpus_id ={corpus_id}")
                cur.execute("DELETE FROM corpus_metadata WHERE corpus_name = %s", (corpusname,))
                print("Deleted corpus ", corpusname)
                conn.commit()
                cur.close()
        except Exception as e:
            err = str(e)
            print(err)

    def _filter(self, filterValue):
        filters = filterValue.split(",")
        resp = []
        for filter_con in filters:
            condition = filter_con.split(":")
            resp.append(condition)
        return resp

    ################### CORPUS API #############################

    def get_Counts(self, conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(Constants.select_query2)
            count = cursor.fetchall()
            conn.commit()
            cursor.close()
            return count
        except Exception as e:
            print(e)

    def list_corpus(self, language, corpus_type, source_type, conn):
        try:
            lan = language
            cor_type = corpus_type
            sor_type = source_type
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            query = (f"SELECT corpus_id, corpus_name, corpus_type, language, source_type, migration_date,"
                     f"lastupdated_ts , description, acquisition_date, (SELECT teamname FROM cfg_udops_teams_metadata"
                     f" tm WHERE tm.team_id IN ( SELECT team_id FROM cfg_udops_teams_acl cta WHERE "
                     f"cta.corpus_id = corpus_metadata.corpus_id )) AS teamname FROM corpus_metadata WHERE "
                     f"language IN (SELECT * FROM unnest(%s)) and corpus_type IN (SELECT * FROM unnest(%s)) "
                     f"and source_type IN (SELECT * FROM unnest(%s))")

            cursor.execute(query, (lan, cor_type, sor_type))
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            if len(rows) == 0:
                return 0
            else:
                return rows
        except Exception as e:
            print(e)

    def language(self, conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(f"select DISTINCT language from corpus_metadata")
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            return rows
        except Exception as e:
            print(e)

    def source_type(self, conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(f"select DISTINCT source_type from corpus_metadata")
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            return rows
        except Exception as e:
            print(e)

    def corpus_type(self, conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(f"select DISTINCT corpus_type from corpus_metadata")
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            return rows
        except Exception as e:
            print(e)

    def search_corpus(self, corpus_name, conn):
        try:
            if corpus_name == "":
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("SELECT corpus_id, corpus_name, corpus_type, language, source_type, "
                               "lastupdated_ts, (SELECT teamname FROM cfg_udops_teams_metadata"
                               " tm WHERE tm.team_id IN (SELECT team_id FROM cfg_udops_teams_acl cta"
                               " WHERE cta.corpus_id = corpus_metadata.corpus_id ) ) AS team_name FROM"
                               " corpus_metadata")
                rows = cursor.fetchall()
                conn.commit()
                cursor.close()
                return rows
            else:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                query = (f"SELECT corpus_id, corpus_name, corpus_type, language, source_type, "
                         f"lastupdated_ts, (SELECT teamname FROM cfg_udops_teams_metadata "
                         f"tm WHERE tm.team_id IN (SELECT team_id FROM cfg_udops_teams_acl cta "
                         f"WHERE cta.corpus_id = corpus_metadata.corpus_id ) ) AS team_name FROM corpus_metadata"
                         f" WHERE corpus_name ILIKE '%{corpus_name}%'")
                cursor.execute(query)
                rows = cursor.fetchall()
                conn.commit()
                cursor.close()
                if rows == None:
                    return 0
                else:
                    return rows
        except Exception as e:
            return e

    def summary(self, conn, column):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            col = column
            query1 = f"select DISTINCT {col} from corpus_metadata"
            cursor.execute(query1)
            rows = cursor.fetchall()
            col_list = [dictionary[col] for dictionary in rows]
            dict = {}

            for i in range(len(col_list)):
                data = col_list[i]
                query = f"SELECT COUNT(*) FROM corpus_metadata WHERE {col} = '{data}'"
                cursor.execute(query)
                # cursor.execute("SELECT COUNT(*) FROM corpus_metadata WHERE language =%s", (data,))
                result = cursor.fetchone()
                count = result['count']
                final_result = {data: count}
                dict.update(final_result)
            json_list = [{'key': k, 'value': v} for k, v in dict.items()]
            json_string = json.dumps(json_list)
            conn.commit()
            cursor.close()
            #   conn.close()
            return json_string
        except Exception as e:
            return e

    def donut(self, conn, column):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            col = column
            query1 = f"select DISTINCT {col} from corpus_metadata"
            cursor.execute(query1)
            rows = cursor.fetchall()
            col_list = [dictionary[col] for dictionary in rows]
            value = []
            for i in range(len(col_list)):
                data = col_list[i]
                query = f"SELECT COUNT(*) FROM corpus_metadata WHERE {col} = '{data}'"
                cursor.execute(query)
                result = cursor.fetchone()
                count = result['count']
                value.append(count)
            conn.commit()
            cursor.close()
            # conn.close()
            return col_list, value
        except Exception as e:
            return e

    def summary_cutom(self, conn, corpus_name):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            q = f"SELECT corpus_custom_fields.field_name, corpus_custom_fields.field_value FROM corpus_custom_fields JOIN corpus_metadata ON corpus_custom_fields.corpus_id= corpus_metadata.corpus_id WHERE corpus_metadata.corpus_name= '{corpus_name}'; "
            cursor.execute(q)
            rows = cursor.fetchall()
            dictionary = {}
            for row in rows:
                key = row['field_name']
                value = row['field_value']
                dictionary[key] = value
            json_list = [{'key': k, 'value': v} for k, v in dictionary.items()]
            json_string = json.dumps(json_list)
            conn.commit()
            cursor.close()
            return json_string
        except Exception as e:
            return e

    def update_custom_field(self, data, conn):
        try:
            for obj in data:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                field_name = obj['field_name']
                field_value = obj['field_value']
                corpus_name = obj['corpus_name']
                query = f"select corpus_id from corpus_metadata where corpus_name ='{corpus_name}';"
                cursor.execute(query)
                rows = cursor.fetchone()
                c_id = rows['corpus_id']
                query_1 = f"UPDATE corpus_custom_fields SET field_value = " \
                          f"'{field_value}' where corpus_id = {c_id} AND field_name = '{field_name}';"
                cursor.execute(query_1)
                conn.commit()
                cursor.close()
            return 1
        except Exception as e:
            return e
