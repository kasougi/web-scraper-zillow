def add_to_url():
    state = 'oh'
    beds_min = 3
    beds_max = 20
    baths_min = 2
    baths_max = 20
    built_min = 1980
    built_max = 2021
    price_min = 1000
    price_max = 150000
    sqft_min = 500
    sqft_max = 15000
    hoa_min = 0
    hoa_max = 500
    park_min = 0
    park_max = 20
    full_args = {
        'state(short)': state,
        'type' : {
            'house' : None,
            'condo' : None,
            'multifamily' : None,
            'mobile' : None,
            'townhouse' : None,
            'apartment' : None,
            'land' : None,
        },
        'baths': {'max': baths_max, 'min': baths_min},
        'beds': {'max': beds_max, 'min': beds_min},
        'built': {'max': built_max, 'min': built_min},
        'hoa': {'max': hoa_max, 'min': hoa_min},
        'parks': {'max': park_max, 'min': park_min},
        'price': {'max': price_max, 'min': price_min},
        'sqft': {'max': sqft_max, 'min': sqft_min},
    }
    url = 'https://www.zillow.com/'
    for key, val in full_args.items():
        if key == "type":
            sch = 0
            for k,a in full_args['type'].items():
                if full_args['type'][k]:
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