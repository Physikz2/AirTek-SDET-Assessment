"""Nested Pydantic contracts for user, address, geo, and company responses."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Geo(BaseModel):
    """Goal: validate geographic coordinate fields nested in a user address.

    Assertion: latitude and longitude values are represented as strings by the API.
    SDET Rationale: nested contract checks catch partial payload regressions.
    """

    model_config = ConfigDict(extra="ignore")

    lat: str
    lng: str


class Address(BaseModel):
    """Goal: validate the address object nested in a GET `/users` record.

    Assertion: address text fields and the nested Geo contract are present.
    SDET Rationale: address consumers rely on the full nested object, not only user basics.
    """

    model_config = ConfigDict(extra="ignore")

    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


class Company(BaseModel):
    """Goal: validate the company object nested in a GET `/users` record.

    Assertion: company name, catch phrase, and business description are strings.
    SDET Rationale: nested business metadata must remain structurally stable.
    """

    model_config = ConfigDict(extra="ignore")

    name: str
    catchPhrase: str
    bs: str


class User(BaseModel):
    """Goal: validate the complete nested record returned by GET `/users`.

    Assertion: identity, validated email, address, and company contracts all pass.
    SDET Rationale: deep validation protects consumers from silently malformed user data.
    """

    model_config = ConfigDict(extra="ignore")

    id: int = Field(ge=1)
    name: str
    username: str
    email: EmailStr
    address: Address
    phone: str
    website: str
    company: Company
