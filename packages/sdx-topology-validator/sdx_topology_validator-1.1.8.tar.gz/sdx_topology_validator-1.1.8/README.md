# sdx_topology_validator

## Introduction

This Validates the topology against the given OpenAPI specification.   

## Installation Steps

pip install sdx-topology-validator  

This installs the module "sdx-topology-validator".  

### Prerequisites

All the Prerequisite pip modules like PyYAML, jsonschema, jsonref will be automatically installed when you run the above command "pip install sdx-topology-validator".  

## Usage

The module "sdx-topology-validator" consists of functions 'load_openapi_schema', 'resolve_references', 'get_validator_schema', 'validate'.  

Import 'validate' function from the module "sdx-topology-validator".  

The function named 'load_openapi_schema' that takes a single parameter 'file_path', which is the yaml_spec_file(validator.yaml) which consists of OpenAPI specification and returns 'openapi_spec' the loaded YAML content as a dictionary.  

The function named 'resolve_references' that takes a single parameter 'openapi_spec', resolves any JSON references in the OpenAPI specification, ensuring that all $ref fields are fully expanded.  

The function named 'get_validator_schema' that takes a single parameter, which is the value returned by the function 'resolve_references'.   This function extracts and returns the JSON schema used for validating the request body of the /validator endpoint from the OpenAPI specification.  

The function named 'validate' that take one parameter: data.  
The first parameter 'data' takes json data as input and validates the given data against the provided JSON schema and returns the result of the validation.     

Note: 'validator.yaml' the yaml_spec_file is packaged with 'sdx-topology-validator' module, so no need of having it from the user side.  

Example of usage:    
from sdx_topology_validator import validate      
validation_result = validate(data)   