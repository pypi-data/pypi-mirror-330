from threedi_api_client.openapi.models import (
    ArrivalTimePostProcessing,
    BasicPostProcessing,
    DamagePostProcessing,
)

from .base import LizardPostprocessingWrapper


class LizardBasicPostprocessingWrapper(LizardPostprocessingWrapper):
    model = BasicPostProcessing
    api_path: str = "basic"
    scenario_name = model.__name__.lower()


class LizardDamagePostprocessingWrapper(LizardPostprocessingWrapper):
    model = DamagePostProcessing
    api_path: str = "damage"
    scenario_name = model.__name__.lower()


class LizardArrivalPostprocessingWrapper(LizardPostprocessingWrapper):
    model = ArrivalTimePostProcessing
    api_path: str = "arrival"
    scenario_name = model.__name__.lower()


WRAPPERS = [
    LizardBasicPostprocessingWrapper,
    LizardDamagePostprocessingWrapper,
    LizardArrivalPostprocessingWrapper,
]
