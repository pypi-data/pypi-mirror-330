import pymongo


def track_request(conn_str, db_name, collection_name, service_provider, key_in_use, SKU, URL, status_code,
                  request_type):
    """
    Tracks the request by updating the count in MongoDB.

    :param conn_str: MongoDB connection string
    :param db_name: Database name
    :param collection_name: Collection (table) name
    :param service_provider: Static value declared by the user
    :param key_in_use: Static key declared by the user
    :param SKU: SKU identifier
    :param URL: URL being tracked
    :param status_code: Status code of the request
    :param request_type: Type of request (e.g., 'review', 'retry', etc.)
    """
    # Establish connection
    connmn = pymongo.MongoClient(conn_str)
    mydb = connmn[db_name]
    collection = mydb[collection_name]

    # Fetch existing record
    record = collection.find_one({'SKU': SKU, 'URL': URL})
    review_count = record.get(request_type, 0) if record else 0

    new_count = review_count + 1
    if review_count == 0:
        collection.insert_one({
            'key_in_use': key_in_use,
            'service_provider': service_provider,
            'SKU': SKU,
            'URL': URL,
            'status_code': status_code,
            request_type: new_count
        })
    else:
        collection.update_one(
            {'SKU': SKU, 'URL': URL},
            {'$set': {request_type: new_count}}
        )


if __name__ == '__main__':
    track_request('mongodb://bhumikab:D3$X&71*@192.168.0.50:27017/?authSource=admin','haier_us_s_n_us_2762_1','retry_graph_2025_02_28','scraper','xxxxxxxxxxxxxxxxxxxxxxxxx794abd','B0CKZCX4D7',
                  'https://www.amazon.com/dp/B0CKZCX4D7','200','review_retry_count')