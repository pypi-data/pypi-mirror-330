# get available categories
SQL_CATEGORIES = """
WITH max_tree_revision AS(
  -- get most recent category tree version per country
  -- # currently only most recent version kept in the table (but with no update dates provided)
  -- # and it's not included in the source table documentation
  -- # so this subquery is added to keep awareness of this column logic for future use cases
    SELECT
      max(tree_revision) AS most_recent_state
    FROM
      awsdatacatalog.olxgroup_reservoir_ares.json_reservoirs_olxgroup_reservoir_eu_bi_category_management_tool_olx{COUNTRY_NAME}

),
current_posting_categories AS(
  -- get most recent posting categories
    SELECT
      distinct category_id,
      name,
      level,
      parent,
      SUBSTRING(brand, 4, 2) as country
    FROM
      awsdatacatalog.olxgroup_reservoir_ares.json_reservoirs_olxgroup_reservoir_eu_bi_category_management_tool_olx{COUNTRY_NAME} cmt
      INNER JOIN max_tree_revision m ON cmt.tree_revision = m.most_recent_state
    WHERE
      children is null
)
--extend categories info
SELECT distinct
    cp.category_id,
    cp.name,
    cp.level,
    cp.parent,
    dim.category_l1_name_en, dim.category_l1_name_lc, dim.category_l1_nk,
    dim.category_l2_name_en, dim.category_l2_name_lc, dim.category_l2_nk,
    dim.category_l3_name_en, dim.category_l3_name_lc, dim.category_l3_nk,
    dim.category_name_en,
    dim.category_parent_sk,
    dim.country_nk,
    dim.site_sk,
    dim.category_sk,
    dim.category_level
FROM
current_posting_categories cp
LEFT JOIN awsdatacatalog.olxgroup_reservoir_ares.reservoirs_olxgroup_reservoir_eu_bi_eu_bi_dim_categories dim ON (
  cp.category_id = dim.category_nk
  AND cp.country = LOWER(dim.country_nk)
  AND cp.parent =  dim.category_parent_nk)
  AND dim.group_sk = 'olx'
"""

SQL_SEARCH_LOGS = """
SELECT 
    country_code,
    date_day,
    search_term,
    cat_l1_id,
    cat_l2_id,
    cat_l3_id, 
    SUM(num_searches) as nb_searches,
    SUM(num_interactions) as nb_interactions,
    SUM(num_clicks) as nb_clicks,
    SUM(num_replies) as nb_replies

FROM awsdatacatalog.odyn_discovery."popular_searches"
WHERE country_code = '{COUNTRY_NAME}'
AND platform = 'android'
AND date_day >= DATE('{START_DATE}')
AND date_day < DATE('{END_DATE}')

GROUP BY 1,2,3,4,5,6
"""
