import pandas as pd


def process_logs(search_logs: pd.DataFrame, k: int = 30, sorting: str = None):
    """Process general search logs made available by vector search pipeline.

    1. Select only free text queries (excluding L1 filter)
    2. Drop irrelevant columns
    3. Rearrange the rank based on organic section only and sorting type (relevance, freshness, price)
    4. Select only first page of results rank < 30
    """

    # Drop duplicates
    cols = [
        "params_user_id",
        "meta_session_long",
        "meta_session",
        "params_search_id",
        "search_string",
        "label",
        "rank",
        "meta_date_dt",
        "ad_source",
        "ad_id",
        "ad_category_l1_id",
        "category_l1_id",
        "cat_l1_id",
        "cat_l2_id",
        "cat_l3_id",
        "cat_l4_id",
        "city_id",
        "region_id",
        "district_id",
        "distance_filter",
        "price_from",
        "price_to",
        "filters",
        "filters_values",
        "order_by",
        "is_free_text",
        "is_extension",
        "platform",
        "country",
        "item_condition",
    ]
    search_logs.drop_duplicates(subset=cols, inplace=True)

    # Filter by organic section only
    df = search_logs.query("ad_source == 'search|organic'").copy()

    # Filter by sorting type
    if sorting:
        df = df.query(f"order_by == '{sorting}'").copy()

    # Convert the column to datetime objects
    df["meta_date_dt"] = pd.to_datetime(df["meta_date_dt"])

    # Extract just the date part
    df["date_nk"] = df["meta_date_dt"].dt.date

    # Select free-text only searches except L1 which is Home and Garden
    filters = [
        "cat_l2_id",
        "cat_l3_id",
        "cat_l4_id",
        "city_id",
        "region_id",
        "district_id",
        "distance_filter",
        "price_from",
        "price_to",
        "filters",
        "filters_values",
        "item_condition",
    ]
    df = df[df[filters].isna().all(axis=1)].copy()

    # Remove duplicates

    df.drop(columns=filters, inplace=True)

    # Removing irrelevant cols
    df.drop(columns=["ad_source", "ad_category_l1_id", "platform"], inplace=True)

    # Keeping the evaluation to the first page only
    if k:
        df = df.query(f"rank <= {k}").copy()

    # Order by session and rank
    mask = [
        "params_user_id",
        "meta_session_long",
        "meta_session",
        "params_search_id",
        "search_string",
        "cat_l1_id",
        "order_by",
        "is_free_text",
        "is_extension",
        "country",
        "date_nk",
        "rank",
    ]
    df = df.sort_values(by=mask)

    # Resetting ranking to organic section only
    # this time we do not include old ranking position in the groupby
    mask = [
        "params_user_id",
        "meta_session_long",
        "meta_session",
        "params_search_id",
        "search_string",
        "cat_l1_id",
        "order_by",
        "is_free_text",
        "is_extension",
        "country",
        "date_nk",
    ]

    df["new_rank"] = df.groupby(mask, dropna=False).cumcount() + 1

    # Removing old rank col
    df.drop(columns=["rank"], inplace=True)
    df.rename(columns={"new_rank": "rank"}, inplace=True)

    return df
