from typing import Optional


from metaml.meta_models.parameters import ParametersModel


class Params(ParametersModel):
    window_length: Optional[int] = 10
