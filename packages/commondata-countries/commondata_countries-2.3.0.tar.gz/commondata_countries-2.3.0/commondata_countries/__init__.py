from typing import Iterator, List, Union, cast

from rapidfuzz import fuzz, process

from commondata_countries.data import countries


class Country:
    """Represents a country with ISO 3166-1 codes and name."""

    def __init__(
        self,
        label: str,
        iso_alpha2: str,
        iso_alpha3: str,
        iso_numeric: int,
        synonyms: List[str],
    ):
        self.label = label
        self.iso_alpha2 = iso_alpha2
        self.iso_alpha3 = iso_alpha3
        self.iso_numeric = iso_numeric
        self.synonyms = synonyms

    def __repr__(self):
        return f"Country(label='{self.label}', iso_alpha2='{self.iso_alpha2}', iso_alpha3='{self.iso_alpha3}', iso_numeric={self.iso_numeric})"

    def to_dict(self):
        return {
            "label": self.label,
            "iso_alpha2": self.iso_alpha2,
            "iso_alpha3": self.iso_alpha3,
            "iso_numeric": self.iso_numeric,
        }


class CountryData:
    """Main API for accessing country data."""

    fuzzy_threshold = 75

    def __init__(self):
        self._countries = self._load_countries()
        self._index = {c.iso_alpha2.upper(): c for c in self._countries}
        self._index.update({c.iso_alpha3.upper(): c for c in self._countries})
        self._index.update({str(c.iso_numeric): c for c in self._countries})
        self._search_index = {c.label.lower(): c for c in self._countries}
        for c in self._countries:
            for synonym in c.synonyms:
                self._search_index[synonym.lower()] = c

    def _load_countries(self) -> List[Country]:
        """Loads country data from a static JSON file."""
        return [
            Country(
                d["label"],
                d["iso_alpha2"],
                d["iso_alpha3"],
                d["iso_numeric"],
                d["synonyms"],
            )
            for d in countries
        ]

    def all(self) -> List[Country]:
        """Returns a list of all countries."""
        return self._countries

    def __iter__(self) -> Iterator[Country]:
        """Allows iteration over all countries."""
        return iter(self._countries)

    def __getitem__(self, key: Union[str, int]) -> Union[Country, None]:
        """Lookup country by ISO Alpha-2, ISO Alpha-3, ISO Numeric, or name (case insensitive, with fuzzy search)."""
        if isinstance(key, int):
            key = str(key)

        direct_match = self.get(key)
        if direct_match:
            return direct_match

        country_labels = list(self._search_index.keys())
        closest_match = process.extractOne(key.lower(), country_labels)

        if closest_match and closest_match[1] > self.fuzzy_threshold:
            return self._search_index[closest_match[0]]

        raise KeyError(f"Country '{key}' not found.")

    def search(self, key: str) -> List[Country]:
        """Search for countries by name (case insensitive, with fuzzy search)."""
        key_lower = key.lower()
        results = process.extract(
            key_lower,
            list(self._search_index.keys()),
            scorer=fuzz.partial_ratio,
            score_cutoff=self.fuzzy_threshold,
        )

        return list(
            set(
                map(
                    lambda c: self._search_index[c[0]],
                    results,
                )
            )
        )

    def get(self, key: str) -> Union[Country, None]:
        if isinstance(key, int):
            key = str(key)

        key_upper = key.upper()
        key_lower = key.lower()

        if key_upper in self._index:
            return self._index[key_upper]
        if key_lower in self._index:
            return self._index[key_lower]

        return None
