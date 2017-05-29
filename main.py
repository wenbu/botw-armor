import json
import os
import sys

from scraper import Scraper
from material import Material

# Scrape the zeldadungeon.net wiki.
def scrape():
    s = Scraper()
    s.scrape()

# Output a checklist of materials needed.
# Assumes scraped data present in required-armor-materials.
def calc():
    try:
        with open('armor-already-have.json', 'r') as f:
            armor_already_have = json.load(f)
    except IOError:
        armor_already_have = dict()
    try:
        with open('materials-already-have.json', 'r') as f:
            materials_already_have = json.load(f)
    except IOError:
        materials_already_have = dict()

    materials_required = sum_materials_needed(armor_already_have)

    # Output dicts
    # <Material material : (int num_have, int num_needed)>
    materials = dict()

    for material, num_needed in materials_required.items():
        num_have = materials_already_have[material.name]        \
                   if material.name in materials_already_have   \
                   else 0
        materials[material] = (num_have, num_needed)

    with open('calc-armor-materials', 'w') as f:
        for material, (num_have, num_needed) in sorted(materials.items()):
            complete_flag = 'X' if num_have >= num_needed else ' '
            out_str = '[{:s}] {:3d}/{:<3d} {:s}\n' .format(complete_flag,
                                                           num_have,
                                                           num_needed,
                                                           material.name)
            f.write(out_str)

# Output a blank materials-already-have.json.
# Assumes scraped data present in required-armor-materials.
def make_blank_material_json():
    materials_needed = sum_materials_needed()

    with open('materials-already-have.json', 'w') as f:
        f.write('{\n')
        for i, material in enumerate(sorted(materials_needed)):
            comma = ',' if i < len(materials_needed) - 1 else ''
            out_str = '  "%s": 0%s\n' % (material.name, comma)
            f.write(out_str)
        f.write('}')

def sum_materials_needed(armor_already_have=dict()):
    try:
        with open('required-armor-materials', 'r') as f:
            required_armor_materials = eval(f.read())
    except IOError:
        print 'Error reading required-armor-materials. Please run scrape.'
        raise

    materials_required = dict()
    for armor, armor_materials_needed in required_armor_materials.items():
        tier_in_process = 1
        if armor in armor_already_have:
            tier_in_process = armor_already_have[armor] + 1
        if tier_in_process < 1:
            tier_in_process = 1

        while tier_in_process <= 4:
            for num, material_name in armor_materials_needed[tier_in_process]:
                material = Material.getMaterial(material_name)
                num_already_needed = materials_required.get(material, 0)
                materials_required[material] = num_already_needed + num
            tier_in_process += 1

    return materials_required

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python main.py scrape|calc|json"
    else:
        arg = sys.argv[1]
        if arg == 'scrape':
            scrape()
        elif arg == 'calc':
            calc()
        elif arg == 'json':
            make_blank_material_json()
