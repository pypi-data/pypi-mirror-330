import os
from datetime import datetime

import pymongo
from bson import ObjectId
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult, UpdateResult
from typing_extensions import Any

# MongoDB error codes
DOCUMENT_VALIDATION_ERROR = 121


client: MongoClient | None = None


def get_mongo_uri() -> str:
    mongo_uri: str = f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASS')}@{os.getenv('MONGO_HOST')}/{os.getenv('MONGO_DB')}?retryWrites=true&w=majority"
    print("Connectando", mongo_uri)
    return mongo_uri


def get_client() -> MongoClient:
    global client  # noqa: PLW0603, W291
    if client is None:
        print("Creating client MONGO")
        client = MongoClient(get_mongo_uri())
    return client


def get_db() -> Database[dict[str, Collection]]:
    db: Database[dict[str, Collection]] = get_client()[os.getenv("MONGO_DB", "")]
    return db


def get_all_data_in_collection(collection: str) -> list[dict]:
    """get all records for corresponding collection (No _id), USE CAREFULLY"""
    col: Collection = get_collection(collection)
    projection: dict = {"_id": 0}
    cursor = col.find({}, projection=projection)
    return list(cursor)


def get_projection_dict(include: list[str] | None = None, exclude: list[str] | None = None) -> dict:
    """include: fields to include in a query, exclude: fields to exclude in a query"""

    selection = {}

    if include and len(include) > 0:
        in_dict = {property: 1 for property in include}
        print(in_dict)

        selection = selection | in_dict
        print(selection)

    if exclude and len(exclude) > 0:
        out_dict = {property: 0 for property in exclude}
        print(out_dict)

        selection = selection | out_dict
        print(selection)

    return selection


def get_document_by_id(collection: str, id: str) -> dict:
    """Get the data using custom id, similar to get document"""
    query: dict = {"id": id}
    return get_document_by_mongo_query(collection, query)


def get_document_by_id_including(collection: str, id: str, include: list[str]) -> dict:
    """When your document/object contains more objects, and you only want specifics properties example, extract only verbs form user"""
    query: dict = {"id": id}
    selection: dict = get_projection_dict(include, None)
    data: dict = get_document_by_mongo_query(collection, query, selection)
    return data


def get_document_by_object_id(collection: str, id: str) -> dict:
    """use mongo ObjectId version instead string this use mongo id property _id"""

    mongo_col = get_collection(collection)
    document = mongo_col.find_one({"_id": ObjectId(id)})
    if document:
        document["id"] = str(document["_id"])
        del document["_id"]
    return document


def get_document_by_mongo_query(collection: str, query: dict, projection: dict = None) -> dict:
    """you may need to now how to query and project, for custom proposals"""
    """ basically a query with a dict, {'property1': property, 'property2': property2}, all queries exclude objectID aka _id """

    if projection is None:
        projection = {}

    projection = projection | {"_id": 0}

    col = get_collection(collection)
    data = col.find_one(query, projection)
    return data


def get_documents_by_query_projection(collection: str, query: dict, projection: dict = None, limit: int = None) -> list[Any]:
    """Get all documents with params, query: mongo query, selection: filters, limit: to limit the query, return a list"""

    if projection is None:
        projection = {}

    table = get_collection(collection)

    # if projection is None:
    projection = projection | {"_id": 0}

    cursor = table.find(query, projection)
    if limit:
        cursor = cursor.limit(limit)
    objects = list(cursor)
    return objects


def save_document(collection: str, document: Any, manual_id: str | None = None, audit_user_id: str | None = None) -> dict[str, Any]:  # noqa: ANN401
    """Depending on id, will update or insert document
    Returns:
        dict with keys:
        - action: "update" or "insert"
        - update: update result if action is "update"
        - document: the saved/updated document
    """
    if isinstance(document, BaseModel):
        document = document.model_dump()

    id_data: str | None = document.get("_id") or document.get("id")

    if id_data:
        update_result = update_document(collection, document, id_data, audit_user_id)
        return {"action": "update", "update": update_result, "document": document}
    else:
        if manual_id:
            document["id"] = manual_id

        inserted_doc = insert_document(collection, document, audit_user_id)
        return {"action": "insert", "update": None, "document": inserted_doc}


# insert_document now does this
# def insert_pretty(collection: str, document: dict, audit_user_id: str = None) -> dict:
#     """Insert a document with Object id '_id' and id string 'id', '_id' is not returned"""

#     if audit_user_id:
#         audit_data = {"createdDate": datetime.now(), "createdBy": audit_user_id}
#         document = document | audit_data

#     document["_id"] = ObjectId()
#     document["id"] = str(document["_id"])

#     col = get_collection(collection)
#     col.insert_one(document)
#     document.pop("_id", None)
#     return document


def insert_document(table: str, document: dict, audit_user_id: str | None = None, cast_object_id: bool = False) -> dict | None:
    """Insert a new document, this method handled fields for document _id and id and createdAt and updatedAt"""
    audit_data: dict = {"createdAt": datetime.now(), "updatedAt": datetime.now()}
    # Check this is handle my mongo in node.
    document["_id"] = ObjectId()
    document["id"] = str(document["_id"])

    if audit_user_id:
        document = document | audit_data

    col: Collection = get_collection(table)
    try:
        result: InsertOneResult = col.insert_one(document)
        print("result", result)
        # after save document, same saved dict is modified (mutable) adding _id: ObjectId
        if cast_object_id:
            document["_id"] = str(document["_id"])

        return document
    except pymongo.errors.WriteError as exc:
        print(".....Error", exc)
        if exc.code == DOCUMENT_VALIDATION_ERROR:
            __handle_invalid_data(col, document)
        return None


def count_array(array_prop: str, col: str, id: str) -> list[dict]:
    collection = get_collection(col)
    condition = {"$match": {"id": id}}
    counter = {"$project": {"count": {"$size": f"${array_prop}"}}}
    a = collection.aggregate([condition, counter])
    return list(a)


def delete_document(collection: str, document_id: str) -> int:
    filters = {"id": document_id}

    mongo_col = get_collection(collection)
    data = mongo_col.delete_one(filters)
    return data.deleted_count


def update_document(collection: str, document: dict, id: str, audit_user_id: str | None = None, override_key_id: str | None = None) -> dict:
    """
    Update all valid properties in dictionary, {"name": "test", "age": "23"}  None is not valid and is skipped
    audit_user_id: is optional, if provided, it will be added to the document
    override_key_id: by default use id as key, but here you can override it.
    """

    if audit_user_id:
        audit_data: dict = {"modifiedDate": datetime.now(), "modifiedBy": audit_user_id}
        document = document | audit_data

    query: dict = {}
    if override_key_id:
        query = {override_key_id: id}
    else:
        query = {"id": id}

    updated_data: dict = {key: value for (key, value) in document.items() if value is not None}

    updated_values: dict = {"$set": updated_data}
    col: Collection = get_collection(collection)

    try:
        result: UpdateResult = col.update_one(query, updated_values)
        return result.raw_result
    except pymongo.errors.WriteError as exc:
        print(".....Error", exc)
        if exc.code == DOCUMENT_VALIDATION_ERROR:
            __handle_invalid_data(col, document)


def update_with_operator(document_id: str, collection: str, update_operation: dict) -> bool:
    """
    :param document_id: id of the object
    :param collection:
    :param update: mongo update object built example: {'$set': {'recommendations.verbs': value}}
    """
    filter = {"id": document_id}
    return update_with_filter_and_operation(filter, update_operation, collection)


def update_with_filter_and_operation(filter: dict, operation: dict, collection: str) -> bool:
    """
    :param filter: custom filter { 'email': 'adamo@appingles.com'}
    :param collection: name of the collection
    :param operation: mongo object for update operation, example: {'$set': {'recommendations.verbs': value}}
    """
    col = get_collection(collection)
    result = col.update_one(filter, operation)
    # Solo dice si algo fue modificado o no, si encuentro un mejor método que regrese la modificación o null sería más util
    return True if result.matched_count >= 1 else False


def insert_record_in_collection(table: str, record: dict) -> None:
    print("inserting data", table, record)
    table = get_collection(table)
    table.insert_one(record)


def get_collection(collection: str | None = None) -> Collection:
    """Get Mongo Collection Object"""
    db: Database[dict[str, Collection]] = get_db()
    if isinstance(collection, str):
        return db[collection]
    else:
        raise Exception("not able to find table in code", "Se intenta obtener una colleccion no registrada en el código")


def update_all_object(collection: str, id_name: str, id: str, object_dict: dict) -> int:
    """Cuidado, cada valor pasado en el objecto lo va a actualizar, asegurarse de la construcción correcta"""

    col = get_collection(collection)
    query = {id_name: id}

    list_attibutes = {}
    attibutes = {}

    for key, value in object_dict.items():
        if isinstance(value, list):
            list_attibutes[key] = {"$each": value}
        else:
            attibutes[key] = value

    # TODO: Add the $set variable so it can set single properties
    updated_values = {"$push": list_attibutes}

    result = col.update_one(query, updated_values)
    return result.raw_result["nModified"]


# @deprecated probar si funciona igual con push_list_into_array
def insert_objects_into_array(collection: str, id: str, property_array: str, records: list[Any]) -> None:
    """Insert documents/objects into existing array example { 'property_array' : [...records] }"""

    filters = {"id": id}
    each = {"$each": records}
    update = {property_array: each}
    push = {"$push": update}
    col = get_collection(collection)
    col.update_one(filters, push)


def transform_object_id_to_string(records: list[dict]) -> list[dict]:
    """Transform ObjectId to string in a list of dictionaries.

    Args:
        records: List of dictionaries containing MongoDB documents

    Returns:
        List of dictionaries with ObjectId converted to strings
    """
    return [dict(record, _id=str(record["_id"])) for record in records]


def __handle_invalid_data(col: Collection, document: dict) -> None:
    # Get the schema for the collection
    opts = col.options()
    schema = opts.get("validator").get("$jsonSchema")

    print("El eschema es .....", schema)
    # Raise a jsonschema.ValidationError with more details
    # if schema is not None:
    #     try:
    #         mongo_schema.validate(document, schema)
    #     except Exception as e:
    #         print('No se puede escribir en la base', e)
    #         raise AppException(
    #             'Error de escritura, los datos no cumplen las validadaciones, esperar v5 mongo para más detalles', e)
