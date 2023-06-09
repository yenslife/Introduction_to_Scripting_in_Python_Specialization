"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal



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


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    
    my_list = []
    max_year = int(gdpinfo['max_year'])
    min_year = int(gdpinfo['min_year'])

    for key, value in gdpdata.items():
        try:
            year = int(key)
        except(ValueError):
            year = 0
        if isinstance(value, str) and value != '':
            try:
                value = float(value) if (value != '') else -1
            except(ValueError):
                value = -1
        else:
            continue
        if min_year <= year <= max_year and value != -1:
            my_list.append((year, value))
    return my_list


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    plot = {}
    plot_data = read_csv_as_nested_dict(gdpinfo["gdpfile"], 
                                       gdpinfo["country_name"], 
                                       gdpinfo["separator"], gdpinfo["quote"])
    for country in country_list:
        plot[country] = []
        for key, value in plot_data.items():
            if key == country:
                tuple_list = build_plot_values(gdpinfo, value)
                plot[country] = tuple_list
    
    return plot

def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    
    my_dict = build_plot_dict(gdpinfo, country_list)
    chart = pygal.XY(xrange=(1960, 2016))
    chart.title = 'gdp'
    #chart.add()
    
    chart.x_title = 'Year'
    chart.y_title = 'GDP in current US Dollars'
    for country in country_list:
        for key,item in my_dict.items():
            try:
                if (key != ""):
                    if key == country:
                        chart.add(key, item)
            except ValueError:
                pass
    #chart.render_in_browser()
    chart.render_to_file(plot_file)


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
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

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")


# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

#test_render_xy_plot()
#print(read_csv_as_nested_dict("gdptable1.csv", "Country", " ", '"'))

print(read_csv_as_nested_dict("table1.csv", "Field1", ",", '"'))

