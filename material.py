class Material:
	def __init__(self, name, index):
		self.name = name
		self._index = index

	@staticmethod
	def getMaterial(name):
		return material_dict[name]

	# override comparison operators to just compare index
	def __eq__(self, other):
		if isinstance(other, Material):
			return self._index == other._index
		return NotImplemented

	def __hash__(self):
		return hash(self._index)

	def __ne__(self, other):
		result = self.__eq__(other)
		if result is NotImplemented:
			return result
		return not result

	def __lt__(self, other):
		if isinstance(other, Material):
			return self._index < other._index
		return NotImplemented

	def __gt__(self, other):
		if isinstance(other, Material):
			return self._index > other._index
		return NotImplemented

	def __le__(self, other):
		if isinstance(other, Material):
			return self._index <= other._index
		return NotImplemented

	def __ge__(self, other):
		if isinstance(other, Material):
			return self._index >= other._index
		return NotImplemented

# The ordering reflected in the index parameter is the order
# that these materials appear in the sorted game inventory menu.

# There are gaps -- the materials in this dict are only those
# that are required for armor upgrades.
material_dict = {
	'Voltfruit':               Material('Voltfruit',                 7),
	'Sunshroom':               Material('Sunshroom',                16),
	'Zapshroom':               Material('Zapshroom',                17),
	'Rushroom':                Material('Rushroom',                 18),
	'Silent Shroom':           Material('Silent Shroom',            21),
	'Swift Carrot':            Material('Swift Carrot',             26),
	'Warm Safflina':           Material('Warm Safflina',            29),
	'Swift Violet':            Material('Swift Violet',             31),
	'Blue Nightshade':         Material('Blue Nightshade',          34),
	'Silent Princess':         Material('Silent Princess',          35),
	'Courser Bee Honey':       Material('Courser Bee Honey',        42),
	'Acorn':                   Material('Acorn',                    47),
	'Star Fragment':           Material('Star Fragment',            54),
	"Dinraal's Scale":         Material("Dinraal's Scale",          55),
	"Dinraal's Claw":          Material("Dinraal's Claw",           56),
	"Shard of Dinraal's Fang": Material("Shard of Dinraal's Fang",  57),
	"Shard of Dinraal's Horn": Material("Shard of Dinraal's Horn",  58),
	"Naydra's Scale":          Material("Naydra's Scale",           59),
	"Naydra's Claw":           Material("Naydra's Claw",            60),
	"Shard of Naydra's Fang":  Material("Shard of Naydra's Fang",   61),
	"Shard of Naydra's Horn":  Material("Shard of Naydra's Horn",   62),
	"Farosh's Scale":          Material("Farosh's Scale",           63),
	"Farosh's Claw":           Material("Farosh's Claw",            64),
	"Shard of Farosh's Fang":  Material("Shard of Farosh's Fang",   65),
	"Shard of Farosh's Horn":  Material("Shard of Farosh's Horn",   66),
	'Hearty Bass':             Material('Hearty Bass',              69),
	'Hyrule Bass':             Material('Hyrule Bass',              70),
	'Stealthfin Trout':        Material('Stealthfin Trout',         75),
	'Sneaky River Snail':      Material('Sneaky River Snail',       81),
	'Smotherwing Butterfly':   Material('Smotherwing Butterfly',    89),
	'Energetic Rhino Beetle':  Material('Energetic Rhino Beetle',   96),
	'Sunset Firefly':          Material('Sunset Firefly',           97),
	'Hot-Footed Frog':         Material('Hot-Footed Frog',          98),
	'Hightail Lizard':         Material('Hightail Lizard',         100),
	'Fireproof Lizard':        Material('Fireproof Lizard',        102),
	'Flint':                   Material('Flint',                   103),
	'Amber':                   Material('Amber',                   104),
	'Opal':                    Material('Opal',                    105),
	'Luminous Stone':          Material('Luminous Stone',          106),
	'Topaz':                   Material('Topaz',                   107),
	'Ruby':                    Material('Ruby',                    108),
	'Sapphire':                Material('Sapphire',                109),
	'Diamond':                 Material('Diamond',                 110),
	'Bokoblin Horn':           Material('Bokoblin Horn',           111),
	'Bokoblin Fang':           Material('Bokoblin Fang',           112),
	'Bokoblin Guts':           Material('Bokoblin Guts',           113),
	'Moblin Horn':             Material('Moblin Horn',             114),
	'Moblin Fang':             Material('Moblin Fang',             115),
	'Moblin Guts':             Material('Moblin Guts',             116),
	'Lizalfos Horn':           Material('Lizalfos Horn',           117),
	'Lizalfos Talon':          Material('Lizalfos Talon',          118),
	'Lizalfos Tail':           Material('Lizalfos Tail',           119),
	'Icy Lizalfos Tail':       Material('Icy Lizalfos Tail',       120),
	'Red Lizalfos Tail':       Material('Red Lizalfos Tail',       121),
	'Yellow Lizalfos Tail':    Material('Yellow Lizalfos Tail',    122),
	'Lynel Horn':              Material('Lynel Horn',              123),
	'Lynel Hoof':              Material('Lynel Hoof',              124),
	'Lynel Guts':              Material('Lynel Guts',              125),
	'Chuchu Jelly':            Material('Chuchu Jelly',            126),
	'White Chuchu Jelly':      Material('White Chuchu Jelly',      127),
	'Red Chuchu Jelly':        Material('Red Chuchu Jelly',        128),
	'Yellow Chuchu Jelly':     Material('Yellow Chuchu Jelly',     129),
	'Keese Wing':              Material('Keese Wing',              130),
	'Ice Keese Wing':          Material('Ice Keese Wing',          131),
	'Fire Keese Wing':         Material('Fire Keese Wing',         132),
	'Electric Keese Wing':     Material('Electric Keese Wing',     133),
	'Keese Eyeball':           Material('Keese Eyeball',           134),
	'Octorok Tentacle':        Material('Octorok Tentacle',        135),
	'Octorok Eyeball':         Material('Octorok Eyeball',         136),
	'Octo Balloon':            Material('Octo Balloon',            137),
	'Molduga Fin':             Material('Molduga Fin',             138),
	'Molduga Guts':            Material('Molduga Guts',            139),
	'Hinox Guts':              Material('Hinox Guts',              142),
	'Ancient Screw':           Material('Ancient Screw',           143),
	'Ancient Spring':          Material('Ancient Spring',          144),
	'Ancient Gear':            Material('Ancient Gear',            145),
	'Ancient Shaft':           Material('Ancient Shaft',           146),
	'Ancient Core':            Material('Ancient Core',            147),
	'Giant Ancient Core':      Material('Giant Ancient Core',      148)
}