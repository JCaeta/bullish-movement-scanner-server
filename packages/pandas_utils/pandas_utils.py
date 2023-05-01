import pandas as pd
import datetime as dt

class PandasFormatter:
    def has_commas(self, df) -> bool:
        for column in df.columns:
            for value in df[column]:
                if isinstance(value, str) and ',' in value:
                    return True
        return False

    def remove_commas(self, df):
        return df.apply(lambda x: x.str.replace(',', ''))
    
    def change_date_format(self, df, new_fmt = ''):
        """
        Formats examples
        01/30/2023 -> %m/%d/%Y
        2022-02-19 -> %Y-%m-%d
        """

        df = pd.to_datetime(df)
        return df.dt.strftime(new_fmt)

    def reverse_dataframe(self, df):
        return df.iloc[::-1]
    
    # def convert_datetime_to_timestamps(self, df):
    #     """
    #     In the df must to have only the datetime columns we want to convert
    #     """
    #     return df.apply(lambda x: int(dt.datetime.timestamp(x)))