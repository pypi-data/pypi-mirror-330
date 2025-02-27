import dataclasses
from typing import List

from zimasabus_sdk.zmsystem import ZmSystem, ZmSystemEnums


@dataclasses.dataclass
class AppointmentService:
    """
    A class representing an appointment service.

    Attributes:
        system (ZmSystem): The ZmSystem object representing the system.
    """

    system: ZmSystem = dataclasses.field(
        default_factory=lambda: ZmSystem(zm_system_enum=ZmSystemEnums.ZIMASAMED)
    )


    def get_appointment_service_types(self) -> dict:
        """
        Retrieves the available appointment service types from the provider.
        
        Returns:
            dict: The response data containing appointment service types.
        """
        url = self.system.base_url + "zimasa/provider/service/type"
        data = self.system.request("get", url)
        return data
