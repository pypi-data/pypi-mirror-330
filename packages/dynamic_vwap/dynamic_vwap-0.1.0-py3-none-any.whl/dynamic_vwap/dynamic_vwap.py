import keras
from keras import ops
from keras.models import Model, Sequential
from keras.initializers import Initializer
from keras.layers import Dense
from tkan import TKAN


@keras.utils.register_keras_serializable(name="EqualInitializer")
class EqualInitializer(Initializer):
    """Initializes weights to 1/n_ahead."""
    
    def __init__(self, n_ahead):
        self.n_ahead = n_ahead
        
    def __call__(self, shape, dtype=None):
        return ops.ones(shape, dtype=dtype) / self.n_ahead

        
    def get_config(self):
        return {'n_ahead': self.n_ahead}


@keras.utils.register_keras_serializable(name="PositiveSumToOneConstraint")
class PositiveSumToOneConstraint(keras.constraints.Constraint):
    """Constrains the weights to be positive and sum to 1."""
    
    def __call__(self, w):
        # First ensure values are positive
        w = keras.ops.maximum(w, 0)
        # Then normalize to sum to 1
        return w / (keras.ops.sum(w) + keras.backend.epsilon())

    def get_config(self):
        return {}


@keras.utils.register_keras_serializable(name="DynamicVWAP")
class DynamicVWAP(Model):
    def __init__(self, lookback, n_ahead, hidden_size=100, hidden_rnn_layer=2, *args, **kwargs):
        super(DynamicVWAP, self).__init__(*args, **kwargs)
        self.lookback = lookback
        self.n_ahead = n_ahead
        self.hidden_size = hidden_size
        self.hidden_rnn_layer = hidden_rnn_layer
        
    def build(self, input_shape):
        feature_shape = input_shape
        assert feature_shape[1] == self.lookback + self.n_ahead - 1
        self.internal_rnn = Sequential([
            TKAN(self.hidden_size, return_sequences=True)
            for _ in range(self.hidden_rnn_layer)
        ])
        self.internal_rnn.build(feature_shape)    
        internal_model_output_shape = self.internal_rnn.compute_output_shape(feature_shape)
        self.internal_hidden_to_volume = [
            Sequential([
                Dense(self.hidden_size, activation='relu'),
                Dense(self.hidden_size, activation='relu'),
                Dense(1, activation='tanh') 
            ])
            for _ in range(self.n_ahead - 1)
        ]
        for i in range(self.n_ahead - 1):
            self.internal_hidden_to_volume[i].build((feature_shape[0], self.hidden_size + i))
        self.base_volume_curve = self.add_weight(
            shape=(self.n_ahead,),
            name="base_curve",
            initializer=EqualInitializer(self.n_ahead),
            constraint=PositiveSumToOneConstraint(),  # Using the new constraint
            trainable=True
        )
        super().build(input_shape)

    def call(self, inputs):
        features = inputs
        rnn_hidden = self.internal_rnn(features)
        total_volume = ops.zeros((ops.shape(features)[0],1))
        
        for t in range(0, self.n_ahead - 1):
            if t>0:
                current_hidden = ops.concatenate([rnn_hidden[:, self.lookback + t, :], volume_curve], axis=1)
            else:
                current_hidden = rnn_hidden[:, self.lookback + t, :]
            estimated_factor = 1. + self.internal_hidden_to_volume[t](current_hidden)
            estimated_volume = self.base_volume_curve[t] * estimated_factor 
            estimated_volume = keras.ops.clip(estimated_volume, 0., 1. - total_volume)
            total_volume += estimated_volume
            if t==0:
                volume_curve=estimated_volume
            else:
                volume_curve=ops.concatenate([volume_curve, estimated_volume], axis=1)
            
        estimated_volume=1. - total_volume
        volume_curve=ops.concatenate([volume_curve, estimated_volume], axis=1)
        volume_curve=ops.expand_dims(volume_curve, axis=2)
        results = keras.ops.concatenate([volume_curve, keras.ops.zeros_like(volume_curve)], axis=-1)
        return results

    def get_config(self):
        config = super().get_config()
        config.update({
            'lookback': self.lookback,
            'n_ahead': self.n_ahead,
            'hidden_size': self.hidden_size,
            'hidden_rnn_layer': self.hidden_rnn_layer,
        })
        return config

    def compute_output_shape(self, input_shape):
        return (input_shape[0], 2, self.n_ahead)