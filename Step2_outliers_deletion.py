import pandas as pd
from tabulate import tabulate

#due to enormous size of our data set and the pandas' interpretetion of column of unknown type as <object> (which is quite memory-intensive) we need to manually define data type of each column

dtypes={
    "FL_DATE": "str",
    "AIRLINE": "str",
    "AIRLINE_CODE": "str",
    "FL_NUMBER": "int",
    "ORIGIN": "str",
    "ORIGIN_CITY": "str",
    "DEST": "str",
    "DEST_CITY": "str",
    "CRS_DEP_TIME": "int",
    "DEP_DELAY": "float64",
    "TAXI_OUT": "float64",
    "TAXI_IN": "float64",
    "CRS_ARR_TIME": "int",
    "ARR_DELAY": "float64",
    "CANCELLED": "bool",
    "CANCELLATION_CODE": "str",
    "DIVERTED": "bool",
    "DISTANCE": "int",
    "DELAY_DUE_CARRIER": "float64",
    "DELAY_DUE_WEATHER": "float64",
    "DELAY_DUE_NAS": "float64",
    "DELAY_DUE_SECURITY": "float64",
    "DELAY_DUE_LATE_AIRCRAFT": "float64"
}


data_set = pd.read_csv('clean_data_set.csv', dtype=dtypes)
searching_for_outliers = data_set.describe()
print(tabulate(searching_for_outliers, headers='keys', tablefmt='psql'))
searching_for_outliers_regular_columns = data_set[["DEP_DELAY", "TAXI_OUT", "TAXI_IN", "ARR_DELAY"]]

#we find outliers using IQR method and then we drop them from our data set with no mercy

def finding_outliers_in_regular_columns(data):
    q1 = data.quantile(0.05)
    q3 = data.quantile(0.95)
    IQR = q3 - q1
    outliers = data[((data < (q1-1.5*IQR)) | (data > (q3+1.5*IQR)))]
    is_outlier = outliers.any(axis=1)
    outliers_indices = set(is_outlier[is_outlier].index)
    return outliers_indices


histogram = data_set.hist(bins=50, figsize=(12, 10))
figure = histogram[0][0].get_figure()
figure.savefig(f'Chart_before_dropping_outliers.pdf')

print(tabulate(data_set.describe(), headers='keys', tablefmt='psql'))
data_set.drop(data_set.index[list(finding_outliers_in_regular_columns(searching_for_outliers_regular_columns))], inplace=True)
print(tabulate(data_set.describe(), headers='keys', tablefmt='psql'))

histogram = data_set.hist(bins=50, figsize=(12, 10))
figure = histogram[0][0].get_figure()
figure.savefig(f'Chart_after_dropping_outliers.pdf')

data_set.to_csv('whole_data_set.csv', index=False, header=True)
