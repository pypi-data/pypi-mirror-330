from typing import Tuple, Optional, Dict, Any

from metaml.meta_models.parameters import ParametersModel


class Params(ParametersModel):
    order: Tuple[int, int, int]
    seasonal_order: Tuple[int, int, int]
    season_length: int = 1
    include_mean: bool = True
    include_drift: bool = False
    blambda: Optional[float] = None
    biasadj: bool = False

    def __init__(self, p: int = 0, d: int = 0, q: int = 0, P: int = 0, D: int = 0, Q: int = 0, **kwargs):
        super().__init__(order=(p, d, q), seasonal_order=(P, D, Q), **kwargs)

    @property
    def external_representation(self) -> Dict[str, Any]:
        external_representation: Dict = super().external_representation

        # Extract individual components from order and seasonal_order
        p, d, q = self.order
        P, D, Q = self.seasonal_order

        # Update keys in external representation
        external_representation.update({"p": p, "d": d, "q": q, "P": P, "D": D, "Q": Q})

        # Remove the old keys
        external_representation.pop("order", None)
        external_representation.pop("seasonal_order", None)

        return external_representation
