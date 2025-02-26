import math
import torch
from torch import Tensor
from torch.optim.optimizer import Optimizer
from torch.optim.lr_scheduler import LRScheduler
from typing import Any, List, Tuple, Union


def _get_param_groups(params: List[Tuple[str, Tensor]], weight_decay: float) -> list:
    """Get the parameters grouped by weight decay and no weight decay.

    Returns:
        dict: a dictionary with two keys, 'params' and 'params_no_decay'
    """
    params_no_decay = [x for n, x in params if not (('bn' in n) or ('bias' in n))]
    params_decay = [x for n, x in params if ('bn' in n) or ('bias' in n)]

    return [
        {'params': params_no_decay, 'weight_decay': 0.},
        {'params': params_decay, 'weight_decay': weight_decay}
    ]


def optim_fn_adam(params: List[Tuple[str, Tensor]],
                  lr: float = 1e-3,
                  beta1: float = 0.9,
                  beta2: float = 0.999,
                  weight_decay: float = 1. / 32768,
                  eps: float = 1e-8) -> Optimizer:
    """An example of a function that creates an Adam optimizer with the given parameters and their names.
        To change the hyperparameters of the optimizer, you can wrap it with `functools.partial` and pass the new values.

    Returns:
        Optimizer: an Adam optimizer
    """
    return torch.optim.Adam(_get_param_groups(params, weight_decay),
                            lr=lr,
                            betas=(beta1, beta2),
                            eps=eps)


def optim_fn_adamw(params: List[Tuple[str, Tensor]],
                   lr: float = 1e-3,
                   beta1: float = 0.9,
                   beta2: float = 0.999,
                   weight_decay: float = 0.1,
                   eps: float = 1e-8) -> Optimizer:
    """An example of a function that creates an AdamW optimizer with the given parameters and their names.
        To change the hyperparameters of the optimizer, you can wrap it with `functools.partial` and pass the new values.

    Returns:
        Optimizer: an AdamW optimizer
    """
    return torch.optim.AdamW(_get_param_groups(params, weight_decay),
                             lr=lr,
                             betas=(beta1, beta2),
                             eps=eps)


def optim_fn_accum_adam(params: List[Tuple[str, Tensor]],
                        lr: float = 1e-3,
                        beta1: float = 0.9,
                        beta2: float = 0.999,
                        eps: float = 1e-8,
                        weight_decay: float = 1. / 32768,
                        accum_iter: int = 4) -> Optimizer:
    """An example of a function that creates an AccumAdam optimizer with the given parameters and their names.
        To change the hyperparameters of the optimizer, you can wrap it with `functools.partial` and pass the new values.

    Returns:
        Optimizer: an AccumAdam optimizer
    """
    return AccumAdam(_get_param_groups(params, weight_decay),
                     lr=lr,
                     betas=(beta1, beta2),
                     eps=eps,
                     accum_iter=accum_iter)


def optim_fn_accum_adamw(params: List[Tuple[str, Tensor]],
                         lr: float = 1e-3,
                         beta1: float = 0.9,
                         beta2: float = 0.999,
                         eps: float = 1e-8,
                         weight_decay: float = 0.1,
                         accum_iter: int = 4) -> Optimizer:
    """An example of a function that creates an AccumAdamW optimizer with the given parameters and their names.
        To change the hyperparameters of the optimizer, you can wrap it with `functools.partial` and pass the new values.

    Returns:
        Optimizer: an AccumAdamW optimizer
    """
    return AccumAdamW(_get_param_groups(params, weight_decay),
                      lr=lr,
                      betas=(beta1, beta2),
                      eps=eps,
                      accum_iter=accum_iter)


def lr_scheduler_fn_cosine_with_warmup(optimizer: Optimizer,
                                       t_max: int,
                                       t_warmup: int,
                                       cosine_eta_min: float = 1e-6,
                                       warmup_decay: float = 0.01) -> LRScheduler:
    """An example of a function that creates a learning rate scheduler that combines a warmup and a cosine annealing schedule.

    Returns:
        LRScheduler: a learning rate scheduler with the linear warmup followed by the cosine annealing
    """
    main_lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=t_max, eta_min=cosine_eta_min)
    warmup_lr_scheduler = torch.optim.lr_scheduler.LinearLR(optimizer, start_factor=warmup_decay, total_iters=t_warmup)
    return torch.optim.lr_scheduler.SequentialLR(optimizer,
                                                 schedulers=[warmup_lr_scheduler, main_lr_scheduler],
                                                 milestones=[t_warmup])


def accum_adamw_foreach(params: List[torch.Tensor],
                       grads: List[torch.Tensor],
                       exp_avgs: List[torch.Tensor],
                       exp_avg_sqs: List[torch.Tensor],
                       accum_grads: List[torch.Tensor],
                       state_steps: List[torch.Tensor],
                       beta1: float,
                       beta2: float,
                       lr: Union[float, torch.Tensor],
                       weight_decay: float,
                       eps: float,
                       accum_iter: int):
    """Optimized version of AccumAdamW optimizer using torch._foreach
        TODO: fused kernel
    """

    torch._foreach_add_(state_steps, 1)
    if weight_decay != 0:
        torch._foreach_mul_(params, 1 - lr * weight_decay)

    step = state_steps[0].item()
    torch._foreach_add_(accum_grads, grads, alpha=1./accum_iter)

    _exp_avgs = torch._foreach_add(exp_avgs, grads, alpha=1-beta1)
    _exp_avg_sqs = torch._foreach_addcmul(exp_avg_sqs, grads, grads, value=1-beta2)

    bias_correction1 = 1 - beta1 ** ((step + accum_iter - 1) // accum_iter)
    bias_correction2 = 1 - beta2 ** ((step + accum_iter - 1) // accum_iter)
    step_size = lr / bias_correction1
    bias_correction2_sqrt = math.sqrt(bias_correction2)

    torch._foreach_sqrt_(_exp_avg_sqs)
    torch._foreach_div_(_exp_avg_sqs, bias_correction2_sqrt)
    torch._foreach_add_(_exp_avg_sqs, eps)
    torch._foreach_addcdiv_(params, _exp_avgs, _exp_avg_sqs, value=-step_size) # type: ignore

    if step % accum_iter == 0:
        torch._foreach_add_(exp_avgs, accum_grads, alpha=1-beta1)
        torch._foreach_mul_(exp_avgs, beta1)
        torch._foreach_addcmul_(exp_avg_sqs, accum_grads, accum_grads, value=1-beta2)
        torch._foreach_mul_(exp_avg_sqs, beta2)
        torch._foreach_zero_(accum_grads)


class AccumAdamW(torch.optim.Optimizer):
    """AccumAdamW optimizer

    Args:
        params (Any): parameters list or groups
        lr (float, optional): base learning rate. Defaults to 1e-3.
        betas (Tuple[float, float], optional): beta1 and beta2. Defaults to (0.9, 0.999).
        eps (float, optional): epsilon. Defaults to 1e-8.
        weight_decay (float, optional): weight decay. Defaults to 0.
        accum_iter (int, optional): number of accumulation steps. Defaults to 4. should be scaling up with the number of workers.
    """
    
    def __init__(self,
                 params: Any,
                 lr: float = 1e-3,
                 betas: Tuple[float, float] = (0.9, 0.999),
                 eps: float = 1e-8,
                 weight_decay: float = 0,
                 accum_iter: int = 4):
        defaults = dict(
            lr=lr,
            betas=betas,
            eps=eps,
            weight_decay=weight_decay,
            accum_iter=accum_iter
        )
        super().__init__(params, defaults)

    def _init_group(self,
                    group,
                    params_with_grad,
                    grads,
                    exp_avgs,
                    exp_avg_sqs,
                    accum_grads,
                    state_steps):
        for p in group['params']:
            if p.grad is not None:
                params_with_grad.append(p)
                grads.append(p.grad)
                state = self.state[p]
                if len(state) == 0:
                    state['step'] = torch.tensor(0, dtype=torch.int64)
                    state['exp_avg'] = torch.zeros_like(p, memory_format=torch.preserve_format)
                    state['exp_avg_sq'] = torch.zeros_like(p, memory_format=torch.preserve_format)
                    state['accum_grad'] = torch.zeros_like(p, memory_format=torch.preserve_format)
                exp_avgs.append(state['exp_avg'])
                exp_avg_sqs.append(state['exp_avg_sq'])
                accum_grads.append(state['accum_grad'])
                state_steps.append(state['step'])

    @torch.no_grad()
    def step(self, closure=None): # type: ignore
        self._cuda_graph_capture_health_check()
        assert closure is None

        for group in self.param_groups:
            params_with_grad = []
            grads = []
            exp_avgs = []
            exp_avg_sqs = []
            accum_grads = []
            state_steps = []
            beta1, beta2 = group["betas"]

            self._init_group(
                group, params_with_grad, grads, exp_avgs, exp_avg_sqs, accum_grads, state_steps
            )

            if len(state_steps) == 0:
                continue

            accum_adamw_foreach(
                params_with_grad,
                grads,
                exp_avgs,
                exp_avg_sqs,
                accum_grads,
                state_steps,
                beta1,
                beta2,
                group['lr'],
                group['weight_decay'],
                group['eps'],
                group['accum_iter']
            )


def accum_adam_foreach(params: List[torch.Tensor],
                       grads: List[torch.Tensor],
                       exp_avgs: List[torch.Tensor],
                       exp_avg_sqs: List[torch.Tensor],
                       accum_grads: List[torch.Tensor],
                       state_steps: List[torch.Tensor],
                       beta1: float,
                       beta2: float,
                       lr: Union[float, torch.Tensor],
                       weight_decay: float,
                       eps: float,
                       accum_iter: int):
    """Optimized version of AccumAdam optimizer using torch._foreach
        TODO: write a fused kernel for this
    """
    torch._foreach_add_(state_steps, 1)
    if weight_decay != 0:
        torch._foreach_add_(grads, params, alpha=weight_decay)

    step = state_steps[0].item()
    torch._foreach_add_(accum_grads, grads, alpha=1./accum_iter)

    _exp_avgs = torch._foreach_add(exp_avgs, grads, alpha=1-beta1)
    _exp_avg_sqs = torch._foreach_addcmul(exp_avg_sqs, grads, grads, value=1-beta2)

    bias_correction1 = 1 - beta1 ** ((step + accum_iter - 1) // accum_iter)
    bias_correction2 = 1 - beta2 ** ((step + accum_iter - 1) // accum_iter)
    step_size = lr / bias_correction1
    bias_correction2_sqrt = math.sqrt(bias_correction2)

    torch._foreach_sqrt_(_exp_avg_sqs)
    torch._foreach_div_(_exp_avg_sqs, bias_correction2_sqrt)
    torch._foreach_add_(_exp_avg_sqs, eps)
    torch._foreach_addcdiv_(params, _exp_avgs, _exp_avg_sqs, value=-step_size) # type: ignore

    if step % accum_iter == 0:
        torch._foreach_add_(exp_avgs, accum_grads, alpha=1-beta1)
        torch._foreach_mul_(exp_avgs, beta1)
        torch._foreach_addcmul_(exp_avg_sqs, accum_grads, accum_grads, value=1-beta2)
        torch._foreach_mul_(exp_avg_sqs, beta2)
        torch._foreach_zero_(accum_grads)


class AccumAdam(torch.optim.Optimizer):
    """AccumAdamW optimizer

    Args:
        params (Any): parameters list or groups
        lr (float, optional): base learning rate. Defaults to 1e-3.
        betas (Tuple[float, float], optional): beta1 and beta2. Defaults to (0.9, 0.999).
        eps (float, optional): epsilon. Defaults to 1e-8.
        weight_decay (float, optional): weight decay. Defaults to 0.
        accum_iter (int, optional): number of accumulation steps. Defaults to 4. should be scaling up with the number of workers.
    """
    def __init__(self,
                 params: Any,
                 lr: float = 1e-3,
                 betas: Tuple[float, float] = (0.9, 0.999),
                 eps: float = 1e-8,
                 weight_decay: float = 1. / 32768,
                 accum_iter: int = 4):
        defaults = dict(
            lr=lr,
            betas=betas,
            eps=eps,
            weight_decay=weight_decay,
            accum_iter=accum_iter
        )
        super().__init__(params, defaults)

    def _init_group(self,
                    group,
                    params_with_grad,
                    grads,
                    exp_avgs,
                    exp_avg_sqs,
                    accum_grads,
                    state_steps):
        for p in group['params']:
            if p.grad is not None:
                params_with_grad.append(p)
                grads.append(p.grad)
                state = self.state[p]
                if len(state) == 0:
                    state['step'] = torch.tensor(0, dtype=torch.int64)
                    state['exp_avg'] = torch.zeros_like(p, memory_format=torch.preserve_format)
                    state['exp_avg_sq'] = torch.zeros_like(p, memory_format=torch.preserve_format)
                    state['accum_grad'] = torch.zeros_like(p, memory_format=torch.preserve_format)
                exp_avgs.append(state['exp_avg'])
                exp_avg_sqs.append(state['exp_avg_sq'])
                accum_grads.append(state['accum_grad'])
                state_steps.append(state['step'])

    @torch.no_grad()
    def step(self, closure=None): # type: ignore
        self._cuda_graph_capture_health_check()
        assert closure is None, "Closure is not supported"

        for group in self.param_groups:
            params_with_grad = []
            grads = []
            exp_avgs = []
            exp_avg_sqs = []
            accum_grads = []
            state_steps = []
            beta1, beta2 = group["betas"]

            self._init_group(
                group, params_with_grad, grads, exp_avgs, exp_avg_sqs, accum_grads, state_steps
            )

            if len(state_steps) == 0:
                continue

            accum_adam_foreach(
                params_with_grad,
                grads,
                exp_avgs,
                exp_avg_sqs,
                accum_grads,
                state_steps,
                beta1,
                beta2,
                group['lr'],
                group['weight_decay'],
                group['eps'],
                group['accum_iter']
            )

__all__ = [
    'optim_fn_adam',
    'optim_fn_adamw',
    'optim_fn_accum_adam',
    'optim_fn_accum_adamw',
    'lr_scheduler_fn_cosine_with_warmup',
    'AccumAdam',
    'AccumAdamW'
]
