import importlib
import functools
from typing import List, Dict, Any
import yaml
import os
from pprint import pprint

def load_pipeline_config(
        filepath: str, 
        profile: str = "default"
):
    """
    Loads a pipeline configuration from a YAML file.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Config file not found at: {filepath}")

    with open(filepath, 'r') as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            raise ValueError(f"Error parsing YAML file: {exc}")


    profile_config = config.get(profile)

    if not profile_config or 'steps' not in profile_config:
        raise KeyError(f"Profile '{profile}' with 'steps' not found in {filepath}")

    return profile_config['steps']

def get_function(path_string):
    module_path, func_name = path_string.split('/')
    module = importlib.import_module(module_path)
    return getattr(module, func_name)

def compose_pipeline(steps_config: List[Dict[str, Any]]):
    func_pipe = [
        functools.partial(
            get_function(step['action']), 
            **step.get('params', {})
        ) 
        for step 
        in steps_config
    ]

    def pipeline(initial_input):
        return functools.reduce(
            lambda data, func: func(data), 
            func_pipe, 
            initial_input
        )

    return pipeline

if __name__ == '__main__':
    config_steps = load_pipeline_config('cfg.yaml')
    pprint(config_steps)
    pipeline = compose_pipeline(config_steps)('hello ')
    print(pipeline)