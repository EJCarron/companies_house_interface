from .appointment import Appointment
from .donation import Donation

appointment_str = Appointment.__name__
donation_str = Donation.__name__

appointment = Appointment
donation = Donation

relationship_dict = {appointment_str: Appointment,
                     donation_str: Donation
                     }
