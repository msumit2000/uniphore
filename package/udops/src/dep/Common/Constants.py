class Constants:
    # list queries
    select_query = "select * from public.corpus_metadata"
    select_query1 = "select * from corpus_metadata where "

    # corpus_metadata query
    metadata_select_query = "select * from corpus_metadata where corpus_id='"
    metadata_select_query_type = "select * from corpus_metadata where corpus_type='"

    # create corpus
    insert_query_metadata = "insert into corpus_metadata (corpus_name,corpus_type,language,source_type,vendor,domain,description,lang_code,acquisition_date, migration_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    insert_query_custom_field = "insert into corpus_custom_fields (corpus_id,field_name,field_value) values(%s,%s,%s)"
    select_query_create = "select * from corpus_metadata "
    query_metadta="select * from corpus_metadata where corpus_name='"
    query_corpus_type="select * from corpus_metadata where corpus_name='"
#    select_query_create = "select * from corpus_metadata "

    # Update Corpus
    update_query = "UPDATE corpus_metadata SET source_type=%s,customer_name=%s,data_domain_name= %s WHERE corpus_id=(%s) "
    corpus_error = "Corpus Doesnt Exist"
    
    #Delete Corpus
    delete_query = "DELETE from corpus_metadata where corpus_name = (%s) "
    # update_timestamp
    update_ts_query = "UPDATE corpus_metadata SET  lastUpdated_ts= timezone(INTERVAL '+00:00', now()) where corpus_name=(%s)"

    # Constants File
    file_location = "/DatabaseConnection.properties"

    # Create table
    create_custom_table = "create TABLE if not exists corpus_custom_fields( field_id serial,corpus_id int, field_name varchar(200) NOT NULL,field_value text DEFAULT NULL,creationTimestamp TIMESTAMP without time zone default timezone(INTERVAL '+00:00', now()),lastUpdated_ts TIMESTAMP without time zone default timezone(INTERVAL '+00:00', now()),primary key(field_id),CONSTRAINT corpus_custom_fields_fk_1 FOREIGN KEY (corpus_id) REFERENCES corpus_metadata(corpus_id) ON DELETE cascade)"
    create_metadata_table = "create table if not exists corpus_metadata(corpus_id serial,corpus_name varchar(200) not null UNIQUE,corpus_type varchar(200) not NULL, language varchar(200) not NULL,source_type varchar(200),customer_name varchar(200), data_domain_name varchar(200), creationTimestamp TIMESTAMP without time zone default timezone(INTERVAL '+00:00', now()),lastUpdated_ts TIMESTAMP without time zone default timezone(INTERVAL '+00:00', now()),primary key(corpus_id))"

    # Dataset queries
    select_dataset_with_name = "select * from dataset_metadata where dataset_name= '"
    select_dataset_query = "select * from dataset_custom_fields where"
    select_dataset_with_id = "select * from dataset_metadata where dataset_id='"
    select_datasetcorpora = "select * from dataset_corpus_list where dataset_id='"
    metadata_select_query = "select * from corpus_metadata where corpus_id='"

    # insert dataset queries
    create_dataset_metadata = '''CREATE TABLE IF NOT EXISTS public.dataset_metadata( dataset_id integer NOT NULL DEFAULT nextval('"dataset_metadata_datasetId _seq"'::regclass), dataset_name character varying COLLATE pg_catalog."default" NOT NULL,corpus_type character varying COLLATE pg_catalog."default",corpus_filter character varying COLLATE pg_catalog."default",created_ts timestamp without time zone DEFAULT timezone('00:00:00'::interval, now()),lastupdated_ts timestamp without time zone DEFAULT timezone('00:00:00'::interval, now()),CONSTRAINT dataset_metadata_pkey PRIMARY KEY (dataset_id))TABLESPACE pg_default'''
    create_dataset_custom_fields = '''
    CREATE TABLE IF NOT EXISTS public.dataset_custom_fields
    (
        dataset_id integer NOT NULL DEFAULT nextval('dataset_custom_fields_dataset_id_seq'::regclass),
        field_id integer NOT NULL DEFAULT nextval('dataset_custom_fields_field_id_seq'::regclass),
        field_name character varying COLLATE pg_catalog."default",
        field_value character varying COLLATE pg_catalog."default",
        CONSTRAINT dataset_custom_fields_pkey PRIMARY KEY (field_id),
        CONSTRAINT dataset_id FOREIGN KEY (dataset_id)
            REFERENCES public.dataset_metadata (dataset_id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )
    
    TABLESPACE pg_default'''

    create_dataset_corpous_list = '''CREATE TABLE IF NOT EXISTS public.dataset_corpus_list
    (
        dataset_id integer NOT NULL DEFAULT nextval('dataset_corpus_list_dataset_id_seq'::regclass),
        corpus_id integer NOT NULL DEFAULT nextval('dataset_corpus_list_corpus_id_seq'::regclass),
        corpus_name character varying COLLATE pg_catalog."default",
        corpus_version character varying COLLATE pg_catalog."default",
        CONSTRAINT dataset_id FOREIGN KEY (dataset_id)
            REFERENCES public.dataset_metadata (dataset_id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )
    
    TABLESPACE pg_default'''

    # insert query
    insert_query_dataset_metadata = "insert into dataset_metadata (dataset_name,corpus_type,corpus_filter,corpus_training) values (%s,%s,%s,%s)"
    insert_query_dataset_custom = "insert into dataset_custom_fields (dataset_id,field_name,field_value) values(%s,%s,%s)"
    insert_query_dataset_corpora = "insert into dataset_corpus_list (dataset_id, corpus_id,corpus_name) values(%s,%s,%s)"
