import json

def get_net_resource_output(infra_object, resource: str = "") -> int:
    if resource == "":
        print("please provide a valid resource")

    with open("functions/buildings.json", 'r') as file:
        values = json.load(file)

    producing_building = None
    output_amount_per_building = 0
    building_count = 0

    for building_name, data in values.items():
        output = data.get("output", {})
        if resource in output:
            producing_building = building_name
            output_amount_per_building = output[resource]
            building_count = getattr(infra_object, building_name, 0)
            break

    if not producing_building:
        return 0

    total_usage = 0
    for building_name, data in values.items():
        inputs = data.get("inputs", {})
        if resource in inputs:
            input_amount_per_building = inputs[resource]
            count = getattr(infra_object, building_name, 0)
            total_usage += input_amount_per_building * count

    return (output_amount_per_building * building_count) - total_usage
