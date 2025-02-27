"""Yet-Another CRC Calculator.

This module provides methods and classes for CRC calculation on various
types of data (`bytes`, `bytearray`, `List[int]`, and `str`). The CRC
calculator is not limited by the data width and supports changing any
CRC model parameter. For more information on CRC model parameters and
how are they used, refer to Ross Williams's "A Painless Guide to CRC
Error Detection Algorithms":

    http://www.ross.net/crc/download/crc_v3.txt

The CRC value can be calculated in three ways:
1) By directly following the mathematical definition, i.e., via the
polynomial division in CRC arithmetic. This also outputs a formatted
string representation of CRC calculation steps.
2) By using a non-optimized CRC calculation algorithm, i.e., the data
buffer is processed bit-by-bit.
3) By using an optimized CRC calculation algorithm that employs a CRC
lookup table to speed up CRC calculations. However, this is limited to
data widths that do not exceed `CRC._MAX_OPT` (`16`) bits.

Classes:
- `CRC`: Bases class for CRC calculation.
- `CRC3`, ..., `CRC82`: Catalog classes for different CRC widths.

The CRC model catalog is based on Greg Cook's "Catalogue of Parametrised
CRC Algorithms":

    https://reveng.sourceforge.io/crc-catalogue/

The following classes contain more than 100 predefined CRC models:
```
======================================================
              CRC3   CRC4   CRC5   CRC6   CRC7   CRC8
       CRC10  CRC11  CRC12  CRC13  CRC14  CRC15  CRC16
CRC17                       CRC21                CRC24
                                   CRC30  CRC31  CRC32
                                                 CRC40
                                                 CRC64
       CRC82
======================================================
```

Usage example:
```python-repl
>>> from yacrc import CRC16
>>> buffer = b'123456789'
>>> obj = CRC16.MODBUS
>>> hex(obj.crc(buffer))
'0x4b37'
>>> obj = CRC16.MODBUS(init=0)
CRC-16/ARC has the same set of parameters
>>> hex(obj.crc(buffer))
'0xbb3d'
```
"""

from dataclasses import dataclass, field, asdict
from typing import ClassVar, Callable, Optional, Union, Tuple, List, Dict

# ==================================================================== #
# SECTION: Utility Methods                                             #
# ==================================================================== #

# The union operator "|" and "TypeAlias" were introduced in Python 3.10.
BufferTypeInt = Union[bytes, bytearray, List[int]]
"""Type alias for integer buffer inputs.

Note:
    - When the data width exceeds 8 bits, the buffer type can no longer
    be `bytes` or `bytearray`.
    - `bytes` is an immutable sequence of bytes.
    - `bytearray` is a mutable sequence of bytes.
"""

BufferType = Union[BufferTypeInt, str]
"""Type alias for buffer inputs used in CRC calculations.

Note:
    - When buffer is a string (`str`), all its characters must be either
    `'0'` or `'1'`, i.e., buffer is a binary string.
    - When the data width exceeds 8 bits, the buffer type can no longer
    be `bytes` or `bytearray`.
    - `bytes` is an immutable sequence of bytes.
    - `bytearray` is a mutable sequence of bytes.
"""


def reflect(data: int, n: int = 8) -> int:
    """Reflects the lower `n` bits of a given data value.

    Example:
    ```
    DATA        n    REFLECTED
    ===========================
    0b11101011  8    0b11010111
    0b11101011  4    0b00001101  # Higher bits are masked out
    ```
    Lower `n` bits are reflected, while other bits are masked out.

    Args:
        `data`: Data value to reflect.
        `n`: Number of lower bits to reflect. Defaults to `8`.

    Returns:
        `int`: Reflected data value.
    """
    return sum([(1 << (n - k - 1)) for k in range(n) if (data & (1 << k))])


# ==================================================================== #
# SECTION: CRC Algorithm Implementation                                #
# ==================================================================== #

@dataclass(frozen=True)
class CRC:
    """Customizable CRC calculator.

    Attributes:
        `width`: CRC width (number of bits).
        `poly`: CRC poly, i.e., polynomial without implied leading '1'.
        `init`: CRC shift register initial value. Defaults to `0`.
        `refin`: Input data reflection. Defaults to `False`.
        `refout`: CRC value reflection. Defaults to `False`.
        `xorout`: Operand for the final XOR. Defaults to `0`.
        `check`: CRC value for `b'123456789'`. Defaults to `None`.
        `residue`: Residue value. Defaults to `None`.
        `name`: CRC model name. Defaults to `''`.
        `alias`: CRC model alias(es). Defaults to `''`.
        `data`: Data width (number of bits). Defaults to `8`.
        `reverse`: Append CRC in reverse. Defaults to `False`.
        `optimize`: Optimize CRC calculations. Defaults to `None`.

    Methods:
        `parameters() -> Dict[str, Union[str, int, bool]]:`
            Returns a dictionary containing CRC model parameters.
        `crc_steps(buffer: BufferType, appended: bool = False)
        -> Tuple[int, str]:`
            Calculates CRC of a given buffer using polynomial division.
        `crc(buffer: BufferType) -> int:`
            Calculates the CRC value of a given buffer.
        `append(buffer: BufferType) -> BufferType:`
            Calculates and appends the CRC value to the given buffer.
        `separate(buffer: BufferType) -> Tuple[BufferType, int]:`
            Extracts the message and its CRC value from the buffer.
        `verify(buffer: BufferType) -> bool:`
            Verifies the given buffer by calculating its residue.
        `optimization(optimize: bool) -> CRC:`
            Enables or disables CRC calculation optimization.
        `table() -> List[int]:`
            Returns a copy of the CRC lookup table.
        `table_2d(cols: int = 8) -> str:`
            Generates a string representation of the CRC lookup table.

    Class methods:
        `catalog() -> List[CRC]:`
            Returns a list of all CRC models in the built-in catalog.
    """

    # --- PUBLIC ATTRIBUTES ---

    width: int                       # CRC width (number of bits)
    poly: int                        # CRC poly
    init: int = 0                    # CRC shift register initial value
    refin: bool = False              # Input byte reflection
    refout: bool = False             # CRC value reflection
    xorout: int = 0                  # Operand for the final XOR
    check: Optional[int] = None      # CRC value for b'123456789'
    residue: Optional[int] = None    # Residue value
    name: str = ''                   # Name for the CRC model
    alias: str = ''                  # Alias(es) for the CRC model
    data: int = 8                    # Data width (number of bits)
    reverse: bool = False            # Append CRC in reverse order
    optimize: Optional[bool] = None  # Optimize CRC calculations

    @dataclass(frozen=True)
    class _CRCPrivate:
        n_crc: int          # Number of buffer elements for CRC value
        width: int          # CRC width rounded up to the data width
        poly: int           # Modified poly for CRC calculations
        init: int           # Modified init for CRC calculations
        msb: int            # Mask to get most-significant bit from CRC
        m_crc: int          # Mask to limit CRC width
        m_data: int         # Mask to limit data width
        diff: int           # Rounded minus actual CRC width
        dist: int           # Distance between CRC and data MSBs
        catalog: bool       # True when the CRC model is in the catalog
        parent: 'CRC'       # Parent CRC model object
        log: List[str]      # Storage for calc. steps from poly_div()
        table: List[int]    # CRC lookup table for opt. CRC calculations
        crc: Optional[Callable[[BufferTypeInt, int], int]]

    # --- PRIVATE ATTRIBUTES ---

    # Private parameters used for CRC calculations
    _p: Optional[_CRCPrivate] = field(default=None, init=False)

    # Catalog of parametrized CRC models
    _catalog: ClassVar[List['CRC']] = []
    _populate: ClassVar[bool] = True

    # Parent object
    _parent: ClassVar['CRC'] = None

    # Maximum data width to allow CRC calculation optimization which is
    # based on a CRC lookup table with 2**data elements. For example,
    # for data width of 16 bits, there will be 2**16=65536 elements in
    # the CRC lookup table.
    _MAX_OPT: ClassVar[int] = 16

    def __post_init__(self):
        """Post-initialization method for the `CRC` class.

        This method pre-calculates all variables needed for the CRC
        calculation, which depend only on CRC model parameters. It
        also performs validation checks on the CRC model parameters.
        It ensures that:
        - The `width` and `data` CRC model parameters are positive.
        - The `poly`, `init`, `xorout`, `check`, and `residue` CRC model
        parameters are within the valid range `[0, 2**width - 1]`.

        Raises:
            `ValueError`: If any CRC model parameter is invalid.
        """

        # If an exception is raised, this makes sure the CRC._parent is
        # reset to None for future CRC objects.
        parent = CRC._parent
        CRC._parent = None

        if self.width <= 0:
            raise ValueError(f'CRC width ({self.width}) must be positive')

        if self.data <= 0:
            raise ValueError(f'Data width ({self.data}) must be positive')

        for attr in ['poly', 'init', 'xorout', 'check', 'residue']:
            self._check_width(attr, getattr(self, attr))

        if not self.name:
            object.__setattr__(self, 'name', f'CRC-{self.width}/')

        # Number of buffer elements to store the CRC value
        n_crc = -(self.width // -self.data)  # ceil

        # This allows CRC widths that are smaller than the data width.
        # CRC is calculated to the width that matches the data width.
        # Once the calculation is done, CRC is realigned to its width.
        width = max(self.width, self.data)

        m_crc = (1 << width) - 1
        m_data = (1 << self.data) - 1
        diff = width - self.width
        dist = width - self.data

        if not self.refin:
            msb = 1 << (width - 1)

            poly = self.poly << diff
            init = self.init << diff

            # Adding "implied" leading bit '1' to the poly will cancel
            # the MSB that "pops out" of the CRC shift register after a
            # left shif by 1. In that way, the CRC will always be within
            # the polynomial width.
            poly |= (msb << 1)

        else:  # self.refin == True
            msb = 0x1

            poly = reflect(self.poly, self.width)
            init = reflect(self.init, self.width)

            # No need to add "implied" leading 1 to poly because MSB is
            # discarded after a right shift by 1. This is not the case
            # with a left shift!

        p = CRC._CRCPrivate(
            n_crc, width, poly, init, msb, m_crc, m_data, diff, dist,
            CRC._populate, parent, [], [], None
        )

        # Parameters must be initialized before the _crc_table() method
        # is called since CRC calculation methods need them to calculate
        # CRC values.
        object.__setattr__(self, '_p', p)

        # The walrus operator ":=" was introduced in Python 3.8
        optimize = self.optimize
        if optimize is None:
            # CRC table is generated by default even for the CRC models
            # from the catalog since they have data = 8.
            optimize = self.data <= 8
            # TODO Consider making a change to speed up the init.
            # optimize = not CRC._populate and self.data <= CRC._MAX_OPT

        self.optimization(optimize)

        if CRC._populate:
            CRC._catalog.append(self)
        else:  # not CRC._populate
            # No need to do validation of the check and residue CRC
            # model parameters for models from the catalog. We will
            # do this in unit tests!
            self._validate()

            for model in CRC._catalog:
                if (model is not parent) and self._equal(model.parameters):
                    print(f'{model} has the same set of parameters')

    @classmethod
    def catalog(cls) -> List['CRC']:
        """Returns a list of all CRC models in the built-in catalog.

        The catalog is built from Greg Cook's "Catalogue of Parametrised
        CRC Algorithms" and includes a comprehensive collection of CRC
        models with their parameters.

        Source:
            https://reveng.sourceforge.io/crc-catalogue/

        Returns:
            `List[CRC]`: List of all CRC models in the built-in catalog.
        """
        return CRC._catalog.copy()

    def _check_width(self, name: str, value: int) -> None:
        """Validates that the given CRC model parameter is within the
        valid range.

        Args:
            `name`: Name of the CRC model parameter being checked.
            `value`: Value of the CRC model parameter being checked.

        Raises:
            `ValueError`: If the CRC model parameter value is not within
            the valid range `[0, 2**width - 1]`.
        """

        if name in ['check', 'residue'] and value is None:
            pass  # check and residue parameters are optional
        elif value < 0:
            raise ValueError(f'\'{name}={value}\' must be positive')
        elif value >= 2**self.width:
            raise ValueError(f'{name}=0x{value:X} >= 2^{self.width}')

    def _check_buffer(self, buffer: BufferType, appended: bool) -> None:
        """Validates buffer size, type, and all its elements.

        Checks that all buffer elements are valid based on the buffer
        type. It ensures that:
        - For integer buffers (`bytes`, `bytearray`, `List[int]`), all
        elements must be within the valid range `[0, 2**data - 1]`.
        - For string buffers (`str`), all elements (characters) must be
        either `'0'` or `'1'`.
        - If the `data` parameter is greater than `8`, the buffer cannot
        be of `bytes` or `bytearray` type.
        - If `appended` is `True`, the buffer must contain at least 1
        element more than what is required to store the CRC value. In
        addition to this, for integer buffers, if the CRC width is not
        a multiple of the data width, the last buffer element must not
        exceed `width % data` bits.

        Args:
            `buffer`: Input buffer to check.
            `appended`: `True` when the buffer contains the CRC value,
            `False` otherwise.

        Raises:
            `ValueError`: If the `buffer` size is incorrect, or if its
            type is not supported, or if any of its elements is invalid.
        """

        if isinstance(buffer, str):
            size = len(buffer) - (int(appended) * self.width)
            if size <= 0:
                raise ValueError(f'Incorrect buffer size ({len(buffer)})')
            elif size % self.data:
                raise ValueError('Buffer is not aligned to the data width')

            for k, char in enumerate(buffer):
                if not (char == '0' or char == '1'):
                    raise ValueError(
                        f'Buffer element \'buffer[{k}]={char}\' '
                        f'must be either \'0\' or \'1\' character.'
                    )
        elif isinstance(buffer, (bytes, bytearray, list)):
            size = len(buffer) - (int(appended) * self._p.n_crc)
            if size <= 0:
                raise ValueError(f'Incorrect buffer size ({len(buffer)})')

            if isinstance(buffer, (bytes, bytearray)) and (self.data > 8):
                raise ValueError(
                    f'{type(buffer)} buffers cannot '
                    f'contain {self.data}-bit elements'
                )
            for k, byte in enumerate(buffer):
                if not (isinstance(byte, int) and (0 <= byte < 2**self.data)):
                    raise ValueError(
                        f'Buffer element \'buffer[{k}]={byte}\' '
                        f'must be in range [0, {2**self.data - 1}]'
                    )

            last = self.width % self.data
            if appended and last:
                if buffer[-1] >> last:
                    raise ValueError(
                        f'\'buffer[-1]={buffer[-1]}\' '
                        f'width exceeds {last} bits'
                    )
        else:  # not isinstance(buffer, (str, bytes, bytearray, str))
            raise ValueError(f'Unsupported buffer type: {type(buffer)}')

    @property
    def parameters(self) -> Dict[str, Union[str, int, bool]]:
        """Returns a dictionary containing CRC model parameters.

        Returns:
            `Dict[str, Union[str, int, bool]]`: A dictionary containing
            CRC model parameters.
        """
        # Leave out instance attributes that start with a sunder because
        # these are considered to be private!
        return {
            key: value for key, value in asdict(self).items()
            if not key.startswith('_')
        }

    def __str__(self) -> str:
        """Returns a string representation of the CRC model.

        Returns:
            `str`: Name of the CRC model.
        """
        return self.name

    def __repr__(self) -> str:
        """Returns a string representation of the CRC model.

        Returns:
            `str`: Name of the CRC model.
        """
        return self.name

    def _equal(self, parameters: Dict[str, Union[str, int, bool]]) -> bool:
        """Checks if the CRC instance matches the given parameters.

        Compares the current CRC instance's parameters with the provided
        parameters to determine if they are equal. Parameters compared
        are: `width`, `poly`, `init`, `refin`, `refout`, and `xorout`.

        Args:
            `parameters`: A dictionary containing CRC model parameters
            to compare against.

        Returns:
            `bool`: `True` if the CRC instance's parameters match the
            provided parameters, `False` otherwise.
        """

        return all(
            getattr(self, p) == parameters[p]
            for p in ['width', 'poly', 'init', 'refin', 'refout', 'xorout']
        )

    def __eq__(self, other) -> bool:
        """Compares two CRC models.

        Returns:
            `bool`: True if the two CRC models would output the same CRC
            value for the same buffer.

        Raises:
            `NotImplementedError`: If the `other` is not `CRC` instance.
        """
        if isinstance(other, CRC):
            return self._equal(other.parameters) and (self.data == other.data)
        raise NotImplementedError

    def __call__(self, **kwargs) -> 'CRC':
        """Creates new `CRC` instance with optional parameter overrides.

        This method allows creating the new CRC instance by overriding
        specific CRC model parameters, whereas only the original `width`
        parameter cannot be changed.

        If the `check` and `residue` parameters are not provided for the
        new set of parameters, the instance initialization routine will
        recalculate the matching values. If the `name` is not provided,
        it is formed by adding a trailing `'*'` to the existing name.

        Args:
            `**kwargs`: Optional keyword arguments to override specific
            CRC model parameters.

        Returns:
            `CRC`: New CRC instance.

        Raises:
            `ValueError`: If an unknown parameter is provided, or if an
            attempt is made to change the CRC width.
        """

        parameters = self.parameters

        if ('data' in kwargs) and (kwargs['data'] != 8):
            parameters['check'] = None

        # Let CRC constructor to decide on CRC calculation optimization
        if 'optimize' not in kwargs:
            parameters['optimize'] = None

        if self._p.parent is None:
            # This will be the case for all CRC models from the catalog
            # and for CRC models created directly via the constructor.
            CRC._parent = self
        else:
            CRC._parent = self._p.parent

        if not kwargs:
            return CRC(**parameters)

        if 'width' in kwargs:
            raise ValueError(f'Cannot change default CRC width: {self}')

        for key, value in kwargs.items():
            if key not in parameters:
                raise ValueError(f'Unknown CRC model parameter: {key}')
            parameters[key] = value

        if not self._equal(parameters):
            # If any of the model defining parameters are changed, the
            # check and residue parameters are no longer valid. In any
            # case, the CRC class constructor will recalculate new check
            # and residue values.
            if 'check' not in kwargs:
                parameters['check'] = None
            if 'residue' not in kwargs:
                parameters['residue'] = None
            if 'name' not in kwargs:
                parameters['name'] += '*'
            if 'alias' not in kwargs:
                parameters['alias'] = ''

        return CRC(**parameters)

    def _log(self, prefix: Union[str, None], step: str) -> None:
        """Logs a step in the CRC calculation process.

        Logs a step in the CRC calculation process, optionally prefixed
        with a given string. When the `prefix` is `None`, the step is
        logged without any prefix. This logging is only used for CRC
        calculations done via polynomial division in CRC arithmetic.

        Args:
            `prefix`: Optional prefix for the log entry. If `None`, the
            calculation step is logged without any prefix.
            `step`: CRC calculation step.
        """

        if prefix is None:
            self._p.log.append(step)
        else:  # prefix is not None
            self._p.log.append(f'{prefix:<10s}{step}')

    def _poly_div(self, message: str) -> int:
        """Calculates CRC of a given message using polynomial division.

        CRC is calculated using polynomial division in CRC arithmetic.
        There are no limits for the message size; it can be as small
        as 1 bit.

        Args:
            `message`: Binary string with MSB at the lowest index.

        Returns:
            `int`: Calculated CRC value.
        """

        # Add implied leading '1' to the poly
        poly = (1 << self.width) | self.poly

        message += ('0' * self.width)
        self._log('AUGMENT', message)

        i_message = int(message, 2)
        x_message = message.replace('0', '.').replace('1', ',')

        n_bit = len(message)

        log = self._p.log
        lw = len(log[0]) - n_bit  # label width

        def _log_operation(label: str, idx: int, operand: int, width: int):
            """Logs a single operation of a CRC polynomial division.

            The operation can be either XOR with the `init` parameter,
            or XOR with the `poly` parameter.

            Args:
                `label`: Operation label. (`'INIT'` or `'POLY'`).
                `idx`: Line starting index.
                `operand`: Operand. (`init` or `poly` parameter).
                `width`: Operand width, i.e., number of bits.
            """

            nonlocal log, i_message, x_message, n_bit, lw

            # Right-align the previous line
            if log[-1][-1] in '.,':
                _idx = lw + idx + width
                left, right = log[-1][:_idx], log[-1][_idx:]
                log[-1] = left.replace('.', '0').replace(',', '1') + right

            i_number = i_message >> (n_bit - width - idx)

            # Placeholder in f-string was introduced in Python 3.12
            # line = f'{'':{idx}s}{{}}{x_message[idx + width:]}'
            line = '{:{}}{}{}'.format('', idx, '{}', x_message[idx + width:])

            self._log(label, line.format(f'{operand:0{width}b}'))
            self._log('',    line.format('-' * width))
            self._log('',    line.format(f'{i_number:0{width}b}'))

        if self.init:
            i_message ^= self.init << (n_bit - self.width)
            _log_operation('INIT', 0, self.init, self.width)

        for k in range(n_bit - self.width):
            if i_message < (2**self.width):
                break
            elif (i_message >> (n_bit - 1 - k)) & 0x1:
                i_message ^= poly << (n_bit - (self.width + 1) - k)
                # poly has leading '1', hence 'width+1'
                _log_operation('POLY', k, poly, self.width + 1)

        if i_message >= (2**self.width):
            raise AssertionError('CRC calculation error')

        # Replace remaining dots and commas in the final line
        log[-1] = log[-1].replace('.', '0').replace(',', '1')

        return i_message

    def crc_steps(
        self,
        buffer: BufferType,
        appended: bool = False
    ) -> Tuple[int, str]:
        """Calculates CRC of a given buffer using polynomial division.

        Args:
            `buffer`: Data buffer over which the CRC will be calculated.
            `appended`: `True` when the buffer contains the CRC value,
            `False` otherwise.

        Returns:
            `int`: Calculated CRC value.
            `str`: String representation of the calculation steps.

        Raises:
            `ValueError`: If any `buffer` element is invalid, or if the
            buffer type is not supported.
        """

        self._check_buffer(buffer, appended)

        if not isinstance(buffer, str):
            last = self.data  # assume the last element has full width
            rem = self.width % self.data
            if appended and rem:
                last = rem
            buffer = ''.join([
                f'{data:0{self.data}b}' if (k < len(buffer) - 1)
                else f'{data:0{last}b}'
                for k, data in enumerate(buffer)
            ])

        self._log(None, '=')
        self._log(None, f'MODEL: {self.name}')
        self._log(None, '=')

        self._log('MESSAGE', buffer)
        self._log(None, '-')

        if self.refin:
            buffer = ''.join([
                buffer[k:k + self.data][::-1]
                for k in range(0, len(buffer), self.data)
            ])
            self._log('REFIN', buffer)

        crc = self._poly_div(buffer)

        total = len(self._p.log[-1])

        indent = ' ' * len(buffer)
        separator = '-' * self.width

        if self.refout:
            crc = reflect(crc, self.width)
            self._log('',       indent + separator)
            self._log('REFOUT', indent + f'{crc:0{self.width}b}')

        if self.xorout:
            crc ^= self.xorout
            self._log('',       indent + separator)
            self._log('XOROUT', indent + f'{crc:0{self.width}b}')

        # Maximum number of hex digits for CRC representation
        nibbles = -(self.width // -4)  # ceil

        self._log(None, '-')
        self._log(None, f'CRC = 0x{crc:0{nibbles}X}')
        self._log(None, '=')

        # Expand separators to the full line width
        for k in [0, 2, 4, -3, -1]:
            self._p.log[k] *= total

        steps = '\n'.join(self._p.log)

        self._p.log.clear()

        return crc, steps

    def _crc_unopt(self, buffer: BufferTypeInt, size: int) -> int:
        """Calculates the CRC value of a given buffer.

        The CRC value is calculated by iterating over each data element
        in the buffer, extracting and processing each bit individually.
        This algorithm is not optimized for calculation speed.

        This method assumes that all buffer elements have a width of
        `data` bits. The `size` parameter makes it possible to exclude
        some data elements from CRC calculation, which is useful when
        the buffer has its CRC value appended at the end and the CRC
        width is not a multiple of the data width.

        Args:
            `buffer`: Data buffer over which the CRC will be calculated.
            `size`: Number of data elements from the buffer to process.

        Returns:
            `int`: Calculated CRC value.
        """

        crc = self._p.init

        for k in range(size):
            crc ^= buffer[k] << self._p.dist
            for _ in range(self.data):
                if crc & self._p.msb:
                    # Implied leading bit '1' added to the poly in the
                    # __post_init__() method cancels the MSB that "pops
                    # out" after the left shift.
                    crc = (crc << 1) ^ self._p.poly
                else:  # msb is 0
                    crc = (crc << 1)

        crc >>= self._p.diff

        return crc

    def _crc_reflected_unopt(self, buffer: BufferTypeInt, size: int) -> int:
        """Calculates the CRC value of a given buffer.

        The CRC value is calculated by iterating over each data element
        in the buffer, extracting and processing each bit individually.
        This algorithm is not optimized for calculation speed.

        This method assumes that all buffer elements have a width of
        `data` bits. The `size` parameter makes it possible to exclude
        some data elements from CRC calculation, which is useful when
        the buffer has its CRC value appended at the end and the CRC
        width is not a multiple of the data width.

        This is reflected variant, i.e., instead of reflecting each data
        element in the `buffer`, the CRC calculation algorithm itself is
        reflected.

        Args:
            `buffer`: Data buffer over which the CRC will be calculated.
            `size`: Number of data elements from the buffer to process.

        Returns:
            `int`: Calculated CRC value.
        """

        crc = self._p.init

        for k in range(size):
            crc ^= buffer[k] >> 0
            for _ in range(self.data):
                if crc & self._p.msb:
                    # The MSB simply disappears after the right shift
                    crc = (crc >> 1) ^ self._p.poly
                else:  # msb is 0
                    crc = (crc >> 1)

        return crc

    def _crc_opt(self, buffer: BufferTypeInt, size: int) -> int:
        """Calculates the CRC value of a given buffer using the
        precomputed CRC lookup table.

        The CRC value is calculated by iterating over each data element
        in the `buffer` and using the precomputed CRC lookup table. This
        avoids iterating over each bit in the data element, making the
        algorithm more efficient than the standard bit-by-bit algorithm.

        This method assumes that all buffer elements have a width of
        `data` bits. The `size` parameter makes it possible to exclude
        some data elements from CRC calculation, which is useful when
        the buffer has its CRC value appended at the end and the CRC
        width is not a multiple of the data width.

        Args:
            `buffer`: Data buffer over which the CRC will be calculated.
            `size`: Number of data elements to process from the buffer.

        Returns:
            `int`: Calculated CRC value.
        """

        crc = self._p.init

        for k in range(size):
            idx = (crc >> self._p.dist) ^ buffer[k]
            crc = (crc << self.data) ^ self._p.table[idx]
            crc &= self._p.m_crc  # Left shift never overflows in Python

        crc >>= self._p.diff

        return crc

    def _crc_reflected_opt(self, buffer: BufferTypeInt, size: int) -> int:
        """Calculates the CRC value of a given buffer using the
        precomputed CRC lookup table.

        The CRC value is calculated by iterating over each data element
        in the `buffer` and using the precomputed CRC lookup table. This
        avoids iterating over each bit in the data element, making the
        algorithm more efficient than the standard bit-by-bit algorithm.

        This method assumes that all buffer elements have a width of
        `data` bits. The `size` parameter makes it possible to exclude
        some data elements from CRC calculation, which is useful when
        the buffer has its CRC value appended at the end and the CRC
        width is not a multiple of the data width.

        This is reflected variant, i.e., instead of reflecting each data
        element in the `buffer`, the CRC calculation algorithm itself is
        reflected.

        Args:
            `buffer`: Data buffer over which the CRC will be calculated.
            `size`: Number of data elements to process from the buffer.

        Returns:
            `int`: Calculated CRC value.
        """

        crc = self._p.init

        for k in range(size):
            idx = (crc ^ buffer[k]) & self._p.m_data
            crc = (crc >> self.data) ^ self._p.table[idx]

        return crc

    def _crc(self, buffer: BufferType, size: int, appended: bool) -> int:
        """Calculates the CRC value of a given buffer.

        Args:
            `buffer`: Data buffer over which the CRC will be calculated.
            `size`: Number of relevant buffer elements.
            `appended`: `True` when the buffer contains the CRC value,
            `False` otherwise.

        Returns:
            `int`: Calculated CRC value.

        Raises:
            `ValueError`: If any `buffer` element is invalid, or if the
            buffer type is not supported.
        """

        self._check_buffer(buffer, appended)

        if isinstance(buffer, str):
            if (size != len(buffer)) and (size % self.data):
                raise AssertionError(
                    'The binary string length is not a '
                    f'multiple of the data width ({size})'
                )
            buffer = [
                int(buffer[k:k + self.data], 2)
                for k in range(0, size, self.data)
            ]

        last = self.width % self.data

        if not (appended and (len(buffer) == size) and last):
            # All buffer elements are aligned to the full data width
            crc = self._p.crc(buffer, size)
        else:  # appended and (len(buffer) == size) and last
            # Calculate the CRC value for all buffer elements except the
            # last, because it is not aligned to the full data width
            crc = self._p.crc(buffer, size - 1)

            # Update the CRC value for the last buffer element which is
            # not aligned to the full data width. The bitwise loops are
            # copied from _crc_unopt() _crc_reflected_unopt() methods.
            if not self.refin:
                dist = self._p.dist + (self.data - last)
                crc <<= self._p.diff
                # --- begin copied loop ---
                crc ^= buffer[-1] << dist  # original: << self._p.dist
                for _ in range(last):  # original: range(self.data)
                    if crc & self._p.msb:
                        crc = (crc << 1) ^ self._p.poly
                    else:  # msb is 0
                        crc = (crc << 1)
                # --- end copied loop ---
                crc >>= self._p.diff
            else:  # self.refin == True
                # --- begin copied loop ---
                crc ^= buffer[-1]
                for _ in range(last):  # original: range(self.data)
                    if crc & self._p.msb:
                        crc = (crc >> 1) ^ self._p.poly
                    else:  # msb is 0
                        crc = (crc >> 1)
                # --- end copied loop ---

        # CRC12.UMTS has "refin = True" and "refin = False". This is the
        # only CRC model from the catalog that has "refin != refout".
        # The reflected CRC algorithm, used when "refin = True", outputs
        # the CRC value as if "refout = True". The CRC value is reversed
        # to match "refout = False".
        if self.refin ^ self.refout:
            crc = reflect(crc, self.width)

        crc ^= self.xorout

        return crc

    def crc(self, buffer: BufferType) -> int:
        """Calculates the CRC value of a given buffer.

        Args:
            `buffer`: Data buffer over which the CRC will be calculated.

        Returns:
            `int`: Calculated CRC value.

        Raises:
            `ValueError`: If any `buffer` element is invalid, or if the
            buffer type is not supported.
        """
        return self._crc(buffer, len(buffer), False)

    def append(self, buffer: BufferType) -> BufferType:
        """Calculates and appends the CRC value to the given buffer.

        When the `buffer` is `str` or `bytes`, the method returns new
        copy of the buffer since these types are immutable. When the
        `buffer` is `bytearray` or `List[int]`, the method appends the
        CRC value to the existing array (list).

        When `refin == False` the CRC value is appended in big endian,
        and vice-versa. The CRC value is aligned to the data width, but
        if the CRC width is not a multiple of the data width, the last
        CRC element appended to the buffer has `width % data` width.
        ```
        CRC         WIDTH  DATA  REFIN  ELEMENTS
        ====================================================
        0b00011001  8      8     False  [0b00011001]
        0b00011001  8      8     True   [0b00011001]
        0b00011001  8      6     False  [0b000110, 0b01]
        0b00011001  8      6     True   [0b011001, 0b00]
        0b00011001  8      4     False  [0b0001, 0b1001]
        0b00011001  8      4     True   [0b1001, 0b0001]
        0b00011001  8      3     False  [0b000, 0b110, 0b01]
        0b00011001  8      3     True   [0b001, 0b011, 0b00]
        ```

        Args:
            `buffer`: Data buffer over which the CRC will be calculated.

        Returns:
            `BufferType`: Buffer with appended CRC value.

        Raises:
            `ValueError`: If any `buffer` element is invalid, or if the
            buffer type is not supported.
        """

        crc = self.crc(buffer)

        # See crc() method for explanation
        if self.refin ^ self.refout:
            crc = reflect(crc, self.width)

        # The CRC value is converted to string for easier manipulation
        crc = f'{crc:0{self.width}b}'

        if len(crc) != self.width:
            raise AssertionError(f'CRC width error ({crc})')

        # Sometimes it happens that the communication interfaces are
        # made in a such a way that the CRC value is appended in the
        # reverse order. This mostly occurs when "refin == True" and
        # the CRC value is appended in big-endian instead of little-
        # endian. The "reverse" parameter makes it possible to take
        # this into account.
        if not (self.refin ^ self.reverse):
            b_crc = [
                crc[k:k + self.data]
                for k in range(0, self.width, self.data)
            ]
        else:  # self.refin ^ self.reverse
            b_crc = [
                crc[max(k - self.data, 0):k]
                for k in range(self.width, 0, -self.data)
            ]

        if isinstance(buffer, str):
            buffer += ''.join(b_crc)
        else:  # bytes, bytearray, List[int]
            b_crc = [int(data, 2) for data in b_crc]
            if isinstance(buffer, bytes):  # immutable
                buffer += bytes(b_crc)
            else:  # bytearray and List[int] are mutable
                buffer.extend(b_crc)

        return buffer

    def _crc_extract(self, buffer: BufferType) -> int:
        """Extracts the CRC value from the buffer.

        Args:
            `buffer`: Data buffer with its CRC appended at the end.

        Returns:
            `int`: CRC value as an integer.

        Raises:
            `ValueError`: If the extracted CRC value exceeds the CRC
            width.
        """

        if isinstance(buffer, str):
            idx = len(buffer) - self.width
            b_crc = [
                int(buffer[idx + k:idx + k + self.data], 2)
                for k in range(0, self.width, self.data)
            ]
        else:  # bytes, bytearray, List[int]
            b_crc = buffer[-self._p.n_crc:]

        # See append() method for explanation
        if self.refin ^ self.reverse:
            b_crc = b_crc[::-1]  # little-endian to big-endian

        base = 2 ** self.data
        exponent = self._p.n_crc - 1

        crc = sum([
            data * (base ** (exponent - e))  # big-endian
            for e, data in enumerate(b_crc)
        ])

        if crc >> self.width:
            raise ValueError(
                f'CRC value exceeds the CRC width (0x{crc:X})'
            )

        # See crc() method for explanation
        if self.refin ^ self.refout:
            crc = reflect(crc, self.width)

        return crc

    def separate(self, buffer: BufferType) -> Tuple[BufferType, int]:
        """Extracts the message and its CRC value from the buffer.

        Args:
            `buffer`: Data buffer with its CRC appended at the end.

        Returns:
            `BufferType`: Message of the same type as the buffer.
            `int`: CRC value as an integer.

        Raises:
            `ValueError`: If any `buffer` element is invalid, or if the
            buffer type is not supported, or if the extracted CRC value
            exceeds the CRC width.
        """

        self._check_buffer(buffer, True)

        if isinstance(buffer, str):
            message = buffer[:-self.width]
        else:  # bytes, bytearray, List[int]
            message = buffer[:-self._p.n_crc]

        crc = self._crc_extract(buffer)

        return message, crc

    def _residue(self, buffer: BufferType) -> int:
        """Calculates the residue of the given buffer.

        The residue is defined as CRC before final XOR calculated over
        a buffer with its CRC appended at the end.

        Args:
            `buffer`: Data buffer with its CRC appended at the end.

        Returns:
            `int`: Calculated residue value.

        Raises:
            `ValueError`: If any `buffer` element is invalid, or if the
            buffer type is not supported.
        """
        return self._crc(buffer, len(buffer), True) ^ self.xorout

    def verify(self, buffer: BufferType) -> bool:
        """Verifies the given buffer by calculating its residue.

        Args:
            `buffer`: Data buffer with its CRC appended at the end.

        Returns:
            `bool`: `True` when the residue verification is successful,
            `False` otherwise.

        Raises:
            `ValueError`: If any `buffer` element is invalid, or if the
            buffer type is not supported.
        """

        if not self.reverse:
            # Residue-based verification can only be done if the CRC
            # value is appended to the message in the correct order:
            #   - big-endian when "refin == False", and
            #   - little-endian when "refin == True".
            return self._residue(buffer) == self.residue
        else:  # self.reverse
            # When the CRC value is appended in the reverse order,
            # it is simpler to directly compare the CRC values.
            crc = self._crc_extract(buffer)

            if isinstance(buffer, str):
                size = len(buffer) - self.width
            else:  # bytes, bytearray, List[int]
                size = len(buffer) - self._p.n_crc

            return self._crc(buffer, size, True) == crc

    def _validate(self) -> None:
        """Validates the `check` and `residue` CRC model parameters.

        The `check` parameter equals CRC calculated for the standard
        test message `b'123456789'` and a data width of 8 bits. If the
        data widht is not 8 bits, the `check` parameter must be defined
        as `None`.

        The `residue` parameter is CRC before final XOR calculated over
        a buffer with its CRC appended at the end.

        This method validates the `check` and `residue` parameters if
        they are defined by the user. If not, the method initializes
        these parameters to the correct values.

        Raises:
            `ValueError`: If either `check` or `residue` parameter
            validation fails, or if the `check` parameter is defined
            when the data width is not 8 bits.
        """

        # --- CHECK PARAMETER ---

        if self.data != 8:
            if self.check is not None:
                raise ValueError(
                    'The check parameter must not be defined when '
                    f'the data width is not 8 bits ({self.data})'
                )
        else:  # self.data == 8
            check = self.crc(b'123456789')

            if self.check is None:
                object.__setattr__(self, 'check', check)
            elif check != self.check:
                raise ValueError(f'Invalid check parameter: {self}')

        # --- RESIDUE PARAMETER ---

        # The reverse parameter affects the append() method output!
        reverse = self.reverse
        object.__setattr__(self, 'reverse', False)

        # Residue does not depend on element value or buffer size. The
        # test buffer '[1]' will work for any data width!
        residue = self._residue(self.append([1]))

        object.__setattr__(self, 'reverse', reverse)

        if self.residue is None:
            object.__setattr__(self, 'residue', residue)
        elif residue != self.residue:
            raise ValueError(f'Invalid residue parameter: {self}')

    def optimization(self, optimize: bool) -> 'CRC':
        """Enables or disables CRC calculation optimization.

        Configures the CRC calculation algorithm:
        - For `optimize == True`, it uses a precomputed CRC lookup
        table for faster calculation.
        - For `optimize == False`, the standard bit-by-bit CRC
        calculation is used.

        Considering memory requirements for the CRC lookup table, the
        CRC calculation optimization can be enabled only if the data
        width does not exceed `CRC._MAX_OPT` bits.

        Args:
            `optimize`: Switch to enable or disable table-based CRC
            calculation optimization.

        Returns:
            `CRC`: `self`, allowing for method chaining.

        Raises:
            `ValueError`: When the data width is too large for the CRC
            lookup table to be generated; i.e., `data > CRC._MAX_OPT`.
        """

        if optimize:
            self._crc_table()
            crc = self._crc_reflected_opt if self.refin else self._crc_opt
        else:  # optimize == False
            crc = self._crc_reflected_unopt if self.refin else self._crc_unopt

        object.__setattr__(self._p, 'crc', crc)
        object.__setattr__(self, 'optimize', optimize)

        return self

    def _crc_table(self) -> None:
        """Generates the CRC lookup table.

        The CRC lookup table is a precomputed table of CRC values for
        each possible buffer element. This means that the lookup table
        will contain `2^data` elements, where `data` is the data width,
        i.e., the number of bits used to represent each buffer element.

        Considering memory requirements, it is not allowed to generate
        the CRC lookup table for data widths beyond `CRC._MAX_OPT` bits.
        If the CRC lookup table is already generated, the method returns
        without generating new table.

        The CRC lookup table speeds up the CRC calculation process by
        allowing the CRC value to be computed (updated) for multiple
        bits at once, instead of bit-by-bit.

        The `init` parameter is temporarily set to 0 during the table
        generation, after which it is restored to its original value.

        Raises:
            `ValueError`: When the data width is too large for the CRC
            lookup table to be generated; i.e., `data > CRC._MAX_OPT`.
        """

        if self._p.table:
            return

        if self.data > CRC._MAX_OPT:
            raise ValueError(
                'Data width is too large for the CRC lookup table '
                f'to be generated ({self.data} > {CRC._MAX_OPT})'
            )

        init = self._p.init
        object.__setattr__(self._p, 'init', 0)

        # Resolve the CRC calculation method
        crc = self._crc_reflected_unopt if self.refin else self._crc_unopt

        # When the CRC width is smaller than the data width, the CRC
        # value is kept aligned with the data during the calculation.
        # This applies only in the un-reflected implementation.
        ls = self._p.diff if not self.refin else 0

        table = [(crc([data], 1) << ls) for data in range(2**self.data)]

        object.__setattr__(self._p, 'init', init)
        object.__setattr__(self._p, 'table', table)

    @property
    def table(self) -> List[int]:
        """Returns a copy of the CRC lookup table.

        If the CRC lookup table is not generated when this method is
        called, it ensures the table is generated. However, the CRC
        lookup table is generated only if the data width defined by
        the `data` parameter is not larger than `CRC._MAX_OPT` bits.

        Returns:
            `List[int]`: A copy of the CRC lookup table.

        Raises:
            `ValueError`: When the data width is too large for the CRC
            lookup table to be generated; i.e., `data > CRC._MAX_OPT`.
        """

        self._crc_table()

        return self._p.table.copy()

    def table_2d(self, cols: int = 8) -> str:
        """Generates a string representation of the CRC lookup table.

        The CRC lookup table is formatted into a 2D grid with the given
        number of columns. The table values are formatted as hexadecimal
        numbers with leading `0x`.

        If the CRC lookup table is not generated when this method is
        called, it ensures the table is generated. However, the CRC
        lookup table is generated only if the data width defined by
        the `data` parameter is not larger than `CRC._MAX_OPT` bits.

        Args:
            `cols`: Number of columns in the 2D grid. Defaults to `8`.

        Returns:
            `str`: String representation of the CRC lookup table.

        Raises:
            `ValueError`: When the data width is too large for the CRC
            lookup table to be generated; i.e., `data > CRC._MAX_OPT`.
        """

        self._crc_table()

        width = self._p.width if not self.refin else self.width
        nibbles = -(width // -4)  # ceil

        return ',\n'.join([
            ', '.join([
                f'0x{crc:0{nibbles}X}'
                for crc in self._p.table[k:k + cols]
            ])
            for k in range(0, len(self._p.table), cols)
        ])


# ==================================================================== #
# SECTION:  Catalog of Well-Known CRC Algorithms                       #
#           https://reveng.sourceforge.io/crc-catalogue/all.htm        #
# ==================================================================== #

# Start populating the CRC._catalog
CRC._populate = True


class CRC3:
    """Collection of 3-bit CRC models.

    ```
    MODEL  POLY  INIT  REFIN  REFOUT  XOROUT  CHECK  RESIDUE
    GSM    0x3   0x0   False  False   0x7     0x4    0x2
    ROHC   0x3   0x7   True   True    0x0     0x6    0x0
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    GSM  = CRC(3, 0x3, 0x0, False, False, 0x7, 0x4, 0x2, 'CRC-3/GSM')
    ROHC = CRC(3, 0x3, 0x7, True,  True,  0x0, 0x6, 0x0, 'CRC-3/ROHC')


class CRC4:
    """Collection of 4-bit CRC models.

    ```
    MODEL       POLY  INIT  REFIN  REFOUT  XOROUT  CHECK  RESIDUE
    G_704       0x3   0x0   True   True    0x0     0x7    0x0
    INTERLAKEN  0x3   0xF   False  False   0xF     0xB    0x2
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    G_704      = CRC(4, 0x3, 0x0, True,  True,  0x0, 0x7, 0x0, 'CRC-4/G-704', 'CRC-4/ITU')
    INTERLAKEN = CRC(4, 0x3, 0xF, False, False, 0xF, 0xB, 0x2, 'CRC-4/INTERLAKEN')


class CRC5:
    """Collection of 5-bit CRC models.

    ```
    MODEL     POLY  INIT  REFIN  REFOUT  XOROUT  CHECK  RESIDUE
    EPC_C1G2  0x09  0x09  False  False   0x00    0x00   0x00
    G_704     0x15  0x00  True   True    0x00    0x07   0x00
    USB       0x05  0x1F  True   True    0x1F    0x19   0x06
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    EPC_C1G2 = CRC(5, 0x09, 0x09, False, False, 0x00, 0x00, 0x00, 'CRC-5/EPC-C1G2', 'CRC-5/EPC')
    G_704    = CRC(5, 0x15, 0x00, True,  True,  0x00, 0x07, 0x00, 'CRC-5/G-704', 'CRC-5/ITU')
    USB      = CRC(5, 0x05, 0x1F, True,  True,  0x1F, 0x19, 0x06, 'CRC-5/USB')


class CRC6:
    """Collection of 6-bit CRC models.

    ```
    MODEL       POLY  INIT  REFIN  REFOUT  XOROUT  CHECK  RESIDUE
    CDMA2000_A  0x27  0x3F  False  False   0x00    0x0D   0x00
    CDMA2000_B  0x07  0x3F  False  False   0x00    0x3B   0x00
    DARC        0x19  0x00  True   True    0x00    0x26   0x00
    G_704       0x03  0x00  True   True    0x00    0x06   0x00
    GSM         0x2F  0x00  False  False   0x3F    0x13   0x3A
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    CDMA2000_A = CRC(6, 0x27, 0x3F, False, False, 0x00, 0x0D, 0x00, 'CRC-6/CDMA2000-A')
    CDMA2000_B = CRC(6, 0x07, 0x3F, False, False, 0x00, 0x3B, 0x00, 'CRC-6/CDMA2000-B')
    DARC       = CRC(6, 0x19, 0x00, True,  True,  0x00, 0x26, 0x00, 'CRC-6/DARC')
    G_704      = CRC(6, 0x03, 0x00, True,  True,  0x00, 0x06, 0x00, 'CRC-6/G-704', 'CRC-6/ITU')
    GSM        = CRC(6, 0x2F, 0x00, False, False, 0x3F, 0x13, 0x3A, 'CRC-6/GSM')


class CRC7:
    """Collection of 7-bit CRC models.

    ```
    MODEL  POLY  INIT  REFIN  REFOUT  XOROUT  CHECK  RESIDUE
    MMC    0x09  0x00  False  False   0x00    0x75   0x00
    ROHC   0x4F  0x7F  True   True    0x00    0x53   0x00
    UMTS   0x45  0x00  False  False   0x00    0x61   0x00
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    MMC  = CRC(7, 0x09, 0x00, False, False, 0x00, 0x75, 0x00, 'CRC-7/MMC', 'CRC-7')
    ROHC = CRC(7, 0x4F, 0x7F, True,  True,  0x00, 0x53, 0x00, 'CRC-7/ROHC')
    UMTS = CRC(7, 0x45, 0x00, False, False, 0x00, 0x61, 0x00, 'CRC-7/UMTS')


class CRC8:
    """Collection of 8-bit CRC models.

    ```
    MODEL       POLY  INIT  REFIN  REFOUT  XOROUT  CHECK  RESIDUE
    AUTOSAR     0x2F  0xFF  False  False   0xFF    0xDF   0x42
    BLUETOOTH   0xA7  0x00  True   True    0x00    0x26   0x00
    CDMA2000    0x9B  0xFF  False  False   0x00    0xDA   0x00
    DARC        0x39  0x00  True   True    0x00    0x15   0x00
    DVB_S2      0xD5  0x00  False  False   0x00    0xBC   0x00
    GSM_A       0x1D  0x00  False  False   0x00    0x37   0x00
    GSM_B       0x49  0x00  False  False   0xFF    0x94   0x53
    HITAG       0x1D  0xFF  False  False   0x00    0xB4   0x00
    I_432_1     0x07  0x00  False  False   0x55    0xA1   0xAC
    I_CODE      0x1D  0xFD  False  False   0x00    0x7E   0x00
    LTE         0x9B  0x00  False  False   0x00    0xEA   0x00
    MAXIM_DOW   0x31  0x00  True   True    0x00    0xA1   0x00
    MIFARE_MAD  0x1D  0xC7  False  False   0x00    0x99   0x00
    NRSC_5      0x31  0xFF  False  False   0x00    0xF7   0x00
    OPENSAFETY  0x2F  0x00  False  False   0x00    0x3E   0x00
    ROHC        0x07  0xFF  True   True    0x00    0xD0   0x00
    SAE_J1850   0x1D  0xFF  False  False   0xFF    0x4B   0xC4
    SMBUS       0x07  0x00  False  False   0x00    0xF4   0x00
    TECH_3250   0x1D  0xFF  True   True    0x00    0x97   0x00
    WCDMA       0x9B  0x00  True   True    0x00    0x25   0x00
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    AUTOSAR    = CRC(8, 0x2F, 0xFF, False, False, 0xFF, 0xDF, 0x42, 'CRC-8/AUTOSAR')
    BLUETOOTH  = CRC(8, 0xA7, 0x00, True,  True,  0x00, 0x26, 0x00, 'CRC-8/BLUETOOTH')
    CDMA2000   = CRC(8, 0x9B, 0xFF, False, False, 0x00, 0xDA, 0x00, 'CRC-8/CDMA2000')
    DARC       = CRC(8, 0x39, 0x00, True,  True,  0x00, 0x15, 0x00, 'CRC-8/DARC')
    DVB_S2     = CRC(8, 0xD5, 0x00, False, False, 0x00, 0xBC, 0x00, 'CRC-8/DVB-S2')
    GSM_A      = CRC(8, 0x1D, 0x00, False, False, 0x00, 0x37, 0x00, 'CRC-8/GSM-A')
    GSM_B      = CRC(8, 0x49, 0x00, False, False, 0xFF, 0x94, 0x53, 'CRC-8/GSM-B')
    HITAG      = CRC(8, 0x1D, 0xFF, False, False, 0x00, 0xB4, 0x00, 'CRC-8/HITAG')
    I_432_1    = CRC(8, 0x07, 0x00, False, False, 0x55, 0xA1, 0xAC, 'CRC-8/I-432-1', 'CRC-8/ITU')
    I_CODE     = CRC(8, 0x1D, 0xFD, False, False, 0x00, 0x7E, 0x00, 'CRC-8/I-CODE')
    LTE        = CRC(8, 0x9B, 0x00, False, False, 0x00, 0xEA, 0x00, 'CRC-8/LTE')
    MAXIM_DOW  = CRC(8, 0x31, 0x00, True,  True,  0x00, 0xA1, 0x00, 'CRC-8/MAXIM-DOW', 'CRC-8/MAXIM, DOW-CRC')
    MIFARE_MAD = CRC(8, 0x1D, 0xC7, False, False, 0x00, 0x99, 0x00, 'CRC-8/MIFARE-MAD')
    NRSC_5     = CRC(8, 0x31, 0xFF, False, False, 0x00, 0xF7, 0x00, 'CRC-8/NRSC-5')
    OPENSAFETY = CRC(8, 0x2F, 0x00, False, False, 0x00, 0x3E, 0x00, 'CRC-8/OPENSAFETY')
    ROHC       = CRC(8, 0x07, 0xFF, True,  True,  0x00, 0xD0, 0x00, 'CRC-8/ROHC')
    SAE_J1850  = CRC(8, 0x1D, 0xFF, False, False, 0xFF, 0x4B, 0xC4, 'CRC-8/SAE-J1850')
    SMBUS      = CRC(8, 0x07, 0x00, False, False, 0x00, 0xF4, 0x00, 'CRC-8/SMBUS', 'CRC-8')
    TECH_3250  = CRC(8, 0x1D, 0xFF, True,  True,  0x00, 0x97, 0x00, 'CRC-8/TECH-3250', 'CRC-8/AES, CRC-8/EBU')
    WCDMA      = CRC(8, 0x9B, 0x00, True,  True,  0x00, 0x25, 0x00, 'CRC-8/WCDMA')


class CRC10:
    """Collection of 10-bit CRC models.

    ```
    MODEL     POLY   INIT   REFIN  REFOUT  XOROUT  CHECK  RESIDUE
    ATM       0x233  0x000  False  False   0x000   0x199  0x000
    CDMA2000  0x3D9  0x3FF  False  False   0x000   0x233  0x000
    GSM       0x175  0x000  False  False   0x3FF   0x12A  0x0C6
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    ATM      = CRC(10, 0x233, 0x000, False, False, 0x000, 0x199, 0x000, 'CRC-10/ATM', 'CRC-10, CRC-10/I-610')
    CDMA2000 = CRC(10, 0x3D9, 0x3FF, False, False, 0x000, 0x233, 0x000, 'CRC-10/CDMA2000')
    GSM      = CRC(10, 0x175, 0x000, False, False, 0x3FF, 0x12A, 0x0C6, 'CRC-10/GSM')


class CRC11:
    """Collection of 11-bit CRC models.

    ```
    MODEL    POLY   INIT   REFIN  REFOUT  XOROUT  CHECK  RESIDUE
    FLEXRAY  0x385  0x01A  False  False   0x000   0x5A3  0x000
    UMTS     0x307  0x000  False  False   0x000   0x061  0x000
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    FLEXRAY = CRC(11, 0x385, 0x01A, False, False, 0x000, 0x5A3, 0x000, 'CRC-11/FLEXRAY', 'CRC-11')
    UMTS    = CRC(11, 0x307, 0x000, False, False, 0x000, 0x061, 0x000, 'CRC-11/UMTS')


class CRC12:
    """Collection of 12-bit CRC models.

    ```
    MODEL     POLY   INIT   REFIN  REFOUT  XOROUT  CHECK  RESIDUE
    CDMA2000  0xF13  0xFFF  False  False   0x000   0xD4D  0x000
    DECT      0x80F  0x000  False  False   0x000   0xF5B  0x000
    GSM       0xD31  0x000  False  False   0xFFF   0xB34  0x178
    UMTS      0x80F  0x000  False  True    0x000   0xDAF  0x000
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    CDMA2000 = CRC(12, 0xF13, 0xFFF, False, False, 0x000, 0xD4D, 0x000, 'CRC-12/CDMA2000')
    DECT     = CRC(12, 0x80F, 0x000, False, False, 0x000, 0xF5B, 0x000, 'CRC-12/DECT', 'X-CRC-12')
    GSM      = CRC(12, 0xD31, 0x000, False, False, 0xFFF, 0xB34, 0x178, 'CRC-12/GSM')
    UMTS     = CRC(12, 0x80F, 0x000, False, True,  0x000, 0xDAF, 0x000, 'CRC-12/UMTS', 'CRC-12/3GPP')


class CRC13:
    """Collection of 13-bit CRC models.

    ```
    MODEL  POLY    INIT    REFIN  REFOUT  XOROUT  CHECK   RESIDUE
    BBC    0x1CF5  0x0000  False  False   0x0000  0x04FA  0x0000
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    BBC = CRC(13, 0x1CF5, 0x0000, False, False, 0x0000, 0x04FA, 0x0000, 'CRC-13/BBC')


class CRC14:
    """Collection of 14-bit CRC models.

    ```
    MODEL  POLY    INIT    REFIN  REFOUT  XOROUT  CHECK   RESIDUE
    DARC   0x0805  0x0000  True   True    0x0000  0x082D  0x0000
    GSM    0x202D  0x0000  False  False   0x3FFF  0x30AE  0x031E
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    DARC = CRC(14, 0x0805, 0x0000, True,  True,  0x0000, 0x082D, 0x0000, 'CRC-14/DARC')
    GSM  = CRC(14, 0x202D, 0x0000, False, False, 0x3FFF, 0x30AE, 0x031E, 'CRC-14/GSM')


class CRC15:
    """Collection of 15-bit CRC models.

    ```
    MODEL  POLY    INIT    REFIN  REFOUT  XOROUT  CHECK   RESIDUE
    DARC   0x0805  0x0000  True   True    0x0000  0x082D  0x0000
    GSM    0x202D  0x0000  False  False   0x3FFF  0x30AE  0x031E
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    CAN     = CRC(15, 0x4599, 0x0000, False, False, 0x0000, 0x059E, 0x0000, 'CRC-15/CAN', 'CRC-15')
    MPT1327 = CRC(15, 0x6815, 0x0000, False, False, 0x0001, 0x2566, 0x6815, 'CRC-15/MPT1327')


class CRC16:
    """Collection of 16-bit CRC models.

    ```
    MODEL              POLY    INIT    REFIN  REFOUT  XOROUT  CHECK   RESIDUE
    ARC                0x8005  0x0000  True   True    0x0000  0xBB3D  0x0000
    CDMA2000           0xC867  0xFFFF  False  False   0x0000  0x4C06  0x0000
    CMS                0x8005  0xFFFF  False  False   0x0000  0xAEE7  0x0000
    DDS_110            0x8005  0x800D  False  False   0x0000  0x9ECF  0x0000
    DECT_R             0x0589  0x0000  False  False   0x0001  0x007E  0x0589
    DECT_X             0x0589  0x0000  False  False   0x0000  0x007F  0x0000
    DNP                0x3D65  0x0000  True   True    0xFFFF  0xEA82  0x66C5
    EN_13757           0x3D65  0x0000  False  False   0xFFFF  0xC2B7  0xA366
    GENIBUS            0x1021  0xFFFF  False  False   0xFFFF  0xD64E  0x1D0F
    GSM                0x1021  0x0000  False  False   0xFFFF  0xCE3C  0x1D0F
    IBM_3740           0x1021  0xFFFF  False  False   0x0000  0x29B1  0x0000
    IBM_SDLC           0x1021  0xFFFF  True   True    0xFFFF  0x906E  0xF0B8
    ISO_IEC_14443_3_A  0x1021  0xC6C6  True   True    0x0000  0xBF05  0x0000
    KERMIT             0x1021  0x0000  True   True    0x0000  0x2189  0x0000
    LJ1200             0x6F63  0x0000  False  False   0x0000  0xBDF4  0x0000
    M17                0x5935  0xFFFF  False  False   0x0000  0x772B  0x0000
    MAXIM_DOW          0x8005  0x0000  True   True    0xFFFF  0x44C2  0xB001
    MCRF4XX            0x1021  0xFFFF  True   True    0x0000  0x6F91  0x0000
    MODBUS             0x8005  0xFFFF  True   True    0x0000  0x4B37  0x0000
    NRSC_5             0x080B  0xFFFF  True   True    0x0000  0xA066  0x0000
    OPENSAFETY_A       0x5935  0x0000  False  False   0x0000  0x5D38  0x0000
    OPENSAFETY_B       0x755B  0x0000  False  False   0x0000  0x20FE  0x0000
    PROFIBUS           0x1DCF  0xFFFF  False  False   0xFFFF  0xA819  0xE394
    RIELLO             0x1021  0xB2AA  True   True    0x0000  0x63D0  0x0000
    SPI_FUJITSU        0x1021  0x1D0F  False  False   0x0000  0xE5CC  0x0000
    T10_DIF            0x8BB7  0x0000  False  False   0x0000  0xD0DB  0x0000
    TELEDISK           0xA097  0x0000  False  False   0x0000  0x0FB3  0x0000
    TMS37157           0x1021  0x89EC  True   True    0x0000  0x26B1  0x0000
    UMTS               0x8005  0x0000  False  False   0x0000  0xFEE8  0x0000
    USB                0x8005  0xFFFF  True   True    0xFFFF  0xB4C8  0xB001
    XMODEM             0x1021  0x0000  False  False   0x0000  0x31C3  0x0000
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    ARC               = CRC(16, 0x8005, 0x0000, True,  True,  0x0000, 0xBB3D, 0x0000, 'CRC-16/ARC', 'ARC, CRC-16, CRC-16/LHA, CRC-IBM')
    CDMA2000          = CRC(16, 0xC867, 0xFFFF, False, False, 0x0000, 0x4C06, 0x0000, 'CRC-16/CDMA2000')
    CMS               = CRC(16, 0x8005, 0xFFFF, False, False, 0x0000, 0xAEE7, 0x0000, 'CRC-16/CMS')
    DDS_110           = CRC(16, 0x8005, 0x800D, False, False, 0x0000, 0x9ECF, 0x0000, 'CRC-16/DDS-110')
    DECT_R            = CRC(16, 0x0589, 0x0000, False, False, 0x0001, 0x007E, 0x0589, 'CRC-16/DECT-R', 'R-CRC-16')
    DECT_X            = CRC(16, 0x0589, 0x0000, False, False, 0x0000, 0x007F, 0x0000, 'CRC-16/DECT-X', 'X-CRC-16')
    DNP               = CRC(16, 0x3D65, 0x0000, True,  True,  0xFFFF, 0xEA82, 0x66C5, 'CRC-16/DNP')
    EN_13757          = CRC(16, 0x3D65, 0x0000, False, False, 0xFFFF, 0xC2B7, 0xA366, 'CRC-16/EN-13757')
    GENIBUS           = CRC(16, 0x1021, 0xFFFF, False, False, 0xFFFF, 0xD64E, 0x1D0F, 'CRC-16/GENIBUS', 'CRC-16/DARC, CRC-16/EPC, CRC-16/EPC-C1G2, CRC-16/I-CODE')
    GSM               = CRC(16, 0x1021, 0x0000, False, False, 0xFFFF, 0xCE3C, 0x1D0F, 'CRC-16/GSM')
    IBM_3740          = CRC(16, 0x1021, 0xFFFF, False, False, 0x0000, 0x29B1, 0x0000, 'CRC-16/IBM-3740', 'CRC-16/AUTOSAR, CRC-16/CCITT-FALSE')
    IBM_SDLC          = CRC(16, 0x1021, 0xFFFF, True,  True,  0xFFFF, 0x906E, 0xF0B8, 'CRC-16/IBM-SDLC', 'CRC-16/ISO-HDLC, CRC-16/ISO-IEC-14443-3-B, CRC-16/X-25, CRC-B, X-25')
    ISO_IEC_14443_3_A = CRC(16, 0x1021, 0xC6C6, True,  True,  0x0000, 0xBF05, 0x0000, 'CRC-16/ISO-IEC-14443-3-A', 'CRC-A')
    KERMIT            = CRC(16, 0x1021, 0x0000, True,  True,  0x0000, 0x2189, 0x0000, 'CRC-16/KERMIT', 'CRC-16/BLUETOOTH, CRC-16/CCITT, CRC-16/CCITT-TRUE, CRC-16/V-41-LSB, CRC-CCITT, KERMIT')
    LJ1200            = CRC(16, 0x6F63, 0x0000, False, False, 0x0000, 0xBDF4, 0x0000, 'CRC-16/LJ1200')
    M17               = CRC(16, 0x5935, 0xFFFF, False, False, 0x0000, 0x772B, 0x0000, 'CRC-16/M17')
    MAXIM_DOW         = CRC(16, 0x8005, 0x0000, True,  True,  0xFFFF, 0x44C2, 0xB001, 'CRC-16/MAXIM-DOW', 'CRC-16/MAXIM')
    MCRF4XX           = CRC(16, 0x1021, 0xFFFF, True,  True,  0x0000, 0x6F91, 0x0000, 'CRC-16/MCRF4XX')
    MODBUS            = CRC(16, 0x8005, 0xFFFF, True,  True,  0x0000, 0x4B37, 0x0000, 'CRC-16/MODBUS', 'MODBUS')
    NRSC_5            = CRC(16, 0x080B, 0xFFFF, True,  True,  0x0000, 0xA066, 0x0000, 'CRC-16/NRSC-5')
    OPENSAFETY_A      = CRC(16, 0x5935, 0x0000, False, False, 0x0000, 0x5D38, 0x0000, 'CRC-16/OPENSAFETY-A')
    OPENSAFETY_B      = CRC(16, 0x755B, 0x0000, False, False, 0x0000, 0x20FE, 0x0000, 'CRC-16/OPENSAFETY-B')
    PROFIBUS          = CRC(16, 0x1DCF, 0xFFFF, False, False, 0xFFFF, 0xA819, 0xE394, 'CRC-16/PROFIBUS', 'CRC-16/IEC-61158-2')
    RIELLO            = CRC(16, 0x1021, 0xB2AA, True,  True,  0x0000, 0x63D0, 0x0000, 'CRC-16/RIELLO')
    SPI_FUJITSU       = CRC(16, 0x1021, 0x1D0F, False, False, 0x0000, 0xE5CC, 0x0000, 'CRC-16/SPI-FUJITSU', 'CRC-16/AUG-CCITT')
    T10_DIF           = CRC(16, 0x8BB7, 0x0000, False, False, 0x0000, 0xD0DB, 0x0000, 'CRC-16/T10-DIF')
    TELEDISK          = CRC(16, 0xA097, 0x0000, False, False, 0x0000, 0x0FB3, 0x0000, 'CRC-16/TELEDISK')
    TMS37157          = CRC(16, 0x1021, 0x89EC, True,  True,  0x0000, 0x26B1, 0x0000, 'CRC-16/TMS37157')
    UMTS              = CRC(16, 0x8005, 0x0000, False, False, 0x0000, 0xFEE8, 0x0000, 'CRC-16/UMTS', 'CRC-16/BUYPASS, CRC-16/VERIFONE')
    USB               = CRC(16, 0x8005, 0xFFFF, True,  True,  0xFFFF, 0xB4C8, 0xB001, 'CRC-16/USB')
    XMODEM            = CRC(16, 0x1021, 0x0000, False, False, 0x0000, 0x31C3, 0x0000, 'CRC-16/XMODEM', 'CRC-16/ACORN, CRC-16/LTE, CRC-16/V-41-MSB, XMODEM, ZMODEM')


class CRC17:
    """Collection of 17-bit CRC models.

    ```
    MODEL   POLY     INIT     REFIN  REFOUT  XOROUT   CHECK    RESIDUE
    CAN_FD  0x1685B  0x00000  False  False   0x00000  0x04F03  0x00000
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    CAN_FD = CRC(17, 0x1685B, 0x00000, False, False, 0x00000, 0x04F03, 0x00000, 'CRC-17/CAN-FD')


class CRC21:
    """Collection of 21-bit CRC models.

    ```
    MODEL   POLY      INIT      REFIN  REFOUT  XOROUT    CHECK     RESIDUE
    CAN_FD  0x102899  0x000000  False  False   0x000000  0x0ED841  0x000000
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    CAN_FD = CRC(21, 0x102899, 0x000000, False, False, 0x000000, 0x0ED841, 0x000000, 'CRC-21/CAN-FD')


class CRC24:
    """Collection of 24-bit CRC models.

    ```
    MODEL       POLY      INIT      REFIN  REFOUT  XOROUT    CHECK     RESIDUE
    BLE         0x00065B  0x555555  True   True    0x000000  0xC25A56  0x000000
    FLEXRAY_A   0x5D6DCB  0xFEDCBA  False  False   0x000000  0x7979BD  0x000000
    FLEXRAY_B   0x5D6DCB  0xABCDEF  False  False   0x000000  0x1F23B8  0x000000
    INTERLAKEN  0x328B63  0xFFFFFF  False  False   0xFFFFFF  0xB4F3E6  0x144E63
    LTE_A       0x864CFB  0x000000  False  False   0x000000  0xCDE703  0x000000
    LTE_B       0x800063  0x000000  False  False   0x000000  0x23EF52  0x000000
    OPENPGP     0x864CFB  0xB704CE  False  False   0x000000  0x21CF02  0x000000
    OS_9        0x800063  0xFFFFFF  False  False   0xFFFFFF  0x200FA5  0x800FE3
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    BLE        = CRC(24, 0x00065B, 0x555555, True,  True,  0x000000, 0xC25A56, 0x000000, 'CRC-24/BLE')
    FLEXRAY_A  = CRC(24, 0x5D6DCB, 0xFEDCBA, False, False, 0x000000, 0x7979BD, 0x000000, 'CRC-24/FLEXRAY-A')
    FLEXRAY_B  = CRC(24, 0x5D6DCB, 0xABCDEF, False, False, 0x000000, 0x1F23B8, 0x000000, 'CRC-24/FLEXRAY-B')
    INTERLAKEN = CRC(24, 0x328B63, 0xFFFFFF, False, False, 0xFFFFFF, 0xB4F3E6, 0x144E63, 'CRC-24/INTERLAKEN')
    LTE_A      = CRC(24, 0x864CFB, 0x000000, False, False, 0x000000, 0xCDE703, 0x000000, 'CRC-24/LTE-A')
    LTE_B      = CRC(24, 0x800063, 0x000000, False, False, 0x000000, 0x23EF52, 0x000000, 'CRC-24/LTE-B')
    OPENPGP    = CRC(24, 0x864CFB, 0xB704CE, False, False, 0x000000, 0x21CF02, 0x000000, 'CRC-24/OPENPGP', 'CRC-24')
    OS_9       = CRC(24, 0x800063, 0xFFFFFF, False, False, 0xFFFFFF, 0x200FA5, 0x800FE3, 'CRC-24/OS-9')


class CRC30:
    """Collection of 30-bit CRC models.

    ```
    MODEL  POLY        INIT        REFIN  REFOUT  XOROUT      CHECK       RESIDUE
    CDMA   0x2030B9C7  0x3FFFFFFF  False  False   0x3FFFFFFF  0x04C34ABF  0x34EFA55A
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    CDMA = CRC(30, 0x2030B9C7, 0x3FFFFFFF, False, False, 0x3FFFFFFF, 0x04C34ABF, 0x34EFA55A, 'CRC-30/CDMA')


class CRC31:
    """Collection of 31-bit CRC models.

    ```
    MODEL    POLY        INIT        REFIN  REFOUT  XOROUT      CHECK       RESIDUE
    PHILIPS  0x04C11DB7  0x7FFFFFFF  False  False   0x7FFFFFFF  0x0CE9E46C  0x4EAF26F1
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    PHILIPS = CRC(31, 0x04C11DB7, 0x7FFFFFFF, False, False, 0x7FFFFFFF, 0x0CE9E46C, 0x4EAF26F1, 'CRC-31/PHILIPS')


class CRC32:
    """Collection of 32-bit CRC models.

    ```
    MODEL       POLY        INIT        REFIN  REFOUT  XOROUT      CHECK       RESIDUE
    AIXM        0x814141AB  0x00000000  False  False   0x00000000  0x3010BF7F  0x00000000
    AUTOSAR     0xF4ACFB13  0xFFFFFFFF  True   True    0xFFFFFFFF  0x1697D06A  0x904CDDBF
    BASE91_D    0xA833982B  0xFFFFFFFF  True   True    0xFFFFFFFF  0x87315576  0x45270551
    BZIP2       0x04C11DB7  0xFFFFFFFF  False  False   0xFFFFFFFF  0xFC891918  0xC704DD7B
    CD_ROM_EDC  0x8001801B  0x00000000  True   True    0x00000000  0x6EC2EDC4  0x00000000
    CKSUM       0x04C11DB7  0x00000000  False  False   0xFFFFFFFF  0x765E7680  0xC704DD7B
    ISCSI       0x1EDC6F41  0xFFFFFFFF  True   True    0xFFFFFFFF  0xE3069283  0xB798B438
    ISO_HDLC    0x04C11DB7  0xFFFFFFFF  True   True    0xFFFFFFFF  0xCBF43926  0xDEBB20E3
    JAMCRC      0x04C11DB7  0xFFFFFFFF  True   True    0x00000000  0x340BC6D9  0x00000000
    MEF         0x741B8CD7  0xFFFFFFFF  True   True    0x00000000  0xD2C22F51  0x00000000
    MPEG_2      0x04C11DB7  0xFFFFFFFF  False  False   0x00000000  0x0376E6E7  0x00000000
    XFER        0x000000AF  0x00000000  False  False   0x00000000  0xBD0BE338  0x00000000
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    AIXM       = CRC(32, 0x814141AB, 0x00000000, False, False, 0x00000000, 0x3010BF7F, 0x00000000, 'CRC-32/AIXM', 'CRC-32Q')
    AUTOSAR    = CRC(32, 0xF4ACFB13, 0xFFFFFFFF, True,  True,  0xFFFFFFFF, 0x1697D06A, 0x904CDDBF, 'CRC-32/AUTOSAR')
    BASE91_D   = CRC(32, 0xA833982B, 0xFFFFFFFF, True,  True,  0xFFFFFFFF, 0x87315576, 0x45270551, 'CRC-32/BASE91-D', 'CRC-32D')
    BZIP2      = CRC(32, 0x04C11DB7, 0xFFFFFFFF, False, False, 0xFFFFFFFF, 0xFC891918, 0xC704DD7B, 'CRC-32/BZIP2', 'CRC-32/AAL5, CRC-32/DECT-B, B-CRC-32')
    CD_ROM_EDC = CRC(32, 0x8001801B, 0x00000000, True,  True,  0x00000000, 0x6EC2EDC4, 0x00000000, 'CRC-32/CD-ROM-EDC')
    CKSUM      = CRC(32, 0x04C11DB7, 0x00000000, False, False, 0xFFFFFFFF, 0x765E7680, 0xC704DD7B, 'CRC-32/CKSUM', 'CKSUM, CRC-32/POSIX')
    ISCSI      = CRC(32, 0x1EDC6F41, 0xFFFFFFFF, True,  True,  0xFFFFFFFF, 0xE3069283, 0xB798B438, 'CRC-32/ISCSI', 'CRC-32/BASE91-C, CRC-32/CASTAGNOLI, CRC-32/INTERLAKEN, CRC-32C, CRC-32/NVME')
    ISO_HDLC   = CRC(32, 0x04C11DB7, 0xFFFFFFFF, True,  True,  0xFFFFFFFF, 0xCBF43926, 0xDEBB20E3, 'CRC-32/ISO-HDLC', 'CRC-32, CRC-32/ADCCP, CRC-32/V-42, CRC-32/XZ, PKZIP')
    JAMCRC     = CRC(32, 0x04C11DB7, 0xFFFFFFFF, True,  True,  0x00000000, 0x340BC6D9, 0x00000000, 'CRC-32/JAMCRC', 'JAMCRC')
    MEF        = CRC(32, 0x741B8CD7, 0xFFFFFFFF, True,  True,  0x00000000, 0xD2C22F51, 0x00000000, 'CRC-32/MEF')
    MPEG_2     = CRC(32, 0x04C11DB7, 0xFFFFFFFF, False, False, 0x00000000, 0x0376E6E7, 0x00000000, 'CRC-32/MPEG-2')
    XFER       = CRC(32, 0x000000AF, 0x00000000, False, False, 0x00000000, 0xBD0BE338, 0x00000000, 'CRC-32/XFER', 'XFER')


class CRC40:
    """Collection of 40-bit CRC models.

    ```
    MODEL  POLY          INIT          REFIN  REFOUT  XOROUT        CHECK         RESIDUE
    GSM    0x0004820009  0x0000000000  False  False   0xFFFFFFFFFF  0xD4164FC646  0xC4FF8071FF
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    GSM = CRC(40, 0x0004820009, 0x0000000000, False, False, 0xFFFFFFFFFF, 0xD4164FC646, 0xC4FF8071FF, 'CRC-40/GSM')


class CRC64:
    """Collection of 64-bit CRC models.

    ```
    MODEL     POLY                INIT                REFIN  REFOUT  XOROUT              CHECK               RESIDUE
    ECMA_182  0x42F0E1EBA9EA3693  0x0000000000000000  False  False   0x0000000000000000  0x6C40DF5F0B497347  0x0000000000000000
    GO_ISO    0x000000000000001B  0xFFFFFFFFFFFFFFFF  True   True    0xFFFFFFFFFFFFFFFF  0xB90956C775A41001  0x5300000000000000
    MS        0x259C84CBA6426349  0xFFFFFFFFFFFFFFFF  True   True    0x0000000000000000  0x75D4B74F024ECEEA  0x0000000000000000
    NVME      0xAD93D23594C93659  0xFFFFFFFFFFFFFFFF  True   True    0xFFFFFFFFFFFFFFFF  0xAE8B14860A799888  0xF310303B2B6F6E42
    REDIS     0xAD93D23594C935A9  0x0000000000000000  True   True    0x0000000000000000  0xE9C6D914C4B8D9CA  0x0000000000000000
    WE        0x42F0E1EBA9EA3693  0xFFFFFFFFFFFFFFFF  False  False   0xFFFFFFFFFFFFFFFF  0x62EC59E3F1A4F00A  0xFCACBEBD5931A992
    XZ        0x42F0E1EBA9EA3693  0xFFFFFFFFFFFFFFFF  True   True    0xFFFFFFFFFFFFFFFF  0x995DC9BBDF1939FA  0x49958C9ABD7D353F
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    ECMA_182 = CRC(64, 0x42F0E1EBA9EA3693, 0x0000000000000000, False, False, 0x0000000000000000, 0x6C40DF5F0B497347, 0x0000000000000000, 'CRC-64/ECMA-182', 'CRC-64')
    GO_ISO   = CRC(64, 0x000000000000001B, 0xFFFFFFFFFFFFFFFF, True,  True,  0xFFFFFFFFFFFFFFFF, 0xB90956C775A41001, 0x5300000000000000, 'CRC-64/GO-ISO')
    MS       = CRC(64, 0x259C84CBA6426349, 0xFFFFFFFFFFFFFFFF, True,  True,  0x0000000000000000, 0x75D4B74F024ECEEA, 0x0000000000000000, 'CRC-64/MS')
    NVME     = CRC(64, 0xAD93D23594C93659, 0xFFFFFFFFFFFFFFFF, True,  True,  0xFFFFFFFFFFFFFFFF, 0xAE8B14860A799888, 0xF310303B2B6F6E42, 'CRC-64/NVME')
    REDIS    = CRC(64, 0xAD93D23594C935A9, 0x0000000000000000, True,  True,  0x0000000000000000, 0xE9C6D914C4B8D9CA, 0x0000000000000000, 'CRC-64/REDIS')
    WE       = CRC(64, 0x42F0E1EBA9EA3693, 0xFFFFFFFFFFFFFFFF, False, False, 0xFFFFFFFFFFFFFFFF, 0x62EC59E3F1A4F00A, 0xFCACBEBD5931A992, 'CRC-64/WE')
    XZ       = CRC(64, 0x42F0E1EBA9EA3693, 0xFFFFFFFFFFFFFFFF, True,  True,  0xFFFFFFFFFFFFFFFF, 0x995DC9BBDF1939FA, 0x49958C9ABD7D353F, 'CRC-64/XZ', 'CRC-64/GO-ECMA')


class CRC82:
    """Collection of 82-bit CRC models.

    ```
    MODEL  POLY                     INIT                     REFIN  REFOUT  XOROUT                   CHECK                    RESIDUE
    DARC   0x0308C0111011401440411  0x000000000000000000000  True   True    0x000000000000000000000  0x09EA83F625023801FD612  0x000000000000000000000
    ```
    Source: https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    DARC = CRC(82, 0x0308C0111011401440411, 0x000000000000000000000, True,  True,  0x000000000000000000000, 0x09EA83F625023801FD612, 0x000000000000000000000, 'CRC-82/DARC')


# Stop populating the CRC._catalog
CRC._populate = False
