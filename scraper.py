# encoding: UTF-8

from lxml import html
import pprint
import requests
import re
import sys
import traceback

class Scraper:
    # already_acquired_armor has format:
    # { <armor_name> : <armor_tier> }
    #
    # excluded_armor has format:
    # [ <armor_name>... ]
    def __init__(self, already_acquired_armor=dict(), excluded_armor=[]):
        self.PAGE_ROOT = 'http://zeldadungeon.net'
        self.total_required_materials = dict()
        self._already_acquired_armor = already_acquired_armor
        self._excluded_armor = excluded_armor

    def scrape(self):
        category_page = requests.get(self.PAGE_ROOT +
                                     '/wiki/Category:Breath_of_the_Wild_Armor')
        category_tree = html.fromstring(category_page.content)

        armor_page_elements_xpath = "//div[@class='mw-category-group']/ul/li/a"
        armor_page_elements = category_tree.xpath(armor_page_elements_xpath)
        armor_page_dicts = [dict( zip(elem.keys(), elem.values()) )
                            for elem in armor_page_elements]

        for armor_page_dict in armor_page_dicts:
            armor_page_url = self.PAGE_ROOT + armor_page_dict['href']
            armor_page_title = armor_page_dict['title']
            self.parseArmorPage(armor_page_url, armor_page_title)

        with open('required-armor-materials', 'w') as out:
            pp = pprint.PrettyPrinter(indent=2)
            out.write(pp.pformat(self.total_required_materials))

    def parseArmorPage(self, url, armor_name):
        # Skip this page if it's on the skip list.
        if armor_name in self._excluded_armor:
            return
        # Skip this page if we already have a fully upgraded armor piece.
        try:
            if self._already_acquired_armor[armor_name] == 4:
                return
        except KeyError:
            pass

        armor_page = requests.get(url)
        armor_page_tree = html.fromstring(armor_page.content)
        table_elements = armor_page_tree.xpath("//table[@class='wikitable']")
        upgrade_table_element = self.findUpgradesTable(table_elements)
        if upgrade_table_element is None:
            # Probably an un-upgradable item.
            return

        row_elements = upgrade_table_element.getchildren()[1:]

        '''
        debug_table_str = u''
        for row in upgrade_table_element.getchildren():
            for cell in row.getchildren():
                debug_table_str += '|'
                debug_table_str += cell.text_content().strip()
            debug_table_str += '\n'
        print debug_table_str.encode(sys.stdout.encoding, errors='replace')
        '''

        '''
        { <armor_name> : { <tier> : [(<material_num>, <material_name>)]}

        ex:
        {
            ...
            'Desert Voe Headband' : {
                1: [
                    (3, 'White Chuchu Jelly')
                ],
                2: [
                    (5, 'White Chuchu Jelly'),
                    (3, 'Ice Keese Wing')
                ],
                3: [
                    (8, 'Ice Keese Wing'),
                    (5, 'Icy Lizalfos Tail')
                ],
                4: [
                    (10, 'Icy Lizalfos Tail'),
                    (5, 'Sapphire')
                ]
            },
            ...
        }
        '''
        tier_material_dict = dict()
        try:
            for i, row_element in enumerate(row_elements):
                # only bother with the tiers that we don't have
                tier = i + 1
                if armor_name in self._already_acquired_armor:
                    if self._already_acquired_armor[armor_name] >= tier:
                        continue

                cell_elements = row_element.getchildren()
                upgrade_cell_element = cell_elements[2]

                materials = self.parseUpgradeCell(upgrade_cell_element)

                tier_material_dict[tier] = materials
        except ValueError as e:
            print '[!] Unable to parse upgrade table on page %s' % title
            traceback.print_exc()
            return

        if not tier_material_dict:
            print '[?] No tiers were processed on page %s' % title
            return

        self.total_required_materials[armor_name] = tier_material_dict

    # There may be multiple tables on the page. Figure out which one contains
    # the upgrade data. The table we are interested in has rows of length 3;
    # the text on the elements of the first row are 'Tier', 'Armor',
    # 'Materials'. One page uses the word 'Rank' instead of 'Tier'. (why???)
    def findUpgradesTable(self, table_elements):
        if len(table_elements) == 1:
            return table_elements[0]
        else:
            upgrade_table_element = None

            for table_element in table_elements:
                first_row_element = table_element.getchildren()[0]
                cell_elements = first_row_element.getchildren()
                if len(cell_elements) != 3:
                    continue
                try:
                    cell_text_contents = [cell.text.strip()
                                          for cell in cell_elements]
                    if (cell_text_contents == ['Tier', 'Armor', 'Materials'] or
                        cell_text_contents == ['Rank', 'Armor', 'Materials']):
                        upgrade_table_element = table_element
                        break
                except AttributeError:
                    continue
            return upgrade_table_element

    # return a list in the form:
    # [
    #     (material_num, material_name),
    #     (material_num, material_name),
    #     ...
    # ]
    def parseUpgradeCell(self, cell_element):
        upgrade_text = cell_element.text_content().strip()
        # upgrade_text is assumed to be in the form:
        # [<num> <x> <material_name>]+
        # with varying whitespace amounts between components, and where
        # <x> can be either the literal 'x' or a unicode cross
        # character (why?????)
        materials_texts_raw = re.split('([0-9]+[^0-9]*)', upgrade_text)
        materials_texts = [c.strip()
                            for c in materials_texts_raw
                            if c.strip()]

        required_materials = []
        for material_text in materials_texts:
            s = re.split(u'x|\xc3\x97', material_text, 1)
            material_num, material_name = [t.strip() for t in s]
            # get rid of curly single quotes
            material_name = material_name.replace(u'\xe2\x80\x98', "'") \
                                           .replace(u'\xe2\x80\x99', "'")
            required_materials.append( (int(material_num), material_name) )
        return required_materials
