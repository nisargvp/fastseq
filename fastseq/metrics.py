# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/11_metrics.ipynb (unless otherwise specified).

__all__ = ['mape', 'smape', 'SMAPELossFlat', 'mase']

# Cell
from fastcore.utils import *
from fastcore.imports import *
from fastai2.basics import *
from .data.all import *


# Cell

def mape(truth, pred, reduction='mean') -> tensor:
    """Computes mean absolute percentage error (MAPE)
    """
    norm = torch.abs(truth)
    ret= torch.div(torch.abs(pred - truth), norm)

    if reduction != 'none':
        ret = torch.mean(ret) if reduction == 'mean' else torch.sum(ret)
    return ret

# Cell
def smape(truth, pred, agg=None, reduction='mean') -> tensor:
    """Computes symmetric mean absolute percentage error (SMAPE) on the mean

    Arguments:
        * data_samples (``np.array``): Sampled predictions (n_timeseries, n_variables, n_timesteps).
        * data_truth (``np.array``): Ground truth time series values (n_timeseries, n_variables, n_timesteps).
        * agg: Aggregation function applied to sampled predictions (defaults to ``np.median``).
    """
    if pred.shape != truth.shape:
        raise ValueError('Last three dimensions of data_samples and data_truth need to be compatible')

    eps = 1e-16  # Need to make sure that denominator is not zero
    norm = (torch.abs(pred) + torch.abs(truth)) + eps
    ret = (2.0 * torch.abs(pred - truth) / norm)

    if reduction != 'none':
        ret = torch.mean(ret) if reduction == 'mean' else torch.sum(ret)
    return ret

def SMAPELossFlat(*args, axis=-1, floatify=True, **kwargs):
    """Same as `smape`, but flattens input and target.
    DOES not work yet
    """
    return BaseLoss(smape, *args, axis=axis, floatify=floatify, is_2d=False, **kwargs)

# Cell

def mase(y_test, y_hat_test, insample, freq, reduction=None):
    """Computes mean absolute scaled error (MASE) as in the `M4 competition
    <https://www.m4.unic.ac.cy/wp-content/uploads/2018/03/M4-Competitors-Guide.pdf>`_.
    Arguments:
        *

    """
    eps = 1e-16  # Need to make sure that denominator is not zero
    # Calculate mean absolute for forecast and naive forecast per time series
    err = torch.abs(y_test - y_hat_test)

    naive_forecast = insample[:, :-freq]
    naive_target = insample[:, freq:]
    naive_err = torch.abs(naive_target - naive_forecast).mean(-1)[:,None]
    ret = torch.div(err, naive_err+eps).mean(-1)
    if reduction is not None:
        ret = torch.mean(ret,-1) if reduction == 'mean' else torch.sum(ret,-1)
    return ret

