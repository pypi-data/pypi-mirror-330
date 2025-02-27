import numpy as np

import jax.numpy as jnp

import netket as nk


def central_diff_grad(func, x, eps, *args, dtype=None):
    if dtype is None:
        dtype = x.dtype

    grad = np.zeros(
        len(x), dtype=nk.jax.maybe_promote_to_complex(x.dtype, func(x, *args).dtype)
    )
    epsd = np.zeros(len(x), dtype=dtype)
    epsd[0] = eps
    for i in range(len(x)):
        assert not np.any(np.isnan(x + epsd))
        grad_r = 0.5 * (func(x + epsd, *args) - func(x - epsd, *args))
        if jnp.iscomplexobj(x):
            grad_i = 0.5 * (func(x + 1j * epsd, *args) - func(x - 1j * epsd, *args))
            grad[i] = grad_r + 1j * grad_i
        else:
            grad[i] = grad_r

        assert not np.isnan(grad[i])
        grad[i] /= eps
        epsd = np.roll(epsd, 1)
    return grad


def same_derivatives(der, num_der, abs_eps=1.0e-6, rel_eps=1.0e-6):
    """
    Checks that two complex-valued arrays are the same.
    Same as `np.testing.assert_allclose` but checks the real
    and imaginary parts independently for better error reporting.
    """
    assert der.shape == num_der.shape

    np.testing.assert_allclose(der.real, num_der.real, rtol=rel_eps, atol=abs_eps)

    np.testing.assert_allclose(der.imag, num_der.imag, rtol=rel_eps, atol=abs_eps)
