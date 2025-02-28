from bsm2_python.bsm2.adm1_bsm2 import ADM1Reactor


class ADM1Performance:
    """Class for ADM1 reactor performance variables.

    Parameters
    ----------
    adm1_obj : ADM1Reactor
        ADM1Reactor instance.

    Attributes
    ----------
    dim : np.ndarray
        Reactor dimensions [m³].
    hydrogen_concentration : int or float
        Concentration of hydrogen in the biogas [mol/m³].
    methane_concentration : int or float
        Concentration of methane in the biogas [mol/m³].
    carbon_dioxide_concentration : int or float
        Concentration of carbon dioxide in the biogas [mol/m³].
    """

    def __init__(self, adm1_obj: ADM1Reactor):
        self.dim = adm1_obj.dim
        self.hydrogen_concentration = 0
        self.methane_concentration = 0
        self.carbon_dioxide_concentration = 0

    def energy_consumption(self, t_new, t_old, rho_h2o=997, cp_h2o=4182):
        """Returns the energy required to heat up the reactor from t_old to t_new.

        Parameters
        ----------
        t_new : int or float
            The new temperature of the reactor [K].
        t_old : int or float
            The old temperature of the reactor [K].
        rho_h2o : int or float
            The density of water [kg/m³].
        cp_h2o : int or float
            The specific heat capacity of water [J/(kg*K)].

        Returns
        -------
        heat_in_kwh : int or float
            Energy required to heat up the reactor [kWh].
        """

        vol_reactor = self.dim[0]
        # Q = mcΔT
        heat_in_joules = rho_h2o * vol_reactor * cp_h2o * (t_new - t_old)
        heat_in_kwh = heat_in_joules / (3600 * 1000)  # Convert from joules to kilowatts

        return heat_in_kwh

    def reactor_temperature(self, heat_in_kwh, t_old, rho_h2o=997, cp_h2o=4182):
        """Returns the new temperature of the reactor after energy has been supplied to the reactor.

        Parameters
        ----------
        heat_in_kwh : int or float
            Energy supplied to heat up the reactor [kWh].
        t_old : int or float
            The old temperature of the reactor [K].
        rho_h2o : int or float
            The density of water [kg/m³].
        cp_h2o : int or float
            The specific heat capacity of water [J/(kg*K)].

        Returns
        -------
        t_new : int or float
            The new temperature of the reactor [K].
        """

        vol_reactor = self.dim[0]
        t_new = t_old + (heat_in_kwh * 3600 * 1000) / (rho_h2o * vol_reactor * cp_h2o)
        return t_new

    def biogas_productions(self, hydrogen_concentration, methane_concentration, carbon_dioxide_concentration):
        """Returns the total biogas production [kWh] from the ADM1 reactor based on the last output.

        Parameters
        ----------
        hydrogen_concentration : int or float
            Hydrogen concentration in the biogas [mol/m³].
        methane_concentration : int or float
            Methane concentration in the biogas [mol/m³].
        carbon_dioxide_concentration : int or float
            Carbon dioxide concentration in the biogas [mol/m³].

        Returns
        -------
        total_energy_kwh : int or float
            Total biogas production [kWh].
        """

        # convert the concentration to kg/m3
        hydrogen_concentration = hydrogen_concentration * 2.016 / 1000
        methane_concentration = methane_concentration * 16.04 / 1000
        carbon_dioxide_concentration = carbon_dioxide_concentration * 44.01 / 1000
        # calculate the total energy in the biogas
        self.hydrogen_concentration = hydrogen_concentration
        self.methane_concentration = methane_concentration
        self.carbon_dioxide_concentration = carbon_dioxide_concentration
        methane_lhv = 890  # [kWh/kg]
        hydrogen_lhv = 33  # [kWh/kg]
        total_energy_kwh = (
            self.hydrogen_concentration * hydrogen_lhv + self.methane_concentration * methane_lhv
        ) * self.dim[1]
        return total_energy_kwh
