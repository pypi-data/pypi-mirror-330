from pydantic import BaseModel
from pyparsing import Any

from app.core.app_enums import MongoCollections
from app.database.mongo import get_collection


class ArrayOperationData(BaseModel):
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

    collection: MongoCollections
    document_id: str = None  # id del documento que contiene el arreglo a operar
    array_property: str = None  # renombrar a property_array
    inner_object_property: str = None  # renombrar inner_object_property
    inner_object_id: Any = None
    value: Any | dict = None


# TODO Guarda la primera vez o actualiza completamente el arreglo
# Seria mejor una versión que actualice solo las variables que se le envían


def extract_update_instructs(value: dict, array_property: str) -> dict:
    update_obj = {}
    for key, val in value.items():
        update_obj[f"{array_property}.$.{key}"] = val
    return update_obj


def update_object_in_array(data: ArrayOperationData, overwrite: bool = True) -> None:
    """Actualiza un objeto en un arreglo, nota sobreescribe todo el objeto"""

    collection = data.collection
    array_property = data.array_property
    document_id = data.document_id
    value = data.value
    inner_object_id = data.inner_object_id

    if overwrite:
        update = {"$set": {f"{array_property}.$": value}}
    else:
        # TODO: Test this methods
        instructs = extract_update_instructs(value, array_property)
        update = {"$set": instructs}

    filters = {"id": document_id, f"{array_property}.id": inner_object_id}

    col = get_collection(collection)
    response = col.update_one(filter=filters, update=update)
    if response.modified_count == 0:
        print("Object does not exist, creating new one")
        push = {"$push": {array_property: value}}
        push_response = col.update_one(filter={"id": document_id}, update=push)
        print(push_response)

    return response


def update_object_property_in_array(d: ArrayOperationData) -> None:
    """Actualiza solo una propiedad de un objeto en un arreglo,
    Ejemplo suponiendo que lesson tiene el arreglo components  { "id": 1, components: { [{id: 1, name: 'name'}, {id: 2, name: 'name2'}] } }
    y solo quiero actualizar name components[1] el de id 2,
    solo funciona si el arreglo que se quiere actualizar tiene objetos con id

    para hacer esto manualmente sería algo así:
    filter = {"word": word, "learningExamples.id": id}
    update = {"$set": {f"learningExamples.$.audio": audio}}
    """

    filters = {"id": d.document_id, f"{d.array_property}.id": d.inner_object_id}
    update = {"$set": {f"{d.array_property}.$.{d.inner_object_property}": d.value}}

    col = get_collection(d.collection)
    col.update_one(filter=filters, update=update)
