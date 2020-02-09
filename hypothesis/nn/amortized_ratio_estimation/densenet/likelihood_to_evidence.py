import hypothesis
import hypothesis.nn
import hypothesis.nn.densenet
import torch

from hypothesis.nn import DenseNetHead
from hypothesis.nn import MultiLayeredPerceptron



class LikelihoodToEvidenceRatioEstimatorDenseNet(BaseLikelihoodToEvidenceRatioEstimator):

    def __init__(self,
        shape_inputs,
        shape_outputs,
        activation=hypothesis.default.activation,
        batchnorm=hypothesis.nn.densenet.default.batchnorm,
        bottleneck_factor=hypothesis.nn.densenet.default.bottleneck_factor,
        channels=hypothesis.nn.densenet.default.channels,
        convolution_bias=hypothesis.nn.densenet.default.convolution_bias,
        depth=hypothesis.nn.densenet.default.depth,
        dropout=hypothesis.default.dropout,
        trunk_activation=None,
        trunk_dropout=None,
        trunk_layers=hypothesis.default.trunk):
        super(LikelihoodToEvidenceRatioEstimatorDenseNet, self).__init__()
        # Allocate the DenseNet head.
        self.head = DenseNetHead(
            shape_xs=shape_outputs,
            activation=activation,
            batchnorm=batchnorm,
            bottleneck_factor=bottleneck_factor,
            channels=channels,
            convolution_bias=convolution_bias,
            depth=depth,
            dropout_dropout)
        # Compute the dimensionality of the inputs.
        self.dimensionality = len(shape_xs)
        # Construct the convolutional DenseNet head.
        self.head = DenseNetHead(
            activation=activation,
            batchnorm=batchnorm,
            bottleneck_factor=bottleneck_factor,
            channels=channels,
            convolution_bias=convolution_bias,
            depth=depth,
            dropout=dropout,
            shape_xs=shape_xs)
        # Compute the embedding dimensionality of the head.
        embedding_dim = self.head.embedding_dimensionality()
        # Allocate the trunk.
        latent_dimensionality = compute_dimensionality(shape_inputs) + self.head.embedding_dimensionality()
        self.trunk = MultiLayeredPerceptron(
            shape_xs=(latent_dimensionality,),
            shape_ys=(1,),
            activation=trunk_activation,
            dropout=trunk_dropout,
            layers=trunk_layers,
            transform_output=None)

    def log_ratio(self, inputs, outputs):
        z_outputs = self.head(outputs)
        z = torch.cat([inputs, z_outputs], dim=1)
        log_ratios = self.trunk(z)

        return log_ratios
