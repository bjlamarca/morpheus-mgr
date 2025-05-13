from .models import Color, ColorFamily

def get_color_list():
    return html_color_list

def create_color_families():
    color_set = set()
    for color in html_color_list:
        for family in color['families']:
            fam_cap = family.capitalize()
            color_set.add(fam_cap)

    for family in color_set:
        new_family = ColorFamily.objects.create(name=family)
        new_family.save()

def colors_db_sync():
    for color in html_color_list:
        print(color['rgb'][4:7],color['rgb'][9:12], color['rgb'][14:17])
        
        new_color = Color.objects.create(
            name = (color['name']).title(),
            favorite = False,
            hex_code = color['hex'],
            red = int(color['rgb'][4:7]),
            green = int(color['rgb'][9:12]),
            blue = int(color['rgb'][14:17])
        )
        new_color.save()
        for family in color['families']:
            fam_cap = family.capitalize()
            fam_obj = ColorFamily.objects.get(name=fam_cap)
            print('fam', fam_obj)
            new_color.color_family.add(fam_obj)
            new_color.save()

def color_sort():
  colors = Color.objects.all().order_by('id')
  sort_order = 20
  for color in colors:
    color.sort = sort_order
    sort_order += 1
    color.save()
  print('done')

def color_add_favorites():
    new_color = Color()
    new_color.favorite = True
    new_color.name = 'Hue Bright'
    new_color.hex_code = '#FFCE78'
    new_color.red = 255
    new_color.green = 206
    new_color.blue = 120
    new_color.favorite = True
    new_color.sort = 1
    new_color.save()


              


html_color_list =[
  {
    "name": "INDIAN RED",
    "hex": "#CD5C5C",
    "rgb": "RGB(205, 092, 092)",
    "families": ["red", "brown"]
  },
  {
    "name": "LIGHT CORAL",
    "hex": "#F08080",
    "rgb": "RGB(240, 128, 128)",
    "families": ["red", "pink", "coral", "light"]
  },
  {
    "name": "SALMON",
    "hex": "#FA8072",
    "rgb": "RGB(250, 128, 114)",
    "families": ["red", "pink", "orange", "salmon"]
  },
  {
    "name": "DARK SALMON",
    "hex": "#E9967A",
    "rgb": "RGB(233, 150, 122)",
    "families": ["red", "pink", "orange", "salmon", "dark"]
  },
  {
    "name": "LIGHT SALMON",
    "hex": "#FFA07A",
    "rgb": "RGB(255, 160, 122)",
    "families": ["red", "pink", "orange", "salmon", "light"]
  },
  {
    "name": "CRIMSON",
    "hex": "#DC143C",
    "rgb": "RGB(220, 020, 060)",
    "families": ["red"]
  },
  {
    "name": "RED",
    "hex": "#FF0000",
    "rgb": "RGB(255, 000, 000)",
    "families": ["red"]
  },
  {
    "name": "DARK RED",
    "hex": "#8B0000",
    "rgb": "RGB(139, 000, 000)",
    "families": ["red", "dark"]
  },
  {
    "name": "PINK",
    "hex": "#FFC0CB",
    "rgb": "RGB(255, 192, 203)",
    "families": ["pink"]
  },
  {
    "name": "LIGHT PINK",
    "hex": "#FFB6C1",
    "rgb": "RGB(255, 182, 193)",
    "families": ["pink", "light"]
  },
  {
    "name": "HOT PINK",
    "hex": "#FF69B4",
    "rgb": "RGB(255, 105, 180)",
    "families": ["pink", "hot"]
  },
  {
    "name": "DEEP PINK",
    "hex": "#FF1493",
    "rgb": "RGB(255, 020, 147)",
    "families": ["pink", "deep"]
  },
  {
    "name": "MEDIUM VIOLETRED",
    "hex": "#C71585",
    "rgb": "RGB(199, 021, 133)",
    "families": ["pink", "purple", "violet", "medium"]
  },
  {
    "name": "PALE VIOLET RED",
    "hex": "#DB7093",
    "rgb": "RGB(219, 112, 147)",
    "families": ["pink", "pale", "violet"]
  },
  {
    "name": "CORAL",
    "hex": "#FF7F50",
    "rgb": "RGB(255, 127, 080)",
    "families": ["orange", "coral"]
  },
  {
    "name": "TOMATO",
    "hex": "#FF6347",
    "rgb": "RGB(255, 099, 071",
    "families": ["orange", "red"]
  },
  {
    "name": "ORANGE RED",
    "hex": "#FF4500",
    "rgb": "RGB(255, 069, 000)",
    "families": ["orange", "red"]
  },
  {
    "name": "DARK ORANGE",
    "hex": "#FF8C00",
    "rgb": "RGB(255, 140, 000)",
    "families": ["orange", "dark"]
  },
  {
    "name": "ORANGE",
    "hex": "#FFA500",
    "rgb": "RGB(255, 165, 000)",
    "families": ["orange"]
  },
  {
    "name": "GOLD",
    "hex": "#FFD700",
    "rgb": "RGB(255, 215, 000)",
    "families": ["yellow"]
  },
  {
    "name": "YELLOW",
    "hex": "#FFFF00",
    "rgb": "RGB(255, 255, 000)",
    "families": ["yellow"]
  },
  {
    "name": "LIGHT YELLOW",
    "hex": "#FFFFE0",
    "rgb": "RGB(255, 255, 224)",
    "families": ["yellow", "light"]
  },
  {
    "name": "LEMON CHIFFON",
    "hex": "#FFFACD",
    "rgb": "RGB(255, 250, 205)",
    "families": ["yellow", "lemon"]
  },
  {
    "name": "LIGHT GOLDENROD YELLOW",
    "hex": "#FAFAD2",
    "rgb": "RGB(250, 250, 210)",
    "families": ["yellow", "light", "goldenrod", "tan"]
  },
  {
    "name": "PAPAYA WHIP",
    "hex": "#FFEFD5",
    "rgb": "RGB(255, 239, 213)",
    "families": ["pink", "tan"]
  },
  {
    "name": "MOCCASIN",
    "hex": "#FFE4B5",
    "rgb": "RGB(255, 228, 181)",
    "families": ["pink", "tan"]
  },
  {
    "name": "PEACH PUFF",
    "hex": "#FFDAB9",
    "rgb": "RGB(255, 218, 185)",
    "families": ["pink", "orange", "peach"]
  },
  {
    "name": "PALE GOLDENROD",
    "hex": "#EEE8AA",
    "rgb": "RGB(238, 232, 170)",
    "families": ["yellow", "tan", "pale", "goldenrod"]
  },
  {
    "name": "KHAKI",
    "hex": "#F0E68C",
    "rgb": "RGB(240, 230, 140)",
    "families": ["yellow", "tan", "khaki"]
  },
  {
    "name": "DARK KHAKI",
    "hex": "#BDB76B",
    "rgb": "RGB(189, 183, 107)",
    "families": ["yellow", "tan", "khaki", "dark"]
  },
  {
    "name": "LAVENDER",
    "hex": "#E6E6FA",
    "rgb": "RGB(230, 230, 250)",
    "families": ["purple"]
  },
  {
    "name": "THISTLE",
    "hex": "#D8BFD8",
    "rgb": "RGB(216, 191, 216)",
    "families": ["purple"]
  },
  {
    "name": "PLUM",
    "hex": "#DDA0DD",
    "rgb": "RGB(221, 160, 221)",
    "families": ["purple"]
  },
  {
    "name": "VIOLET",
    "hex": "#EE82EE",
    "rgb": "RGB(238, 130, 238)",
    "families": ["purple", "violet", "pink"]
  },
  {
    "name": "ORCHID",
    "hex": "#DA70D6",
    "rgb": "RGB(218, 112, 214)",
    "families": ["purple", "orchid"]
  },
  {
    "name": "FUCHSIA",
    "hex": "#FF00FF",
    "rgb": "RGB(255, 000, 255)",
    "families": ["purple", "pink"]
  },
  {
    "name": "MAGENTA",
    "hex": "#FF00FF",
    "rgb": "RGB(255, 000, 255)",
    "families": ["purple", "pink", "magenta"]
  },
  {
    "name": "MEDIUM ORCHID",
    "hex": "#BA55D3",
    "rgb": "RGB(186, 085, 211)",
    "families": ["purple", "orchid", "medium"]
  },
  {
    "name": "MEDIUM PURPLE",
    "hex": "#9370DB",
    "rgb": "RGB(147, 112, 219)",
    "families": ["purple", "medium"]
  },
  {
    "name": "REBECCA PURPLE",
    "hex": "#663399",
    "rgb": "RGB(102, 051, 153)",
    "families": ["purple", "blue"]
  },
  {
    "name": "BLUE VIOLET",
    "hex": "#8A2BE2",
    "rgb": "RGB(138, 043, 226)",
    "families": ["purple", "blue", "violet"]
  },
  {
    "name": "DARK VIOLET",
    "hex": "#9400D3",
    "rgb": "RGB(148, 000, 211)",
    "families": ["purple", "dark", "violet"]
  },
  {
    "name": "DARK ORCHID",
    "hex": "#9932CC",
    "rgb": "RGB(153, 050, 204)",
    "families": ["purple", "dark", "orchid"]
  },
  {
    "name": "DARK MAGENTA",
    "hex": "#8B008B",
    "rgb": "RGB(139, 000, 139)",
    "families": ["purple", "dark", "magenta"]
  },
  {
    "name": "PURPLE",
    "hex": "#800080",
    "rgb": "RGB(128, 000, 128)",
    "families": ["purple"]
  },
  {
    "name": "INDIGO",
    "hex": "#4B0082",
    "rgb": "RGB(075, 000, 130)",
    "families": ["purple", "blue"]
  },
  {
    "name": "SLATE BLUE",
    "hex": "#6A5ACD",
    "rgb": "RGB(106, 090, 205)",
    "families": ["purple", "blue", "slate"]
  },
  {
    "name": "DARK SLATE BLUE",
    "hex": "#483D8B",
    "rgb": "RGB(072, 061, 139)",
    "families": ["purple", "blue", "slate", "dark"]
  },
  {
    "name": "MEDIUM SLATE BLUE",
    "hex": "#7B68EE",
    "rgb": "RGB(123, 104, 238)",
    "families": ["purple", "blue", "slate", "medium"]
  },
  {
    "name": "GREEN YELLOW",
    "hex": "#ADFF2F",
    "rgb": "RGB(173, 255, 047)",
    "families": ["green", "yellow"]
  },
  {
    "name": "CHARTREUSE",
    "hex": "#7FFF00",
    "rgb": "RGB(127, 255, 000)",
    "families": ["green"]
  },
  {
    "name": "LAWN GREEN",
    "hex": "#7CFC00",
    "rgb": "RGB(124, 252, 000)",
    "families": ["green"]
  },
  {
    "name": "LIME",
    "hex": "#00FF00",
    "rgb": "RGB(000, 255, 000)",
    "families": ["green"]
  },
  {
    "name": "LIME GREEN",
    "hex": "#32CD32",
    "rgb": "RGB(050, 205, 050)",
    "families": ["green"]
  },
  {
    "name": "PALE GREEN",
    "hex": "#98FB98",
    "rgb": "RGB(152, 251, 152)",
    "families": ["green", "pale"]
  },
  {
    "name": "LIGHT GREEN",
    "hex": "#90EE90",
    "rgb": "RGB(144, 238, 144)",
    "families": ["green", "light"]
  },
  {
    "name": "MEDIUM SPRING GREEN",
    "hex": "#00FA9A",
    "rgb": "RGB(000, 250, 154)",
    "families": ["green", "medium", "spring"]
  },
  {
    "name": "SPRING GREEN",
    "hex": "#00FF7F",
    "rgb": "RGB(000, 255, 127)",
    "families": ["green", "spring"]
  },
  {
    "name": "MEDIUM SEA GREEN",
    "hex": "#3CB371",
    "rgb": "RGB(060, 179, 113)",
    "families": ["green", "sea", "medium"]
  },
  {
    "name": "SEA GREEN",
    "hex": "#2E8B57",
    "rgb": "RGB(046, 139, 087)",
    "families": ["green", "sea"]
  },
  {
    "name": "FOREST GREEN",
    "hex": "#228B22",
    "rgb": "RGB(034, 139, 034)",
    "families": ["green", "forest"]
  },
  {
    "name": "GREEN",
    "hex": "#008000",
    "rgb": "RGB(000, 128, 000)",
    "families": ["green"]
  },
  {
    "name": "DARK GREEN",
    "hex": "#006400",
    "rgb": "RGB(000, 100, 000)",
    "families": ["green", "dark"]
  },
  {
    "name": "YELLO WGREEN",
    "hex": "#9ACD32",
    "rgb": "RGB(154, 205, 050)",
    "families": ["green", "yellow"]
  },
  {
    "name": "OLIVE DRAB",
    "hex": "#6B8E23",
    "rgb": "RGB(107, 142, 035)",
    "families": ["green", "olive"]
  },
  {
    "name": "OLIVE",
    "hex": "#6B8E23",
    "rgb": "RGB(128, 128, 000)",
    "families": ["green", "olive"]
  },
  {
    "name": "DARK OLIVE GREEN",
    "hex": "#556B2F",
    "rgb": "RGB(085, 107, 047)",
    "families": ["green", "olive", "dark"]
  },
  {
    "name": "MEDIUM AQUA MARINE",
    "hex": "#66CDAA",
    "rgb": "RGB(102, 205, 170)",
    "families": ["green", "blue", "aquamarine", "medium"]
  },
  {
    "name": "DARK SEA GREEN",
    "hex": "#8FBC8B",
    "rgb": "RGB(143, 188, 139)",
    "families": ["green", "sea", "dark"]
  },
  {
    "name": "LIGHT SEA GREEN",
    "hex": "#20B2AA",
    "rgb": "RGB(032, 178, 170)",
    "families": ["green", "blue", "sea", "light"]
  },
  {
    "name": "DARK CYAN",
    "hex": "#008B8B",
    "rgb": "RGB(000, 139, 139)",
    "families": ["green", "blue", "cyan", "dark"]
  },
  {
    "name": "TEAL",
    "hex": "#008080",
    "rgb": "RGB(000, 128, 128)",
    "families": ["green", "blue"]
  },
  {
    "name": "AQUA",
    "hex": "#00FFFF",
    "rgb": "RGB(000, 255, 255)",
    "families": ["blue", "aqua"]
  },
  {
    "name": "CYAN",
    "hex": "#00FFFF",
    "rgb": "RGB(000, 255, 255)",
    "families": ["blue", "cyan"]
  },
  {
    "name": "LIGHT CYAN",
    "hex": "#E0FFFF",
    "rgb": "RGB(224, 255, 255)",
    "families": ["blue", "cyan", "light"]
  },
  {
    "name": "PALE TURQUOISE",
    "hex": "#AFEEEE",
    "rgb": "RGB(175, 238, 238)",
    "families": ["blue", "turquoise", "pale"]
  },
  {
    "name": "AQUA MARINE",
    "hex": "#7FFFD4",
    "rgb": "RGB(127, 255, 212)",
    "families": ["blue", "aquamarine"]
  },
  {
    "name": "TURQUOISE",
    "hex": "#40E0D0",
    "rgb": "RGB(065, 224, 208)",
    "families": ["blue", "turquoise"]
  },
  {
    "name": "MEDIUM TURQUOISE",
    "hex": "#48D1CC",
    "rgb": "RGB(072, 209, 204)",
    "families": ["blue", "turquoise", "medium"]
  },
  {
    "name": "DARK TURQUOISE",
    "hex": "#00CED1",
    "rgb": "RGB(000, 206, 209)",
    "families": ["blue", "turquoise", "dark"]
  },
  {
    "name": "CADET BLUE",
    "hex": "#5F9EA0",
    "rgb": "RGB(095, 158, 160)",
    "families": ["blue", "gray"]
  },
  {
    "name": "STEEL BLUE",
    "hex": "#4682B4",
    "rgb": "RGB(070, 130, 180)",
    "families": ["blue", "steel"]
  },
  {
    "name": "LIGHT STEEL BLUE",
    "hex": "#B0C4DE",
    "rgb": "RGB(176, 196, 222)",
    "families": ["blue", "steel", "light"]
  },
  {
    "name": "POWDER BLUE",
    "hex": "#B0E0E6",
    "rgb": "RGB(176, 224, 230)",
    "families": ["blue"]
  },
  {
    "name": "LIGHT BLUE",
    "hex": "#ADD8E6",
    "rgb": "RGB(173, 216, 230)",
    "families": ["blue", "light"]
  },
  {
    "name": "SKY BLUE",
    "hex": "#87CEEB",
    "rgb": "RGB(135, 206, 235)",
    "families": ["blue", "sky"]
  },
  {
    "name": "LIGHT SKY BLUE",
    "hex": "#87CEFA",
    "rgb": "RGB(135, 206, 250)",
    "families": ["blue", "sky", "light"]
  },
  {
    "name": "DEEP SKY BLUE",
    "hex": "#00BFFF",
    "rgb": "RGB(000, 191, 255)",
    "families": ["blue", "sky", "deep"]
  },
  {
    "name": "DODGER BLUE",
    "hex": "#1E90FF",
    "rgb": "RGB(030, 144, 255)",
    "families": ["blue"]
  },
  {
    "name": "CORN FLOWER BLUE",
    "hex": "#6495ED",
    "rgb": "RGB(100, 149, 237)",
    "families": ["blue"]
  },
  {
    "name": "ROYAL BLUE",
    "hex": "#4169E1",
    "rgb": "RGB(064, 105, 225)",
    "families": ["blue"]
  },
  {
    "name": "BLUE",
    "hex": "#0000FF",
    "rgb": "RGB(000, 000, 255)",
    "families": ["blue"]
  },
  {
    "name": "MEDIUM BLUE",
    "hex": "#0000CD",
    "rgb": "RGB(000, 000, 205)",
    "families": ["blue", "medium"]
  },
  {
    "name": "DARK BLUE",
    "hex": "#00008B",
    "rgb": "RGB(000, 000, 139)",
    "families": ["blue", "dark"]
  },
  {
    "name": "NAVY",
    "hex": "#00008B",
    "rgb": "RGB(000, 000, 128)",
    "families": ["blue", "dark"]
  },
  {
    "name": "MIDNIGHT BLUE",
    "hex": "#191970",
    "rgb": "RGB(025, 025, 112))",
    "families": ["blue", "dark"]
  },
  {
    "name": "CORNSILK",
    "hex": "#FFF8DC",
    "rgb": "RGB(255, 248, 220)",
    "families": ["brown", "tan"]
  },
  {
    "name": "BLANCHED ALMOND",
    "hex": "#FFEBCD",
    "rgb": "RGB(255, 235, 205)",
    "families": ["brown", "tan"]
  },
  {
    "name": "BISQUE",
    "hex": "#FFE4C4",
    "rgb": "RGB(255, 228, 196)",
    "families": ["brown", "tan"]
  },
  {
    "name": "NAVAJO WHITE",
    "hex": "#FFDEAD",
    "rgb": "RGB(255, 222, 173)",
    "families": ["brown", "tan"]
  },
  {
    "name": "WHEAT",
    "hex": "#F5DEB3",
    "rgb": "RGB(245, 222, 179)",
    "families": ["brown", "tan"]
  },
  {
    "name": "BURLY WOOD",
    "hex": "#DEB887",
    "rgb": "RGB(222, 184, 135)",
    "families": ["brown", "tan"]
  },
  {
    "name": "TAN",
    "hex": "#D2B48C",
    "rgb": "RGB(210, 180, 140)",
    "families": ["brown", "tan"]
  },
  {
    "name": "ROSY BROWN",
    "hex": "#BC8F8F",
    "rgb": "RGB(188, 143, 143)",
    "families": ["brown", "tan"]
  },
  {
    "name": "SANDY BROWN",
    "hex": "#F4A460",
    "rgb": "RGB(244, 164, 096)",
    "families": ["brown", "orange"]
  },
  {
    "name": "GOLDENROD",
    "hex": "#DAA520",
    "rgb": "RGB(218, 165, 032)",
    "families": ["brown", "goldenrod", "orange"]
  },
  {
    "name": "DARK GOLDENROD",
    "hex": "#B8860B",
    "rgb": "RGB(184, 134, 011)",
    "families": ["brown", "orange", "goldenrod", "dark"]
  },
  {
    "name": "PERU",
    "hex": "#CD853F",
    "rgb": "RGB(205, 133, 063)",
    "families": ["brown", "orange"]
  },
  {
    "name": "CHOCOLATE",
    "hex": "#D2691E",
    "rgb": "RGB(210, 105, 030)",
    "families": ["brown", "orange"]
  },
  {
    "name": "SADDLE BROWN",
    "hex": "#8B4513",
    "rgb": "RGB(139, 069, 019)",
    "families": ["brown"]
  },
  {
    "name": "SIENNA",
    "hex": "#A0522D",
    "rgb": "RGB(160, 082, 045)",
    "families": ["brown"]
  },
  {
    "name": "BROWN",
    "hex": "#A52A2A",
    "rgb": "RGB(165, 042, 042)",
    "families": ["brown", "red"]
  },
  {
    "name": "MAROON",
    "hex": "#800000",
    "rgb": "RGB(128, 000, 000)",
    "families": ["brown", "red"]
  },
  {
    "name": "WHITE",
    "hex": "#FFFFFF",
    "rgb": "RGB(255, 255, 255)",
    "families": ["white"]
  },
  {
    "name": "SNOW",
    "hex": "#FFFAFA",
    "rgb": "RGB(255, 250, 250)",
    "families": ["white"]
  },
  {
    "name": "HONEY DEW",
    "hex": "#F0FFF0",
    "rgb": "RGB(240, 255, 240)",
    "families": ["white"]
  },
  {
    "name": "MINT CREAM",
    "hex": "#F5FFFA",
    "rgb": "RGB(245, 255, 250)",
    "families": ["white"]
  },
  {
    "name": "AZURE",
    "hex": "#F0FFFF",
    "rgb": "RGB(240, 255, 255)",
    "families": ["white"]
  },
  {
    "name": "ALICE BLUE",
    "hex": "#F0F8FF",
    "rgb": "RGB(240, 248, 255)",
    "families": ["white"]
  },
  {
    "name": "GHOST WHITE",
    "hex": "#F8F8FF",
    "rgb": "RGB(248, 248, 255)",
    "families": ["white"]
  },
  {
    "name": "WHITE SMOKE",
    "hex": "#F5F5F5",
    "rgb": "RGB(245, 245, 245)",
    "families": ["white"]
  },
  {
    "name": "SEA SHELL",
    "hex": "#FFF5EE",
    "rgb": "RGB(255, 245, 238)",
    "families": ["white", "pink"]
  },
  {
    "name": "BEIGE",
    "hex": "#F5F5DC",
    "rgb": "RGB(245, 245, 220)",
    "families": ["white", "tan"]
  },
  {
    "name": "OLDL ACE",
    "hex": "#FDF5E6",
    "rgb": "RGB(253, 245, 230)",
    "families": ["white", "tan"]
  },
  {
    "name": "FLORAL WHITE",
    "hex": "#FDF5E6",
    "rgb": "RGB(253, 245, 230)",
    "families": ["white", "tan"]
  },
  {
    "name": "IVORY",
    "hex": "#FFFFF0",
    "rgb": "RGB(255, 255, 240)",
    "families": ["white", "tan"]
  },
  {
    "name": "ANTIQUE WHITE",
    "hex": "#FAEBD7",
    "rgb": "RGB(250, 235, 215)",
    "families": ["white", "tan"]
  },
  {
    "name": "LINEN",
    "hex": "#FAF0E6",
    "rgb": "RGB(250, 240, 230)",
    "families": ["white", "tan"]
  },
  {
    "name": "LAVENDER BLUSH",
    "hex": "#FFF0F5",
    "rgb": "RGB(255, 240, 245)",
    "families": ["white", "lavender", "pink"]
  },
  {
    "name": "MISTY OSE",
    "hex": "#FFE4E1",
    "rgb": "RGB(255, 228, 225)",
    "families": ["white", "pink"]
  },
  {
    "name": "GAINS BORO",
    "hex": "#DCDCDC",
    "rgb": "RGB(220, 220, 220)",
    "families": ["gray"]
  },
  {
    "name": "LIGHT GRAY",
    "hex": "#D3D3D3",
    "rgb": "RGB(211, 211, 211)",
    "families": ["gray", "light"]
  },
  {
    "name": "SILVER",
    "hex": "#C0C0C0",
    "rgb": "RGB(192, 192, 192)",
    "families": ["gray"]
  },
  {
    "name": "DARK GRAY",
    "hex": "#A9A9A9",
    "rgb": "RGB(169, 169, 169)",
    "families": ["gray", "dark"]
  },
  {
    "name": "GRAY",
    "hex": "#808080",
    "rgb": "RGB(128, 128, 128)",
    "families": ["gray"]
  },
  {
    "name": "DIM GRAY",
    "hex": "#696969",
    "rgb": "RGB(105, 105, 105)",
    "families": ["gray"]
  },
  {
    "name": "LIGHT SLATE GRAY",
    "hex": "#778899",
    "rgb": "RGB(119, 136, 153)",
    "families": ["gray", "light", "slate"]
  },
  {
    "name": "SLATE GRAY",
    "hex": "#708090",
    "rgb": "RGB(112, 128, 144)",
    "families": ["gray",  "slate"]
  },
  {
    "name": "DARK SLATE GRAY",
    "hex": "#2F4F4F",
    "rgb": "RGB(047, 079, 079)",
    "families": ["gray",  "slate", "dark"]
  },
  {
    "name": "BLACK",
    "hex": "#000000",
    "rgb": "RGB(000, 000, 000)",
    "families": ["black"]
  }
]