import yaml
import jsonref
from jsonschema import validate as json_validate
from jsonschema.exceptions import ValidationError
import importlib.resources as pkg_resources

def load_openapi_schema():
    # Adjust the package name to the actual package where the resource is located
    package_name = 'sdx_topology_validator'
    resource_name = 'validator.yaml'
    
    with pkg_resources.open_text(package_name, resource_name) as file:
        openapi_spec = yaml.safe_load(file)
    return openapi_spec

def resolve_references(openapi_spec):
    return jsonref.JsonRef.replace_refs(openapi_spec)

def get_validator_schema(openapi_spec):
    return openapi_spec['paths']['/validator']['post']['requestBody']['content']['application/json']['schema']

def validate(data):
    """Validate the converted topology data against the OpenAPI schema."""
    validator_schema = get_validator_schema(resolve_references(load_openapi_schema()))
    try:
        json_validate(data, validator_schema)
        return {"result": "Validated Successfully", "status_code": 200}
    except ValidationError as e:
        return {"result": f"Validation Error: {e.message}", "status_code": 400}
