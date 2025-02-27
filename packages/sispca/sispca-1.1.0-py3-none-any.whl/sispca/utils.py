import warnings
import torch
import numpy as np

def normalize_col(x, center = True, scale = True):
    """Z-score normalization.

    Args:
        x (2D tensor): (n_sample, n_feature).

    Returns:
        (x - x.mean(dim=0)) / x.std(dim=0)
    """
    x_new = x
    if center:
        x_new = x_new - x_new.mean(dim=0, keepdim = True)
    if scale:
        x_new = x_new / x_new.std(dim=0, keepdim = True)
    return x_new

def tr_cov(x):
    """Calculate the trace of the covariance matrix of the hidden representation.

    Args:
        x (2D tensor): (n_sample, n_feature).

    Returns:
        tr(x @ x.T)
    """
    return torch.norm(x, dim = 1).pow(2).sum()

def gaussian_kernel(x, bw = None):
    """Calculate the Gaussian kernel matrix.

    Args:
        x (2D tensor): (n_sample, n_feature).
        bw: Bendwidth of the Gaussian kernel.
            If None, will set to the median distance.

    Returns
        K (2D tensor): (n_sample, n_sample).
    """
    dist = torch.cdist(x, x, p=2.0)
    if bw is None:
        bw = dist.median()
    K = torch.exp(- 0.5 * dist.pow(2) / bw ** 2)
    return K

def delta_kernel(x):
    """Calculate the delta kernel matrix.

    Args:
        x (2D array): Category labels. (n_sample, n_feature).

    Returns
        K (2D tensor): (n_sample, n_sample).
    """
    if len(x.shape) == 1:
        x = x[:, None] # (n_sample, 1)

    K = torch.zeros(x.shape[0], x.shape[0])
    for i in range(x.shape[1]): # sum over all features
        K_i = (x[:, i:(i+1)] == x[:, i:(i+1)].T) * 1.0
        if isinstance(K_i, np.ndarray):
            K += torch.from_numpy(K_i).float()
        else:
            K += K_i.float()

    return K

def hsic_gaussian(x, y, bw = None):
    """Calculate the HSIC between two tensors using Gaussian kernel.

    Args:
        x (2D tensor): (n_sample, n_feature_1).
        y (2D tensor): (n_sample, n_feature_2).
        bw: Bendwidth of the Gaussian kernel.
            If None, will set to the median distance.

    Returns:
        HSIC (float): HSIC between x and y.
    """
    n_sapmle = x.shape[0]

    # scale x and y to unit variance
    x_new = normalize_col(x, center = True, scale = True)
    y_new = normalize_col(y, center = True, scale = True)

    # calculate kernel matrices
    K = gaussian_kernel(x_new, bw=bw) # (n_sample, n_sample)
    L = gaussian_kernel(y_new, bw=bw) # (n_sample, n_sample)

    # center kernel matrices
    K_H = normalize_col(K, center = True, scale = False)
    L_H = normalize_col(L, center = True, scale = False)

    # calculate HSIC
    return torch.trace(K_H @ L_H) / ((n_sapmle - 1) ** 2)

def hsic_linear(x, y):
    """Calculate the HSIC between two tensors using linear kernel.

    Args:
        x (2D tensor): (n_sample, n_feature_1).
        y (2D tensor): (n_sample, n_feature_2).

    Returns:
        HSIC (float): HSIC between x and y.
    """
    n_sapmle = x.shape[0]

    # scale x and y to unit variance
    x_new = normalize_col(x, center = True, scale = False)
    y_new = normalize_col(y, center = True, scale = False)

    # # calculate kernel matrices
    # K = x_new @ x_new.T # (n_sample, n_sample)
    # L = y_new @ y_new.T # (n_sample, n_sample)

    # # calculate HSIC
    # return torch.trace(K @ L) / ((n_sapmle - 1) ** 2)

    return (torch.norm(x_new.T @ y_new, 'fro') / (n_sapmle - 1)) ** 2


def gram_schmidt(x):
    """Project the data to an orthogonal space using Gram-Schmidt process.

    Args:
        x (2D tensor).

    Returns:
        x_new (2D tensor): data with orthonormal columns.
    """
    # x_new.T @ x_new == I
    return torch.linalg.qr(x, mode = 'reduced')[0]

class Kernel:
    """Custom data class for more efficient storage of kernels.

    Usage:
        kernel = Kernel('continuous', Q = target_data) # K = Q @ Q.T
        kernel.realization() # return the (n, n) kernel matrix
        kernel.subset(idx) # return the sub-kernel matrix of shape (m, m) where m = len(idx)
        kernel.xtKx(x) # return x.T @ K @ x
    """
    def __init__(self, target_type, Q = None, target_kernel = None):
        """
        Args:
            target_type (str): One of ['continuous', 'categorical', 'identity','custom']. The type of the target data.
                If 'custom', the target_kernel should be provided.
            Q (int or 2D tensor): If int, Q is the dimension of the identity matrix.
                                  If 2D tensor, Q is the decomposed matrix (n_obs, n_var) where K = Q @ Q.T.
            target_kernel (2D tensor): The pre-calculated kernel matrix of shape (n_obs, n_obs). 
                Applied when target_type is 'custom'. Will be stored as a sparse tensor.
        """
        self.target_type = target_type
        self.Q = Q # K = Q @ Q.T
        self.target_kernel = target_kernel # K or None

        self._sanity_check()
        self.shape = self._shape() # shape of the kernel matrix
        self._rank = None # rank of the kernel matrix, will be calculated when needed
    
    def _sanity_check(self):
        # check the target type
        _valid_types = ['continuous', 'categorical', 'identity','custom']
        assert self.target_type in _valid_types, \
            f"Currently only support type in {_valid_types}."
        
        if self.target_type == 'custom':
            # use pre-calculated kernel matrix and ignore the target data
            assert self.target_kernel is not None, \
                "If target_type is 'custom', the target_kernel should be provided."

            # convert the kernel matrix to tensor if ndarray
            if isinstance(self.target_kernel, np.ndarray):
                self.target_kernel = torch.from_numpy(self.target_kernel).float()

            # convert the kernel matrix to sparse
            if isinstance(self.target_kernel, torch.Tensor):
                self.target_kernel = self.target_kernel.to_sparse()
            
            # check the shape of the kernel matrix
            assert self.target_kernel.shape[0] == self.target_kernel.shape[1], \
                "The kernel matrix should be square."

            # set Q to None
            if self.Q is not None:
                warnings.warn("Kernel is provided. The Q matrix will be ignored.")
                self.Q = None

        elif self.target_type == 'identity':
            assert isinstance(self.Q, int), \
                "If target_type is 'identity', the dimension (int) should be provided."
        else:
            # check Q 
            assert self.Q is not None, \
                "If target_type is 'continuous' or 'categorical', the Q matrix should be provided."
            assert len(self.Q.shape) == 2, \
                "The Q matrix should be 2D tensor of shape (n_obs, k)."
    
    def _shape(self): 
        if self.target_type == 'identity':
            return (self.Q, self.Q)
        elif self.target_type == 'custom':
            return (self.target_kernel.shape[0], self.target_kernel.shape[1])
        else:
            return (self.Q.shape[0], self.Q.shape[0])
            
    def realization(self):
        if self.target_type == 'identity':
            return torch.eye(self.Q)
        elif self.target_type == 'custom':
            return self.target_kernel
        else:
            return self.Q @ self.Q.T

    def xtKx(self, x):
        # Avoid realising the kernel matrix to save memory
        if self.target_type == 'identity':
            return x.T @ x
        elif self.target_type == 'custom':
            return x.T @ self.target_kernel @ x
        else:
            return x.T @ self.Q @ self.Q.T @ x
        
    def subset(self, idx):
        """Helper function to extract batched inputs for training. idx (tensor) is the index of the batch."""
        if self.target_type == 'identity':
            return Kernel('identity', Q = idx.shape[0])
        elif self.target_type == 'custom':
            return Kernel('custom', target_kernel = slice_sparse_matrix(self.target_kernel, idx))
        else:
            return Kernel(self.target_type, Q = self.Q[idx, :])

    def rank(self):
        """Calculate the rank of the kernel matrix"""
        if self._rank is None:
            if self.target_kernel is not None:
                self._rank = torch.linalg.matrix_rank(self.target_kernel.to_dense()).item()
            else:
                self._rank = torch.linalg.matrix_rank(self.Q).item()
        return self._rank
        

def slice_sparse_matrix(K: torch.sparse_coo_tensor, index: torch.Tensor):
    """
    Slice a PyTorch sparse matrix `K` by the indices in `index` such that the result is K[index, :][:, index].
    
    Args:
        K: Input sparse matrix (torch.sparse_coo_tensor).
        index: 1D tensor of row/column indices to slice (torch.Tensor).
    
    Returns:
        A new sparse matrix (torch.sparse_coo_tensor) corresponding to K[index, :][:, index].
    """
    # Ensure index is a torch tensor and sorted (for efficient matching)
    index = index.to(K.indices().device)  # Move index to the same device as K
    index = torch.unique(index)  # Ensure no duplicate indices (optional, depending on your use case)

    # Extract the indices and values of the sparse matrix
    row, col = K.indices()
    values = K.values()

    # Create a mask for rows and columns that match the given indices
    row_mask = torch.isin(row, index)
    col_mask = torch.isin(col, index)
    mask = row_mask & col_mask  # Keep only the elements that match both row and column indices

    # Filter the indices and values based on the mask
    new_row = row[mask]
    new_col = col[mask]
    new_values = values[mask]

    # Map the old indices to the new ones (relative to `index`)
    index_map = {old_idx.item(): new_idx for new_idx, old_idx in enumerate(index)}
    new_row = torch.tensor([index_map[r.item()] for r in new_row], device=K.device)
    new_col = torch.tensor([index_map[c.item()] for c in new_col], device=K.device)

    # Create the new sparse matrix
    new_size = (len(index), len(index))  # The size of the sliced matrix
    new_indices = torch.stack([new_row, new_col], dim=0)
    new_sparse_matrix = torch.sparse_coo_tensor(new_indices, new_values, size=new_size, device=K.device)

    return new_sparse_matrix