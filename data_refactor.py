
def get_dict_from_data(ret_data, url, price, bd_ba_sq, adr_city_zip, overview):
    dafa_frame = {
        'url' : url,
        'price' : price,
        'overview': overview,
        'Bedrooms': bd_ba_sq[0],
        'Bathrooms': bd_ba_sq[1],
        'square footage': bd_ba_sq[2],
        'address': adr_city_zip[0],
        'city': adr_city_zip[1],
        'zip': adr_city_zip[2],
        'Full bathrooms': None,
        'Basement': None,
        'Flooring': None,
        'Heating': None,
        'Cooling': None,
        'Appliances': None,
        'Interior': None,
        'Parking': None,
        'Totalspaces': None,
        'Hometype': None,
        'Architecturalstyle': None,
        'Parkingfeatures': None,
        'Lot': None,
        'Otherpropertyinformation': None,
        'Typeandstyle': None,
        'Construction materials': None,
        'Foundation': None,
        'Roof': None,
        'Utility': None,
        'New construction': None,
        'type': None,
        'Condition': None,
        'Annual Tax Amount': None
    }

    def onlstr(st):
        new_s = ''.join([a for a in st if a.isalpha() or a.islower()])
        return new_s

    categories = ['Basement', 'Flooring', 'Heating', 'Cooling', 'Appliances', 'Interior', 'Features', 'Otherinteriorfeatures',
                  'Parking', 'Property', 'Lot', 'Otherpropertyinformation', 'Typeandstyle', 'Materialinformation', 'Condition',
                  'Utility', 'Location', 'Otherfinancialinformation']

    rez_data = dafa_frame
    for st in ret_data:
        if onlstr(st) in categories:
            i = ret_data.index(st)
            ret_str = ''
            i += 1
            while onlstr(ret_data[i]) not in categories[categories.index(onlstr(st))+1:] and categories[categories.index(onlstr(st))+1:]:

                ret_str += ret_data[i]
                i += 1
            rez_data[onlstr(st)] = ret_str

    rez_data['Full bathrooms'] = ret_data[6]
    if rez_data.get('Parking'):
        if 'Totalspaces' in rez_data['Parking']:
            rez_data['Totalspaces'] = rez_data['Parking'].split(':')[1][0]
            if 'Parkingfeatures' in rez_data['Parking']:
                i = rez_data['Parking'].split(':')[2].find('Attached')
                if i == -1:
                    i = rez_data['Parking'].find('Garagespace')
                rez_data['Parkingfeatures'] = rez_data['Parking'].split(':')[2][0:i]
        else:
            if 'Parkingfeatures' in rez_data['Parking']:
                i = rez_data['Parking'].split(':')[1].find('Attached')
                if i == -1:
                    i = rez_data['Parking'].split(':')[1].find('Garagespace')
                rez_data['Parkingfeatures'] = rez_data['Parking'].split(':')[1][0:i]

    if rez_data.get('Cooling'):
        rez_data['Cooling'] = rez_data['Cooling'].split(':')[1]
    if rez_data.get('Appliances'):
        rez_data['Appliances'] = rez_data['Appliances'].split(':')[1]
    if rez_data.get('Condition'):
        if 'Yearbuilt' in rez_data['Condition']:
            rez_data['Yearbuilt'] = rez_data['Condition'].split(':')[1][:4]
    if rez_data.get('Heating'):
        rez_data['Heating'] = rez_data['Heating'].split(':')[1]

    if rez_data.get('Typeandstyle'):
        if 'Hometype' in rez_data['Typeandstyle']:
            i = rez_data['Typeandstyle'].split(':')[1].find('Architecturalstyle')
            if i == -1:
                i = rez_data['Typeandstyle'].split(':')[1].find('PropertysubType')
            rez_data['Hometype'] = rez_data['Typeandstyle'].split(':')[1][0:i]
            if 'Architecturalstyle' in rez_data['Typeandstyle']:
                ii = rez_data['Typeandstyle'].split(':')[2].find('PropertysubType')
                rez_data['Architecturalstyle'] = rez_data['Typeandstyle'].split(':')[2][:ii]
        else:
            if 'Architecturalstyle' in rez_data['Typeandstyle']:
                ii = rez_data['Typeandstyle'].split(':')[1].find('PropertysubType')
                rez_data['Architecturalstyle'] = rez_data['Typeandstyle'].split(':')[1][:ii]

    if rez_data.get('Materialinformation'):
        if 'Constructionmaterials' in rez_data['Materialinformation']:
            i = rez_data['Materialinformation'].split(':')[1].find('Foundation')
            if i == -1:
                i = rez_data['Materialinformation'].split(':')[1].find('Roof')
            rez_data['Constructionmaterials'] = rez_data['Materialinformation'].split(':')[1][0:i]

            if 'Foundation' in rez_data['Materialinformation']:
                ii = rez_data['Materialinformation'].split(':')[2].find('Roof')
                if ii != -1:
                    rez_data['Foundation'] = rez_data['Materialinformation'].split(':')[2][:ii]
                    if 'Roof' in rez_data['Materialinformation']:
                        rez_data['Architecturalstyle'] = rez_data['Materialinformation'].split(':')[3][:ii]
                else:
                    rez_data['Foundation'] = rez_data['Materialinformation'].split(':')[2]
        elif 'Foundation' in rez_data['Materialinformation']:
            ii = rez_data['Materialinformation'].split(':')[1].find('Roof')
            if ii != -1:
                rez_data['Foundation'] = rez_data['Materialinformation'].split(':')[1][:ii]
                if 'Roof' in rez_data['Materialinformation']:
                    rez_data['Architecturalstyle'] = rez_data['Materialinformation'].split(':')[2][:ii]
            else:
                rez_data['Foundation'] = rez_data['Materialinformation'].split(':')[1]

        elif 'Roof:' in rez_data['Materialinformation']:
            rez_data['Roof'] = rez_data['Materialinformation'].split('Roof:')[1]

    for i in ret_data:
        if 'Annualtaxamount:' in i:
            try:
                st = i
                ata = st.split('mount:')[1]
                rez_data['Annual Tax Amount'] = ata
            except:
                pass

    try:
        fb = ret_data[3].split(':')[1]
        rez_data['Full bathrooms'] = fb[0]
    except:
        rez_data['Full bathrooms'] = None

    rez_data.pop('Parking')
    rez_data.pop('type')
    rez_data.pop('Typeandstyle')
    rez_data.pop('Location')
    rez_data.pop('Otherfinancialinformation')
    rez_data.pop('Materialinformation')
    rez_data.pop('Utility')
    rez_data.pop('Condition')
    return(rez_data)



