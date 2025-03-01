from __future__ import annotations

from typing import Union, Optional, List, TypeVar, Dict

import yaml
from pydantic import BaseModel, StrictInt, StrictStr, StrictBool, field_validator

TField = TypeVar("TField", bound="IField")


class IField(BaseModel):
    """Base class for all intent fields."""

    is_nullable: StrictBool = False

    class Config:
        extra = "forbid"
        frozen = True

    def __repr__(self):
        return yaml.dump(self.model_dump())

    def as_nullable(self) -> TField:
        """Make this field nullable.

        Returns:
            TField: the nullable version of this field.

        """
        return self.model_copy(update={"is_nullable": True})


class IStr(IField):
    """Class representing a string-valued field in an intent."""

    max_tokens: StrictInt
    regex: Union[StrictStr, None]
    stop: Union[StrictStr, List[StrictStr], None]


class IEnum(IField):
    """Class representing an enum-valued field in an intent. This is a value that can take on one of a discrete set of
    string values.

    """

    options: List[StrictStr]

    @field_validator("options")
    @classmethod
    def assert_non_empty(cls, v):
        if isinstance(v, (list, tuple)) and len(v) < 2:
            raise ValueError("Enum must have at least two options.")
        return v


class IInt(IField):
    """Class representing an integer-valued field in an intent."""

    values: List[StrictInt]
    allow_negative: StrictBool


class IReal(IField):
    """Class representing a real (continuous number) valued field in an intent."""

    allow_negative: StrictBool


class IBool(IField):
    """Class representing a boolean-valued field in an intent."""


class IConst(IField):
    """Class representing a constant-value field in an intent."""

    value: StrictStr


class IObj(IField):
    """Class representing a structured object with fixed fields."""

    fields: Dict[str, Union[IDict, IArr, IObj, IEnum, IStr, IBool, IReal, IInt, str]]

    @field_validator("fields")
    @classmethod
    def validate_fields(cls, v):
        if len(v) == 0:
            raise ValueError("Obj must have at least one field.")
        return v


class IDict(IField):
    """Class representing a variable-sized dictionary with string-valued keys and items of the same defined type."""

    obj: Union[IDict, IArr, IObj, IEnum, IStr, IBool, IReal, IInt]
    keys: Union[IStr, IEnum, List[StrictStr]]


class IArr(IField):
    """Class representing a variable length array intent field with a defined element type."""

    min_len: StrictInt
    max_len: Union[None, StrictInt]
    obj: Union[IDict, IArr, IObj, IEnum, IStr, IBool, IReal, IInt]


IObj.model_rebuild()
IDict.model_rebuild()


class Fns:

    @staticmethod
    def str(
        max_tokens: Optional[int] = 8000,
        regex: Optional[str] = None,
        stop: Optional[List[str]] = None,
    ) -> IStr:
        """Create a string-type intent field.

        Args:
            max_tokens (Optional[int]): max number of tokens when generating a string.
            regex (Optional[str]): regex to apply to string generation.
            stop (Optional[List[str]]): stop string that stop the generation process.

        Returns:
            IStr: the string intent field.

        """
        return IStr(max_tokens=max_tokens, regex=regex, stop=stop)

    @staticmethod
    def int(
        values: Optional[List[int]] = None, allow_negative: Optional[bool] = True
    ) -> IInt:
        """Create an int-type intent field.

        Args:
            values (Optional[List[int]]): optional finite set of values to choose from. If not given the field can be
            any integer value.
            allow_negative (Optional[bool]): whether negative values can be generated (default = True)

        Returns:
            IInt: the int intent field.

        """
        values = [] if values is None else values
        return IInt(values=list(values), allow_negative=allow_negative)

    @staticmethod
    def real(allow_negative: Optional[bool] = True) -> IReal:
        """Create a real-type intent field.

        Args:
            allow_negative (Optional[bool]): whether negative values can be generated (default = True)

        Returns:
            IReal: the real intent field.

        """
        return IReal(allow_negative=allow_negative)

    @staticmethod
    def bool() -> IBool:
        """Create a bool-valued intent field.

        Returns:
            IBool: the bool intent field.

        """
        return IBool()

    @staticmethod
    def enum(*fields: str) -> IEnum:
        """Create an enum-valued intent field.

        Args:
            *fields (str): the possible values of the enum.

        Returns:
            IEnum: the enum intent field.

        """
        return IEnum(options=list(fields))

    @staticmethod
    def date() -> IStr:
        """Create a date-valued intent field.

        This will create a string field that is constrained to form an ISO-format date.

        Returns:
            IStr: the string field that is constrained to generate date strings

        """
        return Fns.str(regex=r"\d{4}-\d{2}-\d{2}")

    @staticmethod
    def datetime() -> IStr:
        """Create a datetime-valued intent field.

        This will create a string field that is constrained to form an ISO-format datetime.

        Returns:
            IStr: the string field that is constrained to generate datetime strings

        """
        return Fns.str(regex=r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}")

    @staticmethod
    def arr(obj, min_len: Optional[int] = 0, max_len: Optional[int] = None) -> IArr:
        """Create an array-valued intent field with a given element type and min/max length.

        Args:
            obj (IField): the element definition.
            min_len (Optional[int]): the min length of the array (default = 0)
            max_len (Optional[int]): the max length of the array (default = None)

        Returns:
            IArr: the array field.

        """
        return IArr(min_len=min_len, max_len=max_len, obj=obj)

    @staticmethod
    def dict(obj, keys: Optional[List[str]] = None) -> IDict:
        """Create a dictionary-valued intent field where the keys are string and the values are a given type.
        Keys can be restricted to a particular set of string values.

        Args:
            obj (IField): the object definition for dictionary values.
            keys (Optional[List[str]]): an optional list of field values to choose from. If not specified the keys can
            be any string and are unconstrained.

        Returns:
            IDict: the dict field.

        """
        if keys is None:
            keys = Fns.str()
        return IDict(obj=obj, keys=keys)

    @staticmethod
    def obj(**fields) -> IObj:
        """Create an object-valued field with a fixed structure. This structure consists of named fields with
        particular intent field types.

        Args:
            **fields: IField: keyword args where the keyword defines the fields of the object and the value defines the
            field value.

        Returns:
            IObj: the object field.

        """
        return IObj(fields=dict(fields))


intent = Fns()
