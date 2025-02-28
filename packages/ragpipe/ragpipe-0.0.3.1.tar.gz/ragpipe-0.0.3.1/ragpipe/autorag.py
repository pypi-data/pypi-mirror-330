
from pathlib import Path
import itertools
import copy

def build_configs(options_fname):
    import yaml

    with open(options_fname, 'r') as f:
        options_data = yaml.safe_load(f)
    
    # build a list of all cross product of options. apply override to base_config
    
    # Separate each field and its options for combination generation
    fields = []
    values = []
    
    # Handles only one-level nested fields. TODO: generalize!
    for key, options in options_data.items():
        if isinstance(options, dict):
            for sub_key, sub_values in options.items():
                fields.append((key, sub_key))
                values.append(sub_values)
        else:
            fields.append((key,))
            values.append(options)
    
    # Generate all combinations
    combinations = list(itertools.product(*values))
    
    # Build configurations for each combination
    configs = []
    for combination in combinations:
        config = {}
        for (field_keys, value) in zip(fields, combination):
            # Traverse the fields and assign the combination values
            current = config
            for key in field_keys[:-1]:
                current = current.setdefault(key, {})
            current[field_keys[-1]] = value
        configs.append(config)
    
    return configs


def explore(workflow_class, base_config_fname, options_fname):
    from .common import load_func, printd
    from .config import RPConfig, load_config, deep_update

    W = load_func(workflow_class)()
    base_configd = load_config(base_config_fname, as_dict=True)
    _, json_path, query_text = W.init(base_config_fname)

    optionds = build_configs(options_fname)
    #print(optionds)
    printd(1, f'query: {query_text}')
    
    for optiond in optionds:
        configd = deep_update(copy.deepcopy(base_configd), optiond)
        #print(configd)
        config = RPConfig(**configd)

        D = W.build_data_model(json_path, config)
        from ragpipe import Retriever
        
        docs_retrieved = Retriever(config).eval(query_text, D, clear_reps=['query.text'])
        #print(docs_retrieved) #response generator
        for doc in docs_retrieved: doc.show()

def draw():
    import matplotlib.pyplot as plt

    # Define x values and two y value sets
    x = [100, 1000, 5000, 10000]
    y1 = [4.5, 5, 5, 5]   # y1 stays low and relatively flat
    y2 = [5, 16, 76, 135] # y2 diverges quickly

    # Create the plot
    plt.figure(figsize=(8, 6))
    plt.plot(x, y1, label='M2V encoder (flat)', marker='o', color='blue', linestyle='--')
    plt.plot(x, y2, label='BGE small encoder (diverges)', marker='o', color='red', linestyle='-')

    # Add labels and title
    plt.xlabel("dataset size")
    plt.ylabel("time (s)")
    plt.legend()
    plt.grid(True)

    # Show plot
    plt.show()

if __name__ == '__main__':
    draw()
    raise ValueError()

    import time
    parent = Path(__file__).parent / '../examples' ; 
    base_config_fname = f'{parent}/startups.yml'
    options_fname = f'{parent}/startups_options.yml'
    start_time = time.perf_counter()
    explore('examples.startups.Workflow', base_config_fname, options_fname)

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Duration: {duration} seconds")