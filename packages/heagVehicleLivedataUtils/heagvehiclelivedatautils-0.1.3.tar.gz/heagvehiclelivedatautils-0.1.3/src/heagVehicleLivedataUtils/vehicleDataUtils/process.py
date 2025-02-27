"""
methods for working with collection of vehicle data.
"""

import pandas as pd

from ..vehicleInformation import get_tram_number, st12Numbers, st13Numbers, st14Numbers, \
    st15Numbers
from .read import vehicledata_index_timestamp,vehicledata_index_vehicleid

def remove_duplicated_index(df: pd.DataFrame) -> pd.DataFrame:
    """removes entries with duplicated index

    Args:
        df: pandas dataframe

    Returns:
        dataframe where only fist occurrence of each index is kept
        """
    return df[~df.index.duplicated(keep='first')]

def _df_changes(df: pd.DataFrame)-> pd.DataFrame:
    """
    returns changes in entires of dataframe

    Args:
        df:

    Returns:
        dataframe of same shape as df, with values True if entries in columns changed. first row will always be True

    """
    return df.ne(df.shift())

def remove_stationary_vehicles(vehicledata:pd.DataFrame, max_number_of_occorences:int = 5):
    """
    removes entries of vehicles that are stationary
    Args:
        vehicledata: the data to be filtered ('vehicleid' and 'timestamp' as columns)
        max_number_of_occorences: max number of tolerated stationary frames

    Returns:
        filterd vehicledata
    """
    vehicledata = vehicledata.sort_values(['vehicleid', 'timestamp'])

    changes = (_df_changes(vehicledata['longitude']) + _df_changes(vehicledata['latitude']) + _df_changes(vehicledata['vehicleid'])).cumsum() # TODO: vllt drauf achten das da nur am depot gefilterd wird?
    # TODO: ist vehicleid changes relevant? -> could save some ms?

    return vehicledata.groupby(changes).head(max_number_of_occorences)



def _vehicles_in_service_helper(vehicledata:pd.DataFrame, columns:list|None, vehicles:list|None, column_mapper) -> pd.DataFrame:
    """ list the lines the vehicles are in service on, based on the presented vehicleData
    #TODO: das passt nicht mehr so

    Args:
        vehicledata: with ('vehicleid' and 'timestamp' as columns)
        columns: columns to be included in return
        vehicles: the trams to be included in return

    Returns:
        DataFrame: DataFrame indexed by timestamps and columns are the give mulitindexed with trams
    """
    # remove duplicated index
    vehicledata = remove_duplicated_index(vehicledata)

    if columns is not None:
        if not (set(columns).union({'vehicleid', 'timestamp'})).issubset(vehicledata.columns):
            raise KeyError('columns not in vehicledata')

        vehicledata = vehicledata.reindex(columns=columns + ['vehicleid', 'timestamp'])
    else:
        columns = set(vehicledata.columns) - {'vehicleid', 'timestamp'} # we keep this to be able to reindex with multidex later on
        # TODO: geht das nicht auch noch anders? -> so ist das iwi zimlich unklar was da passiert!!
    # TODO: maybe geht hier auch schon die vehicles zu filtern? -> könnte mit drop(index) klappen aba keine ahnung wie das funktioniert

    if vehicledata.empty:
        raise ValueError('empty Dataframe, cannot pivot')

    vehicles_in_service = vehicledata.reset_index().pivot(index=vehicledata_index_timestamp,
                                                          columns=vehicledata_index_vehicleid)

    vehicles_in_service.columns = vehicles_in_service.columns.map(column_mapper)  # keep column and convert vehicleid

    if vehicles is not None:
        column_names = vehicles_in_service.columns.names  # keeps vehicleid as named column index
        new_columns = pd.MultiIndex.from_product((columns, vehicles), names=column_names)
        vehicles_in_service = vehicles_in_service.reindex(columns=new_columns)
        # TODO: maybe geht das hier auch über nen drop columns?

    return vehicles_in_service


def trams_in_service(vehicledata: pd.DataFrame, columns: list | None=None, vehicles: list | None =None) -> pd.DataFrame:
    """ list the lines the trams are in service on, based on the presented vehicleData
    #TODO: das passt nicht mehr so

    Args:
        vehicledata: dataFrame as given by vehicleData_from_jsonFiles
        columns: columns to be included in return
        vehicles: the trams to be included in return

    Returns:
        DataFrame: DataFrame indexed by timestamps and columns are the give mulitindexed with trams
    """
    trams = vehicledata[vehicledata['category'] == 1].reset_index()
    trams = remove_stationary_vehicles(trams)

    return  _vehicles_in_service_helper(trams, columns, vehicles, lambda x: (x[0], get_tram_number(x[1])))

def buses_in_service(vehicledata: pd.DataFrame, columns: list | None = None,
                     vehicles: list | None = None) -> pd.DataFrame:
    """ list the lines the buses are in service on, based on the presented vehicleData
    #TODO: das passt nicht mehr so

    Args:
        vehicledata (DataFrame): dataFrame as given by vehicleData_from_jsonFiles
        columns: columns to be included in return
        vehicles: the buses to be included in return

    Returns:
        DataFrame: DataFrame indexed by timestamps that contains the line the selected buses are in service on
    """
    buses = vehicledata[vehicledata['category'] == 5]
    buses.reset_index(inplace=True)

    return _vehicles_in_service_helper(buses, columns, vehicles, lambda x: (x[0], str(x[1])))


def number_of_trams_in_service(trams_in_service: pd.DataFrame) -> pd.DataFrame:
    """
    counts the number of trams in each class, that are in servie for at each timestamp
    TODO: ahh grammar

    Args:
        trams_in_service: the service dataframe, formated like return of trams_in_service

    Returns: dataframe containing the counts per class at each timestamp

    """
    tram_class_number_tuples=[("ST12", st12Numbers), ("ST13", st13Numbers), ("ST14", st14Numbers), ("ST15", st15Numbers)]
    number_of_trams_in_service_series_list_by_class: list[pd.Series] = []
    visited_columns: list[str] = []

    for tram_class_tuple in tram_class_number_tuples:
        number_of_trams_of_class_series = (trams_in_service.reindex(columns=tram_class_tuple[1])
                                           .fillna(0).map(lambda x: x > 0).sum(axis=1)) # adds one for every tram in service
        number_of_trams_of_class_series.name = tram_class_tuple[0]
        number_of_trams_in_service_series_list_by_class.append(number_of_trams_of_class_series)

        visited_columns.extend(tram_class_tuple[1])

    other_trams = trams_in_service.columns.difference(visited_columns)
    number_of_other_trams_in_service = trams_in_service.reindex(columns=other_trams).fillna(0).map(lambda x: x > 0).sum(axis=1)
    number_of_other_trams_in_service.name="other"
    number_of_trams_in_service_series_list_by_class.append(number_of_other_trams_in_service)

    return pd.concat(number_of_trams_in_service_series_list_by_class,axis=1)


def get_vehicle_journeys(vehicledata:pd.DataFrame):
    """

    Args:
        vehicledata: with ('vehicleid' and 'timestamp' as columns)

    Returns:
        dataframe with journeys, with timestamp for begin and end, as well as line number and destination.
        index by vehicleid and journeynumber

    """
    vehicledata.sort_values(['vehicleid','timestamp'])
    changes = (_df_changes(vehicledata['lineid']) + _df_changes(vehicledata['direction']) + _df_changes(vehicledata['vehicleid'])).cumsum()

    journeys = vehicledata.groupby(changes)

    return journeys.agg(
        start=pd.NamedAgg(column='timestamp', aggfunc='first'),
        end=pd.NamedAgg(column='timestamp', aggfunc='last'),
        lineid=pd.NamedAgg(column='lineid', aggfunc='first'),
        direction=pd.NamedAgg(column='direction', aggfunc='first'),
        vehicleid=pd.NamedAgg(column='vehicleid', aggfunc='first'),
    )
