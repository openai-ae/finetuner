import abc

import paddle
import paddle.nn.functional as F
from paddle import nn


class HeadLayer(nn.Layer):
    default_loss: nn.Layer  #: the recommended loss function to be used when equipping this layer to base model
    arity: int

    def __init__(self, arity_model: nn.Layer):
        super().__init__()
        self._arity_model = arity_model

    def forward(self, *inputs):
        return self.call(*self._arity_model(*inputs))

    @abc.abstractmethod
    def call(self, *args, **kwargs):
        ...


class CosineLayer(HeadLayer):
    default_loss = nn.MSELoss()
    arity = 2

    def call(self, lvalue, rvalue):
        return F.cosine_similarity(lvalue, rvalue)


class TripletLayer(HeadLayer):
    default_loss = nn.MSELoss()
    arity = 3

    def __init__(self, arity_model: nn.Layer, margin: float = 1.0):
        super().__init__(arity_model)
        self._margin = margin

    def call(self, anchor, positive, negative):
        dist_pos = paddle.pow(anchor - positive, 2).sum(axis=1)
        dist_neg = paddle.pow(anchor - negative, 2).sum(axis=1)

        return F.relu(dist_pos - dist_neg + self._margin)