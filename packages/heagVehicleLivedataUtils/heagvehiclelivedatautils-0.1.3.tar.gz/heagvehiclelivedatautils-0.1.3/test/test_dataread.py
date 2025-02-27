import unittest

import numpy as np
import pandas as pd
from heagVehicleLivedataUtils.analyze.plot import VehicleDataPlotter
from heagVehicleLivedataUtils.vehicleInformation import encode_line_name, st15Numbers, articlated_bus_numbers
from heagVehicleLivedataUtils.vehicleDataUtils.read import verify_vehicledata_format

class TestRead(unittest.TestCase):
    def test_regular_read_and_plot(self):
        da = VehicleDataPlotter(vehicledata_path="../test/vehicleInfo_test/")

        # test if working with data does not throw errors
        da.plot_number_of_trams_in_service(sample_time="15Min",show_plot=False)
        da.plot_all_trams_in_service(sample_time="15Min",show_plot=False)
        da.plot_electric_buses_in_service(sample_time="15Min",show_plot=False)

        da.get_tram_journeys()
        da.get_tram_journeys()

        # check if dataframe is formated to expected spec
        self.assertTrue(verify_vehicledata_format(da.get_vehicledata()))


    # TODO: what about ill formed data?/ -> error handling
    def test_special_read(self):
        da = VehicleDataPlotter(vehicledata_path="../test/vehicleInfo_test_special_cases/") # TODO seems to have problems with "6E" and such lines
        vehicle_data = da.get_vehicledata()

        timestamp = pd.Timestamp("2024-11-09T09:29:49+0100")

        # bus line as category 1(tram)
        self.assertEqual(vehicle_data.loc[(timestamp, 444),'category'],1)

        # added offset to vehicleid
        self.assertEqual(vehicle_data.loc[(timestamp, 4284), 'lineid'], encode_line_name("L"))

        # line name that can be read as float
        self.assertEqual(vehicle_data.loc[(timestamp, 430), 'lineid'], encode_line_name("4E"))

        # tram vehicleid on bus line
        self.assertEqual(vehicle_data.loc[(timestamp, 112), 'lineid'], encode_line_name("WE2"))


        timestamp = pd.Timestamp("2024-11-09T23:04:49+0100")

        # line name that can be read as float
        self.assertEqual(vehicle_data.loc[(timestamp, 69), 'lineid'], encode_line_name("8E"))

        # switched category
        self.assertEqual(vehicle_data.loc[(timestamp, 114), 'category'], 5)


        timestamp = pd.Timestamp("2024-11-09T23:39:49+0100")

        self.assertEqual(vehicle_data.loc[(timestamp, 405), 'lineid'], encode_line_name("8"))

        self.assertEqual(vehicle_data.loc[(timestamp, 68), 'lineid'], encode_line_name("6E"))

    def test_get_journeys(self):
        da = VehicleDataPlotter(vehicledata_path="../test/vehicleInfo_test/")

        for vehicles in (None, st15Numbers, articlated_bus_numbers):
            self.check_journeys_format(da.get_tram_journeys(vehicles=vehicles),vehicles)
            #self.check_journeys_decoded_line_format(da.get_tram_journeys(decode_line_id=True,vehicles=vehicles),vehicles)

            self.check_journeys_format(da.get_bus_journeys(vehicles=vehicles),vehicles)
            #self.check_journeys_decoded_line_format(da.get_bus_journeys(decode_line_id=True,vehicles=vehicles),vehicles)

    def check_journeys_format(self, journeys, vehicles=None):
        self.assertTrue({'vehicleid', 'lineid', 'start', 'end', 'direction'} <= set(journeys.columns))
        self.assertTrue(isinstance(journeys['lineid'].dtype, np.dtypes.Int64DType))

        self.assertEqual((journeys['lineid'] == 0).sum(),0)

        self.check_journeys_format_helper(journeys, vehicles)


    def check_journeys_decoded_line_format(self, journeys, vehicles=None):
        self.assertTrue({'vehicleid', 'line', 'start', 'end', 'direction'} <= set(journeys.columns))
        self.assertFalse(isinstance(journeys['line'].dtype, np.dtypes.Int64DType))

        self.assertEqual((journeys['line'] == '0').sum(),0)

        self.check_journeys_format_helper(journeys, vehicles)

    def check_journeys_format_helper(self, journeys, vehicles):
        self.assertTrue(isinstance(journeys['start'].dtype, pd.core.dtypes.dtypes.DatetimeTZDtype))
        self.assertTrue(isinstance(journeys['end'].dtype, pd.core.dtypes.dtypes.DatetimeTZDtype))

        self.assertEqual((journeys['start'] <= journeys['end']).prod(), 1)

        if vehicles is not None:
            self.assertTrue(set(journeys['vehicleid']) <= set(vehicles))

if __name__ == '__main__':
    unittest.main()
