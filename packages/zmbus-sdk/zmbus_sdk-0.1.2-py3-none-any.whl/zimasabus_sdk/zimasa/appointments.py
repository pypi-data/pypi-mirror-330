import dataclasses
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from dataclasses import field
import json

from zimasabus_sdk.zmsystem import ZmSystem, ZmSystemEnums


@dataclasses.dataclass
class ServiceType:
    """
    A class representing a service type.
    """
    id: int
    name: str
    description: str


@dataclasses.dataclass
class ServiceCategory:
    """
    A class representing a service category.
    """
    id: int
    name: str
    description: str
    service_type: Union[ServiceType, str]


@dataclasses.dataclass
class PageInfo:
    """
    A class representing pagination information.
    """
    page_number: int
    page_size: int
    total_elements: int
    total_pages: int
    is_first: bool
    is_last: bool
    is_empty: bool


@dataclasses.dataclass
class PagedResponse:
    """
    A class representing a paged response.
    """
    content: List[Any]
    page_info: PageInfo


@dataclasses.dataclass
class PaymentMethod:
    """
    A class representing a payment method.
    """
    id: int
    method: str
    is_global: Optional[bool] = None
    country: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclasses.dataclass
class ProviderServicePaymentMethod:
    """
    A class representing a provider service payment method.
    """
    id: int
    payment_method: PaymentMethod


@dataclasses.dataclass
class ProviderType:
    """
    A class representing a provider type.
    """
    id: int
    provider_type: str


@dataclasses.dataclass
class Provider:
    """
    A class representing a provider.
    """
    id: int
    name: str
    provider_type: ProviderType
    description: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    blacklisted: Optional[bool] = None
    accredited: Optional[int] = None
    capitation: Optional[bool] = None
    discount: Optional[float] = None
    effective_date: Optional[str] = None
    licence_number: Optional[str] = None


@dataclasses.dataclass
class Member:
    """
    A class representing a member.
    """
    id: str
    email: str
    first_name: str
    last_name: str
    username: str
    email_verified: Optional[int] = None
    enabled: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclasses.dataclass
class ProviderUser:
    """
    A class representing a provider user.
    """
    id: int
    provider: Provider
    member: Member
    status: str
    provider_type: ProviderType
    role: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclasses.dataclass
class ServiceHandler:
    """
    A class representing a service handler.
    """
    id: int
    is_available: bool
    provider_user: ProviderUser
    service_name: str


@dataclasses.dataclass
class ServiceAvailability:
    """
    A class representing service availability.
    """
    id: int
    day_of_week: str
    start_time: str
    end_time: str
    service_name: str


@dataclasses.dataclass
class ProviderService:
    """
    A class representing a provider service.
    """
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None
    service_category: Optional[ServiceCategory] = None
    maximum_capacity: Optional[int] = None
    duration_mins: Optional[int] = None
    availability: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    insurance_accepted: Optional[bool] = None
    tags: Optional[List[str]] = None
    service_mode: Optional[str] = None
    service_location: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    provider_user: Optional[ProviderUser] = None
    provider_service_payment_methods: Optional[List[ProviderServicePaymentMethod]] = None
    service_handlers: Optional[List[ServiceHandler]] = None
    service_availability: Optional[List[ServiceAvailability]] = None


@dataclasses.dataclass
class TimeSlot:
    """
    A class representing a time slot.
    
    Attributes:
        start_time (str): The start time in format "HH:mm" or "HH:mm:ss"
        end_time (str): The end time in format "HH:mm" or "HH:mm:ss"
        booked (bool): Whether the slot is already booked
    """
    start_time: str
    end_time: str
    booked: bool

    def get_duration_minutes(self) -> int:
        """Calculate the duration of the slot in minutes"""
        try:
            # Parse start time
            start_parts = self.start_time.split(':')
            start_hour = int(start_parts[0])
            start_minute = int(start_parts[1])
            
            # Parse end time
            end_parts = self.end_time.split(':')
            end_hour = int(end_parts[0])
            end_minute = int(end_parts[1])
            
            # Calculate duration in minutes
            duration = (end_hour - start_hour) * 60 + (end_minute - start_minute)
            return max(duration, 0)  # Ensure non-negative duration
        except (ValueError, IndexError):
            return 0  # Return 0 if parsing fails

    def format_time(self, time_str: str) -> str:
        """
        Format time string to ensure it has seconds.
        Converts "HH:mm" to "HH:mm:ss" if needed.
        """
        if ':' not in time_str:
            return time_str
        
        parts = time_str.split(':')
        if len(parts) == 2:
            return f"{time_str}:00"
        return time_str


@dataclasses.dataclass
class AvailableDate:
    """
    A class representing an available date with time slots.
    
    Attributes:
        date (str): The date in format "DD/MM/YY"
        time_slots (List[TimeSlot]): List of available time slots for this date
    """
    date: str
    time_slots: List[TimeSlot]

    def format_date_iso(self) -> str:
        """
        Convert date from "DD/MM/YY" to "YYYY-MM-DDThh:mm:ss.sssZ" format
        """
        try:
            day, month, year_short = self.date.split('/')
            year = f"20{year_short}"  # Assuming 21st century
            # Return in ISO format with timezone
            return f"{year}-{month}-{day}T10:00:00.000Z"  # Using 10:00 AM as default time
        except (ValueError, IndexError):
            return self.date  # Return original if parsing fails


@dataclasses.dataclass
class AvailabilityResponse:
    """
    A class representing the availability response.
    """
    available_dates: List[AvailableDate]


@dataclasses.dataclass
class AppointmentMember:
    """
    A class representing a member in an appointment response.
    """
    id: str
    email: Optional[str] = None
    email_verified: Optional[int] = None
    enabled: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclasses.dataclass
class AppointmentScheduleType:
    """
    A class representing a schedule type in an appointment response.
    """
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    slot_duration_minutes: Optional[int] = None
    break_duration_minutes: Optional[int] = None


@dataclasses.dataclass
class AppointmentResponse:
    """
    A class representing an appointment response.
    """
    id: int
    start_time: str
    end_time: str
    appointment_date: str
    notes: Optional[str]
    status: str
    action_reason: Optional[str]
    member: Optional[AppointmentMember]
    service: ProviderService
    schedule_type: AppointmentScheduleType
    created_at: Optional[str]
    updated_at: Optional[str]


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


    def get_appointment_service_types(self) -> PagedResponse:
        """
        Retrieves the available appointment service types from the provider.
        
        Returns:
            PagedResponse: A paged response containing service types.
        """
        url = self.system.base_url + "zimasa/provider/service/type"
        data = self.system.request("get", url)
        
        # Convert raw data to ServiceType objects
        service_types = []
        if isinstance(data, dict) and 'content' in data:
            for item in data['content']:
                service_types.append(ServiceType(
                    id=item.get('id'),
                    name=item.get('name'),
                    description=item.get('description')
                ))
            
            # Create page info
            page_info = PageInfo(
                page_number=data.get('pageable', {}).get('pageNumber', 0),
                page_size=data.get('pageable', {}).get('pageSize', 0),
                total_elements=data.get('numberOfElements', 0),
                total_pages=1,  # Assuming single page if not specified
                is_first=data.get('first', True),
                is_last=data.get('last', True),
                is_empty=data.get('empty', False)
            )
            
            return PagedResponse(content=service_types, page_info=page_info)
        
        return data  # Return raw data if format is unexpected
        
    def get_service_categories(self, service_type_id: int) -> PagedResponse:
        """
        Retrieves the service categories for a specific service type.
        
        Args:
            service_type_id (int): The ID of the service type to get categories for.
            
        Returns:
            PagedResponse: A paged response containing service categories.
        """
        url = f"{self.system.base_url}zimasa/provider/service/category?serviceTypeId={service_type_id}"
        data = self.system.request("get", url)
        
        # Convert raw data to ServiceCategory objects
        categories = []
        if isinstance(data, dict) and 'content' in data:
            for item in data['content']:
                service_type_data = item.get('serviceType', {})
                if isinstance(service_type_data, dict):
                    service_type = ServiceType(
                        id=service_type_data.get('id'),
                        name=service_type_data.get('name'),
                        description=service_type_data.get('description')
                    )
                else:
                    service_type = service_type_data  # Just use the string value
                
                categories.append(ServiceCategory(
                    id=item.get('id'),
                    name=item.get('name'),
                    description=item.get('description'),
                    service_type=service_type
                ))
            
            # Create page info
            page_info = PageInfo(
                page_number=data.get('pageable', {}).get('pageNumber', 0),
                page_size=data.get('pageable', {}).get('pageSize', 0),
                total_elements=data.get('numberOfElements', 0),
                total_pages=1,  # Assuming single page if not specified
                is_first=data.get('first', True),
                is_last=data.get('last', True),
                is_empty=data.get('empty', False)
            )
            
            return PagedResponse(content=categories, page_info=page_info)
        
        return data  # Return raw data if format is unexpected
        
    def get_bookable_services(self, service_category_id: int) -> PagedResponse:
        """
        Retrieves the list of services that can be booked for a specific category.
        
        Args:
            service_category_id (int): The ID of the service category to get bookable services for.
            
        Returns:
            PagedResponse: A paged response containing bookable services.
        """
        url = f"{self.system.base_url}zimasa/provider/service/search?isActive=true&serviceCategoryId={service_category_id}"
        data = self.system.request("get", url)
        
        # Convert raw data to ProviderService objects
        services = []
        if isinstance(data, dict) and 'content' in data:
            for item in data['content']:
                # Process service category
                service_category_data = item.get('serviceCategory', {})
                service_category = None
                if service_category_data:
                    service_type_data = service_category_data.get('serviceType')
                    service_category = ServiceCategory(
                        id=service_category_data.get('id'),
                        name=service_category_data.get('name'),
                        description=service_category_data.get('description'),
                        service_type=service_type_data  # This could be a string or a dict
                    )
                
                # Process payment methods
                payment_methods = []
                for pm_data in item.get('providerServicePaymentMethods', []):
                    pm = pm_data.get('paymentMethod', {})
                    payment_method = PaymentMethod(
                        id=pm.get('id'),
                        method=pm.get('method'),
                        is_global=pm.get('isGlobal'),
                        country=pm.get('country'),
                        created_at=pm.get('createdAt'),
                        updated_at=pm.get('updatedAt')
                    )
                    payment_methods.append(ProviderServicePaymentMethod(
                        id=pm_data.get('id'),
                        payment_method=payment_method
                    ))
                
                # Process service handlers
                service_handlers = []
                for handler_data in item.get('serviceHandlers', []):
                    provider_user_data = handler_data.get('providerUser', {})
                    
                    # Process provider
                    provider_data = provider_user_data.get('provider', {})
                    provider_type_data = provider_data.get('providerType', {})
                    provider_type = ProviderType(
                        id=provider_type_data.get('id'),
                        provider_type=provider_type_data.get('providerType')
                    )
                    provider = Provider(
                        id=provider_data.get('id'),
                        name=provider_data.get('name'),
                        provider_type=provider_type,
                        description=provider_data.get('description'),
                        contact_email=provider_data.get('contactEmail'),
                        contact_phone=provider_data.get('contactPhone'),
                        address=provider_data.get('address'),
                        created_at=provider_data.get('createdAt'),
                        updated_at=provider_data.get('updatedAt'),
                        blacklisted=provider_data.get('blacklisted'),
                        accredited=provider_data.get('accredited'),
                        capitation=provider_data.get('capitation'),
                        discount=provider_data.get('discount'),
                        effective_date=provider_data.get('effectiveDate'),
                        licence_number=provider_data.get('licenceNumber')
                    )
                    
                    # Process member
                    member_data = provider_user_data.get('member', {})
                    member = Member(
                        id=member_data.get('id'),
                        email=member_data.get('email'),
                        first_name=member_data.get('firstName'),
                        last_name=member_data.get('lastName'),
                        username=member_data.get('username'),
                        email_verified=member_data.get('emailVerified'),
                        enabled=member_data.get('enabled'),
                        phone=member_data.get('phone'),
                        address=member_data.get('address'),
                        date_of_birth=member_data.get('dateOfBirth'),
                        created_at=member_data.get('createdAt'),
                        updated_at=member_data.get('updatedAt')
                    )
                    
                    # Process provider user
                    provider_user = ProviderUser(
                        id=provider_user_data.get('id'),
                        provider=provider,
                        member=member,
                        status=provider_user_data.get('status'),
                        provider_type=ProviderType(
                            id=provider_user_data.get('providerType', {}).get('id'),
                            provider_type=provider_user_data.get('providerType', {}).get('providerType')
                        ),
                        role=provider_user_data.get('role'),
                        created_at=provider_user_data.get('createdAt'),
                        updated_at=provider_user_data.get('updatedAt')
                    )
                    
                    service_handlers.append(ServiceHandler(
                        id=handler_data.get('id'),
                        is_available=handler_data.get('isAvailable'),
                        provider_user=provider_user,
                        service_name=handler_data.get('serviceName')
                    ))
                
                # Process service availability
                service_availability = []
                for avail_data in item.get('serviceAvailability', []):
                    service_availability.append(ServiceAvailability(
                        id=avail_data.get('id'),
                        day_of_week=avail_data.get('dayOfWeek'),
                        start_time=avail_data.get('startTime'),
                        end_time=avail_data.get('endTime'),
                        service_name=avail_data.get('serviceName')
                    ))
                
                # Create the provider service
                services.append(ProviderService(
                    id=item.get('id'),
                    name=item.get('name'),
                    description=item.get('description'),
                    duration=item.get('duration'),
                    duration_mins=item.get('durationMins'),
                    price=item.get('price'),
                    is_active=item.get('isActive'),
                    service_category=service_category,
                    maximum_capacity=item.get('maximumCapacity'),
                    availability=item.get('availability'),
                    start_date=item.get('startDate'),
                    end_date=item.get('endDate'),
                    insurance_accepted=item.get('insuranceAccepted'),
                    tags=item.get('tags'),
                    service_mode=item.get('serviceMode'),
                    service_location=item.get('serviceLocation'),
                    created_at=item.get('createdAt'),
                    updated_at=item.get('updatedAt'),
                    provider_service_payment_methods=payment_methods,
                    service_handlers=service_handlers,
                    service_availability=service_availability
                ))
            
            # Create page info
            page_info = PageInfo(
                page_number=data.get('pageable', {}).get('pageNumber', 0),
                page_size=data.get('pageable', {}).get('pageSize', 0),
                total_elements=data.get('numberOfElements', 0),
                total_pages=1,  # Assuming single page if not specified
                is_first=data.get('first', True),
                is_last=data.get('last', True),
                is_empty=data.get('empty', False)
            )
            
            return PagedResponse(content=services, page_info=page_info)
        
        return data  # Return raw data if format is unexpected
        
    def get_available_slots(self, provider_service_id: int, year: int, month: int) -> AvailabilityResponse:
        """
        Retrieves available appointment slots for a specific provider service, year, and month.
        
        Args:
            provider_service_id (int): The ID of the provider service to check availability for.
            year (int): The year to check availability for.
            month (int): The month to check availability for (1-12).
            
        Returns:
            AvailabilityResponse: The response containing available appointment slots.
        """
        url = f"{self.system.base_url}zimasa/appointments/available-slots?providerServiceId={provider_service_id}&year={year}&month={month}"
        data = self.system.request("get", url)
        
        # Convert raw data to AvailabilityResponse
        if isinstance(data, list):
            available_dates = []
            for date_item in data:
                time_slots = []
                # Check if the response uses 'timeSlots' (as in the sample) or 'slots' (as in previous implementation)
                slots_data = date_item.get('timeSlots', date_item.get('slots', []))
                for slot in slots_data:
                    time_slots.append(TimeSlot(
                        start_time=slot.get('startTime'),
                        end_time=slot.get('endTime'),
                        booked=slot.get('booked', False)
                    ))
                
                available_dates.append(AvailableDate(
                    date=date_item.get('date'),
                    time_slots=time_slots
                ))
            
            return AvailabilityResponse(available_dates=available_dates)
        
        return data  # Return raw data if format is unexpected
        
    def reserve_appointment(
        self,
        provider_service_id: int,
        schedule_type: int,
        appointment_date: str,
        duration: int,
        start_time: str,
        end_time: str,
        communication_preference: str = "EMAIL",
        service_mode: str = "TELEHEALTH",
        notes: Optional[str] = None
    ) -> Union[AppointmentResponse, Dict[str, Any]]:
        """
        Reserves an appointment slot based on the available slots.
        
        Args:
            provider_service_id (int): The ID of the provider service to book.
            schedule_type (int): The type of schedule (e.g., 3 for regular appointment).
            appointment_date (str): The date of the appointment in ISO format with timezone.
            duration (int): The duration of the appointment in minutes.
            start_time (str): The start time of the appointment in format "HH:mm" or "HH:mm:ss".
            end_time (str): The end time of the appointment in format "HH:mm" or "HH:mm:ss".
            communication_preference (str, optional): The preferred communication method. Defaults to "EMAIL".
            service_mode (str, optional): The mode of service (e.g., "TELEHEALTH"). Defaults to "TELEHEALTH".
            notes (str, optional): Additional notes for the appointment. Defaults to None.
            
        Returns:
            Union[AppointmentResponse, Dict[str, Any]]: The response containing the reserved appointment details.
        """
        url = f"{self.system.base_url}zimasa/appointments"
        
        # Create a TimeSlot object to handle time formatting
        slot = TimeSlot(start_time=start_time, end_time=end_time, booked=False)
        
        # Format times to ensure HH:mm:ss format
        start_time = slot.format_time(start_time)
        end_time = slot.format_time(end_time)
        
        # Ensure appointment date is in ISO format with timezone
        if not appointment_date.endswith('Z'):
            if 'T' not in appointment_date:
                appointment_date = f"{appointment_date}T10:00:00.000Z"
            else:
                appointment_date = f"{appointment_date.split('T')[0]}T10:00:00.000Z"
        
        payload = {
            "providerService": provider_service_id,  # Send ID directly
            "scheduleType": schedule_type,  # Send ID directly
            "appointmentDate": appointment_date,
            "duration": duration,
            "startTime": start_time,
            "endTime": end_time,
            "communicationPreference": communication_preference,
            "serviceMode": service_mode,
            "notes": notes or ""
        }
        
        # Print the payload for debugging
        print("\nRequest payload:")
        print(json.dumps(payload, indent=2))
            
        data = self.system.request("post", url, json=payload)
        
        # Convert raw data to AppointmentResponse
        if isinstance(data, dict):
            try:
                # Parse member data if present
                member_data = data.get('member')
                member = None
                if member_data:
                    member = AppointmentMember(
                        id=member_data.get('id'),
                        email=member_data.get('email'),
                        email_verified=member_data.get('emailVerified'),
                        enabled=member_data.get('enabled'),
                        first_name=member_data.get('firstName'),
                        last_name=member_data.get('lastName'),
                        username=member_data.get('username'),
                        phone=member_data.get('phone'),
                        address=member_data.get('address'),
                        date_of_birth=member_data.get('dateOfBirth'),
                        created_at=member_data.get('createdAt'),
                        updated_at=member_data.get('updatedAt')
                    )
                
                # Parse schedule type data
                schedule_type_data = data.get('scheduleType', {})
                schedule_type = AppointmentScheduleType(
                    id=schedule_type_data.get('id', 0),
                    name=schedule_type_data.get('name'),
                    description=schedule_type_data.get('description'),
                    slot_duration_minutes=schedule_type_data.get('slotDurationMinutes'),
                    break_duration_minutes=schedule_type_data.get('breakDurationMinutes')
                )
                
                # Parse service data using existing ProviderService class
                service_data = data.get('service', {})
                service = self._parse_provider_service(service_data) if service_data else None
                
                return AppointmentResponse(
                    id=data.get('id'),
                    start_time=data.get('startTime'),
                    end_time=data.get('endTime'),
                    appointment_date=data.get('appointmentDate'),
                    notes=data.get('notes'),
                    status=data.get('status'),
                    action_reason=data.get('actionReason'),
                    member=member,
                    service=service,
                    schedule_type=schedule_type,
                    created_at=data.get('createdAt'),
                    updated_at=data.get('updatedAt')
                )
            except Exception as e:
                print(f"Error parsing appointment response: {e}")
                return data
        
        return data  # Return raw data if format is unexpected

    def _parse_provider_service(self, data: Dict[str, Any]) -> ProviderService:
        """Helper method to parse provider service data from appointment response."""
        try:
            # Parse service category
            category_data = data.get('serviceCategory', {})
            service_category = ServiceCategory(
                id=category_data.get('id'),
                name=category_data.get('name'),
                description=category_data.get('description'),
                service_type=category_data.get('serviceType')
            ) if category_data else None
            
            # Parse payment methods
            payment_methods = []
            for pm_data in data.get('providerServicePaymentMethods', []):
                pm = pm_data.get('paymentMethod', {})
                payment_method = PaymentMethod(
                    id=pm.get('id'),
                    method=pm.get('method'),
                    is_global=pm.get('isGlobal'),
                    country=pm.get('country'),
                    created_at=pm.get('createdAt'),
                    updated_at=pm.get('updatedAt')
                )
                payment_methods.append(ProviderServicePaymentMethod(
                    id=pm_data.get('id'),
                    payment_method=payment_method
                ))
            
            # Parse service handlers
            service_handlers = []
            for handler_data in data.get('serviceHandlers', []):
                handler = ServiceHandler(
                    id=handler_data.get('id'),
                    is_available=handler_data.get('isAvailable'),
                    provider_user=None,  # Skip nested provider user for simplicity
                    service_name=handler_data.get('serviceName')
                )
                service_handlers.append(handler)
            
            # Parse service availability
            service_availability = []
            for avail_data in data.get('serviceAvailability', []):
                availability = ServiceAvailability(
                    id=avail_data.get('id'),
                    day_of_week=avail_data.get('dayOfWeek'),
                    start_time=avail_data.get('startTime'),
                    end_time=avail_data.get('endTime'),
                    service_name=avail_data.get('serviceName')
                )
                service_availability.append(availability)
            
            return ProviderService(
                id=data.get('id'),
                name=data.get('name'),
                description=data.get('description'),
                duration=data.get('duration'),
                duration_mins=data.get('durationMins'),
                price=data.get('price'),
                is_active=data.get('isActive'),
                service_category=service_category,
                maximum_capacity=data.get('maximumCapacity'),
                availability=data.get('availability'),
                start_date=data.get('startDate'),
                end_date=data.get('endDate'),
                insurance_accepted=data.get('insuranceAccepted'),
                tags=data.get('tags'),
                service_mode=data.get('serviceMode'),
                service_location=data.get('serviceLocation'),
                created_at=data.get('createdAt'),
                updated_at=data.get('updatedAt'),
                provider_service_payment_methods=payment_methods,
                service_handlers=service_handlers,
                service_availability=service_availability
            )
        except Exception as e:
            print(f"Error parsing provider service: {e}")
            return None
