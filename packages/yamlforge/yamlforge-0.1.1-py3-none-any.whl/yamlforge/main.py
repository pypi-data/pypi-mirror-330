import os

import logging
from textwrap import dedent

from .utils import upper_string, get_models_dict
from .parser import load_yaml_config

logger = logging.getLogger(__name__)

TAB = "    "

ALLOWED_FIELDS = [
    "primary_key",
    "required",
    "default",
    "index",
    "decimal_places",
    "max_digits",
    "unique",
    "max_items",
    "max_length",
    "nullable",
    "regex",
]

def set_relation_args(rel: dict[str, any], rel_type: str, target_model_lower: str) -> set[str]:
    relationship_args = set()

    on_delete = rel.get("on_delete", None)
 
    if rel.get("back_populates", False):
        relationship_args.add(f"back_populates='{target_model_lower}'")
    if on_delete:
        relationship_args.add(f"ondelete='{on_delete.upper()}'")
    if rel.get("cascade_delete", False):
        relationship_args.add("cascade_delete=True")
    if rel_type == "OneToOne":
        relationship_args.add("sa_relationship_kwargs={'uselist': False}")

    return relationship_args
    
def set_foreign_relation_args(rel: dict[str, any], rel_type: str, target_model_lower: str) -> str:
    relationship_args = []
    
    if rel.get("back_populates", None) is True:
        relationship_args.append(f"back_populates='{target_model_lower}'")
    if rel_type == "OneToOne":
        relationship_args.append("sa_relationship_kwargs={'uselist': False}")

    return relationship_args

def add_relations(model_name: str, model_data: dict[str, any], models_in_memory: dict[str, dict[str, any]]) -> list[str]:
    relationships, models, links = [], [], []

    for rel in model_data.relationships:
        rel_type = rel["type"]
        target_model = rel["model"]
        target_model_data = models_in_memory.get(target_model, {})
  
        if not target_model_data:
            raise ValueError(f"Modelo objetivo '{target_model}' no encontrado para la relación en '{model_name}'.")
        
        target_model_lower = target_model_data.file_name
        plural_target_model = target_model_data.plural_model_name

        relationship_args = set_relation_args(rel, rel_type, target_model_lower)

        models.append(target_model)

        target_id_type = next(
            (field["type"] for field in target_model_data.fields if field.get("primary_key", False)),
            "int"
        )

        if rel_type == "OneToOne":
            relationships.append(
                f"{TAB}{target_model_lower}: '{target_model}' | None = Relationship({', '.join(list(relationship_args))})"
            )
        elif rel_type == "OneToMany":
            relationships.append(
                f"{TAB}{plural_target_model}: list['{target_model}'] | None = Relationship({', '.join(list(relationship_args))})"
            )
        elif rel_type == "ManyToMany":
            link_table_name = f"{model_data.file_name}_{target_model_lower}_link"
            relationship_args.add(f"link_model={model_name}{target_model}Link")

            code_link = dedent(f"""
                class {model_name}{target_model}Link(SQLModel, table=True):
                    {model_data.file_name}_id: {target_id_type} | None = Field(default=None, foreign_key='{model_data.file_name}.id', primary_key=True)
                    {target_model_lower}_id: {target_id_type} | None = Field(default=None, foreign_key='{target_model_lower}.id', primary_key=True)
            """)

            with open(f"db/models/{link_table_name}.py", "w") as f:
                f.write("from sqlmodel import SQLModel, Field\n")
                f.write(code_link)
            
            models.append(f"{model_name}{target_model}Link")
            links.append(f"{model_data.file_name}_{target_model_lower}_link")

            foreign_key = f"{plural_target_model}: list['{target_model}'] | None = Relationship({', '.join(list(relationship_args))})"
            relationships.append(f"{TAB}{foreign_key}")

    return relationships, models, links

def add_foreign_relations(model_name: str, model_data: dict[str, any], models_in_memory: dict[str, dict[str, any]]) -> list[str]:
    relationships = []
    imports = []
    for model in models_in_memory:
        if model == model_name:
            continue

        model_data = models_in_memory[model]

        lower_model_name = model_data.lower_model_name
        if not lower_model_name:
            raise ValueError(f"Nombre de modelo no encontrado para '{model}'.")

        for relation in model_data.relationships:
            if relation.get("model", None) == model_name:
                target_model = model
                target_model_data = model_data

                imports.append(target_model)

                target_model_lower = target_model_data.file_name
                plural_target_model = target_model_data.plural_model_name

                target_id_type = next(
                    (field["type"] for field in target_model_data.fields if field.get("primary_key", False)),
                    "int"
                )

                rel_type = relation["type"]
                relationship_args = set_foreign_relation_args(relation, rel_type, target_model_lower)

                if rel_type == "OneToOne":
                    relationships.append(f"{TAB}{target_model_lower}_id: {target_id_type} | None = Field(default=None, foreign_key='{target_model_lower}.id')")
                    relationships.append(
                        f"{TAB}{target_model_lower}: '{target_model}' | None = Relationship({', '.join(relationship_args)})"
                    )
                elif rel_type == "OneToMany":
                    relationships.append(
                        f"{TAB}{lower_model_name}_id: {target_id_type} | None = Field(default=None, foreign_key='{target_model_lower}.id')"
                    )

                    if any('back_populates' in arg for arg in relationship_args):
                        relationships.append(
                            f"    {target_model_lower}: '{target_model}' | None = Relationship({', '.join(relationship_args)})"
                        )

                elif rel_type == "ManyToMany":
                    relationship_args.append(f"link_model={target_model}{model_name}Link")

                    imports.append(f"{target_model}{model_name}Link")
                    foreign_key = f"{plural_target_model}: list['{target_model}'] | None = Relationship({', '.join(relationship_args)})"
                    relationships.append(f"    {foreign_key}")

    return relationships, imports

def generate_imports(additional_imports: set[str]) -> str:
    """Genera los imports necesarios."""
    imports = "from sqlmodel import SQLModel, Field, Relationship\n"
    imports += "from typing import TYPE_CHECKING\n\n"
    imports += "if TYPE_CHECKING:\n"
    imports += "".join(f"{TAB}from db.models import {imp}\n" for imp in additional_imports)
    return imports

def set_fields(model_data: dict[str, any]) -> list[str]:
    fields = []

    for field in model_data.fields:
        field_name = field["name"]
        field_type = field["type"]

        field_options = []
        seen_options = set()

        for af in ALLOWED_FIELDS:
            if af not in field or af in seen_options:
                continue

            f = field.get(af, None)
            seen_options.add(af)

            if f is not None:
                if isinstance(f, str) and f != "None":
                    f = f"'{f}'"
                field_options.append(f"{af}={f}")

        fields.append(f"{TAB}{field_name}: {field_type} = Field({', '.join(field_options)})")

    return fields

def set_dto_fields(model_data: dict[str, any]) -> list[str]:
    fields = []

    for field in model_data.fields:
        field_name = field["name"]
        field_type = field["type"]
        
        if field.get("nullable", False) or field.get("default", None) is None:
            field_type = f"{field_type} | None"
        
        if "default" in field:
            default_value = field["default"]
            if isinstance(default_value, str):
                default_value = f"'{default_value}'"
            fields.append(f"{TAB}{field_name}: {field_type} = {default_value}")
        else:
            fields.append(f"{TAB}{field_name}: {field_type}")

    return fields

def generate_schemas(models_in_memory: dict[str, dict[str, any]] | None = None, config_path: str = "yamlforge.yaml") -> None:
    schemas_dir = "schemas"
    if not os.path.exists(schemas_dir):
        os.makedirs(schemas_dir)

    if models_in_memory is None:
        config = load_yaml_config(config_path)
        models_in_memory = get_models_dict(config)  

    for model_name, model_data in models_in_memory.items():
        file_name = model_data.file_name
        file_path = f"{schemas_dir}/{file_name}.py"

        dto_fields = set_dto_fields(model_data)

        code = "from pydantic import BaseModel\n\n"
        code += f"class {model_name}DTO(BaseModel):\n"
        code += "\n".join(dto_fields) + "\n"

        with open(file_path, "w") as f:
            f.write(code)

    init_schemas_path = os.path.join(schemas_dir, "__init__.py")
    with open(init_schemas_path, "w") as f:
        for model_name in models_in_memory:
            f.write(f"from schemas.{models_in_memory[model_name].file_name} import {model_name}DTO\n")


def generate_models(models_dict: dict[str, dict[str, any]] | None = None, config_path: str = "yamlforge.yaml") -> None:
    models_dir = "db/models"
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    init_db_path = os.path.join("db", "__init__.py")
    with open(init_db_path, 'w') as f:
        pass

    if models_dict is None:
        config = load_yaml_config(config_path)
        models_in_memory = get_models_dict(config)
    else:
        models_in_memory = models_dict

    copy_in_memory = models_in_memory.copy()
    links = []
    
    for model_name, model_data in models_in_memory.items():
        file_name = model_data.file_name
        file_path = f"db/models/{file_name}.py"

        fields = set_fields(model_data)

        additional_imports = set()
 
        try: 
            relationships, imports, relation_links = add_relations(model_name, model_data, models_in_memory)
            foreign_relations, foreign_imports = add_foreign_relations(model_name, model_data, models_in_memory)
            relationships += foreign_relations
         
            additional_imports.update(imports)
            additional_imports.update(foreign_imports)
        
            links.extend(relation_links)
        except ValueError as e:
            logger.error(e)
            copy_in_memory.pop(model_name)
            continue

        code = generate_imports(additional_imports)
        code += f"\nclass {model_name}(SQLModel, table=True):\n"
        code += "\n".join(fields + relationships) + "\n\n"

        with open(file_path, "w") as f:
            f.write(code)

    init_models_path = os.path.join(models_dir, "__init__.py")
    with open(init_models_path, 'w') as f:
        for model_name in copy_in_memory:
            f.write(f"from db.models.{copy_in_memory[model_name].file_name} import {model_name}\n")
        for link in links:
            f.write(f"from db.models.{link} import {upper_string(link)}\n")

def generate(config_path: str = "yamlforge.yaml") -> None:
    """Generate models and schemas from a YAML file.

    Args:
        path (str): Path to the YAML file.
    """

    config = load_yaml_config(config_path)
    models_dict = get_models_dict(config)

    generate_models(models_dict)
    generate_schemas(models_dict)

    logger.info("Models and schemas generated successfully.")
