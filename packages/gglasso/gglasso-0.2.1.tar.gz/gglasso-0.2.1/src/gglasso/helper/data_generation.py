"""
Generates data for numerical experiments

Power law network: methodology is inspired by "The joint graphical lasso for inverse covariance estimation across
multiple classes" from Danaher et al.

"""

import numpy as np
import networkx as nx

from .basic_linalg import trp

def generate_precision_matrix(p=100, M=10, style='powerlaw', gamma=2.8, prob=0.1, scale=False, seed=None):
    """
    Generates a sparse precision matrix with associated covariance matrix from a random network.
    
    
    Parameters
    ----------
    p : int, optional
        size of the matrix. The default is 100.
    M : int, optional
        number of subblocks. p/M must result in an integer. The default is 10.
    style : str, optional
        Type of the random network. Available network types:
            * 'powerlaw': a powerlaw network.
            * 'erdos': a Erdos-Renyi network.
        
        The default is 'powerlaw'.
    gamma : float, optional
        parameter for powerlaw network. The default is 2.8.
    prob : float, optional
        probability of edge creation for Erdos-Renyi network. The default is 0.1.
    scale : boolean, optional
        whether Sigma (cov. matrix) is scaled by diagonal entries (as described by Danaher et al.). If set to True, then the generated precision matrix is not
        the inverse of Sigma anymore.
    seed : int, optional
        Seed for network creation and matrix entries. The default is None.

    Returns
    -------
    Sigma : array of shape (p,p)
        Covariance matrix.
    
    Theta: array of shape (p,p)
        Precisiion matrix, inverse of Sigma. If ``scale=True`` we return ``None``.

    """
    
    L = int(p/M)
    assert M*L == p
    
    A = np.zeros((p, p))
    Sigma = np.zeros((p, p))
    
    if seed is not None:
        nxseed = seed
    else:
        nxseed = None
    
    for m in np.arange(M):
        
        if nxseed is not None:
            nxseed = int(nxseed +m)
        
        if style == 'powerlaw':
            G_m = nx.generators.random_graphs.random_powerlaw_tree(n=L, gamma=gamma, tries=max(5*p,1000), seed=nxseed)
        elif style == 'erdos':
            G_m = nx.generators.random_graphs.erdos_renyi_graph(n=L, p=prob, seed=nxseed, directed=False)
        else:
            raise ValueError(f"{style} is not a valid choice for the network generation.")
        A_m = nx.to_numpy_array(G_m)
        
        # generate random numbers for the nonzero entries
        if seed is not None:
            rng = np.random.default_rng(seed)
        else:
            rng = np.random.default_rng(np.random.randint(low=11111, high=99999))

        B1 = rng.uniform(low=.1, high=.4, size=(L,L))
        B2 = rng.choice(a=[-1,1], p=[.5, .5], size=(L,L))
        
        A_m = A_m * (B1*B2)
        
        A[m*L:(m+1)*L, m*L:(m+1)*L] = A_m
    
    row_sum_od = 1.5 * abs(A).sum(axis = 1) + 1e-10
    # broadcasting in order to divide ROW-wise
    A = A / row_sum_od[:,np.newaxis]
    
    A = .5 * (A + A.T)
    
    # A has 0 on diagonal, fill with 1s
    A = A + np.eye(p)
    assert all(np.diag(A)==1), "Expected 1s on diagonal"
    
    # make sure A is pos def
    D = np.linalg.eigvalsh(A)
    if D.min() < 1e-8:
        A += (0.1+abs(D.min())) * np.eye(p)    
        
    Ainv = np.linalg.pinv(A, hermitian=True)
    
    # scale by inverse of diagonal and 0.6*1/sqrt(d_ii*d_jj) on off-diag
    if scale:
        d = np.diag(Ainv)
        scale_mat = np.tile(np.sqrt(d),(Ainv.shape[0], 1))
        scale_mat = (1/0.6)*(scale_mat.T * scale_mat)
        np.fill_diagonal(scale_mat, d)

        Sigma = Ainv/scale_mat
        Theta = None
        
    else:
        Sigma = Ainv.copy()
        Theta = A.copy()
          
    assert abs(Sigma.T - Sigma).max() <= 1e-8
    D = np.linalg.eigvalsh(Sigma)
    assert D.min() > 0, "generated matrix Sigma is not positive definite"
         
    return Sigma, Theta

def time_varying_power_network(p=100, K=10, M=10, scale = False, seed = None):
    """
    generates a power law network. The first block disappears at half-time, while the second block appears
    third block decays exponentially
    p: dimension
    K: number of instances/time-stamps
    M: number of sublocks in each instance, should be greater or equal than 3
    """  
    Sigma = np.zeros((K,p,p))
    
    L = int(p/M)
    assert M*L == p
    assert M >=3
    
    Sigma_0,_ = generate_precision_matrix(p=p, M=M, style='powerlaw', scale=scale, seed=seed) 
    
    for k in np.arange(K):
        Sigma_k = Sigma_0.copy()

        if k <= K/2:   
            Sigma_k[L:2*L, L:2*L] = np.eye(L)
        else:
            Sigma_k[0:L, 0:L] = np.eye(L)
                  
        Sigma[k,:,:] = Sigma_k
        
    Theta = np.linalg.pinv(Sigma, hermitian=True)
    
    decay = np.exp(-.5 * np.arange(K)) 
    helper = np.ones((K, L, L)) * decay[:, None, None]
    for k in np.arange(K):
        np.fill_diagonal(helper[k,:,:], 1)

    Theta[:,2*L:3*L, 2*L:3*L] *= helper
    
    Sigma, Theta = ensure_sparsity(Sigma, Theta)
    
    return Sigma, Theta
    
def group_power_network(p=100, K=10, M=10, scale=False, seed=None):
    """
    generates a power law network. In each single network one block disappears (randomly)
    p: dimension
    K: number of instances/time-stamps
    M: number of sublocks in each instance
    """  
    Sigma = np.zeros((K,p,p))
    
    L = int(p/M)
    assert M*L == p
    
    Sigma_0,_ = generate_precision_matrix(p=p, M=M, style='powerlaw', scale=scale, seed=seed)
    # contains the number of the block disappearing for each k=1,..,K
    if seed is not None:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng(np.random.randint(low=11111, high=99999))

    block = rng.integers(M, size=K)
    
    for k in np.arange(K):    
        Sigma_k = Sigma_0.copy()           
        if K > 1:
            Sigma_k[block[k]*L : (block[k]+1)*L, block[k]*L : (block[k]+1)*L] = np.eye(L)
        
        Sigma[k,:,:] = Sigma_k
            
    Theta = np.linalg.pinv(Sigma, hermitian=True)
    Sigma, Theta = ensure_sparsity(Sigma, Theta)
    
    return Sigma, Theta    

def ensure_sparsity(Sigma, Theta):
    
    Theta[abs(Theta) <= 1e-2] = 0
    
    D = np.linalg.eigvalsh(Theta)
    assert D.min() > 0, "generated matrix Theta is not positive definite"
    
    Sigma = np.linalg.pinv(Theta, hermitian=True)
    
    return Sigma, Theta

    
def sample_covariance_matrix(Sigma, N, seed=None):
    """
    samples data for a given covariance matrix Sigma (with K layers)
    return: sample covariance matrix S
    """
    rng = np.random.default_rng(seed)
        
    if len(Sigma.shape) == 2:
        assert abs(Sigma - Sigma.T).max() <= 1e-10
        (p,p) = Sigma.shape
        
        sample = rng.multivariate_normal(np.zeros(p), Sigma, N).T
        S = np.cov(sample, bias=True)
        
    else:
        assert abs(Sigma - trp(Sigma)).max() <= 1e-10
        (K,p,p) = Sigma.shape

        sample = np.zeros((K,p,N))
        for k in np.arange(K):
            sample[k,:,:] = rng.multivariate_normal(np.zeros(p), Sigma[k,:,:], N).T
    
        S = np.zeros((K,p,p))
        for k in np.arange(K):
            # normalize with N --> bias = True
            S[k,:,:] = np.cov(sample[k,:,:], bias=True)
            
    return S,sample


