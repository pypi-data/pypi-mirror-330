from node_hermes_core.nodes.depedency import HermesDependencies

PATH = r"packages\datacapture-core\test\yaml\basic_config.hermes"

modules = HermesDependencies.import_from_yaml(PATH)

print("Loaded modules:")
for module in modules:
    print(f" - {module.__name__}")

# # Reload the model to add the new components
from node_hermes_core.nodes.root_nodes import HermesConfig

output = "schema.json"
with open(output, "w") as schema_file:
    schema_file.write(HermesConfig.get_schema_json())
