# TODO: complete this dictionary of countries-languages map:
country_language_map = {
        'egypt': {
                'language': 'arabic',
                'ISO_code': 'ar',
                'country_code': 'eg',
                }, 
        'azerbaijan': {
                'language': 'azerbaijani',
                'ISO_code': 'az',
                'country_code': 'az',
                }, 
        'ukraine': {
                'language': 'ukrainian',
                'ISO_code': 'uk',
                'country_code': 'ua',
                }, 
        'czech republic': {
                'language': 'czech',
                'ISO_code': 'cs',
                'country_code': 'cz',
                }, 
        'hungary': {
                'language': 'hungarian',
                'ISO_code': 'hu',
                'country_code': 'hu',
                },
        'kazakhstan': {
                'language': 'kazakh',
                'ISO_code': 'kk',
                'country_code': 'kz',
                },
        'nigeria': {
                'language': 'igbo',
                'ISO_code': 'ig',
                'country_code': 'ng',
                },
        'comoros': {
                'language': 'french',
                'ISO_code': 'fr',
                'country_code': 'km',
                },
        'iraq': {
                'language': 'arabic',
                'ISO_code': 'ar',
                'country_code': 'iq',
                },
        'burundi': {
                'language': 'french',
                'ISO_code': 'fr',
                'country_code': 'bi',
                },
        'south korea': {
                'language': 'korean',
                'ISO_code': 'ko',
                'country_code': 'kr',
                },
        'russia': {
                'language': 'russian',
                'ISO_code': 'ru',
                'country_code': 'ru',
                },
        'finland': {
                'language': 'finnish',
                'ISO_code': 'fi',
                'country_code': 'fi',
                },
        'sweden': {
                'language': 'swedish',
                'ISO_code': 'sv',
                'country_code': 'se',
                },
        'netherlands': {
                'language': 'dutch',
                'ISO_code': 'nl',
                'country_code': 'nl',
                },
        'turkey': {
                'language': 'turkish',
                'ISO_code': 'tr',
                'country_code': 'tr',
                },
        'ecuador': {
                'language': 'spanish',
                'ISO_code': 'es',
                'country_code': 'ec',
                },
        'argentina': {
                'language': 'spanish',
                'ISO_code': 'es',
                'country_code': 'ar',
                },
        'brazil': {
                'language': 'portugese',
                'ISO_code': 'pt',
                'country_code': 'br',
                },
        'bulgaria': {
                'language': 'bulgarian',
                'ISO_code': 'bg',
                'country_code': 'bg',
                },
        'chad': {
                'language': 'french',
                'ISO_code': 'fr',
                'country_code': 'td',
                },
        'chile': {
                'language': 'spanish',
                'ISO_code': 'es',
                'country_code': 'cl',
                },
        'colombia': {
                'language': 'spanish',
                'ISO_code': 'es',
                'country_code': 'co',
                },
        'egpyt': {
                'language': 'arabic',
                'ISO_code': 'ar',
                'country_code': 'eg',
                },
        'greece': {
                'language': 'greek',
                'ISO_code': 'el',
                'country_code': 'gr',
                },
        'indonesia': {
                'language': 'indonesian',
                'ISO_code': 'id',
                'country_code': 'id',
                },
        'iran': {
                'language': 'persian',
                'ISO_code': 'fa',
                'country_code': 'ir',
                },
        'italy': {
                'language': 'italian',
                'ISO_code': 'it',
                'country_code': 'it',
                },
}

USERS = {
            "Gryffindor": {
                "recent_filter": True,
                "date_restrict": "m[1]"
            },
            
}


USERNAME = "..."
PASSWORD = "CapoteDraconas"
HOST = "#.#.#.#"
PORT = "<port>"
SCHEMA = "search_automation"
DATE_PATTERNS = {
    "(\d{4})-?(\d{1,2})-?(\d{1,2})": {
        "output_format": "{year}-{month}-{day}",
        "positions": {"year": 0, "month": 1, "day": 2},
        "is_month": True
    },
    "^(\d{1,2}\s+)(\w+\s+)(\d{4}).*|.*\s+(\d{1,2}\s+)(\w+\s+)(\d{4}).*": {
        "output_format": "{day} {month} {year}",
        "positions": {"day": 0, "month": 1, "year": 2},
        "is_month": False
    },
    "^(\d{1,2})\.(\d+)\.(\d{4}).*|.*\s+(\d{1,2})\.(\d+)\.(\d{4}).*": {
        "output_format": "{year}-{month}-{day}",
        "positions": {"day": 0, "month": 1, "year": 2},
        "is_month": False
    },
    "^(\w+,\s+)(\d{1,2}\s+)(\w+\s+)(\d{4}).*|.*\s+(\w+,\s+)(\d{1,2}\s+)(\w+\s+)(\d{4}).*": {
        "output_format": "{day}{month}{year}",
        "positions": {"day": 1, "month": 2, "year": 3},
        "is_month": False
    },
    "^(\d{4}).*": {
        "output_format": "{year}",
        "positions": {"year": 0},
        "is_month": False
    },
    "^(\d+)\w*\s+(\w+\s+)(\d{4}).*|.*\s+(\d+)\w*\s+(\w+\s+)(\d{4}).*": {
        "output_format": "{year}-{month}-{day}",
        "positions": {"day": 0, "month": 1, "year": 2},
        "is_month": False
    },
    "^(\d{1,2})\/(\d{1,2})\/(\d{1,4}).*|.*\s+(\d{1,2})\/(\d{1,2})\/(\d{1,4}).*": {
        "output_format": "{year}-{month}-{day}",
        "positions": {"day": 0, "month": 1, "year": 2},
        "is_month": False
    },
    "^(\w+\s+)(\d+)\w*\s+(\d{4}).*|.*\s+(\w+\s+)(\d+)\w*\s+(\d{4}).*": {
        "output_format": "{year}-{month}-{day}",
        "positions": {"day": 1, "month": 0, "year": 2},
        "is_month": False
    },
}
