import pandas as pd
from IPython.display import HTML, display


class DisplayResults:

    def __init__(self, data: pd.DataFrame):
        self.data = data

    @staticmethod
    def image_row(urls: pd.Series, titles: pd.Series, descriptions: pd.Series, height: int = 100):
        """
        Generates HTML for displaying images in a grid with three columns, including titles, descriptions, and prices below each image, with smaller tile sizes.

        Args:
            urls (pd.Series): Image URLs.
            titles (pd.Series): Titles to display below each image.
            descriptions (pd.Series): Descriptions to display below the titles.
            height (int, optional): Max image height in pixels. Defaults to 100.

        Returns:
            An HTML object with images, titles, descriptions, and prices in a grid layout.

        Note:
            Use in IPython environments for direct HTML rendering.
        """
        html_str = '<div style="display: flex; flex-wrap: wrap; justify-content: space-around; gap: 1cm;">'
        for url, title, description in zip(urls, titles, descriptions):
            html_str += '<div style="flex-basis: 20%; box-shadow: 0 2px 4px 0 rgba(0,0,0,0.2);">'
            html_str += (
                f'<img src="{url}" style="width: 100%; height: {height}px; object-fit: cover;">'
            )
            html_str += '<div style="padding: 5px;">'
            html_str += f"<h5>{title}</h5>"
            html_str += f'<p style="font-size: 12px;">{description}</p>'
            html_str += "</div></div>"
        html_str += "</div>"

        return HTML(html_str)

    def show_results(self, results: list, k=10):
        """
        Displays images for the top k results, including titles, descriptions, and prices, with smaller tiles.

        Args:
            results (list): A list of IDs representing the results.
            k (int, optional): The number of results to display. Defaults to 10.

        Returns:
            An HTML object with the images displayed in a grid if there are results to show; otherwise, prints a message indicating no ads to display.
        """
        query_str = f"id in {results}"
        filtered_data = self.data.query(query_str).head(k)
        urls = filtered_data["apollo_url"]
        titles = filtered_data["title"]
        descriptions = filtered_data["description"]

        if len(urls) > 0:
            return self.image_row(urls, titles, descriptions)
        else:
            print("No ads to display. Ad might not be available anymore.")

    def baseline_vs_vector_display_results(self, text, qrels, baseline_run, new_run, k=3):

        print(f"SEARCH REQUEST: {text}")
        print("###### BASELINE ######")
        baseline_ads = list(baseline_run[text].keys())

        res_base = self.show_results(results=baseline_ads, k=k)
        display(res_base)

        print("###### NEW APPROACH ######")
        new_run_ads = list(new_run[text].keys())

        res = self.show_results(results=new_run_ads, k=k)
        display(res)

        print("###### RELEVANT ADS ######")
        relevant_ads = list(qrels[text].keys())

        res = self.show_results(results=relevant_ads, k=k)
        display(res)
