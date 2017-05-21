import json
import os
import pprint
import scraper
import sys

def scrape():
    s = scraper.Scraper()
    s.scrape()

def calc():
    components_file = './required-armor-components'
    if not os.path.isfile(components_file):
        scrape()
    with open(components_file, 'r') as f:
        components = eval(f.read())
    try:
        with open('armor-already-have.json', 'r') as f:
            armor_already_have = json.load(f)
    except IOError:
        armor_already_have = dict()
    try:
        with open('components-already-have.json', 'r') as f:
            components_already_have = json.load(f)
    except IOError:
        components_already_have = dict()

    components_needed = dict()

    for armor, armor_components_needed in components.items():
        tier_in_process = 1
        if armor in armor_already_have:
            tier_in_process = armor_already_have[armor]
        if tier_in_process < 1:
            tier_in_process = 1

        while tier_in_process <= 4:
            for num, component in armor_components_needed[tier_in_process]:
                num_already_needed = components_needed.get(str(component), 0)
                components_needed[str(component)] = num_already_needed + num
            tier_in_process += 1

    for component, num in components_already_have.items():
        if component in components_needed:
            num_needed = components_needed[component]
            if num >= num_needed:
                components_needed.pop(component)
            else:
                components_needed[component] -= num

    with open('calc-armor-components', 'w') as f:
        pp = pprint.PrettyPrinter(indent=2)
        f.write(pp.pformat(components_needed))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python main.py scrape|calc"
    else:
        arg = sys.argv[1]
        if arg == 'scrape':
            scrape()
        elif arg == 'calc':
            calc()
