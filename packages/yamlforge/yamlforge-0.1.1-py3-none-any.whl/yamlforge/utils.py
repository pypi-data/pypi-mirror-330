import inflect
from dataclasses import dataclass

p = inflect.engine()

def lower_string(s: str) -> str:
    return ''.join(['_'+c.lower() if c.isupper() else c for c in s]).lstrip('_')

def upper_string(s: str) -> str:
    return ''.join([c.upper() if i == 0 or s[i-1] == '_' else c for i, c in enumerate(s)]).replace('_', '')

def add_underscores_based_on_reference(original: str, reference: str) -> str:
    result = []
    ref_index = 0
    for char in original:
        if ref_index < len(reference) and reference[ref_index].isupper():
            result.append('_')
            result.append(char.lower())
            ref_index += 1
        else:
            result.append(char.lower())
            ref_index += 1
    return ''.join(result).lstrip('_')

@dataclass
class ModelData:
    model_name: str
    file_name: str
    plural_model_name: str
    lower_model_name: str
    fields: list[dict[str, any]]
    relationships: list[dict[str, any]]

def get_file_name(model_name: str) -> str:
    return lower_string(model_name)

def get_models_dict(models: dict[str, any]) -> dict[str, ModelData]:
    models_in_memory = {}
    for model_name, config in models.items():
        file_name = get_file_name(model_name)
        plural_model = add_underscores_based_on_reference(p.plural(model_name.lower()), model_name)
        models_in_memory[model_name] = ModelData(
            model_name=model_name,
            file_name=file_name,
            plural_model_name=plural_model,
            lower_model_name=file_name,
            fields=config.get("fields", []),
            relationships=config.get("relationships", []),
        )
    return models_in_memory
