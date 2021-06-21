"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""

class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        import numpy as np

        debug= False
        self._neos = neos
        self._approaches = approaches

        self._pdes_to_neos= {neo.designation: neo for neo in neos}
        self._pdes_to_approaches= dict()
        self._neos_name_to_pdes= dict()

        self._time_to_pdes= {approach.time : approach._designation for approach in self._approaches} 
        self._distance_to_pdes= {approach.distance : approach._designation for approach in self._approaches}
        self._velocity_to_pdes= {approach.velocity : approach._designation for approach in self._approaches}
        self._diameter_to_pdes= {neo.diameter : neo.designation for neo in self._neos}
        
        self._time_arr= np.array(self._time_to_pdes.keys())
        self._distance_arr= np.array(self._distance_to_pdes.keys())
        self._velocity_arr= np.array(self._velocity_to_pdes.keys())
        self._diameter_arr= np.array(self._diameter_to_pdes.keys())

        for approach in self._approaches:
            pdes= approach._designation
            # To add the neo in the approach.neo list in model.py
            try:
                approach.neo = self._pdes_to_neos[pdes]
            except KeyError:
                print(f'No neo with the pdes {pdes} is found in the neos csv files')
                continue

            try:
                self._pdes_to_neos[pdes].approaches.append(approach)
            except KeyError:
                print(f'No neo with the pdes {pdes} is found in the neos csv files')
     
            if debug:
                print(f'success pdes: {pdes}')
            if self._pdes_to_neos[pdes].name!= None:
                self._neos_name_to_pdes[self._pdes_to_neos[pdes].name]=pdes
       
    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        try:
            neo= self._pdes_to_neos[designation]
            return neo
        except:
            return None

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        try:
            pdes= self._neos_name_to_pdes[name]
            return self._pdes_to_neos[pdes]
        except:
            return None

    def query(self, filters):
        """
        Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        if len(filters) == 0:
            for approach in self._approaches:
                yield approach
        else: 
            for approach in self._approaches:
                filter_res= False
                for filt in filters:
                    filter_res= filt(approach)
                    if filter_res:
                        continue
                    else:
                        break

                if filter_res:
                    yield approach
                else:
                    continue





