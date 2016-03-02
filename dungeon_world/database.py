from pymongo import MongoClient

ASCENDING = 1
DESCENDING = -1

class Database(object):
    """ MongoDB database and collections used in the project """

    def __init__(self, mongourl, dbname):
        self.client = MongoClient(mongourl)
        self.database = self.client[dbname]

    def create(self, collection, document):
        if document is not None:
            self.database[collection].insert(document)
        else:
            raise Exception("Nothing to save, because document parameter is None")
            logger.warning("A document could not be created in MongoDB Collection: %s" % (collection))

    def read(self, collection, query={}, document_id=None, desc_order=False, asc_order=False):
        if document_id is None:
            if desc_order:
                return self.database[collection].find(query).sort("$natural",DESCENDING)
            elif asc_order:
                return self.database[collection].find(query).sort("$natural",ASCENDING)
            else:
                return self.database[collection].find(query)
        else:
            if desc_order:
                return self.database[collection].find({"_id":document_id}).sort("$natural",DESCENDING)
            elif asc_order:
                return self.database[collection].find({"_id":document_id}).sort("$natural",ASCENDING)
            else:
                return self.database[collection].find({"_id":document_id})

    def read_one(self, collection, query={}, document_id=None):
        if document_id is None:
            return self.database[collection].find_one(query)
        else:
            return self.database[collection].find_one({"_id":document_id})

    def read_with_projection(self, collection, projection, query={}, document_id=None ):
        if document_id is None:
            return self.database[collection].find(query, projection)
        else:
            return self.database[collection].find({"_id":document_id}, projection)

    def read_one_with_projection(self, collection, projection, query={}, document_id=None ):
        if document_id is None:
            return self.database[collection].find_one(query, projection)
        else:
            return self.database[collection].find_one({"_id":document_id}, projection)

    def read_lastXdocuments(self, collection, amount, query={} ):
        return self.database[collection].find(query).sort("$natural",DESCENDING).limit(amount)

    def read_last_one(self, collection, query={} ):
        cursor = self.database[collection].find(query).sort("$natural",DESCENDING).limit(1)
        return cursor[0]

    def exists_document(self, collection, query={}, document_id=None):
        if document_id is None:
            cursor = self.database[collection].find(query).limit(1)
        else:
            cursor = self.database[collection].find({"_id":document_id}).limit(1)
        if cursor.count() > 0:
            return True
        else:
            return False

    def update(self, collection, query, value, upsert=False):
        self.database[collection].update_many(query,{"$set": value},upsert=upsert)

    def update_byID(self, collection, document):
        """ Use update if the _id exists, if not use insert """
        if document is not None:
            self.database[collection].save(document)
        else:
            raise Exception("Nothing to update, because project parameter is None")
            logger.warning("A document could not be updated in MongoDB Collection: %s" % (collection))

    def update_one_array_addtoset(self, collection, array, value, query={}, upsert=False):
        x = self.database[collection].update_one(query,{"$addToSet": {array: value}},upsert=upsert)
        return x

    def update_one_array_pull(self, collection, array, value, query={}, upsert=False):
        x = self.database[collection].update_one(query,{"$pull": {array: value}},upsert=upsert)
        return x

    def delete_byID(self, collection, document):
        """ Remove the document if _id exists"""
        if document is not None:
            self.database[collection].remove(document)
        else:
            raise Exception("Nothing to delete, because project parameter is None")
            logger.warning("A document could not be deleted in MongoDB Collection: %s" % (collection))

    def create_index(self, collection, key, order=None):
        if order:
            self.database[collection].create_index( [(key, order)] )
        else:
            self.database[collection].create_index( key )