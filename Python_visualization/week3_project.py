"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.

Remember to install pygal_maps_world module for this project.
You can use `python3 -m pip install pygal_maps_world` to install.
"""

import csv
import math
import pygal

# helper function
def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='', encoding='UTF-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    out_dict = {}
    remove_set = set()
    print('Norway' in gdp_countries.keys())
    for key, country in plot_countries.items():
        if country not in gdp_countries.keys():
            remove_set.add(key)
        else:
            out_dict[key] = country
    return out_dict, remove_set
    


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year. 找 csv 沒有ㄉ
    """
    
    gdp_country_name_dict = read_csv_as_nested_dict(gdpinfo['gdpfile']
            , gdpinfo['country_name']
            , gdpinfo['separator']
            ,  gdpinfo['quote'])
    # test
    print(gdp_country_name_dict)
    found_id_dict, not_found_id_set = reconcile_countries_by_name(plot_countries, 
                                                                  gdp_country_name_dict)
    print(found_id_dict)
    out_dict = {}
    second_set = set()
    for country_name in found_id_dict.values():
        country_id = list(found_id_dict.keys())[list(found_id_dict.values()).index(country_name)]
        try:
            gdp = math.log(int(gdp_country_name_dict[country_name][year]), 10)
            out_dict[country_id] = gdp
        except(ValueError):
            second_set.add(country_id)  # Prin)
        
         
    return out_dict, not_found_id_set, second_set


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    plot_dict_1, plot_set_1,plot_set_2 = build_map_dict_by_name(gdpinfo, plot_countries, year)
    worldmap_chart = pygal.maps.world.World()
    title_map = 'GDP by country for ' + year + ' (log scale), unifiedby common country NAME'
    worldmap_chart.title = title_map
    label_map = 'GDP for ' + year
    worldmap_chart.add(label_map,plot_dict_1 )
    worldmap_chart.add('Missing from World Bank Data',plot_set_1 )
    worldmap_chart.add('No GDP Data' ,plot_set_2 )
    worldmap_chart.render_in_browser()
    return


def test_render_world_map():
    """
    Test the project code for several years.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()
