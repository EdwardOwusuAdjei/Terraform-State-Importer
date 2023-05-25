import json
import sys
import re


def find_resource_name(file_path):

    # Open the Terraform file
    with open(file_path) as f:
        tf_file = f.read()

    # Use regular expressions to extract resource identifiers
    # resource_identifiers = re.findall(r'resource ".*" "(.*)"', tf_file)
    resource_names = re.findall(r'resource "(.*?)" "(.*?)"', tf_file)
    resource_identifiers = [f"{name[0]}.{name[1]}" for name in resource_names]
    module_identifiers = re.findall(r'module "(.*)" {', tf_file)
    module_identifiers = ["module." + x for x in module_identifiers]
   
    print("----------")
        # Combine the lists and remove duplicates
    all_identifiers = list(resource_identifiers + module_identifiers)

    return all_identifiers

def find_outputs(file_path):

    # Open the Terraform file
    with open(file_path) as f:
        tf_file = f.read()

    output_identifiers = re.findall(r'output "(.*)" {', tf_file)
    return output_identifiers

tfstate_file = sys.argv[1]
resource_names = find_resource_name(sys.argv[2])
outputs = find_outputs(sys.argv[2])

print(f"found {len(resource_names)} resources and modules, with names: ")
print('resources:', *resource_names, sep='\n* ')
if outputs:
    print("--------------------------------------------")
    print(f"found {len(outputs)} outputs, with names: ")
    print('output:', *outputs, sep='\n- ')
with open(tfstate_file, 'r') as f:
    tfstate = json.load(f)

outer_blocks = []
module_blocks = []
for resource_name in resource_names:
    resource_block = None
    for resource in tfstate['resources']:
        ignore_message = False
        if resource.get('module') is None and f"{resource['type']}.{resource['name']}" == resource_name:
            resource_block = resource
            break
        elif resource.get('module') is not None and resource.get('module') == resource_name:
            ignore_message = True
            for this_module in  tfstate['resources']:
                if this_module.get('module') == resource_name:
                    module_blocks.append(this_module)
            break

    if resource_block:
        current_block = resource_block
        while current_block.get('parent'):
            for block in tfstate['resources']:
                if block['address'] == current_block['parent']:
                    current_block = block
                    break
            else:
                break
        else:
            outer_block = current_block
            if outer_block not in outer_blocks:
                outer_blocks.append(outer_block)
    else:
        if not ignore_message:
            print(f"Identifier '{resource_name}' not found")

outer_blocks = outer_blocks + module_blocks
output_list = []
# work on outputs here
for output in tfstate['outputs']:
    if output in outputs:
        output_list.append({output: tfstate['outputs'].get(output)})

# convert them into key val struct out tfstate output
new_outputs = {}
for item in output_list:
    key = list(item.keys())[0]
    value = item[key]
    new_outputs[key] = {
        **value
    }


output_tfstate = {
    "version": tfstate['version'],
    "terraform_version": tfstate['terraform_version'],
    "serial": tfstate['serial'],
    "lineage": tfstate['lineage'],
    "outputs": new_outputs,
    "resources": outer_blocks
}

with open("default.tfstate", "w") as tf_file:
    tf_file.write(json.dumps(output_tfstate, indent=4))