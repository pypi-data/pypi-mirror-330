import logging

from peaqevcore.common.spotprice.const import *
from peaqevcore.common.spotprice.energidataservice import EnergiDataServiceUpdater
from peaqevcore.common.spotprice.models.spotprice_type import SpotPriceType
from peaqevcore.common.spotprice.nordpool import NordPoolUpdater
from peaqevcore.common.spotprice.spotpricebase import SpotPriceBase
from peaqevcore.common.models.peaq_system import PeaqSystem

_LOGGER = logging.getLogger(__name__)


class SpotPriceFactory:

    sources = {
        SpotPriceType.NordPool: NordPoolUpdater,
        SpotPriceType.EnergidataService: EnergiDataServiceUpdater
    }

    @staticmethod
    def create(
        hub, 
        observer, 
        system: PeaqSystem,
        test:bool = False, 
        is_active: bool = False,
        custom_sensor: str = None,
        spotprice_type: SpotPriceType = SpotPriceType.NordPool
        ) -> SpotPriceBase:
        if test:
            return NordPoolUpdater(hub, test, system, observer)
        source = SpotPriceFactory.test_connections(hub.state_machine, spotprice_type, system, custom_sensor)
        return SpotPriceFactory.sources[source](hub, observer, system, test, is_active, custom_sensor)

    @staticmethod
    def test_connections(hass, spotprice_type: SpotPriceType, system: PeaqSystem, custom_sensor: str = None) -> SpotPriceType:
        if spotprice_type == SpotPriceType.NordPool and system == PeaqSystem.PeaqEv:
            """only do new logic if coming from peaqev."""
            return SpotPriceType.NordPool
        sensor = hass.states.get(ENERGIDATASERVICE_SENSOR)       
        if sensor or (custom_sensor and custom_sensor == ENERGIDATASERVICE_SENSOR):
            return SpotPriceType.EnergidataService
        return SpotPriceType.NordPool
                

    