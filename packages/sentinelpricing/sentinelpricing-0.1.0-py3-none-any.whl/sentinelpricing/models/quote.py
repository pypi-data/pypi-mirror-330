"""Quote"""

import uuid
from operator import add, sub, mul, truediv
from typing import Any, Mapping, Optional, Union, Callable, Hashable, Type

from .breakdown import Breakdown
from .rate import Rate
from .step import Step
from .note import Note
from .testcase import TestCase

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .framework import Framework


class Quote:
    """
    Represents a quote containing test case data and a detailed calculation
    breakdown.

    This object encapsulates the input data used for calculating a quote,
    along with a breakdown of the calculation steps taken to achieve the
    final price for the quote. It supports arithmetic operations that update
    the breakdown and allows retrieval of test case or pricing data via
    subscript notation.

    Attributes:
        identifier (uuid.UUID): Unique identifier for the quote.
        framework: Optional framework instance associated with the quote.
        quotedata (Mapping[str, Any]): Test case data used for quote
            calculation.
        breakdown (Breakdown): A breakdown of calculation steps leading to the
            final price.
    """

    def __init__(
        self,
        testcase: Union[Mapping, "TestCase"],
        framework: Optional[Type["Framework"]] = None,
        final_price: Optional[float] = None,
        identifier: Optional[Any] = None,
    ) -> None:
        """
        Initialize a new Quote instance.

        Args:
            testcase (Mapping or TestCase): The test case data or a TestCase
                instance. If a TestCase is provided, its `quotedata` attribute
                will be used.
            framework (Optional[Framework]): instance associated with this
                quote.
            final_price (Optional[float]): A pre-calculated final price. If
                provided, the breakdown will start with this value.
            identifier (Optional[Any]): An optional unique identifier for the
                quote. If not provided, a new UUID will be generated.
        """
        self.identifier = identifier or uuid.uuid4()
        self.framework = framework

        if isinstance(testcase, TestCase):
            self.quotedata = testcase.data
        elif isinstance(testcase, dict):
            self.quotedata = testcase
        else:
            raise TypeError(
                "testcase must be a Mapping or a TestCase instance."
            )

        self.breakdown = (
            Breakdown(final_price) if final_price is not None else Breakdown()
        )

    def __repr__(self) -> str:
        """
        Return a string representation of the Quote, including its identifier
        and breakdown.

        Returns:
            str: A string representation of the quote.
        """
        return f"{self.__class__.__name__}-{self.identifier}"

    def __getitem__(self, key: Hashable) -> Any:
        """
        Retrieve a value from the quote's data.

        Args:
            key (hashable): The key to look up.

        Returns:
            Any: The value associated with the key.
        """
        if key in self.quotedata:
            return self.quotedata[key]
        raise KeyError(f"Key '{key}' not found in quote data.")

    def __add__(self, other: Any) -> "Quote":
        """
        Add a value or merge with another Quote.

        If the other operand is a Quote, this operation is interpreted as a
        merge (currently a no-op, returning self). Otherwise, it applies an
        addition operation to the current final price in the breakdown.

        Args:
            other (Any): The value or Quote to add.

        Returns:
            Quote: The modified Quote instance.
        """
        if isinstance(other, Quote):
            # Optionally implement merging logic.
            return self
        return self._operation(other, add)

    def __radd__(self, other: Any) -> "Quote":
        """
        Reflective addition for Quote.

        Args:
            other (Any): The value to add.

        Returns:
            Quote: The modified Quote instance.
        """
        if isinstance(other, Quote):
            return self
        return self._operation(other, add)

    def __sub__(self, other: Any) -> "Quote":
        """
        Subtract a value from the quote's final price.

        Args:
            other (Any): The value to subtract.

        Returns:
            Quote: The modified Quote instance.
        """
        return self._operation(other, sub)

    def __rsub__(self, other: Any) -> "Quote":
        """
        Reflective subtraction for Quote.

        Args:
            other (Any): The value from which the quote's final price is
                subtracted.

        Returns:
            Quote: The modified Quote instance.
        """
        return self._operation(other, sub)

    def __mul__(self, other: Any) -> "Quote":
        """
        Multiply the quote's final price by a value.

        Args:
            other (Any): The value to multiply by.

        Returns:
            Quote: The modified Quote instance.
        """
        return self._operation(other, mul)

    def __rmul__(self, other: Any) -> "Quote":
        """
        Reflective multiplication for Quote.

        Args:
            other (Any): The value to multiply by.

        Returns:
            Quote: The modified Quote instance.
        """
        return self._operation(other, mul)

    def __truediv__(self, other: Any) -> "Quote":
        """
        Divide the quote's final price by a value.

        Args:
            other (Any): The divisor.

        Returns:
            Quote: The modified Quote instance.
        """
        return self._operation(other, truediv)

    def __rtruediv__(self, other: Any) -> "Quote":
        """
        Reflective division for Quote.

        Args:
            other (Any): The dividend.

        Returns:
            Quote: The modified Quote instance.
        """
        return self._operation(other, truediv)

    def __eq__(self, other: Any) -> bool:
        """
        Compare the Quote with another Quote or a numeric value.

        If comparing with another Quote, the quotedata is compared.
        If comparing with an int or float, the final price is compared.

        Args:
            other (Any): The object to compare against.

        Returns:
            bool: True if the quotes are considered equal; otherwise, False.

        Raises:
            NotImplementedError: If comparison with the given type is not
                supported.
        """
        if isinstance(other, Quote):
            return self.breakdown.final_price == other.breakdown.final_price
        if isinstance(other, (int, float)):
            return self.breakdown.final_price == other
        return NotImplemented

    def __lt__(self, other: Any) -> bool:
        """
        Compare the Quote with another Quote or a numeric value.

        If comparing with another Quote, the final price of each is compared.
        If comparing with an int or float, the final price and int or float are
            compared.

        Args:
            other (Any): The object to compare against.

        Returns:
            bool: True if the quote is less than other; otherwise, False.

        Raises:
            NotImplementedError: If comparison with the given type is not
                supported.
        """
        if isinstance(other, Quote):
            return self.breakdown.final_price < other.breakdown.final_price
        if isinstance(other, (int, float)):
            return self.breakdown.final_price < other
        raise NotImplementedError(
            "Less Than Comparison is only supported for Quote, int or floats."
        )

    def __gt__(self, other: Any) -> bool:
        """
        Compare the Quote with another Quote or a numeric value.

        If comparing with another Quote, the final price of each is compared.
        If comparing with an int or float, the final price and int or float are
            compared.

        Args:
            other (Any): The object to compare against.

        Returns:
            bool: True if the quote is greater than other; otherwise, False.

        Raises:
            NotImplementedError: If comparison with the given type is not
                supported.
        """
        return not self < other and not self == other

    def __le__(self, other) -> bool:
        """
        Compare the Quote with another Quote or a numeric value.

        If comparing with another Quote, the final price of each is compared.
        If comparing with an int or float, the final price and int or float are
            compared.

        Args:
            other (Any): The object to compare against.

        Returns:
            bool: True if the quote is less than or equal to other; otherwise,
                False.

        Raises:
            NotImplementedError: If comparison with the given type is not
                supported.
        """
        return self < other or self == other

    def __ge__(self, other):
        """
        Compare the Quote with another Quote or a numeric value.

        If comparing with another Quote, the final price of each is compared.
        If comparing with an int or float, the final price and int or float are
            compared.

        Args:
            other (Any): The object to compare against.

        Returns:
            bool: True if the quote is greater than or equal to other;
                otherwise, False.

        Raises:
            NotImplementedError: If comparison with the given type is not
                supported.
        """
        return not self <= other

    def __contains__(self, key):
        return key in self.quotedata

    def _operation(
        self, other: Any, oper: Callable[[Any, Any], Any]
    ) -> "Quote":
        """
        Apply an arithmetic operation to the quote's final price.

        This internal helper performs an operation (such as addition,
        subtraction, multiplication, or division) using the current final price
        and the provided value. It then records the operation as a Step in the
        breakdown.

        Args:
            other (Any): The value or Rate instance to operate with.
            oper (Callable[[Any, Any], Any]): The operator function
                (e.g., add, sub).

        Returns:
            Quote: The modified Quote instance.
        """
        if isinstance(other, Rate):
            name = other.name
            other_value = other.value
        else:
            name = "CONST"
            other_value = other

        result = oper(self.breakdown.final_price, other_value)
        step = Step(name, oper, other_value, result)
        self.breakdown.append(step)
        return self

    def note(self, text: str) -> None:
        """
        Append a note to the quote's breakdown.

        Args:
            text (str): The note text to be recorded.
        """
        self.breakdown.append(Note(text))

    def get(self, *args, **kwargs):
        return self.quotedata.get(*args, **kwargs)

    @property
    def calculated(self) -> bool:
        """
        Check if the quote has been calculated.

        Returns:
            bool: True if a final price is available; otherwise, False.
        """
        return bool(self.breakdown.final_price)

    @property
    def final_price(self) -> float:
        """
        Retrieve the final calculated price from the quote.

        Returns:
            float: The final price as determined by the breakdown.
        """
        return self.breakdown.final_price

    def summary(self):
        """Outputs Quote Breakdown.

        Returns the quote breakdown as a string.

        Returns:
            str: Quote Breakdown.
        """
        return repr(self) + "\n" + repr(self.breakdown)
