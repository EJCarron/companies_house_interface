from .appointment import Appointment
from .doppelganger import Doppelganger
from .donation import Donation

relationship_factory = {'Appointment': Appointment,
                        'Doppelganger': Doppelganger,
                        'Donation': Donation
                        }