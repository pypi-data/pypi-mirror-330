# +
SEARCH_LOGS = """SELECT *
FROM hive.odyn_discovery.vector_search_logs
WHERE country = '{COUNTRY_NAME}'
    AND date_nk >= date '{START_DATE}'
    AND date_nk < date '{END_DATE}'
    AND (category_l1_id = 13 OR category_l1_id = 4918)
    AND ad_source = "search|organic"
"""

ADS_DATA = """
SELECT id,
        category_id,
        category_l1_id,
        CONCAT(category_l1_name_en, ' > ', category_l2_name_en, ' > ', category_l3_name_en) as cat_path,
        title,
        description, 
        image_filename, 
        date_nk
FROM odyn_discovery.vector_search_ads
where country = '{COUNTRY_NAME}'
AND category_l1_id IN (13, 4918)
AND date_nk >= date '{START_DATE}'
AND date_nk < date '{END_DATE}'
"""

UNIQUE_ADS_DATA = """
SELECT DISTINCT
        id,
        category_id,
        category_l1_id,
        title,
        description, 
        image_filename
FROM hive.odyn_discovery."search_ads"
WHERE country = '{COUNTRY_NAME}'
AND category_l1_id IN (13, 4918)
AND date_nk >= date '{START_DATE}'
AND date_nk < date '{END_DATE}'

"""

# getting the most recent version of an ad in a given time interval
ADS_SQL = """
WITH RecentAds AS (
    SELECT id, MAX(date_nk) AS most_recent_date
    FROM hive.odyn_discovery."search_ads"
    WHERE country = '{COUNTRY_NAME}'
    AND date_nk >= date '{START_DATE}'
    AND date_nk < date '{END_DATE}'
    GROUP BY id
)

SELECT a.*,
       CONCAT(category_l1_name_en, ' > ', category_l2_name_en, ' > ', category_l3_name_en) as cat_path
FROM hive.odyn_discovery."search_ads" a
JOIN RecentAds r ON a.id = r.id AND a.date_nk = r.most_recent_date

"""
