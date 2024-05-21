""" db related functions """
import os
import pandas as pd
from opensearchpy import OpenSearch

_db_index = None
_db_host = None
_db_port = None
_db_user = None
_db_password = None
_db_allowed_languages = ["pl", "en"]

__db_conn = None



env_vars = "DB_HOST DB_PORT DB_USER DB_PASSWORD DB_ALLOWED_LANGUAGES DB_INDEX"
for e in env_vars.split():
    if e in os.environ:
        if e == "DB_ALLOWED_LANGUAGES":
            data = os.environ[e].lower().split(",")
            globals()["_" + e.lower()] = data
        else:
            globals()["_" + e.lower()] = os.environ[e]


def index_name():
    """ return opensearch index name """
    return _db_index


def get_db_client() -> OpenSearch:
    """ Return opensearch python client"""
    global __db_conn # pylint: disable=global-statement
    if not __db_conn:
        __db_conn = OpenSearch(
            hosts = [{'host': _db_host, 'port': _db_port}],
            http_compress = True, # enables gzip compression for request bodies
            http_auth = (_db_user, _db_password),
            use_ssl = True,
            verify_certs = False,
            ssl_assert_hostname = False,
            ssl_show_warn = False,
        )
    return __db_conn


def drob_db(args):
    """ drop db """

    client: OpenSearch = get_db_client()
    if _db_index not in client.indices.get("*"):
        raise Exception("Index not found:", _db_index)
    
    if not args.dry_run:
        res = client.indices.delete(index=_db_index)
        print(res)

def init_db(args):
    client: OpenSearch = get_db_client()
    if _db_index in client.indices.get("*"):
        raise Exception("Index allready present:", _db_index)
    
    mapping = {
        "properties": {
            "title":  {"type": "text"},
            "lang": {"type": "keyword"},
            "desc":  {"type": "text"},
            "institution": {"type": "keyword"},
            "service_type": {"type": "keyword"},
            "client_type": {"type": "keyword"},
            "url":  {"type": "text"},
            "email":  {"type": "text"},
        }
    }

    if not args.dry_run:
        res = client.indices.create(_db_index, body={"mappings": mapping})
        print(res)

def load_data(infile):
    """ initialize/update db with data from xlsx file """
    df = pd.read_excel(infile)
    new_columns = list(df.columns)

    new_columns[0] = "raw_id"
    new_columns[1] = "lang"
    new_columns[2] = "title"
    new_columns[3] = "desc"
    new_columns[4] = "service_type"
    new_columns[5] = "client_type"
    new_columns[6] = "institution"
    new_columns[7] = "url"
    new_columns[8] = "email"
    df.columns = new_columns

    if df.lang.hasnans:
        raise Exception("Empty values exist withing the language column")

    df.lang = df.lang.str.lower()
    df["id"] = df.raw_id + "_" + df.lang

    languages = set(df.lang)
    for l in languages:
        if l not in _db_allowed_languages:
            raise Exception(f"Found language '{l}', which is not present in allowed languages list ('{_db_allowed_languages}')." +
                             "please fix data in input file or extend allowed language list using DB_ALLOWED_LANGUAGES env var.")

    if len(set(df.id)) != df.id.shape[0]:
        ids = list(df.id)
        for val in set(df.id):
            ids.remove(val)
        raise Exception("duplicates found in computed id column:", ids)

    return df


def upload(args, quiet=True):
    """ Upload data. If args.dry_run and quiet==False report changes"""
    df = load_data(args.file)
    client: OpenSearch = get_db_client()

    xls_doc_cnt = 0
    new_doc_cnt = 0
    diff_doc_cnt = 0
    ids = []
    for _, row in df.iterrows():
        xls_doc_cnt += 1
        client_type = [x.strip() for x in row["client_type"].split(",")]
        service_type = [x.strip() for x in row["service_type"].split(",")]
        for i in range(len(client_type)):
            # note: do not use lower(), as capital 
            # letters may be important in some languages
            client_type[i] = client_type[i].strip()

        new_doc = {
            "title": row["title"],
            "lang": row["lang"],
            "desc": row["desc"],
            "institution": row["institution"],
            "service_type": service_type,
            "client_type": client_type,
            "url": row["url"],
            "email": row["email"]
        }

        for k, v in new_doc.items():
            if k == "client_type" or k == "service_type":
                if type(v) != list:
                    raise Exception("Internal error - expected list, got", type(v), v)
            else:
                if pd.isna(v):
                    new_doc[k] = ""

        ids.append(row["id"])
        if client.exists(index=_db_index, id=row["id"]):
            doc = client.get(index=_db_index, id=row["id"])["_source"]
            if doc == new_doc:
                continue

            diff_docs_cnt += 1
            if not quiet:
                print("\n\nOld/new entry differs:", row["id"], row["title"])
            all_keys = set(list(new_doc.keys()) + list(doc.keys()))
            for key in all_keys:
                action = False
                if key not in new_doc:
                    action = "delete"
                    val = doc[key]
                elif key not in doc:
                    action = "add"
                    val = new_doc[key]

                if action:
                    if not quiet:
                        print(f"- going to {action} field '{key}' with contents '{val}'")
                    continue

                val_old = doc[key]
                val_new = new_doc[key]

                if val_old != val_new and not quiet:
                    print(f"- going to change field '{key}':")
                    print("  - old value:", val_old)
                    print("  - new value:", val_new)

            if not args.dry_run:
                ret = client.update(index=_db_index, id=row["id"], body=new_doc)
                print(ret)
        else:
            new_doc_cnt += 1
            if not quiet:
                print("\n\nNew document", row["id"])
                for k, v in new_doc.items():
                    print(f"{k}: {v}")
            if not args.dry_run:
                ret = client.index(index=_db_index, id=row["id"], body=new_doc)
                print(ret)



    print("Operation complete:")
    print(f"Number of documents found in xls file: {xls_doc_cnt}")
    print(f"Number of differing documents found in xls file: {diff_doc_cnt}")
    print(f"Number of new documents found in xls file: {new_doc_cnt}")
