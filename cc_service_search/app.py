""" Main flask app"""

import flask
import os
import cc_service_search
app = flask.Flask(__name__, static_folder=None)

@app.route("/<path:path>")
def serve_static(path):
    """ Main handler for serving webpage static content"""
    return flask.send_from_directory("website_data/", path) # keep send_from_dir
                                                           # as it was designed to be
                                                           # immune against malformed paths



@app.route("/fallbackLocale", methods=["GET"])
def fallback_locale():
    """ Return fallback locale string - used when cookie/url quary string param are not used
         for specification and locale specified by the browser does not match avaliable one """
    
    return flask.jsonify({"lang": os.environ.get("FALLBACK_LOCALE", "en").lower()})


@app.route("/", methods=["GET"])
def index_html():
    """ Handle '/' """
    return flask.send_from_directory("website_data/", "index.html")


@app.route("/getFilterValues", methods=["GET"])
def get_filter_values():
    """ query for posible filter values """
    args = flask.request.args
    if not "lng" in args:
        return flask.jsonify({}) # TODO: 400  response ?

    language = args["lng"].lower() # todo: verify, that language is in lang list?

    client = cc_service_search.get_db_client()
    index = cc_service_search.index_name()

    body = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {"term": {"lang": language}},
                ]
            }
        },        
        "aggs": {
            "client_type": {
                "terms": {
                    "field": "client_type",
                    "size": 100
                }
            },
            "service_type": {
                "terms": {
                    "field": "service_type",
                    "size": 100
                }
            }
        }    
    }

    response = client.search(index=index, body=body)
    ret = {}
    todo = ["client_type", "service_type"]
    for t in todo:
        data = response["aggregations"][t]["buckets"]
        data_ret = []
        for entry in data:
            name = entry["key"]
            cnt = entry["doc_count"]
            data_ret.append([name, cnt])

        ret[t] = sorted(data_ret, key=lambda x: -x[1]) # returned data is sorted, 
                                                       # sorting added just in case sth changes
                                                       # in logic/call types    

    return flask.jsonify(ret)



@app.route("/query", methods=["GET"])
def query():
    """ query handler - convert query string into opensearch simple query """   

    args = flask.request.args
    if not "q" in args or not "lng" in args:
        return flask.jsonify({})

    query_string = args["q"]
    language = args["lng"].lower() # todo: verify, that language is in lang list?
    if not isinstance(query_string, str):
        return flask.jsonify({})    # TODO - 400 response

    client = cc_service_search.get_db_client()
    index = cc_service_search.index_name()
    body = {
        "size": 30, # TODO
        "query": {
            "bool": {
                "must": [
                    {"term": {"lang": language}}
                ]
            }
        }
    }

    if query_string:
        body["query"]["bool"]["must"].append(
            {"simple_query_string":{"query": query_string, "default_operator": "AND"}}
        )

    service_types = args["serviceTypes"].split(",")
    service_types = [x for x in service_types if x]
    if service_types:
        if [x for x in service_types if not isinstance(x, str)]:
            return flask.jsonify({}) # TODO - 400
        body["query"]["bool"]["must"].append({"terms":{"service_type": service_types}})

    client_types = args["clientTypes"].split(",")
    client_types = [x for x in client_types if x]
    if client_types:
        if [x for x in client_types if not isinstance(x, str)]:
            return flask.jsonify({}) # TODO - 400
        body["query"]["bool"]["must"].append({"terms":{"client_type": client_types}})


    ret = client.search(index=index, body=body)
    hits = ret["hits"]["hits"]
    hits = [h["_source"] for h in hits]

    return flask.jsonify(hits)
