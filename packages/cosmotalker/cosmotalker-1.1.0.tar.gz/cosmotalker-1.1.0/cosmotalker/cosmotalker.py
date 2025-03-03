import os
import importlib
import importlib.util
import unicodedata
import json

def get(key: str):
    if not key:
        return "Invalid key."

    key = unicodedata.normalize("NFC", key.strip().lower())  # Normalize the key
    first_letter = key[0]
    module_path = f"cosmotalker.data.{first_letter}"

    try:
        module = importlib.import_module(module_path)
        importlib.reload(module)  # Force reload

        if hasattr(module, "data"):
            info = module.data.get(key, None)
            if info:
                return f"{info}\n\nCosmoTalker v1.1 currently covers celestial objects within our solar system, whether natural or synthetic. For more data, check the latest version."
            else:
                return "No information found.\n\nCosmoTalker v1.1 currently covers celestial objects within our solar system, whether natural or synthetic. For more data, check the latest version."

        return "Error: 'data' dictionary not found in module."

    except ModuleNotFoundError:
        return f"No information available for this key. (Missing {module_path})\n\nCosmoTalker v1.1 currently covers celestial objects within our solar system, whether natural or synthetic. For more data, check the latest version."
    except AttributeError:
        return "Data format error in the module.\n\nCosmoTalker v1.1 currently covers celestial objects within our solar system, whether natural or synthetic. For more data, check the latest version."

def get_data():
    # Load data dynamically from 'data' directory
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    all_keys = {}
    
    if os.path.exists(data_dir):
        for filename in os.listdir(data_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # Remove .py extension
                file_path = os.path.join(data_dir, filename)
                
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, "data") and isinstance(module.data, dict):
                    all_keys[module_name] = list(module.data.keys())
    
    # Print the keys from each module neatly using JSON formatting
    print(json.dumps(all_keys, indent=4))
