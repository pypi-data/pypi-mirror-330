"""QuoteSet"""

from collections import Counter
from statistics import mean
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Union,
)

from .quote import Quote
from sentinelpricing.utils.calculations import percentage, dict_difference


class QuoteSet:
    """
    A collection of Quote objects.

    A QuoteSet is generated after running either a TestSuite or TestCase
    through a Framework. It supports aggregation, statistical operations, and
    grouping of quotes.
    """

    def __init__(
        self, quotes: Iterable["Quote"], framework: Optional[Any] = None
    ) -> None:
        """
        Initialize a QuoteSet instance.

        Args:
            quotes (Iterable[Quote]): An iterable of Quote objects.
            framework: Optional framework associated with these quotes.
        """
        self.quotes: List["Quote"] = list(quotes)
        self.unique_id_check()

    def __iter__(self) -> Iterator["Quote"]:
        """
        Return an iterator over the Quote objects in the list.

        Returns:
            Iterator[Quote]: An iterator over the quotes.
        """
        return iter(self.quotes)

    def __getitem__(self, index) -> Quote:
        """
        Get item from the Quote objects in the quotes list.

        Returns:
            Quote: An instance of a Quote.
        """
        return self.quotes[index]

    def __len__(self) -> int:
        """
        Return the number of Quote objects in the set.

        Returns:
            int: The count of quotes.
        """
        return len(self.quotes)

    def __add__(self, other: "QuoteSet") -> "QuoteSet":
        """
        Combine two QuoteSets.

        Args:
            other (QuoteSet): Another QuoteSet to add.

        Returns:
            QuoteSet: A new QuoteSet containing quotes from both sets.
        """
        return QuoteSet(self.quotes + other.quotes)

    def __sub__(self, other: "QuoteSet") -> "QuoteSet":
        """
        Subtract One QuoteSet From the Other QuoteSet.

        Args:
            other (QuoteSet): Another QuoteSet to subtract.

        Returns:
            QuoteSet: A new QuoteSet containing quotes from both sets.
        """

        other_identifiers = {q.identifier for q in other.quotes}

        return QuoteSet(
            list(
                filter(
                    lambda q: q.identifier in other_identifiers, self.quotes
                )
            )
        )

    def __contains__(self, other):
        if isinstance(other, Quote):
            # Should this be comparing quotedata or identifier?
            return any(other.quotedata == q.quotedata for q in self)
        if isinstance(other, dict):
            return any(other == q.quotedata for q in self)

    def _groupby(
        self,
        quotes: Union[None, List[Quote]] = None,
        by: Optional[Union[Any, Iterable[Any]]] = None,
    ) -> Dict[Any, List["Quote"]]:
        """
        Group quotes by a specified key or set of keys.

        Args:
            by (Any or Iterable[Any], optional): The key(s) used for grouping.
                If an iterable is provided (and not a string/bytes), the keys
                are combined into a tuple.

        Returns:
            Dict[Any, List[Quote]]: A mapping from group key to list of Quote
                objects.
        """
        _by: Any = (
            tuple(by)
            if isinstance(by, Iterable) and not isinstance(by, (str, bytes))
            else by
        )
        groups: Dict[Any, List["Quote"]] = {}
        iterable = quotes or self.quotes
        for q in iterable:
            key: Any = q[_by]
            groups.setdefault(key, []).append(q)
        return groups

    def _statistic_function(
        self,
        func: Callable[[Iterable[Any]], Any],
        by: Optional[Union[Any, Iterable[Any]]] = None,
        on: Optional[str] = None,
        where: Optional[Callable[["Quote"], bool]] = None,
        sort_keys: bool = True,
    ) -> Union[Dict[Any, Any], Any]:
        """
        Apply an aggregation function to the quotes or to groups of quotes.

        Args:
             func (Callable): A function that aggregates a list of numeric
                values (e.g., mean, max).
             by (Any or Iterable[Any], optional): Key(s) to group quotes before
                applying the function.
            on (str, optional): The attribute name to extract from each Quote
                (defaults to "final_price").
            slice_filter (Callable, optional): A function to filter quotes
                before aggregation.
             sort_keys (bool): Whether to sort the grouping keys in the result.

        Returns:
            Union[Dict[Any, Any], Any]:
                If no grouping is specified, returns the aggregated value for
                    all quotes.
                If grouping is specified, returns a dictionary mapping group
                    keys to aggregated values.
        """
        attribute: str = on or "final_price"

        filtered_quotes = (
            list(filter(where, self.quotes)) if where else self.quotes
        )

        if by is None:
            values = [getattr(q, attribute) for q in filtered_quotes]
            return func(values)

        grouped_data = self._groupby(quotes=filtered_quotes, by=by)
        prelim: Dict[Any, List[Any]] = {
            key: [getattr(q, attribute) for q in quotes]
            for key, quotes in grouped_data.items()
        }

        if sort_keys:
            prelim = {key: prelim[key] for key in sorted(prelim.keys())}

        return {key: func(values) for key, values in prelim.items()}

    def avg(self, *args, **kwargs) -> Union[Dict[Any, float], float]:
        """
        Compute the average of a specified attribute across quotes.

        Args:
            by (Any or Iterable[Any], optional): Key(s) to group quotes before
                averaging.
            on (str, optional): The attribute to average (defaults to
                "final_price").

        Returns:
            Union[Dict[Any, float], float]:
                - A single average value if no grouping is specified.
                - A dictionary mapping group keys to their average values if
                    grouping is used.
        """
        return self._statistic_function(mean, *args, **kwargs)

    def max(self, *args, **kwargs) -> Union[Dict[Any, float], float]:
        """
        Compute the maximum of a specified attribute across quotes.

        Args:
            by (Any or Iterable[Any], optional): Key(s) to group quotes before
                finding the maximum.
            on (str, optional): The attribute to consider (defaults to
                 "final_price").

        Returns:
            Union[Dict[Any, float], float]:
                - A single maximum value if no grouping is specified.
                - A dictionary mapping group keys to their maximum values if
                    grouping is used.
        """
        return self._statistic_function(max, *args, **kwargs)

    def min(self, *args, **kwargs) -> Union[Dict[Any, float], float]:
        """
        Compute the minimum of a specified attribute across quotes.

        Args:
            by (Any or Iterable[Any], optional): Key(s) to group quotes before
                finding the minimum.
            on (str, optional): The attribute to consider (defaults to
                "final_price").

        Returns:
            Union[Dict[Any, float], float]:
                - A single minimum value if no grouping is specified.
                - A dictionary mapping group keys to their minimum values if
                    grouping is used.
        """
        return self._statistic_function(min, *args, **kwargs)

    def sum(self, *args, **kwargs) -> Union[Dict[Any, float], float]:
        """
        Compute the sum of a specified attribute across quotes.

        Args:
            by (Any or Iterable[Any], optional): Key(s) to group quotes before
                summing.
            on (str, optional): The attribute to sum (defaults to
                "final_price").

        Returns:
            Union[Dict[Any, float], float]:
                - A single sum if no grouping is specified.
                - A dictionary mapping group keys to their sums if grouping is
                    used.
        """
        return self._statistic_function(sum, *args, **kwargs)

    def apply(
        self,
        func: Callable[[Iterable[Any]], Any],
        *args: Any,
        **kwargs: Any,
    ) -> Union[Dict[Any, Any], Any]:
        """
        Apply a custom aggregation function to the quotes.

        Args:
            func (Callable): A function that aggregates a list of values.
            *args: Additional positional arguments for the function.
            by (Any or Iterable[Any], optional): Key(s) to group quotes before
                applying the function.
            on (str, optional): The attribute on which to apply the function
                (defaults to "final_price").
            **kwargs: Additional keyword arguments for the function.

        Returns:
            Union[Dict[Any, Any], Any]:
                - The aggregated value if no grouping is specified.
                - A dictionary mapping group keys to their aggregated values if
                    grouping is used.
        """
        return self._statistic_function(func, *args, **kwargs)

    def mix(
        self,
        by: Optional[Union[Any, Iterable[Any]]] = None,
        percent: bool = False,
        **kwargs: Any,
    ) -> Dict[Any, Union[int, float]]:
        """
        Get a mapping of factors present in the quotes along with their
        frequency.

        Args:
            by (Any or Iterable[Any], optional): Key(s) to group quotes.
            percent (bool): If True, returns the percentage representation of
                 each group.
            **kwargs: Additional keyword arguments to pass to the percentage
                function.

        Returns:
            Dict[Any, Union[int, float]]: A dictionary mapping each group key
                to its count or percentage.
        """
        grouped = self._groupby(by=by)
        if percent:
            return {
                k: percentage(len(v), len(self), **kwargs)
                for k, v in grouped.items()
            }
        return {k: len(v) for k, v in grouped.items()}

    def difference_in_mix(
        self,
        other: "QuoteSet",
        by: Optional[Union[Any, Iterable[Any]]] = None,
        percent: bool = False,
    ) -> Dict[Any, float]:
        """
        Calculate the difference in mix between this QuoteSet and another.

        Args:
            other (QuoteSet): Another QuoteSet to compare.
            by (Any or Iterable[Any], optional): Key(s) to group quotes before
                comparing.
            percent (bool): If True, computes differences in percentage terms.

        Returns:
            Dict[Any, float]: A dictionary mapping group keys to the difference
                in mix.

        Raises:
            NotImplementedError: If `other` is not a QuoteSet.
        """
        if not isinstance(other, QuoteSet):
            raise NotImplementedError(
                "Difference only implemented for QuoteSet"
            )
        return dict_difference(
            self.mix(by=by, percent=percent), other.mix(by=by, percent=percent)
        )

    def difference(
        self,
        other: "QuoteSet",
        func: Callable[[Iterable[Any]], Any],
        by: Optional[Union[Any, Iterable[Any]]] = None,
    ) -> Dict[Any, Any]:
        """
        Calculate the difference between aggregated values of this QuoteSet and
            another.

        Args:
            other (QuoteSet): Another QuoteSet to compare.
            func (Callable): An aggregation function to apply.
            by (Any or Iterable[Any], optional): Key(s) to group quotes before
                applying the function.

        Returns:
            Dict[Any, Any]: A dictionary mapping group keys to the difference
                in aggregated values.

        Raises:
            NotImplementedError: If `other` is not a QuoteSet.
        """
        if not isinstance(other, QuoteSet):
            raise NotImplementedError(
                "Difference only implemented for QuoteSet"
            )
        return dict_difference(
            self.apply(func, by=by), other.apply(func, by=by)
        )

    def factors(self, keys: Optional[Iterable[str]] = None) -> Dict[str, set]:
        """
        Retrieve unique sets of factors present in the quote data.

        Args:
            keys (Iterable[str], optional): Specific factor keys to include.
                If not provided, all keys from each quote's data are
                considered.

        Returns:
            Dict[str, set]: A dictionary mapping each factor to a set of its
                unique values.
        """
        factor_dict: Dict[str, set] = {}
        for quote in self:
            for key, value in quote.quotedata.items():
                if keys is not None and key not in keys:
                    continue
                factor_dict.setdefault(key, set()).add(value)
        return factor_dict

    def subset(
        self, by: Union[Callable[["Quote"], bool], Dict[Any, Any]]
    ) -> "QuoteSet":
        """
        Retrieve a subset of quotes based on filtering criteria.

        Args:
            by (Callable or Dict): If callable, it is used to filter quotes via
                filter(). If a dict is provided (deprecated), its keys refer to
                factors in the quote and its values specify the desired
                selection.

        Returns:
            QuoteSet: A new QuoteSet containing quotes that match the filtering
                criteria.

        Raises:
            NotImplementedError: If dict-based filtering is attempted.
        """
        if callable(by):
            return QuoteSet(filter(by, self))
        raise NotImplementedError(
            "Dict-based filtering is deprecated. Use a function instead."
        )

    def unique_id_check(self) -> None:
        """
        Check for duplicate quote identifiers and warn if duplicates exist.

        Prints a warning message if any Quote in the set has a non-unique
            identifier.
        """
        ids = [q.identifier for q in self]
        id_counts = Counter(ids)
        if any(count > 1 for count in id_counts.values()):
            print("Warning, non-unique IDs")
