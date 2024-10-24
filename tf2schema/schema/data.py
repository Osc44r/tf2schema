"""
Source:
https://github.com/dixon2004/python-tf2-utilities/blob/main/tf2utilities/schema.py
"""

exclusive_genuine = {
    "810": 831,  # Genuine Red-Tape Recorder
    "811": 832,  # Genuine Huo-Long Heater
    "812": 833,  # Genuine Flying Guillotine
    "813": 834,  # Genuine Neon Annihilator
    "814": 835,  # Genuine Triad Trinket
    "815": 836,  # Genuine Champ Stamp
    "816": 837,  # Genuine Marxman
    "817": 838,  # Genuine Human Cannonball
    "30720": 30740,  # Genuine Arkham Cowl
    "30721": 30741,  # Genuine Firefly
    "30724": 30739  # Genuine Fear Monger
}

exclusive_genuine_reversed = {
    "831": 820,  # Red-Tape Recorder
    "832": 811,  # Huo-Long Heater
    "833": 812,  # Flying Guillotine
    "834": 813,  # Neon Annihilator
    "835": 814,  # Triad Trinket
    "836": 815,  # Champ Stamp
    "837": 816,  # Marxman
    "838": 817,  # Human Cannonball
    "30740": 30720,  # Arkham Cowl
    "30741": 30721,  # Firefly
    "30739": 30724  # Fear Monger
}

strangifier_chemistry_set_series = {
    "647": 1,  # All-Father
    "828": 1,  # Archimedes
    "776": 1,  # Bird-Man of Aberdeen
    "451": 1,  # Bonk Boy
    "103": 1,  # Camera Beard
    "446": 1,  # Fancy Dress Uniform
    "541": 1,  # Merc's Pride Scarf
    "733": 1,  # RoBro 3000
    "387": 1,  # Sight for Sore Eyes
    "486": 1,  # Summer Shades
    "386": 1,  # Teddy Roosebelt
    "757": 1,  # Toss-Proof Towel
    "393": 1,  # Villain's Veil
    "30132": 2,  # Blood Banker
    "707": 2,  # Boston Boom-Bringer
    "30073": 2,  # Dark Age Defender
    "878": 2,  # Foppish Physician
    "440": 2,  # Lord Cockswain's Novelty Mutton Chops and Pipe
    "645": 2,  # Outback Intellectual
    "343": 2,  # Professor Speks
    "643": 2,  # Sandvich Safe
    "336": 2,  # Stockbroker's Scarf
    "30377": 3,  # Antarctic Researcher
    "30371": 3,  # Archer's Groundings
    "30353": 3,  # Backstabber's Boomslang
    "30344": 3,  # Bullet Buzz
    "30348": 3,  # Bushi-Dou
    "30361": 3,  # Colonel's Coat
    "30372": 3,  # Combat Slacks
    "30367": 3,  # Cute Suit
    "30357": 3,  # Dark Falkirk Helm
    "30375": 3,  # Deep Cover Operator
    "30350": 3,  # Dough Puncher
    "30341": 3,  # Ein
    "30369": 3,  # Eliminator's Safeguard
    "30349": 3,  # Fashionable Megalomaniac
    "30379": 3,  # Gaiter Guards
    "30343": 3,  # Gone Commando
    "30338": 3,  # Ground Control
    "30356": 3,  # Heat of Winter
    "30342": 3,  # Heavy Lifter
    "30378": 3,  # Heer's Helmet
    "30359": 3,  # Huntsman's Essentials
    "30363": 3,  # Juggernaut Jacket
    "30339": 3,  # Killer's Kit
    "30362": 3,  # Law
    "30345": 3,  # Leftover Trap
    "30352": 3,  # Mustachioed Mann
    "30360": 3,  # Napoleon Complex
    "30354": 3,  # Rat Stompers
    "30374": 3,  # Sammy Cap
    "30366": 3,  # Sangu Sleeves
    "30347": 3,  # Scotch Saver
    "30365": 3,  # Smock Surgeon
    "30355": 3,  # Sole Mate
    "30358": 3,  # Sole Saviors
    "30340": 3,  # Stylish DeGroot
    "30351": 3,  # Teutonic Toque
    "30376": 3,  # Ticket Boy
    "30373": 3,  # Toowoomba Tunic
    "30346": 3,  # Trash Man
    "30336": 3,  # Trencher's Topper
    "30337": 3,  # Trencher's Tunic
    "30368": 3,  # War Goggles
    "30364": 3,  # Warmth Preserver
}

retired_keys = [
    {"defindex": 5049, "name": 'Festive Winter Crate Key'},
    {"defindex": 5067, "name": 'Refreshing Summer Cooler Key'},
    {"defindex": 5072, "name": 'Naughty Winter Crate Key'},
    {"defindex": 5073, "name": 'Nice Winter Crate Key'},
    {"defindex": 5079, "name": 'Scorched Key'},
    {"defindex": 5081, "name": 'Fall Key'},
    {"defindex": 5628, "name": 'Eerie Key'},
    {"defindex": 5631, "name": 'Naughty Winter Crate Key 2012'},
    {"defindex": 5632, "name": 'Nice Winter Crate Key 2012'},
    {"defindex": 5713, "name": 'Spooky Key'},  # Non-Craftable
    {"defindex": 5716, "name": 'Naughty Winter Crate Key 2013'},  # Non-Craftable
    {"defindex": 5717, "name": 'Nice Winter Crate Key 2013'},  # Non-Craftable
    {"defindex": 5762, "name": 'Limited Late Summer Crate Key'},  # Non-Craftable
    {"defindex": 5791, "name": 'Naughty Winter Crate Key 2014'},
    {"defindex": 5792, "name": 'Nice Winter Crate Key 2014'}
]

retired_keys_names = [key.get("name").lower() for key in list(retired_keys)]

__all__ = [
    "exclusive_genuine",
    "exclusive_genuine_reversed",
    "strangifier_chemistry_set_series",
    "retired_keys",
    "retired_keys_names"
]
