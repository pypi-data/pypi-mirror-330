import traceback
import janus_swi as janus
try:
    import transformers
except ImportError:
    import sys
    sys.exit("The 'transformers' is not installed. Please manual install or "
             "run `pip install prolog-env[toolbox]` to enable this feature.")


def prolog_add_rules(id: str, code: str):
    try:
        janus.consult(id, code)
    except:
        return traceback.format_exc()

def prolog_query(code):
    try:
        return list(janus.query(code))
    except:
        return traceback.format_exc()

prolog_toolbox = transformers.Toolbox(
    [
        transformers.tool(prolog_add_rules),
        transformers.tool(prolog_query),
    ]
)