from .appointment import Appointment
from .doppelganger import Doppelganger
from .donation import Donation

appointment_str = Appointment.__name__
doppelganger_str = Doppelganger.__name__
donation_str = Donation.__name__

appointment = Appointment
doppelganger = Doppelganger
donation = Donation

relationship_dict = {appointment_str: Appointment,
                     doppelganger_str: Doppelganger,
                     donation_str: Donation
                     }
