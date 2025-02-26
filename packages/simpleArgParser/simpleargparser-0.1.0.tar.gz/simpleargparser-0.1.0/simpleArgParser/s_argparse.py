import argparse
import dataclasses
from dataclasses import fields, MISSING, asdict
from typing import Optional, Union, get_origin, get_args, Type, List
import enum
import json
import sys
import types
import inspect
import re

# Global sentinel
NOT_PROVIDED = object()

class SpecialLoadMarker:
    pass

def bool_converter(s):
    """Supports case-insensitive yes/no, true/false conversion to boolean values"""
    if isinstance(s, bool):
        return s
    lower = s.lower()
    if lower in ("yes", "true", "t", "y", "1"):
        return True
    elif lower in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError(f"Invalid boolean value: {s}")

def extract_field_comments(cls: Type) -> dict:
    """
    Extracts comments above fields from the class's source code, returns a dictionary of {field_name: comment_content}.
    Only effective when source code is accessible.
    """
    try:
        source = inspect.getsource(cls)
    except Exception:
        return {}
    lines = source.splitlines()
    field_pattern = re.compile(r'^\s*(\w+)\s*:')
    field_help = {}
    current_comments = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            comment_text = stripped.lstrip('#').strip()
            current_comments.append(comment_text)
        else:
            m = field_pattern.match(line)
            if m:
                field_name = m.group(1)
                if current_comments:
                    field_help[field_name] = " ".join(current_comments)
                current_comments = []
            else:
                current_comments = []
    return field_help

def get_by_path(d: dict, path: str):
    """Retrieve a value from a nested dictionary d based on a dot-separated path"""
    parts = path.split('.')
    current = d
    for p in parts:
        if isinstance(current, dict) and p in current:
            current = current[p]
        else:
            return None
    return current

def remove_by_path(d: dict, path: str):
    """Remove a key from a nested dictionary d based on a dot-separated path"""
    parts = path.split('.')
    current = d
    for p in parts[:-1]:
        if p in current:
            current = current[p]
        else:
            return
    current.pop(parts[-1], None)

def convert_type(typ: Type):
    """
    Returns a conversion function. For bool type, uses custom bool_converter; for Enum types,
    matches based on enum member name; otherwise returns typ itself.
    """
    if typ is bool:
        return bool_converter
    if isinstance(typ, type) and issubclass(typ, enum.Enum):
        return lambda s: typ[s]
    return typ

def convert_value(value, target_type: Type):
    """Converts value to target_type, supports bool, Enum, list and basic types"""
    if get_origin(target_type) in (Union, types.UnionType):
        non_none = [a for a in get_args(target_type) if a is not type(None)]
        if len(non_none) == 1:
            target_type = non_none[0]
    if target_type is bool:
        return bool_converter(value) if isinstance(value, str) else bool(value)
    if isinstance(target_type, type) and issubclass(target_type, enum.Enum):
        if isinstance(value, str):
            return target_type[value]
        return target_type(value)
    if get_origin(target_type) is list:
        inner_type = get_args(target_type)[0]
        if isinstance(value, str):
            return [convert_value(item.strip(), inner_type) for item in value.split(',')]
        elif isinstance(value, list):
            return [convert_value(item, inner_type) for item in value]
        else:
            raise ValueError(f"Cannot convert {value} to {target_type}")
    try:
        return target_type(value)
    except Exception:
        return value

def nest_namespace(ns: dict) -> dict:
    """Convert a flat argparse namespace to a nested dictionary (based on dot-separated names)"""
    nested = {}
    for k, v in ns.items():
        parts = k.split('.')
        current = nested
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = v
    return nested

def deep_merge(a: dict, b: dict) -> dict:
    """
    Recursively merge dictionaries, b's values override a's values, but if the value in b is NOT_PROVIDED,
    then preserve the valid values already in a.
    """
    result = dict(a)
    for k, v in b.items():
        # If b's value is NOT_PROVIDED, don't override a's value
        if v is NOT_PROVIDED:
            continue
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result

def fill_defaults(d: dict, cls: Type) -> dict:
    """
    Fill in dataclass default values, and check if required fields are missing.
    If required fields are missing, raise an error.
    """
    result = dict(d)
    for f in fields(cls):
        if f.name not in result or result[f.name] is NOT_PROVIDED:
            if f.default is MISSING and f.default_factory is MISSING:
                raise ValueError(f"Missing required parameter: {f.name}")
            elif f.default is not MISSING:
                result[f.name] = f.default
            elif f.default_factory is not MISSING:
                result[f.name] = f.default_factory()
        else:
            if dataclasses.is_dataclass(f.type) and isinstance(result[f.name], dict):
                result[f.name] = fill_defaults(result[f.name], f.type)
    return result

def from_dict(cls: Type, d: dict):
    """Construct a dataclass instance from a dictionary, supports nested dataclasses"""
    kwargs = {}
    for f in fields(cls):
        if dataclasses.is_dataclass(f.type):
            sub_dict = d.get(f.name, {})
            kwargs[f.name] = from_dict(f.type, sub_dict)
        else:
            if f.name in d:
                kwargs[f.name] = convert_value(d[f.name], f.type)
    return cls(**kwargs)

def add_arguments_from_dataclass(parser: argparse.ArgumentParser, cls: Type, prefix: str = "", special_fields: set = None):
    """
    Recursively add command line arguments based on dataclass definition:
      - Nested fields use dot notation for parameter names;
      - Supports list, Enum, bool types, etc.;
      - Automatically captures comments above fields;
      - If a field's default value is special_load() (a SpecialLoadMarker instance), records the complete path of that field in the special_fields set.
    """
    if special_fields is None:
        special_fields = set()
    field_help_map = extract_field_comments(cls)
    for f in fields(cls):
        field_type = f.type
        if get_origin(field_type) in (Union, types.UnionType):
            non_none = [a for a in get_args(field_type) if a is not type(None)]
            if len(non_none) == 1:
                field_type = non_none[0]
        full_field_name = f"{prefix}{f.name}"
        if dataclasses.is_dataclass(field_type):
            new_prefix = f"{full_field_name}."
            add_arguments_from_dataclass(parser, field_type, prefix=new_prefix, special_fields=special_fields)
        else:
            arg_name = f"--{full_field_name}"
            dest_name = full_field_name
            if get_origin(field_type) is list:
                inner_type = get_args(field_type)[0]
                def list_converter(s, inner_type=inner_type):
                    return [convert_value(item.strip(), inner_type) for item in s.split(',')]
                conv_type = list_converter
            else:
                conv_type = convert_type(field_type)
            extra_help = field_help_map.get(f.name, "")
            help_text = f"{extra_help} (type: {field_type})".strip()
            kwargs = {
                "dest": dest_name,
                "type": conv_type,
                "help": help_text
            }
            if isinstance(field_type, type) and issubclass(field_type, enum.Enum):
                kwargs["choices"] = list(field_type.__members__.keys())
            # If the field's default value is special_load() (a SpecialLoadMarker instance), record the field's path
            if isinstance(f.default, SpecialLoadMarker):
                special_fields.add(full_field_name)
            if f.default is MISSING and f.default_factory is MISSING:
                kwargs["required"] = True
            else:
                kwargs["default"] = NOT_PROVIDED
                default_val = f.default if f.default is not MISSING else f.default_factory()
                kwargs["help"] += f" (default: {default_val})"
            parser.add_argument(arg_name, **kwargs)

def recursive_post_process(obj):
    """
    Recursively call the process_args or post_process method of a dataclass object, executed from top to bottom.
    If the object defines process_args, call it first; otherwise call post_process.
    """
    if dataclasses.is_dataclass(obj):
        if hasattr(obj, "process_args") and callable(obj.process_args):
            obj.process_args()
        elif hasattr(obj, "post_process") and callable(obj.post_process):
            obj.post_process()
        for field in fields(obj):
            value = getattr(obj, field.name)
            if dataclasses.is_dataclass(value):
                recursive_post_process(value)

def parse_args(cls: Type, pass_in: List[str] = None):
    """
    Parse command line arguments, supporting:
      - Code-provided arguments pass_in merged with sys.argv (command line arguments take priority);
      - JSON configuration file loading: if a field's default value is special_load() (SpecialLoadMarker instance), and the user provides a non-empty string,
        then try to load that string as a JSON file path and merge with other configurations;
      - Merge default values (and check required fields);
      - Recursively call post-processing methods (process_args/post_process) for all dataclasses;
      - If --help/-h is detected, directly print help information and exit.
    Priority: command line > code input > specially loaded JSON config > default values.
    """
    code_args = pass_in if pass_in is not None else []
    cmd_args = sys.argv[1:]
    args_list = code_args + cmd_args

    if any(arg in ('-h', '--help') for arg in args_list):
        full_parser = argparse.ArgumentParser()
        add_arguments_from_dataclass(full_parser, cls)
        full_parser.print_help()
        sys.exit(0)

    special_fields = set()
    parser = argparse.ArgumentParser()
    add_arguments_from_dataclass(parser, cls, special_fields=special_fields)
    args = parser.parse_args(args_list)
    flat_ns = vars(args)
    nested_args = nest_namespace(flat_ns)

    # If special load fields exist, ensure there's at most one
    if len(special_fields) > 1:
        raise ValueError(f"At most one special load field is allowed, found: {special_fields}")
    if special_fields:
        special_field_path = next(iter(special_fields))
        special_value = get_by_path(nested_args, special_field_path)
        if isinstance(special_value, str) and special_value.strip():
            try:
                with open(special_value, 'r') as f:
                    json_special = json.load(f)
            except Exception as e:
                print(f"Error loading JSON config from {special_value}: {e}", file=sys.stderr)
                json_special = {}
            # Remove the special field and merge the loaded JSON into the configuration (command line arguments have higher priority)
            remove_by_path(nested_args, special_field_path)
            nested_args = deep_merge(json_special, nested_args)
    final_dict = fill_defaults(nested_args, cls)
    config = from_dict(cls, final_dict)
    recursive_post_process(config)
    return config

def to_json(config) -> str:
    """Convert a dataclass instance to a JSON string (Enum types are converted to their names)"""
    def default(o):
        if isinstance(o, enum.Enum):
            return o.name
        raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")
    return json.dumps(asdict(config), indent=4, default=default)

def main():
    print("simpleArgParser: Please use parse_args() in your code to parse configuration.")

if __name__ == "__main__":
    main()