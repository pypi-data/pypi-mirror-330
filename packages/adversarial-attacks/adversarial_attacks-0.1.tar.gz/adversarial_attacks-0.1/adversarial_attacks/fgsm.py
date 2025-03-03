import torch
import torch.nn as nn

class FGSM:
    def __init__(self, model, epsilon=0.03):
        """
        Fast Gradient Sign Method (FGSM) attack.
        :param model: PyTorch model
        :param epsilon: Attack strength
        """
        self.model = model
        self.epsilon = epsilon

    def perturb(self, image, label):
        """
        Generates an adversarial example.
        :param image: Input image tensor
        :param label: True label tensor
        :return: Adversarial image
        """
        image.requires_grad = True
        output = self.model(image)
        loss = nn.CrossEntropyLoss()(output, label)
        loss.backward()
        perturbed_image = image + self.epsilon * image.grad.sign()
        return torch.clamp(perturbed_image, 0, 1)  # Keep pixel values valid
