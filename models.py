"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""


from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether
    it's marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments
        supplied to the constructor.
        """
        self.designation = str(info['pdes'])
        self.name = info['name'] if ('name' in info) else None

        if 'diameter' in info:
            self.diameter = float(info['diameter'])
        else:
            self.diameter = float('nan')

        hazad = info.get('pha', '')
        self.hazardous = True if hazad == 'Y' else False

        self.approaches = []

    @property
    def fullname(self):
        """Full name of NEO.

        Return a representation of the full name of this NEO.
        """
        return f'{self.designation} {self.name}'

    def __str__(self):
        """Return `str(self)`.

        To print the NEO info.
        """
        if self.hazardous:
            hazardous = ' '
        else:
            hazardous = ' not'

        if self.diameter:
            diameter = self.diameter
        else:
            diameter = 'NOT FOUND'
        return (f"A NearEarthObject with primary designation :"
                f"{self.designation}, name: {self.name} has a"
                f"diameter of {diameter} and is{hazardous}"
                f"potentialy hazardous.")

    def __repr__(self):
        """Print option.

        Return `repr(self)`, a computer-readable
        string representation of this object.

        """
        return (f"NearEarthObject(designation={self.designation!r},"
                f"name={self.name!r}, diameter={self.diameter:.3f},"
                f"hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close
    approach to Earth, such as the date and time (in UTC) of closest
    approach, the nominal approach distance in astronomical units,
    and the relative approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its
    `NearEarthObject` - initally, this information (the NEO's
    primary designation) is saved in a private attribute, but the
    referenced NEO is eventually replaced in the`NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to
        the constructor.
        """
        self._designation = info['des']
        self.time = cd_to_datetime(info['cd']) if 'cd' in info else None
        self.distance = float(info['dist']) if 'dist' in info else 0.0
        self.velocity = float(info['v_rel']) if 'v_rel' in info else 0.0

        self.neo = None

    @property
    def time_str(self):
        """Approach Time.

        Return a formatted representation of this `CloseApproach`'s
        approach time. The value in `self.time` should be a Python
        `datetime` object. While a `datetime` object has a string
        representation, the default representation includes seconds
        - significant figures that don't exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object
        to a formatted string that can be used in human-readable
        representations and in serialization to CSV and JSON files.
        """
        if self.time is not None:
            return datetime_to_str(self.time)
        else:
            return None

    def __str__(self):
        """Return `str(self)`.

        Represent the str.
        """
        return (f"A CloseApproach with primary designation "
                f"{self._designation}, on {self.time_str},"
                f"is at closest distance {self.distance} au."
                f"and having the velosity {self.velocity}")

    def __repr__(self):
        """Return Computer Readable str.

        Return `repr(self)`, a computer-readable string
        representation of this object.
        """
        return (f"CloseApproach(time={self.time_str!r}, i"
                f"distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")
