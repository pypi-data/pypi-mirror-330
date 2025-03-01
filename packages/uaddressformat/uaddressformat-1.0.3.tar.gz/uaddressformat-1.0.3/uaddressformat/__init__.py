import re

types = {

    'region': 'обл.',
    'street': 'вул.',
    'area': 'пл.',
    'avenue': 'просп.',
    'lane': 'пров.',
    'boulevard': 'бульв.',
    'dway': 'проїзд',
    'microdistrict': 'мікр.',
    'quay': 'наб.',
    'housing': 'корп.',
    'house': 'буд.',
    'apartment': 'кв.',
    'highway': 'шосе',
    'housingarea': 'ж/м',
    'end': 'тупик',
    'road': 'дорога',
    'city': 'м.',
    'village': 'с.',
    'settlement': 'с-ще',
    'urbansettlement': 'смт',
    'entrancetype': 'підʼїзд'

}

##
# CLEAR TRASH
#
def clearTrash(str):

    return re.sub(r'\.$|\(', '', str)
##
#  REGION TYPE
#
def RegionType(str, region):
    pattern = r'^(?:(обл)|область)(?:\.|\.?)$'

    if re.match(pattern, str):
        return re.sub(pattern, types['region'], str)

    else:
        if region:
            str = types['region']

    return str
##
# LOCALITY
#
def Locality(type, name):

    pattern = {

        'city': r'^(?:м(?:істо|\.?)|г(?:ород|\.?))(?:\.|\.\s|$)',
        'village': r'^(с(?:ело|\.?))(?:\.|\.\s|$)',
        'settlement': r'^(с(?:(?:\-|ели\.?)ще))(?:\.|\.\s|$)',
        'urbansettlement': r'^(смт|с\.м\.т)(?:\.|\.\s|$)'

    }

    if name:
        
        for i in pattern:

            if re.match(pattern[i], name):
                type = types[i]
                name = re.sub(pattern[i], '', name)
                break

            if re.match(pattern[i], type.lower()):
                type = types[i]

    
    return {
        'name': name,
        'type': type
    }
    

##
# STREET
#
def Street(str, type = False):

    pattern = {

        'street': r'^(?:(?:(?:В|в)ул|ул)(?:иця|\.?)|(?:влу))(?:\.|\.?(?=\s)|$)',
        'avenue': r'^(п(?:р|рос|роспект|\-рт|р\-т))(?:\.|\.?(?=\s))',
        'lane': r'^(про(?:вулок|улок|\.?)|пер(?:еулок|\.?))(?:\.|\.?(?=\s))',
        'area': r'^(площа|пл)(?:\.|\.?(?=\s))',
        'boulevard': r'^(бульвар|бул|бульв|б\-р)(?:\.|\.?(?=\s))',
        'quay': r'^(наб(?:ер|ережная|\.?))(?:\.|\.?(?=\s))',
        'highway': r'^шо(?:с|сс)(?:е\.|\.|\.?(?=\s))',
        'housingarea': r'^ж(\/|\.)м(\.|\.?)',
        'end': r'^туп(\.(?:\s|\.?)|ик\s)',
        'road': r'дор(?:ога|\.?)((?=\s)|$)'

    }

    if str:

        if not type:
            for i in pattern:

                if re.match(pattern[i], str):
            
                    # FIX SPACE
                    str = re.sub(r'(?<=\d)\s(?=\-[а-яА-ЯіІїЇьєЄ])', '', str)
                    #
                    return re.sub(pattern[i], '', str)
            
        else:

            for i in pattern:
             
                if re.match(pattern[i], str.lower()):
                   
                    return types[i]
    
##
# STREET TYPE
#
def StreetType(str):
    
    pattern = {
        'street': r'^(?:(вул)|влу|ул|вулиця)(?:\.|\.?)$',
        'avenue': r'^(п(?:р|рос|роспект|\-рт|р\-т|р\_т))(?:\.|\.?)$',
        'lane': r'^(про(?:вулок|улок|\.?)|пер(?:еулок|\.?))(?:\.|\.?)$',
        'area': r'^(?:(пл)|площа)(?:\.|\.?)$',
        'boulevard': r'^(?:(бул)|бульвар|б(\-|\_)р)(?:\.|\.?)$',
        'dway': r'^(?:(проїзд)|проезд)(?:\.|\.?)$',
        'microdistrict': r'^(?:(м\-н)|мкр|мікр|м\/н|мкрн)(?:\.|\.?)$',
        'quay': r'^(?:(наб(?:ер|ережная|\.?)))(?:\.|\.?)$',
        'highway': r'^шо(?:с|сс)(?:е\.|\.|\.?)$',
        'housingarea': r'ж(\/|\.)м(\.|\.?)$',
        'end': r'^туп(\.|ик)$',
        'road': r'^дор(?:ога|\.?)$'
    }

    if str:

        for i in pattern:

            if re.match(pattern[i], str.lower()):
                return re.sub(pattern[i], types[i], str.lower())
        
    return str

##
# HOUSING
#
def Housing(str, type = False):

    pattern = r'^(?:кор(?:п|\.?)|к)(?:\.|\.?)'

    if str:

        if not type:
            return re.sub(pattern, '', str.lower())
        else:
            return types['housing']

    return str

##
# ENTRANCE TYPE
#
def EntranceType(str, type = False):
    
    pattern = r'^п(о|і)д(\’|\`|\”|\'|\“|\"|\_|\ʼ|\.?)(ъе|ї)зд$'

    if str:
        if not type:
            return re.sub(pattern, '', str)
        else:
            return types['entrancetype']

    return str

##
# HOUSE NUMBER TYPE
#
def HouseNumberType(str, house):

    pattern = r'^(?:буд|бу|б|д(?:ом|\.?)|№)(?:\.|$)'

    if str:

        if re.match(pattern, str):
            str = re.sub(pattern, types['house'], str)
    
    else:

        if house:
            str = types['house']
   
    return str


##
# HOUSE NUMBER
#
def HouseNumber(str, additionally):
    
    pattern = r'^(?:буд|бу|б|д(?:ом|\.?))(\.|\s|(?=\d))'
    
    house = str
    house = clearTrash(house)
    additionally = additionally

    if house:

        if re.match(pattern, house.lower()):

            house = re.sub(pattern, '', house.lower())
            additionally = HouseNumberAdditionally(house, additionally)

            house = additionally['number']
            additionally = additionally['sub']

        else: 
            
            additionally = HouseNumberAdditionally(house, additionally)
            house = additionally['number']
            additionally = additionally['sub']

        house = re.sub(r'\_', '/', house)
    
    return {
        'house': house,
        'additionally': additionally
    }
##
# HOUSE NUMBER ADDITIONALLY
#
def HouseNumberAdditionally(number, sub):

    number = re.sub(r"\\|\/\/|\'", "/", number)
    
    if not sub:
        if re.match(r'\d+\/[а-яА-ЯіІїЇґҐ0-9]+', number):
            sub = re.sub(r'^\d+', '', number)
            number = re.sub(r'\/[а-яА-ЯіІїЇґҐ0-9]+', '', number)
        elif re.match(r'^\d+[а-яА-ЯіІїЇґҐ”]+$', number):
            sub = re.sub(r'^\d+', '', number)
            number = re.sub(r'[а-яА-ЯіІїЇґҐ”]+', '', number)
        elif re.match(r'^\d+\-[а-яА-ЯіІїЇґҐ](?:\/\d+|\.?)+', number):
            sub = re.sub(r'^\d+', '', number)
            number = re.sub(r'\-[а-яА-ЯіІїЇґҐ](?:\/\d+|\.?)+', '', number)
        elif re.match(r'\d+\-\d+', number):
            sub = re.sub(r'\d+(?=\-\d+)', '', number)
            number = re.sub(r'(?<=\d)\-\d+', '', number)

    return {
        'number': number,
        'sub': sub
    }
##
# APARTMENT TYPE
#
def ApartmentType(str, type = False):

    pattern = r'^(?:(кв)|\-кв|№)(?:\.|\.?)'

    if str:

        if type and re.match(pattern, str):
            return {
                'number': re.sub(pattern, '', str),
                'type': types['apartment']
            }
        elif re.match(pattern, str):
            return re.sub(pattern, types['apartment'], str.lower())

    else:
        str = types['apartment']
    
    return str