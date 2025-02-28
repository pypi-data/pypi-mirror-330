import pandas as pd


def df_to_html(df, 
               remove_highlights=True,
               remove_fields=[]) -> str:
    """
    Convert a pandas DataFrame to an HTML table.

    Args:
        df (pandas.DataFrame): The DataFrame to convert.
        description (str): The description to display above the table. Default is "Search Details".
        remove_fields (list): A list of fields to remove from the DataFrame. Default is [].

    Returns:
        str: The HTML representation of the DataFrame as a table.
    """

    if remove_highlights:
        if 'highlight' in df.columns:
            df = df.drop('highlight', axis=1)

    df = df.drop(remove_fields, axis=1)

    html = df.to_html(index=False, escape=False)
    html = f'''
            <style>
                table {{
                    width: 100%;
                }}
                th {{
                    text-align: center;
                }}
                td, th {{
                    padding: 10px;
                    border-bottom: 1px solid #ddd;
                }}
                em {{
                    background-color: #ff0; /* bright yellow background */
                    color: #000; /* black text */
                    font-weight: bold; /* bold text */
                }}
            </style>
            {html}
        '''
    return html
