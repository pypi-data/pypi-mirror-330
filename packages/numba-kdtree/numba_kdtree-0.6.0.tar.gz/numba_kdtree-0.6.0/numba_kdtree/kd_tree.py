from __future__ import annotations
import numba as nb
import numpy as np

from numba.core import types, cgutils
from numba.experimental import structref
from numba.extending import overload_method, intrinsic, overload_attribute
from .ckdtree import ckdtree as ckdtree_ct
import warnings
from typing import Optional, Any
from numba.core.unsafe.nrt import NRT_get_api
from numba.core.runtime import nrt
from numba.core.registry import cpu_target # Get the CPU target singleton
cpu_target.target_context # Access the target_context property to initialize

__all__ = ["KDTree", "KDTreeType"]

INT_TYPE = np.int64
INT_TYPE_T = nb.int64

DIM_TYPE = np.uint32
DIM_TYPE_T = nb.uint32

FLOAT_TYPE = np.float32
FLOAT_TYPE_T = nb.float32

BOOL_TYPE = np.uint8
BOOL_TYPE_T = nb.uint8

IntArray = np.ndarray
DimIndexArray = np.ndarray
DataArray = np.ndarray
BoolArray = np.ndarray

NUMBA_THREADS = nb.config.NUMBA_NUM_THREADS


@nb.njit(nogil=True, inline='always', cache=True)
def _list_to_2d_array(arraylist, dtype):
    n = len(arraylist)
    k = arraylist[0].shape[0]
    array = np.zeros((n, k), dtype)
    for i in range(n):
        array[i] = arraylist[i]
    return array

# code adapted from https://github.com/numba/numba/issues/1269#issuecomment-472574352
@nb.njit(nogil=True, inline='always', fastmath=True, cache=True)
def _np_apply_along_axis(func1d, axis, arr):
  assert arr.ndim == 2
  assert axis in [0, 1]
  if axis == 0:
    result = np.empty(arr.shape[1], dtype=arr.dtype)
    for i in range(len(result)):
      result[i] = func1d(arr[:, i])
  else:
    result = np.empty(arr.shape[0], dtype=arr.dtype)
    for i in range(len(result)):
      result[i] = func1d(arr[i, :])
  return result

@nb.njit(nogil=True, fastmath=True, cache=True, inline='always')
def _np_min(array, axis):
  return _np_apply_along_axis(np.amin, axis, array)

@nb.njit(nogil=True, fastmath=True, cache=True, inline='always')
def _np_max(array, axis):
  return _np_apply_along_axis(np.amax, axis, array)


def _convert_to_valid_input(X, n_features, dtype):
    # this is a stub for numba overload
    pass


@nb.extending.overload(_convert_to_valid_input, jit_options={'nogil': True, 'fastmath': True, "cache": True})
def _ol_convert_to_valid_input_impl(X, n_features, dtype):
    convert_list_to_array = isinstance(X, (nb.types.ListType, nb.types.List)) and isinstance(X.dtype, nb.types.ArrayCompatible)

    def _convert_impl(X, n_features, dtype):
        if convert_list_to_array:
            x_tmp = _list_to_2d_array(X, dtype)
        else:
            x_tmp = np.asarray(X, dtype=dtype)
        return np.ascontiguousarray(x_tmp).reshape(-1, n_features)

    return _convert_impl


_meminfo_treeptr = types.MemInfoPointer(types.voidptr)


@structref.register
class KDTreeNumbaType(types.StructRef):
    def __init__(self, fields):
        fields = list(fields)
        # create fields for the nrt meminfo and the pointer to the c struct as well but hide them from the constructor as they are statically typed
        static_fields = [
            ("meminfo", _meminfo_treeptr),
            ("ckdtree", types.voidptr)
        ]
        fields = static_fields + fields
        super().__init__(fields)

    def preprocess_fields(self, fields):
        # We don't want the struct to take Literal types.
        return [(name, types.unliteral(typ)) for name, typ in fields] 


class KDTreeType(structref.StructRefProxy):
    def __new__(cls, root_bbox, data, idx):
        return structref.StructRefProxy.__new__(cls,
                                                root_bbox,
                                                data,
                                                idx)
    @property
    def root_bbox(self) -> DataArray:
        """Returns the root bounding box of the kdtree.

        Returns:
            Numpy array of shape (2, n_features).
        """
        return _KDTree_get_root_bbox(self)

    @property
    def data(self) -> DataArray:
        """Returns the underlying data array.

        Returns:
            Numpy array of shape (n, n_features)
        """
        return _KDTree_get_data(self)

    @property
    def idx(self) -> DataArray:
        """Returns the underlying index array of all points in the data array sorted by the tree traversal order.

        Returns:
            Numpy array of shape (n,)
        """
        return _KDTree_get_idx(self)

    @property
    def size(self) -> int:
        """Returns the number of nodes in the kdtree. 
        """
        return _KDTree_get_size(self)
    
    @property
    def leafsize(self) -> int:
        """Returns the size of a leaf in the kdtree in bytes.
        """
        return _KDTree_get_leafsize(self)

    def __reduce__(self) -> Any:
        """Pickle support
        """
        args = _KDTree_reduce_args(self)
        return _restore_kdtree, args

    def query(self, 
              X: DataArray, 
              k: int = 1, 
              p: float = 2.0, 
              eps: float = 0.0, 
              distance_upper_bound: float = np.inf) -> tuple[DataArray, DataArray, DataArray]:
        """Query the k nearest neighbors of the given query points. The results are returned as 3 arrays containing the 
        distances, indices, and number of found neighbors. As the distance and index arrays are allocated before the query, the number of
        neighbors found has to be checked against the returned number of found neighbors. 
        Indices and distances above the number of neighbors found are invalid.

        Args:
            X: The query points as an array of shape (n, n_features) or (n_features,).
            k: The number of neighbors to search. Defaults to 1.
            p: The distance metric (p-norm) to use. Defaults to 2.0 (euclidean norm).
            eps: Optional epsilon for approximative search. Defaults to 0.0 (exact search).
            distance_upper_bound: The upper bound of the distance between the query and the found neighbors. Defaults to np.inf.

        Returns:
            A tuple of:
                - Numpy array of shape (n, k) containing the distances between each query point and it's k nearest neighbors.
                - Numpy array of shape (n, k) containng the indices of the nearest neighbors for each query point.
                - Numpy array of shape (n,) containing the number of neighbors found for each query point. 
                  This is usually equal to k, except of the distance_upper_bound has been set.
        """
        return _KDTree_query(self, X, k, p, eps, distance_upper_bound)
    
    def query_parallel(self, 
              X: DataArray, 
              k: int = 1, 
              p: float = 2.0, 
              eps: float = 0.0, 
              distance_upper_bound: float = np.inf) -> tuple[DataArray, DataArray, DataArray]:
        """Query to k nearest neighbors of the given query points using a parallel implementation with one thread per query point. 
        See query() for details.
        """
        return _KDTree_query_parallel(self, X, k, p, eps, distance_upper_bound)

    def query_radius(self, X: DataArray, 
                     r: DataArray | float, 
                     p: float = 2.0, 
                     eps: float = 0.0, 
                     return_sorted: bool = False, 
                     return_length: bool = False) -> list[DataArray]:
        """Query all neighbors within a given radius for each query point.

        Args:
            X: The query points as an array of shape (n, n_features) or (n_features,).
            r: The search radius. If given as an array of shape (n,), a different radius will be used for each query point.
            p: The distance metric (p-norm) to use. Defaults to 2.0 (euclidean norm).
            eps: Optional epsilon for approximative search. Defaults to 0.0 (exact search).
            return_sorted: Return the neighbors sorted by their index. Defaults to False.
            return_length: Returns the number of neighbors found instead of their indices. Defaults to False.

        Returns:
            A list of numpy arrays containing either the indices of each neighbor or the number of neihbors found within the given search radius.
        """
        return _KDTree_query_radius(self, X, r, p, eps, return_sorted, return_length)
    
    def query_radius_parallel(self, X: DataArray, 
                     r: DataArray | float, 
                     p: float = 2.0, 
                     eps: float = 0.0, 
                     return_sorted: bool = False, 
                     return_length: bool = False) -> list[DataArray]:
        """Query all neighbors within a given radius for each query point using a parallel implementation with one thread per query point.
        See query_radius() for details.
        """
        return _KDTree_query_radius_parallel(self, X, r, p, eps, return_sorted, return_length)


structref.define_proxy(KDTreeType, KDTreeNumbaType,
                       ["root_bbox", "data", "idx"])


# define wrapper functions for each method of the kdtree
@nb.njit(cache=True)
def _KDTree_get_root_bbox(self):
    return self.root_bbox


@nb.njit(cache=True)
def _KDTree_get_data(self):
    return self.data


@nb.njit(cache=True)
def _KDTree_get_idx(self):
    return self.idx


@nb.njit(cache=True)
def _KDTree_get_size(self):
    return self.size


@nb.njit(cache=True)
def _KDTree_get_leafsize(self):
    return self.leafsize


@nb.njit(cache=True)
def _KDTree_reduce_args(self):
    return self._reduce_args()


@nb.njit(cache=True)
def _KDTree_query(self, X, k=1, p=2, eps=0.0, distance_upper_bound=np.inf):
    return self.query(X, k=k, p=p, eps=eps, distance_upper_bound=distance_upper_bound)


@nb.njit(cache=False)
def _KDTree_query_parallel(self, X, k=1, p=2, eps=0.0, distance_upper_bound=np.inf):
    return self.query_parallel(X, k=k, p=p, eps=eps, distance_upper_bound=distance_upper_bound)


@nb.njit(cache=True)
def _KDTree_query_radius(self, X, r, p=2.0, eps=0.0, return_sorted=False, return_length=False):
    return self.query_radius(X, r, p, eps, return_sorted, return_length)


@nb.njit(cache=False)
def _KDTree_query_radius_parallel(self, X, r, p=2.0, eps=0.0, return_sorted=False, return_length=False):
    return self.query_radius_parallel(X, r, p, eps, return_sorted, return_length)


# functions required for pickling the Kdtree
@overload_attribute(KDTreeNumbaType, "size", jit_options={"cache": True})
def _ol_size(self):
    dtype = self.field_dict['data'].dtype
    if dtype != nb.types.float32:
        dtype = nb.types.float64

    func_size = ckdtree_ct.size[dtype]

    def size_impl(self):
        return func_size(self.ckdtree)

    return size_impl


@overload_attribute(KDTreeNumbaType, "_leafsize", jit_options={"cache": True})
def _ol_leafsize(self):
    """Returns the leaf size of the underlying tree
    """
    dtype = self.field_dict['data'].dtype
    if dtype != nb.types.float32:
        dtype = nb.types.float64

    func_leafsize = ckdtree_ct.leafsize[dtype]

    def _leafsize_impl(self):
        return func_leafsize(self.ckdtree)

    return _leafsize_impl


@overload_method(KDTreeNumbaType, "_reduce_args", jit_options={"cache": True})
def _ol_reduce_args(self):
    dtype = self.field_dict['data'].dtype
    if dtype != nb.types.float32:
        dtype = nb.types.float64

    # functions to retrieve the parameters of the tree
    func_leafsize = ckdtree_ct.leafsize[dtype]
    func_size = ckdtree_ct.size[dtype]
    func_nodesize = ckdtree_ct.nodesize[dtype]
    func_copy_tree = ckdtree_ct.copy_tree[dtype]

    def _reduce_args_impl(self):
        leafsize = func_leafsize(self.ckdtree)
        size_bytes = func_size(self.ckdtree) * func_nodesize(self.ckdtree)
        # copy the tree into a fresh buffer
        tree_buffer = np.empty(size_bytes, dtype=np.uint8)
        size_copied = func_copy_tree(self.ckdtree, tree_buffer.ctypes)
        if size_copied != size_bytes:
            raise ValueError("__getstate__ failed.")
        return (tree_buffer, self.data, self.root_bbox, leafsize, self.idx)
    
    return _reduce_args_impl


@intrinsic
def _meminfo_getdata(typingctx, meminfo):
    def codegen(context, builder, signature, args):
        meminfo = args[0]
        data_pointer = context.nrt.meminfo_data(builder, meminfo)
        #data_pointer = builder.bitcast(data_pointer, types.voidptr)
        return data_pointer

    sig = types.voidptr(meminfo)
    return sig, codegen


@overload_method(KDTreeNumbaType, "build_index", jit_options={"nogil": True, "cache" : True, "fastmath": True})
def _ol_build_index(self, leafsize, balanced=False, compact=False):
    # choose the appropriate methods based on the data type
    dtype = self.field_dict['data'].dtype
    if dtype != nb.types.float32:
        dtype = nb.types.float64

    func_init = ckdtree_ct.init[dtype]
    func_build = ckdtree_ct.build[dtype]

    def _build_index_impl(self, leafsize, balanced=False, compact=False):
        n_data, n_features = self.data.shape
        nrt = NRT_get_api() # get the nrt API as a voidptr
        self.meminfo = func_init(nrt, 0, 0, self.data.ctypes, self.idx.ctypes, n_data, n_features, leafsize, self.root_bbox[0].ctypes, self.root_bbox[1].ctypes)
        self.ckdtree = _meminfo_getdata(self.meminfo) # get the handle to the actual c struct from the meminfo pointer
        compact_ = 1 if compact else 0
        balanced_ = 1 if balanced else 0
        func_build(self.ckdtree, 0, n_data, self.root_bbox[0].ctypes, self.root_bbox[1].ctypes, balanced_, compact_)

    return _build_index_impl


@overload_method(KDTreeNumbaType, "query", jit_options={"nogil": True, "cache": True, "fastmath": True, 'parallel': False})
def _ol_query(self, X, k=1, p=2, eps=0.0, distance_upper_bound=np.inf):
    # choose the appropriate methods based on the data type
    dtype = self.field_dict['data'].dtype
    if dtype == nb.types.float32:
        dtype_npy = np.float32
    else:
        dtype = nb.types.float64
        dtype_npy = np.float64

    func_query_knn = ckdtree_ct.query_knn[dtype] 
    
    # single threaded case
    def _query_impl(self, X, k=1, p=2, eps=0.0, distance_upper_bound=np.inf):
        n_features = self.data.shape[1]
        xx = _convert_to_valid_input(X, n_features, dtype_npy)
        n_queries = xx.shape[0]
        if p < 1:
            raise ValueError("Only p-norms with 1<=p<=infinity permitted")

        dd = np.empty((n_queries, k), dtype=dtype_npy)
        ii = np.full((n_queries, k), fill_value=-1, dtype=INT_TYPE)
        nn = np.empty((n_queries,), dtype=INT_TYPE)

        for i in range(n_queries):
            func_query_knn(self.ckdtree, dd[i].ctypes, ii[i].ctypes, nn[i:i+1].ctypes,
                            xx[i].ctypes, 1, k, eps, p, distance_upper_bound)
        return dd, ii, nn

    return _query_impl
    

# parallel version
@overload_method(KDTreeNumbaType, "query_parallel", jit_options={"nogil": True, "cache": False, "fastmath": True, 'parallel': True})
def _ol_query_parallel(self, X, k=1, p=2, eps=0.0, distance_upper_bound=np.inf):
    # choose the appropriate methods based on the data type
    dtype = self.field_dict['data'].dtype
    if dtype == nb.types.float32:
        dtype_npy = np.float32
    else:
        dtype = nb.types.float64
        dtype_npy = np.float64

    func_query_knn = ckdtree_ct.query_knn[dtype]

    def _query_parallel_impl(self, X, k=1, p=2, eps=0.0, distance_upper_bound=np.inf):
        n_features = self.data.shape[1]
        xx = _convert_to_valid_input(X, n_features, dtype_npy)
        n_queries = xx.shape[0]

        if p < 1:
            raise ValueError("Only p-norms with 1<=p<=infinity permitted")
        
        dd = np.empty((n_queries, k), dtype=dtype_npy)
        ii = np.full((n_queries, k), fill_value=-1, dtype=INT_TYPE)
        nn = np.empty((n_queries,), dtype=INT_TYPE)

        for i in nb.prange(n_queries):
            func_query_knn(self.ckdtree, dd[i].ctypes, ii[i].ctypes, nn[i:i + 1].ctypes,
                            xx[i].ctypes, 1, k, eps, p, distance_upper_bound)
        return dd, ii, nn

    return _query_parallel_impl


@overload_method(KDTreeNumbaType, "query_radius", jit_options={"nogil": True, "cache": True, "fastmath": True, 'parallel': False})
def _ol_query_radius(self, X, r, p=2.0, eps=0.0, return_sorted=False, return_length=False):
    # choose the appropriate methods based on the data type
    dtype = self.field_dict['data'].dtype
    if dtype == nb.types.float32:
        dtype_npy = np.float32
    else:
        dtype = nb.types.float64
        dtype_npy = np.float64

    broadcast_r = (r != nb.types.Array)

    func_query_knn = ckdtree_ct.query_radius[dtype]
    radius_result_set_get_size = ckdtree_ct.radius_result_set_get_size
    radius_result_set_copy_and_free = ckdtree_ct.radius_result_set_copy_and_free

    result_array_type = types.int64[:]

    # noinspection PyShadowingNames
    def _query_radius_impl(self, X, r, p=2.0, eps=0.0, return_sorted=False, return_length=False):
        n_features = self.data.shape[1]
        xx = _convert_to_valid_input(X, n_features, dtype_npy)
        n_queries = xx.shape[0]

        # broadcast a scalar r into the appropriate shape
        if broadcast_r:
            r_ = np.broadcast_to(r, n_queries)
        else:
            r_ = _convert_to_valid_input/(r, 1, dtype_npy).squeeze()

            if r_.shape != (n_queries,):
                raise ValueError("Invalid shape for r. Must be broadcastable to the number of queries.")

        if p < 1:
            raise ValueError("Only p-norms with 1<=p<=infinity permitted")

        # prepare result list
        results_list = nb.typed.List.empty_list(item_type=result_array_type, allocated=n_queries)
        results_list.extend([np.empty(0, dtype=np.int64) for i in range(n_queries)])

        for i in range(n_queries):
            result_set = func_query_knn(self.ckdtree, xx[i].ctypes, 1, r_[i], eps, p, return_length, return_sorted)
            # copy the result set into a separate buffer owned by python
            num_results = radius_result_set_get_size(result_set)
            results = np.empty(num_results, dtype=np.int64)
            radius_result_set_copy_and_free(result_set, results.ctypes)
            results_list[i] = results

        return results_list

    return _query_radius_impl


@overload_method(KDTreeNumbaType, "query_radius_parallel", jit_options={"nogil": True, "cache": False, "fastmath": True, 'parallel': True})
def _ol_query_radius_parallel(self, X, r, p=2.0, eps=0.0, return_sorted=False, return_length=False):
    # choose the appropriate methods based on the data type
    dtype = self.field_dict['data'].dtype
    if dtype == nb.types.float32:
        dtype_npy = np.float32
    else:
        dtype = nb.types.float64
        dtype_npy = np.float64

    broadcast_r = (r != nb.types.Array)

    func_query_knn = ckdtree_ct.query_radius[dtype]
    radius_result_set_get_size = ckdtree_ct.radius_result_set_get_size
    radius_result_set_copy_and_free = ckdtree_ct.radius_result_set_copy_and_free

    result_array_type = types.int64[:]

    # noinspection PyShadowingNames
    def _query_radius_parallel_impl(self, X, r, p=2.0, eps=0.0, return_sorted=False, return_length=False):
        n_features = self.data.shape[1]
        xx = _convert_to_valid_input(X, n_features, dtype_npy)
        n_queries = xx.shape[0]

        # broadcast a scalar r into the appropriate shape
        if broadcast_r:
            r_ = np.broadcast_to(r, n_queries)
        else:
            r_ = _convert_to_valid_input/(r, 1, dtype_npy).squeeze()
            if r_.shape != (n_queries,):
                raise ValueError("Invalid shape for r. Must be broadcastable to the number of queries.")
            
        if p < 1:
            raise ValueError("Only p-norms with 1<=p<=infinity permitted")

        # prepare result list
        results_list = nb.typed.List.empty_list(item_type=result_array_type, allocated=n_queries)
        results_list.extend([np.empty(0, dtype=np.int64) for i in range(n_queries)])

        for i in nb.prange(n_queries):
            result_set = func_query_knn(self.ckdtree, xx[i].ctypes, 1, r_[i], eps, p, return_length, return_sorted)
            # copy the result set into a separate buffer owned by python
            num_results = radius_result_set_get_size(result_set)
            results = np.empty(num_results, dtype=np.int64)
            radius_result_set_copy_and_free(result_set, results.ctypes)
            results_list[i] = results

        return results_list

    return _query_radius_parallel_impl





@nb.njit(nogil=True, cache=True)
def _make_kdtree(data, root_bbox, idx, leafsize=10, balanced=False, compact=False) -> KDTreeNumbaType:
    # create the transparent underlying c object by calling the function appropriate to the data dtype
    kdtree = KDTreeType(root_bbox, data, idx)
    kdtree.build_index(leafsize, balanced, compact)
    return kdtree


def _restore_kdtree_impl(tree_buffer, data, root_bbox, leafsize, indices):
    # this is a stub for numba overload
    pass


@nb.extending.overload(_restore_kdtree_impl, jit_options={'nogil': True, 'fastmath': True, "cache": True})
def _ol_restore_kdtree_impl(tree_buffer, data, root_bbox, leafsize, indices):
    dtype = data.dtype
    if dtype == nb.types.float32:
        dtype_npy = np.float32
    else:
        dtype = nb.types.float64
        dtype_npy = np.float64

    func_init = ckdtree_ct.init[dtype]

    def _restore_kdtree_impl_impl(tree_buffer, data, root_bbox, leafsize, indices):
        data_conv = data.astype(dtype_npy) # is this really needed?
        n_data, n_features = data.shape
        kdtree = KDTreeType(root_bbox, data_conv, indices)
        nrt = NRT_get_api() # get the nrt API as a voidptr
        
        # call init with the existing tree
        kdtree.meminfo = func_init(nrt, tree_buffer.ctypes, tree_buffer.size, data_conv.ctypes, indices.ctypes, n_data, n_features, leafsize, root_bbox[0].ctypes, root_bbox[1].ctypes)
        kdtree.ckdtree = _meminfo_getdata(kdtree.meminfo) # get the handle to the actual c struct from the meminfo pointer
        return kdtree

    return _restore_kdtree_impl_impl


# wrapper function to call the overloaded function above
@nb.njit(cache=True)
def _restore_kdtree(tree_buffer, data, root_bbox, leafsize, indices):
    return _restore_kdtree_impl(tree_buffer, data, root_bbox, leafsize, indices)


# python constructor function
def KDTree(data: DataArray, leafsize: int = 10, compact: bool = False, balanced: bool = False, root_bbox: Optional[DataArray] = None) -> KDTreeType:
    """
    Represents a KDTree usable from python as well as within numba functions. The tree is represented by the custom structref KDTreeType and 
    can be freely constructed and passed between numba and regular python code. 
    The underlying implementation uses a modified version of the ckdtree 
    available in the scipy package (https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.cKDTree.html) 
    and is comparable regarding performance and results.
    The data array stored by reference if possible, so no additional copy will be made. The user has to ensure, 
    that the data is not modified during the lifetime of the tree to avoid corruption.

    The resulting KDTree is fully pickable and can be passed between processes and stored on disk. The data array will be serialized with the tree in that case.

    Args:
        data: The data to build the tree from as an array of shape (n, n_features). This array is not copied into the tree but stored by reference so it must 
              not be modified during the lifetime of the tree.
        leafsize: The maximum number of points in the leafs of the tree. Larger values result in a smaller tree but higher search time. Defaults to 10.
        compact: If True, the KDTree is built to shrink the hyperrectangles to the actual data range. 
                 This usually gives a more compact tree that is robust against degenerated input data and 
                 gives faster queries at the expense of longer build time. Defaults to False.
        balanced: If True, the median is used to split the hyperrectangles instead of the midpoint. 
                  This usually gives a more compact tree and faster queries at the expense of longer build time.
                  Defaults to False.
        root_bbox: Initial bounding box to use for the root. If None (default), the bounds will be determined from the data array before building the tree.

    Returns:
        The python proxy objects containing the KDTree.
    """
    if data.dtype == np.float32:
        conv_dtype = np.float32
    else:
        conv_dtype = np.float64

    data = np.ascontiguousarray(data).astype(conv_dtype)
    n_data, n_features = data.shape

    if root_bbox is None:
        # compute the bounding box
        mins = np.amin(data, axis=0) if n_data > 0 else np.zeros(n_features, dtype=conv_dtype)
        maxes = np.amax(data, axis=0) if n_data > 0 else np.zeros(n_features, dtype=conv_dtype)
        root_bbox = np.vstack((mins, maxes))

    root_bbox = np.ascontiguousarray(root_bbox, dtype=conv_dtype)

    idx = np.arange(n_data, dtype=INT_TYPE)

    kdtree = _make_kdtree(data, root_bbox, idx, leafsize, balanced, compact)
    return kdtree


# numba constructor implementation
@nb.extending.overload(KDTree, jit_options={'nogil': True, 'fastmath': True, 'cache': True})
def KDTree_numba(data, leafsize: int = 10, compact: bool = False, balanced: bool = False, root_bbox=None):
    if data.dtype == nb.types.float32:
        conv_dtype = nb.types.float32
        finfo = np.finfo(np.float32)

    else:
        conv_dtype = nb.types.float64
        finfo = np.finfo(np.float64)

    #cmax = finfo.max
    #cmin = finfo.min

    def KDTree_impl(data, leafsize=10, compact=False, balanced=False, root_bbox=None):
        data = np.ascontiguousarray(data).astype(conv_dtype)
        n_data, n_features = data.shape

        if root_bbox is None:
            # compute the bounding box
            mins = _np_min(data, 0) if n_data > 0 else np.zeros(n_features, dtype=conv_dtype)
            maxes = _np_max(data, 0) if n_data > 0 else np.zeros(n_features, dtype=conv_dtype)
            root_bbox_ = np.vstack((mins, maxes))
            # root_bbox_ = np.empty((2, n_features), dtype=data.dtype)
            # root_bbox_[0] = cmax
            # root_bbox_[1] = cmin

            # for i in range(n_data):
            #     for j in range(n_features):
            #         if data[i, j] < root_bbox_[0, j]:
            #             root_bbox_[0, j] = data[i, j]
            #         if data[i, j] > root_bbox_[1, j]:
            #             root_bbox_[1, j] = data[i, j]
        else:
            root_bbox_ = root_bbox
        root_bbox__ = np.ascontiguousarray(root_bbox_).astype(conv_dtype)


        idx = np.arange(n_data, dtype=INT_TYPE)

        kdtree = _make_kdtree(data, root_bbox__, idx, leafsize, balanced, compact)

        return kdtree

    return KDTree_impl
