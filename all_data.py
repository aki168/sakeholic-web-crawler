import requests
import pandas as pd
import numpy as np

get_area = requests.get("https://raw.githubusercontent.com/aki168/sakeData/main/areas.json")
get_brand_flavor_tags = requests.get("https://raw.githubusercontent.com/aki168/sakeData/main/brand-flavor-tags.json")
get_brands = requests.get(
    "https://raw.githubusercontent.com/aki168/sakeData/main/brands.json")
get_breweries = requests.get(
    "https://raw.githubusercontent.com/aki168/sakeData/main/breweries.json")
get_flavor_charts = requests.get(
    "https://raw.githubusercontent.com/aki168/sakeData/main/flavor-charts.json")
# get_flavor_tags = requests.get(
#     "https://raw.githubusercontent.com/aki168/sakeData/main/flavor-tags.json")
# get_ranking = requests.get(
#     "https://raw.githubusercontent.com/aki168/sakeData/main/rankings.json")

## craweler-data
area = get_area.json()['areas']
# print(area, end="\n\n")
brand_flavor_tags = get_brand_flavor_tags.json()['flavorTags']
# print(brand_flavor_tags[1], end="\n\n")
brands = get_brands.json()['brands']
# print(brands, end="\n\n")
breweries = get_breweries.json()['breweries']
# print(breweries, end="\n\n")
flavor_charts = get_flavor_charts.json()['flavorCharts']
# print(flavor_charts[0], end="\n\n")

## trans to DataFrame
brands_df = pd.DataFrame(brands)
breweries_df = pd.DataFrame(breweries)
area_df = pd.DataFrame(area)
brand_tags_df = pd.DataFrame(brand_flavor_tags)
flavor_charts_df = pd.DataFrame(flavor_charts)

## rename for merge
breweries_df.rename(columns={'name': 'brewery_name', 'id': 'breweryId'}, inplace=True)
area_df.rename(columns={'id':'areaId', 'name':'area'}, inplace=True)
brand_tags_df.rename(columns={'brandId':'id'}, inplace=True)
flavor_charts_df.rename(columns={'brandId':'id'}, inplace=True)

## merge data
merged_df = pd.merge(brands_df, breweries_df)
merged_df = pd.merge(merged_df, area_df)
merged_df = pd.merge(merged_df, brand_tags_df, how='left')
merged_df = pd.merge(merged_df, flavor_charts_df, how='left')
result_df = merged_df.drop("breweryId", axis=1).drop("areaId", axis=1)

## example: export json
result = result_df.to_json(path_or_buf="./records.json", orient="records", force_ascii=False)


