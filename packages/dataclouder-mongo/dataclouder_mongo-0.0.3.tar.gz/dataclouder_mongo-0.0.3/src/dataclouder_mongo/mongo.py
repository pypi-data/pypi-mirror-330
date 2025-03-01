import os
from datetime import datetime

# import mongo_schema
import pymongo
from bson import ObjectId
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from typing_extensions import Any, TypedDict

# MongoDB error codes
DOCUMENT_VALIDATION_ERROR = 121


client: MongoClient | None = None


def get_mongo_uri() -> str:
    mongo_uri: str = f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASS')}@{os.getenv('MONGO_HOST')}/{os.getenv('MONGO_DB')}?retryWrites=true&w=majority"
    print("Connectando", mongo_uri)
    return mongo_uri


def get_client() -> MongoClient:
    global client
    if client is None:
        print("Creating client MONGO")
        client = MongoClient(get_mongo_uri())
    return client


def get_db() -> Database[dict[str, Collection]]:
    db: Database[dict[str, Collection]] = get_client()[os.getenv("MONGO_DB", "")]
    return db


# db: Database[dict[str, Collection]] = get_client()[os.getenv("MONGO_DB", "")]


class ArrayOperationData(TypedDict):
    """
    Con esta estructura puedo solucionar la mayoría de las operaciones de arreglos de un solo nivel.


    Collection to find, las operaciones se permiten a 1 nivel es decir puedo afectar
    user.verbs = [ {word: 'run'}, {word: 'walk'}] pero si cada objeto tiene más arreglos entonces hay que hacer otra clase
    CREATE requieres collection, document_id, array_property, value. UPDATE inner_object_property and inner_object_id

    document_id: id del documento que contiene el arreglo a operar ej. id: user.id
    array_property: atributo donde se encuentra el arreglo a operar ej. verbs: user.verbs
    inner_object_property: propiedad del arreglo usado como identificador ej. word: user.verbs.word
    inner_object_id: valor del id usado para identificar comparar ej. life: user.verbs.word == 'life'
    value: value to insert ej.  [tree, leaf]: user.verbs.word = [tree, leaf]
    """

    collection: str
    document_id: str  # id del documento que contiene el arreglo a operar
    array_property: str  # renombrar a property_array
    inner_object_property: str  # renombrar inner_object_property
    inner_object_id: Any
    value: Any


def get_all_data_in_collection(collection: str) -> list[dict]:
    """get all records for corresponding collection (No _id), USE CAREFULLY"""
    col = get_collection(collection)
    projection = {"_id": 0}
    cursor = col.find({}, projection=projection)
    return list(cursor)


def get_projection_dict(include: list[str] = None, exclude: list[str] = None) -> dict:
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
    query = {"id": id}
    return get_document_by_mongo_query(collection, query)


def get_document_by_id_including(collection: str, id: str, include: list[str]) -> dict:
    """When your document/object contains more objects, and you only want specifics properties example, extract only verbs form user"""
    query = {"id": id}
    selection = get_projection_dict(include, None)
    data = get_document_by_mongo_query(collection, query, selection)
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


def save_document(collection: str, document: Any, manual_id: str | None = None, audit_user_id: str | None = None) -> dict:  # noqa: ANN401
    """mongo agrega ids automaticamente, manual id para evitar este comportamiento"""
    if isinstance(document, BaseModel):
        document = document.dict()

    # TODO: en realidad ya no creo trabajar con _id por que implica acutalizar con el ObjectId()
    id_data = document.get("_id") or document.get("id")

    if id_data:
        return update(collection, document, id_data, audit_user_id)
    else:
        if manual_id:
            document["id"] = manual_id
        return insert(collection, document, audit_user_id)


def insert_pretty(collection: str, document: dict, audit_user_id: str = None) -> dict:
    """Insert a document with Object id '_id' and id string 'id', '_id' is not returned"""

    if audit_user_id:
        audit_data = {"createdDate": datetime.now(), "createdBy": audit_user_id}
        document = document | audit_data

    document["_id"] = ObjectId()
    document["id"] = str(document["_id"])

    col = get_collection(collection)
    col.insert_one(document)
    document.pop("_id", None)
    return document


# Es en teoria el mismo que insert_word_mongo pero más general
def insert(table: str, document: dict, audit_user_id: str = None, cast_object_id: bool = False) -> dict:
    if audit_user_id:
        audit_data = {"createdDate": datetime.now(), "createdBy": audit_user_id}
        document = document | audit_data

    col = get_collection(table)
    try:
        col.insert_one(document)
        # after save document, same saved dict is modified (mutable) adding _id: ObjectId
        if cast_object_id:
            document["_id"] = str(document["_id"])

        return document
    except pymongo.errors.WriteError as exc:
        print(".....Error", exc)
        if exc.code == DOCUMENT_VALIDATION_ERROR:
            __handle_invalid_data(col, document)


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


def update(table: str, document: dict, id: str, audit_user_id: str = None, update_by_property: str = None) -> int:
    """Actualiza solo las propiedades que se envian $set, si  recibe  audit_user_id se guardan datos adicionales."""

    if audit_user_id:
        audit_data = {"modifiedDate": datetime.now(), "modifiedBy": audit_user_id}
        document = document | audit_data

    query = {}
    if update_by_property:
        query = {update_by_property: id}
    else:
        query = {"id": id}

    updated_data = {key: value for (key, value) in document.items() if value is not None}

    updated_values = {"$set": updated_data}
    col = get_collection(table)

    try:
        result = col.update_one(query, updated_values)
        return result.raw_result["nModified"]
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


def get_collection(collection: str) -> Collection:
    """Get Mongo Collection Object"""
    if isinstance(collection, str):
        print(f"WARNING: not validated {collection} collection, pass it as Enum so it can be validated")
        return db[collection]

    elif collection in str:
        return db[collection.value]
    else:
        raise AppException("not able to find table in code", "Se intenta obtener una colleccion no registrada en el código")


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


def push_into_array(array_operation: ArrayOperationData) -> int:
    """Push data in the property value array i.e. { words: [...] }"""

    collection = array_operation["collection"]
    document_id = array_operation["document_id"]
    array_property = array_operation["array_property"]
    value = array_operation["value"]

    filters = {"id": document_id}
    push_update = {"$push": {array_property: value}}
    mongo_col = get_collection(collection)
    update_results = mongo_col.update_one(filters, push_update)
    return update_results.raw_result["nModified"]


# Probar esto inserta multiples documentos en un arreglo  debería sustituir a
def push_list_into_array(data: ArrayOperationData) -> None:
    """Similar to  push_into_array but when you want to  push multiple objects, data['value'] should be a list"""

    collection = data["collection"]
    array_property = data["array_property"]
    document_id = data["document_id"]
    records = data["value"]

    filters = {"id": document_id}
    each = {"$each": records}
    update = {array_property: each}
    push = {"$push": update}

    col = get_collection(collection)
    col.update_one(filters, push)


def update_all_objects_in_array(data: ArrayOperationData) -> None:
    """Actualiza todos los objetos para agregar el valor que se requiere"""
    # TODO: quiza valga la pena una versión con filtro ya que actualiza la propiedad parejo

    collection = data["collection"]
    array_property = data["array_property"]
    document_id = data["document_id"]
    value = data["value"]
    inner_object_property = data["inner_object_property"]

    filters = {"id": document_id}
    update = {"$set": {f"{array_property}.$[].{inner_object_property}": value}}

    col = get_collection(collection)
    col.update_one(filter=filters, update=update)


def update_object_in_array(data: ArrayOperationData) -> None:
    ## revisar si funciona, y refactorizar ahora. el objeto  ArrayOperationData.
    # Crear el array frameworks con los scenarios para actualizar objects en un array
    """Actualiza un objeto en un arreglo, nota sobreescribe todo el objeto"""
    collection = data["collection"]
    array_property = data["array_property"]
    document_id = data["document_id"]
    value = data["value"]
    inner_object_id = data["inner_object_id"]

    filters = {"id": document_id, f"{array_property}.id": inner_object_id}
    update = {"$set": {array_property: value}}

    col = get_collection(collection)
    col.update_one(filter=filters, update=update)


def update_object_property_in_array(data: ArrayOperationData) -> None:
    """Ejemplo suponiendo que lesson tiene  { "id": 1, components: { [{id: 1, name: 'name'}, {id: 2, name: 'name2'}] } }
    y solo quiero actualizar name components[1] el de id 2, solo puede actualizar si el array property tiene id."""

    collection = data["collection"]
    array_property = data["array_property"]
    document_id = data["document_id"]
    value = data["value"]
    inner_object_property = data["inner_object_property"]
    inner_object_id = data["inner_object_id"]

    filters = {"id": document_id, f"{array_property}.id": inner_object_id}
    update = {"$set": {f"{array_property}.$.{inner_object_property}": value}}

    col = get_collection(collection)
    col.update_one(filter=filters, update=update)


def push_into_array_sort_and_trim(data: ArrayOperationData, trim_number: int, sort_property: str) -> None:
    collection = data["collection"]
    array_property = data["array_property"]
    document_id = data["document_id"]
    new_object = data["value"]

    filters = {"id": document_id}

    rules = {"$each": [new_object], "$sort": {sort_property: -1}, "$slice": trim_number}
    update = {"$push": {array_property: rules}}

    col = get_collection(collection)

    col.update_one(filter=filters, update=update)


# @deprecated probar si funciona igual con push_list_into_array
def insert_objects_into_array(collection: str, id: str, property_array: str, records: list[Any]) -> None:
    """Insert documents/objects into existing array example { 'property_array' : [...records] }"""

    filters = {"id": id}
    each = {"$each": records}
    update = {property_array: each}
    push = {"$push": update}
    col = get_collection(collection)
    col.update_one(filters, push)


def delete_from_array(array_operation: ArrayOperationData) -> None:
    """Deletes an existing object from array, property: using ArrayOperationData Object, note that there are 2 ids,
    one for collection document, and one for current value in the array, inner_object_id is the value to match,
    example  array_property='words', inner_object_property='word', inner_object_id='forest'    {'words' { 'word' : 'forest' } }"""

    collection = array_operation["collection"]
    array_property = array_operation["array_property"]
    inner_object_property = array_operation.get("inner_object_property", "id")
    inner_object_id = array_operation["inner_object_id"]
    document_id = array_operation["document_id"]

    update = {array_property: {inner_object_property: inner_object_id}}
    remove = {"$pull": update}
    mongo_col = get_collection(collection)
    filters = {"id": document_id}

    mongo_col.update_one(filters, remove)


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
