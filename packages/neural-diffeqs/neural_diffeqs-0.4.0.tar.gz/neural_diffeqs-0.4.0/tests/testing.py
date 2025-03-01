import os
import torch


def load_install_torchsde():
    """Try importing torchsde. If not installed, it will be installed and imported."""
    try:
        import torchsde
    except:
        os.system("pip install torchsde")
        import torchsde

    return torchsde

def test_sdeint(
    SDE, y0=torch.randn([200, 50]), t=torch.Tensor([0, 0.5, 1.0]), **kwargs
):
    torchsde = load_install_torchsde()
    """Generate some random data and test the ODE as it's passed through torchsde.sdeint."""
    return torchsde.sdeint(SDE, y0, t, dt=0.1, **kwargs)