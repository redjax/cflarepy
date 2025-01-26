from loguru import logger as log

from pydantic import BaseModel, Field, field_validator, ValidationError, computed_field

from ..schemas import (
    CloudflareZoneBase,
    CloudflareAccountIn,
    CloudflareAccountOut,
    CloudflareAccountSettingsIn,
    CloudflareAccountSettingsOut,
    CloudflareWAFFilterIn,
    CloudflareWAFFilterOut,
    CloudflareZoneIn,
    CloudflareZoneOut,
    CloudflareZoneMetaIn,
    CloudflareZoneMetaOut,
    CloudflareZoneOwnerIn,
    CloudflareZoneOwnerOut,
    CloudflareZonePlanIn,
    CloudflareZonePlanOut,
    CloudflareZoneTenantIn,
    CloudflareZoneTenantOut,
    CloudflareZoneTenantUnitIn,
    CloudflareZoneTenantUnitOut
)

class CloudflareZonesBase(BaseModel):
    zones: list[CloudflareZoneBase] = Field(default_factory=[])


class CloudflareZones(CloudflareZonesBase):
    pass