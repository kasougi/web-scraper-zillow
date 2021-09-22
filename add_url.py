def start():
    states = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado',
              'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
              'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
              'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota',
              'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New',
              'NJ': 'New', 'NM': 'New', 'NY': 'New', 'NC': 'North', 'ND': 'North', 'OH': 'Ohio', 'OK': 'Oklahoma',
              'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode', 'SC': 'South', 'SD': 'South', 'TN': 'Tennessee',
              'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West',
              'WI': 'Wisconsin', 'WY': 'Wyoming'}


    args = {'state(short)' : 'st',
            'price_min': 'price',
            'price_max': 'price',
            'house_type' : {
                    'house' : None,
                    'condo' : None,
                    'multifamily' : None,
                    'mobile' : None,
                    'townhouse' : None,
                    'apartment' : None,
                    'land' : None,
                },
           'beds_min': 'beds',
           'beds_max': 'beds',
           'baths_min': 'baths',
           'baths_max': 'baths',
            'parks_min': 'parks',
            'sqft_max': 'sqft',
            'sqft_min': 'sqft',
            'built_min': 'built',
            'built_max': 'built',
            'hoa_max': 'hoa'
            }
    full_args = {
        'state(short)': None,
        'type' : {
            'house' : None,
            'condo' : None,
            'multifamily' : None,
            'mobile' : None,
            'townhouse' : None,
            'apartment' : None,
            'land' : None,
        },
        'ah': {'value': True},
     'apa': {'value': False},
     'apco': {'value': False},
     'baths': {'max': None, 'min': None},
     'beds': {'max': None, 'min': None},
     'built': {'max': None, 'min': None},
     'con': {'value': False},
     'hoa': {'max': None},
     'land': {'value': False},
     'manu': {'value': False},
     'mp': {'max': None, 'min': None},
     'parks': {'min': None},
     'price': {'max': None, 'min': None},
     'sf': {'value': False},
     'sqft': {'max': None, 'min': None},
     'tow': {'value': False}}

    def house_type():
        for h_arg, h_val in args['house_type'].items():
            val = input(f"\rPlease enter something if want housetype: {h_arg}:\n")
            if val:
                full_args['type'][h_arg] = True

    for arg, arg_web in args.items():
        if arg == 'house_type':
            house_type()
            continue
        val = input(f"\rPlease enter {arg}:\n")

        if arg_web == 'st':
            full_args[arg] = val
            try:
                if states.get(val.upper()):
                    pass
                else:
                    print('Wrong format. Please try again. example: OH')
                    return 0
            except:
                print('Wrong format')
                return 0
        else:
            try:
                val = int(val)
            except:
                pass
            if val != '-':
                if len(arg.split('_')) > 1:
                    full_args[arg.split('_')[0]][arg.split('_')[1]] = val
                else:
                    full_args[arg]['value'] = val
            else:
                if len(arg.split('_')) > 1:
                    full_args[arg.split('_')[0]][arg.split('_')[1]] = None
                else:
                    full_args[arg]['value'] = None

    if not(check(full_args)):
        return 0

    args = delete_arggs(full_args)
    url = 'https://www.zillow.com/'
    for key, val in args.items():
        if key == "type":
            sch = 0
            for k,a in args['type'].items():
                if args['type'][k]:
                    url += f'{k},'
                    sch = 1
            if sch:
                url = url[:len(url)-1]+f'_type/'
            continue
        if key == "state(short)":
            url += f'{val}/'
            continue
        min = '' if not(val.get('min')) else val.get('min')
        max = '' if not(val.get('max')) else val.get('max')
        url += f'{min}-{max}_{key}/'
    return url

def check(full_args):
    print("Please check")
    for key, val in full_args.items():
        print(f"{key}: {val}")
    print("You shoud? (y/n)")
    val = input()
    if val == 'y' or val == 'yes':
        return 1
    elif val == 'n' or val == 'no':
        return 0
    if not(val == 'y' or val == 'yes' or val == 'n' or val == 'no'):
        print('Invalid value, please try again')
        return check(full_args)


def delete_arggs(full_args):
    del_item = []
    for key, val in full_args.items():
        if key == "state(short)" or key == 'type':
            continue
        if len(val) > 1:
            if not(val['min'] and val['max']):
                del_item.append(key)
                continue
        elif not(val.get('min')):
            del_item.append(key)
        elif not(val.get('max')):
            del_item.append(key)
    for i in del_item:
        if len(full_args[i]) == 1:
            full_args.pop(i)
        elif not(full_args[i]['min']):
            full_args[i].pop('min')
        elif not(full_args[i]['max']):
            full_args[i].pop('max')

    return full_args


def main():
    x = True
    while x:
        start_arggs = start()
        if start_arggs != 0:
            x = False
    return start_arggs

if __name__ == '__main__':
    print(main())



