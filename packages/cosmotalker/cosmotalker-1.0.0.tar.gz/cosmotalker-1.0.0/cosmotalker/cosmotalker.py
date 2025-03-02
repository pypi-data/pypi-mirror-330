import importlib
import unicodedata

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
            return module.data.get(key, "No information found.")
        else:
            return "Error: 'data' dictionary not found in module."

    except ModuleNotFoundError:
        return f"No information available for this key. (Missing {module_path})"
    except AttributeError:
        return "Data format error in the module."
