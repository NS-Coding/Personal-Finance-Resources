from utils.config_manager import load_config
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64

def get_allocations(age, config):
    glide_path = sorted(config['glide_path'], key=lambda x: x['age'])
    if not glide_path:
        return {}
    # If age is before the first glide path entry
    if age <= glide_path[0]['age']:
        return glide_path[0]['allocations']
    # If age is after the last glide path entry
    if age >= glide_path[-1]['age']:
        return glide_path[-1]['allocations']
    # Interpolate between glide path entries
    for i in range(len(glide_path) - 1):
        age1 = glide_path[i]['age']
        age2 = glide_path[i + 1]['age']
        if age1 <= age <= age2:
            allocations1 = glide_path[i]['allocations']
            allocations2 = glide_path[i + 1]['allocations']
            ratio = (age - age1) / (age2 - age1)
            interpolated_allocations = {}
            for key in allocations1.keys():
                value = allocations1[key] + ratio * (allocations2[key] - allocations1[key])
                interpolated_allocations[key] = round(value, 2)
            return interpolated_allocations
    return {}

def plot_allocations(config=None):
    if config is None:
        config = load_config()
    ages = list(range(1, 101))
    allocation_keys = config['glide_path'][0]['allocations'].keys()
    allocations_over_age = {key: [] for key in allocation_keys}
    for age in ages:
        allocations = get_allocations(age, config)
        for key in allocations_over_age:
            allocations_over_age[key].append(allocations.get(key, 0))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.stackplot(ages, allocations_over_age.values(), labels=allocations_over_age.keys())
    ax.legend(loc='upper right')
    ax.set_xlabel('Age')
    ax.set_ylabel('Allocation Percentage')
    ax.set_title('Asset Allocation Over Age')

    # Save the plot to a bytes buffer and encode it
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    plt.close(fig)
    graph = base64.b64encode(image_png).decode('utf-8')
    return graph
