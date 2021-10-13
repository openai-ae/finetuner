# Tuner

Tuner is one of the three key components of Finetuner. Given an {term}`embedding model` and {term}`labeled data`, Tuner
trains the model to fit the data.

Labeled data can be constructed {ref}`by following this<construct-labeled-data>`.

## Fit method

Tuner can be called via `finetuner.fit()`:

```python
import finetuner

finetuner.fit(
    embed_model,
    train_data,
    **kwargs   
)
```


Here, `embed_model` must be {term}`embedding model`; and `train_data` must be {term}`labeled data`.


Besides, it accepts the following `**kwargs`:

|Argument| Description |
|---|---|
|`eval_data` | the evaluation data (same format as `train_data`) to be used on every epoch|
|`batch_size`| the number of `Document` in each batch|
|`epochs` |the number of epochs for training |

## Examples

### Tune a simple MLP on Fashion-MNIST

1. Write an embedding model. An embedding model can be written in Keras/PyTorch/Paddle. It can be either a new model or
   an existing model with pretrained weights. Below we construct a `784x128x32` MLP that transforms Fashion-MNIST images
   into 32-dim vectors.

    ````{tab} PyTorch
    ```python
    import torch
    embed_model = torch.nn.Sequential(
          torch.nn.Flatten(),
          torch.nn.Linear(in_features=28 * 28, out_features=128),
          torch.nn.ReLU(),
          torch.nn.Linear(in_features=128, out_features=32))
    ```
   
    ````
    ````{tab} Keras
    ```python
    import tensorflow as tf
    embed_model = tf.keras.Sequential([
                tf.keras.layers.Flatten(input_shape=(28, 28)),
                tf.keras.layers.Dense(128, activation='relu'),
                tf.keras.layers.Dense(32)
            ])
    ```
    ````
    ````{tab} Paddle
    ```python
    import paddle
    embed_model = paddle.nn.Sequential(
          paddle.nn.Flatten(),
          paddle.nn.Linear(in_features=28 * 28, out_features=128),
          paddle.nn.ReLU(),
          paddle.nn.Linear(in_features=128, out_features=32))
    ```
   
    ````

2. Build labeled match data {ref}`according to the steps in here<build-mnist-data>`. One can refer
   to `finetuner.toydata.generate_fashion_match` for an implementation. In this example, for each `Document` we generate 10 positive matches and 10 negative matches.

3. Feed labeled data and the embedding model into Finetuner:
    ```python
    import finetuner
    from finetuner.toydata import generate_fashion_match

    finetuner.fit(
        embed_model,
        train_data=lambda: generate_fashion_match(num_pos=10, num_neg=10),
        eval_data=lambda: generate_fashion_match(num_pos=10, num_neg=10, is_testset=True)
    )
    ```

By default, `head_layer` is set to `CosineLayer`, one can also use `TripletLayer`:

````{tab} CosineLayer

```{figure} mlp.cosine.png
:align: center
```

````

````{tab} TripletLayer

```{figure} mlp.triplet.png
:align: center
```

````

### Tune a bidirectional LSTM on Covid QA

1. Write an embedding model.

  ````{tab} Keras
  ```python
  import tensorflow as tf
  embed_model = tf.keras.Sequential([
         tf.keras.layers.Embedding(input_dim=5000, output_dim=64),
         tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
         tf.keras.layers.Dense(32)])
  ```
  ````

  ````{tab} PyTorch
  ```python
  import torch
  class LastCell(torch.nn.Module):
    def forward(self, x):
      out, _ = x
      return out[:, -1, :]

  embed_model = torch.nn.Sequential(
    torch.nn.Embedding(num_embeddings=5000, embedding_dim=64),
    torch.nn.LSTM(64, 64, bidirectional=True, batch_first=True),
    LastCell(),
    torch.nn.Linear(in_features=2 * 64, out_features=32))
  ```
  ````

  ````{tab} Paddle
  ```python
  import paddle
  class LastCell(paddle.nn.Layer):
     def forward(self, x):
         out, _ = x
         return out[:, -1, :]

  embed_model = paddle.nn.Sequential(
     paddle.nn.Embedding(num_embeddings=5000, embedding_dim=64),
     paddle.nn.LSTM(64, 64, direction='bidirectional'),
     LastCell(),
     paddle.nn.Linear(in_features=2 * 64, out_features=32))
  ```
  ````

2. Build labeled match data {ref}`according to the steps in here<build-qa-data>`. One can refer
   to `finetuner.toydata.generate_qa_match` for an implementation.

3. Feed labeled data and the embedding model into Finetuner:

    ```python
    import finetuner
    from finetuner.toydata import generate_qa_match

    finetuner.fit(
        embed_model,
        train_data=lambda: generate_qa_match(num_neg=5),
        eval_data=lambda: generate_qa_match(num_neg=5)
    )
    ```

By default, `head_layer` is set to `CosineLayer`, one can also use `TripletLayer`:

````{tab} CosineLayer

```{figure} lstm.cosine.png
:align: center
```

````

````{tab} TripletLayer

```{figure} lstm.triplet.png
:align: center
```

````

