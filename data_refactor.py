import json

def get_dict_from_data(dfj, zpid):
    arg = "ForSaleDoubleScrollFullRenderQuery{'zpid':"+str(zpid)+",'contactFormRenderParameter':{'zpid':"+str(zpid)+",'platform':'desktop','isDoubleScroll':true}}"
    dfj = dfj[arg]['property']

    data_for_save = dict()

    arg_dict = {
        "City" : "city",
        "City Id" : "cityId",
        "Country" : "country",
        "Bathrooms" : "bathrooms",
        "Bedrooms" : "bedrooms",
        "Brokerage Name" : "brokerageName",
        "BrokerId Dimension" : "brokerIdDimension",
        "Date Posted" : "datePostedString",
        "Overview" : "description",
        "Url" : "hdpUrl",
        "Home Type": "homeType",
        "Home Status" : "homeStatus",
        "living Area Value" : "livingAreaValue",
        "Living Area UnitsShort": "livingAreaUnitsShort",
        "Lot Area Value" : "lotAreaValue",
        "Lot Area Units" : "lotAreaUnits",
        "Lot Size" : "lotSize",
        "Price" : "price",
        "Property Type Dimension" : "propertyTypeDimension",
        "State" : "state",
        "Address" : "streetAddress",
        "Tax Assessed Value" : "taxAssessedValue",
        "Year Built" : "yearBuilt",
        "zip" : "zipcode",
    }

    for name_in_csv, name_in_json in arg_dict.items():
        if dfj.get(name_in_json):
            data_for_save[name_in_csv] = dfj[name_in_json]
        else:
            data_for_save[name_in_csv] = None

    dfj = dfj['resoFacts']

    arg_dict = {
        "Full bathrooms" : "bathroomsFull",
        "Basement" : "basement",
        "Parking" : "garageSpaces",
        "Architectural Style" : "architecturalStyle",
        "Elementary School" : "elementarySchool",
        "Middle Or Junior School" : "middleOrJuniorSchool",
        "High School" : "highSchool",
        "Tax Annual Amount" : "taxAnnualAmount",
        "Hoa Fee" : "hoaFee",
        "Price Per Square Foot" : "pricePerSquareFoot",
        "Fireplaces" : "fireplaces",

    }

    for name_in_csv, name_in_json in arg_dict.items():
        if dfj.get(name_in_json):
            data_for_save[name_in_csv] = dfj[name_in_json]
        else:
            data_for_save[name_in_csv] = None

    arg_of_list_in_dict = {
        "Heating" : "heating",
        "Flooring" : "flooring",
        "Cooling" : "cooling",
        "Fireplace Features" : "fireplaceFeatures",
        "Parking Features" : "parkingFeatures",
    }

    for name_in_csv, list_name_in_json in arg_of_list_in_dict.items():
        if dfj.get(list_name_in_json):
            data_for_save[name_in_csv] = ''
            for i in dfj[list_name_in_json]:
                data_for_save[name_in_csv] += i+", "
            else:
                data_for_save[name_in_csv] = data_for_save[name_in_csv][:len(data_for_save[name_in_csv])-2]
        else:
            data_for_save[name_in_csv] = None
    return(data_for_save)



