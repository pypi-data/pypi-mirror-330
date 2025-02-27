from typing import Type, Annotated, List, Dict, Literal, Optional, Any
from pydantic import Field, BaseModel, create_model
from pydantic_core import PydanticUndefined
from chronulus_core.types.attribute import ImageFromUrl



from pydantic.fields import FieldInfo




def create_model_from_schema(schema):
    fields = {}
    properties = schema.get("properties", {})

    type_mapping = {
        "integer": int,
        "string": str,
        "number": float,
        "boolean": bool,
        "array": List,
        "object": dict,
        "ImageFromUrl": ImageFromUrl,
        # Add null/None handling
        "null": type(None)
    }

    for field_name, field_schema in properties.items():
        # Handle case where type might be missing or in a different format
        field_type = field_schema.get("type", "object")

        # Handle multiple types (like ["string", "null"])
        if isinstance(field_type, list):
            # If null is one of the types, make it Optional
            if "null" in field_type:
                other_types = [t for t in field_type if t != "null"]
                field_type = other_types[0] if other_types else "string"
                is_optional = True
            else:
                field_type = field_type[0]
                is_optional = False
        else:
            is_optional = False

        python_type = type_mapping.get(field_type, Any)

        # Handle arrays/lists
        if field_type == "array":
            items = field_schema.get("items", {})
            item_type = items.get("type", "string")
            if item_type in type_mapping:
                python_type = List[type_mapping[item_type]]
            else:
                python_type = List[Any]

        # Handle optional fields
        is_required = field_name in schema.get("required", [])
        if is_required and not is_optional:
            fields[field_name] = (python_type, ...)
        else:
            fields[field_name] = (Optional[python_type], None)

    model_name = schema.get("title", "DynamicModel")
    return create_model(model_name, **fields)

Model2 = create_model_from_schema(schema)

Model2.model_json_schema() == schema


InputField.model_json_schema() == schema