# XtrapNet

XtrapNet is a robust package for extrapolation control in neural networks. It provides advanced uncertainty quantification, ensemble methods, and fallback mechanisms to improve predictions in out-of-distribution regions.

## Installation
pip install xtrapnet

## Usage
from xtrapnet import XtrapNet, XtrapTrainer, XtrapController

net = XtrapNet(input_dim=2)
trainer = XtrapTrainer(net, num_epochs=100)
trainer.train(labels, features)
xtrap_ctrl = XtrapController(trained_model=net, train_features=features, train_labels=labels, mode='clip')

predictions = xtrap_ctrl.predict([[0.5, 0.5]])
print(predictions)
License
MIT License 