from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.helpers.typing import ConfigType
import voluptuous as vol
import logging

DOMAIN = "custom_event"
_LOGGER = logging.getLogger(__name__)

CALL_SCHEMA = vol.Schema(
    {
        vol.Required("event_type"): vol.All(str, vol.Length(min=1, max=64)),
        vol.Optional("event_data", default={}): dict,
    }
)


async def async_setup(hass: HomeAssistant, config: ConfigType):
    async def handle_fire(call: ServiceCall):
        event_type = call.data.get("event_type")
        event_data = call.data.get("event_data")
        _LOGGER.debug("Firing event %s with data: %s", event_type, event_data)
        hass.bus.async_fire(event_type, event_data)
        return {"event": event_type, "sent": True}

    hass.services.async_register(
        DOMAIN, "fire", handle_fire, CALL_SCHEMA, supports_response=SupportsResponse.OPTIONAL
    )
    return True
