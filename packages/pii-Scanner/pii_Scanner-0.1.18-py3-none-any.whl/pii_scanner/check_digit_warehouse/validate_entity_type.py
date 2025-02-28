from pii_scanner.check_digit_warehouse.verification_required_list import VERIFY_ENTITIES
from typing import Dict, List, Union
import logging
from pii_scanner.check_digit_warehouse.checker import validate_check_digit


logger = logging.getLogger(__name__)


async def validate_entity_check_digit(entity_text: str, entity_type: str, region: str) -> Dict[str, Union[str, List[Dict[str, Union[str, bool]]]]]:
    """
    Validates an entity's check digit based on country-specific rules and updates the entity information.
    """
    # Fetch country-specific verification requirements
    verify_required = VERIFY_ENTITIES.get(region, [])
    if not verify_required:
        logger.warning(f"No verification rules defined for country: {region}")
        return {"entity_detected": [{"type": entity_type, "text": entity_text}], "check_digit": False}

    # Check if the entity type requires verification
    if entity_type not in verify_required:
        logger.info(f"Entity type {entity_type} does not require verification.")
        return {"entity_detected": [{"type": entity_type, "text": entity_text}], "check_digit": False}

    # Validate entity using check digit logic
    validation_result = validate_check_digit(entity_text, region)

    # Initialize entity dictionary to update
    entity = {"type": entity_type, "text": entity_text}

    if validation_result and validation_result.get("success"):
        # Update the entity type and add check digit success
        entity["type"] = validation_result.get("type")
        entity["check_digit"] = True
        return {"entity_detected": [entity], "check_digit": True}
    else:
        logger.info(f"Entity {entity_text} of type {entity_type} failed validation.")
        return {"entity_detected": [entity], "check_digit": False}
