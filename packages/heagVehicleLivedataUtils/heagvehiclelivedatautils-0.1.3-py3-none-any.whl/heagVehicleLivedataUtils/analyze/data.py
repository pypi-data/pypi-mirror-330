"""
provides the DataAnalysis class which provides tools for analyzing the vehicle data

TODO: write more
"""
import pandas as pd

from ..vehicleDataUtils.read import verify_vehicledata_format, vehicledata_from_dir
from ..vehicleDataUtils.process import trams_in_service, number_of_trams_in_service, buses_in_service, \
    get_vehicle_journeys, remove_duplicated_index, remove_stationary_vehicles
from ..vehicleInformation import decode_line_id as decode_line_id_mapping, get_tram_number


# TODO: vllt hier auch weitere optionen?

class DataAnalysis:
    """
    Class to provide tools to analyze given vehicle data.

    TODO: add a bit of detail
    """

    def __init__(self,
                 /,
                 vehicledata: pd.DataFrame = None,
                 *,
                 vehicledata_path: str = None
                 ):
        """


        Args:
            vehicledata: dataframe containing vehicle data. if vehicledata_path or response_paths are specified, this will be disregarded

            vehicledata_path: path to directory where to look for vehicle data json files. if vehicledata is specified, this will be disregarded
        """

        self._vehicledata: pd.DataFrame

        if (vehicledata_path is not None) + (vehicledata is not None) > 1:
            # more than one data sources specified
            Warning("more than one data sources specified, only the fist one will be regarded")


        if vehicledata is not None:
            self.__set_vehicledata_dataframe(vehicledata)
        elif vehicledata_path is not None:
            self.__set_vehicledata_dataframe(vehicledata_from_dir(vehicledata_path))

    def __set_vehicledata_dataframe(self, vehicledata: pd.DataFrame):
        """
        provide vehicledata dataframe directly
        Args:
            vehicledata: dataframe to analyze
        """
        verify_vehicledata_format(vehicledata)

        self._vehicledata = vehicledata

    def get_vehicledata(self) -> pd.DataFrame:
        """

        Returns: the vehicledata dataframe

        """
        return self._vehicledata

    def get_tram_data(self,trams_to_return:list|None =None):
        """
        gives the part of vehicle data that contains info about trams

        Args:
            trams_to_return: the trams for which we should return data

        Returns:
            vehicledata (with 'timestamp' and 'vehicleid' as columns)
        """
        vehicledata = self.get_vehicledata()
        vehicledata = remove_duplicated_index(vehicledata)

        trams = vehicledata[vehicledata['category'] == 1].reset_index()
        # TODO: remove reset index when we move away form vehicleid timestamp index

        trams = remove_stationary_vehicles(trams)

        trams['vehicleid'] = trams['vehicleid'].map(get_tram_number)

        if trams_to_return is not None:
            trams = trams[trams['vehicleid'].isin(trams_to_return)]

        return trams

    def get_bus_data(self, buses_to_return:list|None =None):
        """
        gives the part of vehicle data that contains info about buses

        Args:
            buses_to_return: the buses for which we should return data

        Returns:
            vehicledata (with 'timestamp' and 'vehicleid' as columns)
        """
        vehicledata = self.get_vehicledata()
        vehicledata = remove_duplicated_index(vehicledata)

        buses = vehicledata[vehicledata['category'] == 5].reset_index()
        # TODO: remove reset index when we move away form vehicleid timestamp index

        buses = remove_stationary_vehicles(buses)

        buses['vehicleid'] = buses['vehicleid'].map(lambda x: str(x))

        if buses_to_return is not None:
            buses = buses[buses['vehicleid'].isin(buses_to_return)]

        return buses

    def get_trams_in_service(self, **kwargs) -> pd.DataFrame:
        """
        Args:
            same as process.trams_in_service

        Returns: the dataframe containing the service assignemt of the trams in this analysis

        """
        return trams_in_service(self._vehicledata, **kwargs)

    def get_number_of_trams_in_service(self, sample_time: str|None = None) -> pd.DataFrame:
        """
        Args:
            sample_time: sample size of the vehicledata

        Returns:
            dataframe with numbers of trams in service, index by timestamp.
        """
        number_in_service = number_of_trams_in_service(self.get_trams_in_service()['lineid'])
        if sample_time is not None:
            number_in_service = number_in_service.resample(sample_time).mean()
        return number_in_service

    def get_buses_in_service(self, **kwargs) -> pd.DataFrame:
        """
        Args:
            same as process.buses_in_service

        Returns: the dataframe containing the service assignemt of the buses in this analysis

        """

        return buses_in_service(self._vehicledata, **kwargs)

    def get_tram_journeys(self, vehicles:list|None =None, decode_line_id:bool= False) -> pd.DataFrame:
        """
        extracts journeys of tram vehicles from vehicle data
        Args:
            vehicles: the vehicles for which journeys should be extracted
            decode_line_id: whether the lineid should be decoded to string
        Returns:
            dataframe of journeys indexed by vehicleid and journey count
        """

        journeys = get_vehicle_journeys(self.get_tram_data(vehicles))

        if decode_line_id:
            journeys['line'] = journeys['lineid'].map(decode_line_id_mapping)
            journeys = journeys.drop(columns=['lineid'])
        return journeys

    def get_bus_journeys(self, vehicles:list|None =None, decode_line_id:bool= False) -> pd.DataFrame:
        """
        extracts journeys of buses from vehicle data
        Args:
            vehicles: the vehicles for which journeys should be extracted
            decode_line_id: whether the lineid should be decoded to string
        Returns:
            dataframe of journeys indexed by vehicleid and journey count
        """
        journeys = get_vehicle_journeys(self.get_bus_data(vehicles))

        if decode_line_id:
            journeys['line'] = journeys['lineid'].map(decode_line_id_mapping)
            journeys = journeys.drop(columns=['lineid'])
        return journeys