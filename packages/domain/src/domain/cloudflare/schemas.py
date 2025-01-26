from loguru  import logger as log

from pydantic import BaseModel, Field, field_validator, ValidationError, computed_field


class CloudflareAccountSettingsBase(BaseModel):
    enforce_twofactor: bool
    api_access_enabled: bool
    use_account_custom_ns_by_default: bool
    default_nameservers: str | None = Field(default=None)
    abuse_contact_email: str | None = Field(default=None)
    legacy_flags: dict | None = Field(default_factory={})
    created_on: str


class CloudflareAccountSettingsIn(CloudflareAccountSettingsBase):
    pass


class CloudflareAccountSettingsOut(CloudflareAccountSettingsBase):
    account_settings_id: int


class CloudflareAccountBase(BaseModel):
    id: str
    name: str
    type: str | None = Field(default=None)


class CloudflareAccountIn(CloudflareAccountBase):
    pass


class CloudflareAccountOut(CloudflareAccountBase):
    account_id: int
    

class CloudflareZoneMetaBase(BaseModel):
    custom_certificate_quota: int
    page_rule_quota: int
    phishing_detected: bool
    step: int
    
    
class CloudflareZoneMetaIn(CloudflareZoneMetaBase):
    pass


class CloudflareZoneMetaOut(CloudflareZoneMetaBase):
    zone_meta_id: int
    
    
class CloudflareZoneOwnerBase(BaseModel):
    email: str | None = Field(default=None)
    id: str | None = Field(default=None)
    type: str | None = Field(default=None)
    

class CloudflareZoneOwnerIn(CloudflareZoneOwnerBase):
    pass


class CloudflareZoneOwnerOut(CloudflareZoneOwnerBase):
    zone_owner_id: int


class CloudflareZonePlanBase(BaseModel):
    can_subscribe: bool
    currency: str
    externally_managed: bool
    frequency: str | None = Field(default=None)
    id: str
    is_subscribed: bool
    legacy_discount: bool
    name: str
    price: float


class CloudflareZonePlanIn(CloudflareZonePlanBase):
    pass


class CloudflareZonePlanOut(CloudflareZonePlanBase):
    zone_plan_id: int


class CloudflareZoneTenantBase(BaseModel):
    id: str | None = Field(default=None)
    

class CloudflareZoneTenantIn(CloudflareZoneTenantBase):
    name: str | None = Field(default=None)

class CloudflareZoneTenantOut(CloudflareZoneTenantBase):
    zone_tenant_id: int
    name: str | None = Field(default=None)
    
    
class CloudflareZoneTenantUnitIn(CloudflareZoneTenantBase):
    pass


class CloudflareZoneTenantUnitOut(CloudflareZoneTenantBase):
    zone_tenant_unit_id: int


class CloudflareZoneBase(BaseModel):
    account: CloudflareAccountIn
    activated_on: str
    created_on: str
    development_mode: int
    id: str
    meta: CloudflareZoneMetaIn
    modified_on: str
    name_servers: list[str] | None = Field(default_factory=[])
    original_dnshost: str | None = Field(default=None)
    original_name_servers: list[str] | None = Field(default_factory=[])
    original_registrar: str | None = Field(default=None)
    owner: CloudflareZoneOwnerIn
    paused: bool
    permissions: list[str] | None = Field(default_factory=[])
    plan: CloudflareZonePlanIn
    status: str
    tenant: CloudflareZoneTenantIn
    tenant_unit: CloudflareZoneTenantUnitIn    
    
    
class CloudflareZoneIn(CloudflareZoneBase):
    pass


class CloudflareZoneOut(CloudflareZoneBase):
    zone_id: int


class CloudflareWAFFilterBase(BaseModel):
    id: str
    expression: str | None = Field(default=None)
    paused: bool
    
    
class CloudflareWAFFilterIn(CloudflareWAFFilterBase):
    pass


class CloudflareWAFFilterOut(CloudflareWAFFilterBase):
    waf_filter_id: int
    
    
class CloudflareWAFFilterIn(BaseModel):
    pass


class CloudflareWAFFilterOut(BaseModel):
    waf_filter_id: int


## DTOs
# class CloudflareZonesBase(BaseModel):
#     zones: list[CloudflareZoneBase] = Field(default_factory=[])


# class CloudflareZones(CloudflareZonesBase):
#     pass
