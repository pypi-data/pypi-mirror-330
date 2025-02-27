import numpy as np
import pandas as pd
import networkx as nx
from tqdm import tqdm
from anndata import AnnData
from datetime import datetime
from collections import defaultdict
from sklearn.neighbors import NearestNeighbors
from typing import Union, Optional, Tuple, Sequence, Dict, Any

from ..util import find_knee
from .tree_utils import _edge_two_ends
from .trajectory import cumsum_Hspace, M_create_matrix_coordinates_trajectory_Hspace


def edge_cumsum_median(adata,
                       full_traj_matrix:str="full_traj_matrix",
                       clusters:str = "trajs_clusters",
                       evector_name:str = None,
                       verbose=True,
                      ):
    """
    for all edges in the cumsum space, we calculate the median of the edge cumsum coordinate

    Parameters
    ----------
    adata: :class:`~anndata.AnnData`
        an Annodata object
    full_traj_matrix: `str` (default: `full_traj_matrix`)
        the key in `adata.uns` where the full trajectory matrix is stored
    clusters: `str` (default: `trajs_clusters`)
        the key in `adata.uns` where the cluster labels are stored
    evector_name: `str` (default: None)
        the key in `adata.uns` where the eigenvectors are stored
    verbose: `bool` (default: `True`)
        whether to print the progress bar
    """
    if "graph_basis" in adata.uns.keys() and not evector_name:
        evector_name = adata.uns["graph_basis"] + "_triangulation_circle_L1Norm_decomp_vector"
    if 'eigen_value_knee' in adata.uns.keys():
        knee = adata.uns['eigen_value_knee']
    else:
        knee = find_knee(adata)
    if verbose:
        print(datetime.now(), "projecting trajs to harmonic...")
    mat_coord_Hspace = M_create_matrix_coordinates_trajectory_Hspace(adata.uns[evector_name][:knee],
                                                                                adata.uns[full_traj_matrix])
    if verbose:
        print(datetime.now(), "cumsum...")
    cumsums =cumsum_Hspace(mat_coord_Hspace, range(knee))


    if verbose:
        print(datetime.now(), "edge cumsum dict...")

    itrajs = range(len(cumsums))
    edges_cumsum_dict = defaultdict(list)
    for itraj in tqdm(itrajs):
        traj_mtx = adata.uns[full_traj_matrix][itraj]
        traj_edge_idx = [j for i in np.argmax(np.abs(traj_mtx.astype(int)), axis=0).tolist() for j in i]
        for i, edge_idx in enumerate(traj_edge_idx):
            edges_cumsum_dict[edge_idx].append(cumsums[itraj][i, ])
    edge_median_dict = {k: np.median(v, axis=0) for k,v in edges_cumsum_dict.items()}
    #edge_median_dict = {k: np.mean(v, axis=0) for k,v in edges_cumsum_dict.items()}
    if verbose:
        print(datetime.now(), "done...")
    return edge_median_dict

def node_cumsum_coor(adata, d_edge, d_e2n, approximate_k=5):
    """
    construct node to edges list dict to enumerate all edge connect to this node
    When a node is not visited, just find the top 5 nearest nodes has been visited and use their average of

    Parameters
    ----------
    adata: :class:`~anndata.AnnData`
        an Annodata object
    d_edge: `dict`
        the edge to its median cumsum coordinate dict
    d_e2n: `dict`
        the edge to its two ends node dict
    approximate_k: `int` (default: 5)
        when a node has no edge being visited, find its 5 nearest visited nodes and assign the average the cumsum coordinate
    """
    d_n2e = defaultdict(list)
    for k, vs in d_e2n.items():
        for v in vs:
            d_n2e[v].append(k)
    ## get mean of a node by the edge cumsum coordinate
    d_cumsum_nodes = {}
    unvisited = []
    for k,vs in d_n2e.items():
        cumsum_arr = np.array([d_edge[v] for v in vs if v in d_edge])
        if len(cumsum_arr) == 0:
            unvisited.append(k)
            continue
        d_cumsum_nodes[k] = np.mean(cumsum_arr, axis=0)


    if len(unvisited) > 0:
        print(f"there are {len(unvisited)} nodes not visited in the tree")
        print(f"will approximate the node cumsum coordinate by {approximate_k} nearest accessible neighbors")
    ## assign the mean cumsum coordinate to the missing node.
    X = adata.obsm['X_pca']
    nbrs = NearestNeighbors(n_neighbors=len(unvisited)+approximate_k + 1, algorithm='ball_tree').fit(X)
    distances, indices = nbrs.kneighbors(X)
    s = set(unvisited)
    for uv in unvisited:
        ids = [i for i in indices[uv][1:] if i not in s][:approximate_k]
        cumsum_arr = np.array([d_cumsum_nodes[v] for v in ids])
        d_cumsum_nodes[uv] = np.mean(cumsum_arr, axis=0)

    return d_cumsum_nodes

def add_root_cumsum(adata, evector_name=None, fate_tree:str='fate_tree', iscopy=False):
    """
    root cumsum is the mean of the root node

    Since the random walk is a wide range start, we need the root be the very first nodes in the tree
    The cumsum would be not available for the root node.

    Thus the root cumsum is just can be the harmonic coordinate of the root nodes.

    Parameters
    ----------
    adata: :class:`~anndata.AnnData`
        an Annodata object
    evector_name: `str` (default: None)
        the key in `adata.uns` where the eigenvectors are stored
    fate_tree: `str` (default: `fate_tree`)
        the key in `adata.uns` where the fate tree is stored
    iscopy: `bool` (default: `False`)
        whether to return a copy of adata or not
    """
    import networkx as nx

    adata = adata.copy() if iscopy else adata

    if "graph_basis" in adata.uns.keys() and not evector_name:
        evector_name = adata.uns["graph_basis"] + "_triangulation_circle_L1Norm_decomp_vector"
    if 'eigen_value_knee' in adata.uns.keys():
        knee = adata.uns['eigen_value_knee']
    else:
        knee = phlower.tl.find_knee(adata)

    n_edges = adata.uns[evector_name].shape[1]
    n_edges


    n_ecount = len(adata.uns[fate_tree].nodes['root']['ecount'] )
    n_ecount

    m = np.zeros(shape=(n_edges, n_ecount))
    for i, (k,v) in enumerate(adata.uns[fate_tree].nodes['root']['ecount'][:knee]):
        m[k, i] = 1
    coord_Hspace = adata.uns[evector_name][:knee] @ m
    attrs = {'root': {"cumsum": np.mean(coord_Hspace, axis=1)}}
    #print(attrs)
    nx.set_node_attributes(adata.uns[fate_tree], attrs)

    return adata if iscopy else None

def trans_tree_node_attr(adata, from_='fate_tree', to_='stream_tree', attr='cumsum', iscopy=False):
    """
    transfer node attribute from fate_tree to stream_tree

    Parameters
    ----------
    adata: :class:`~anndata.AnnData`
        an Annodata object
    from_: `str` (default: `fate_tree`)
        the key in `adata.uns` where the node attribute is stored
    to_: `str` (default: `stream_tree`)
        the key in `adata.uns` where the node attribute is stored
    attr: `str` (default: `cumsum`)
        the node attribute to be transfered
    iscopy: `bool` (default: `False`)
        whether to return a copy of adata or not
    """
    adata = adata.copy() if iscopy else adata
    if attr not in adata.uns[from_].nodes['root']:
        raise ValueError(f"attr {attr} is not an node attribute of tree {from_}")
    attrs = nx.get_node_attributes(adata.uns[from_], attr)
    to_attrs = {k:{'cumsum': attrs[k] } for k in adata.uns[to_].nodes()}
    nx.set_node_attributes(adata.uns[to_], to_attrs)

    return adata if iscopy else None


def node_cumsum_mean(adata,
                     graph_name = None,
                     full_traj_matrix:str="full_traj_matrix",
                     clusters:str = "trajs_clusters",
                     evector_name:str = None,
                     approximate_k:int = 5,
                     iscopy=False,
                     verbose=True,
                     ):

    """
    get each node cumsum coordinate:
        1. get each edge cumsum coordinate median
        2. average cumsum of all edges that connect to a node
        3. add the cumsum to cumsum_mean

    Parameters
    ----------
    adata: :class:`~anndata.AnnData`
        an Annodata object
    graph_name: `str` (default: None)
        the key in `adata.uns` where the graph is stored
    full_traj_matrix: `str` (default: `full_traj_matrix`)
        the key in `adata.uns` where the full trajectory matrix is stored
    clusters: `str` (default: `trajs_clusters`)
        the key in `adata.uns` where the cluster labels are stored
    evector_name: `str` (default: None)
        the key in `adata.uns` where the eigenvectors are stored
    approximate_k: `int` (default: 5)
        the number of nearest neighbors to approximate the cumsum coordinate of the missing node
    iscopy: `bool` (default: `False`)
        whether to return a copy of adata or not
    verbose: `bool` (default: `True`)
        whether to print the progress bar or not
    """
    adata = adata.copy() if iscopy else adata


    if len(adata.uns['fate_tree'].nodes['root']['cumsum']) == 0:
            add_root_cumsum(adata, evector_name=evector_name, fate_tree='fate_tree')
    trans_tree_node_attr(adata, from_='fate_tree', to_='stream_tree',  attr='cumsum')


    if "graph_basis" in adata.uns.keys() and not graph_name:
        graph_name = adata.uns["graph_basis"] + "_triangulation_circle"

    d = edge_cumsum_median(adata, full_traj_matrix, clusters, evector_name, verbose)
    d_e2n = _edge_two_ends(adata, graph_name=graph_name)
    d_node_cumsum = node_cumsum_coor(adata, d, d_e2n, approximate_k=approximate_k)
    assert(len(d_node_cumsum) == adata.n_obs)

    ## sort by the node order of adata
    cumsum_mean = np.array([j for i,j in sorted(d_node_cumsum.items(), key=lambda x: x[0], reverse=False)])
    adata.obsm['cumsum_mean'] = cumsum_mean
    return adata if iscopy else None

def stream_tree_order_end_nodes(stree):
    """
    construct a dataframe to list all branches with 2 milestones ends
    like:
    	from	from_id	to	to_id	length	directed
        0	root	-1	0_28	0	1	True
        1	0_28	0	1_77	1	1

    Parameters
    ----------
    stree: `nx.DiGraph`
        the stream tree
    """
    #return [a,b if() for a,b in node_pair_list]

    from_list = []
    fromid_list = []
    toid_list = []
    to_list = []
    len_list = []
    idx_list = []

    for idx, (a,b) in enumerate(stree.edges()):
        i1 = a.split("_")
        i2 = b.split("_")
        ## pairs with root
        if i1[0] == 'root':
            from_list.append(a)
            fromid_list.append(-1)
            to_list.append(b)
            toid_list.append(i2[0])
            len_list.append(int(i2[1]) + 1)
            idx_list.append(idx)
        elif i2[0] == "root":
            from_list.append(b)
            fromid_list.append(-1)
            to_list.append(a)
            toid_list.append(i1[0])
            len_list.append(int(i1[1]) + 1)
            idx_list.append(idx)
        elif int(i1[0]) > int(i2[0]):
            from_list.append(b)
            fromid_list.append(i2[0])
            to_list.append(a)
            toid_list.append(i1[0])
            len_list.append(int(i1[1]) - int(i2[1]) + 1)
            idx_list.append(idx)
        else:
            from_list.append(a)
            fromid_list.append(i1[0])
            to_list.append(b)
            toid_list.append(i2[0])
            len_list.append(int(i2[1]) - int(i1[1]) + 1)
            idx_list.append(idx)
    df = pd.DataFrame({
        "from": from_list,
        "from_id": map(int, fromid_list),
        "to": to_list,
        "to_id": map(int, toid_list),
        #"length": len_list,
        "length": 1,
        "directed": [True]*len(len_list),
    })

    df.sort_values(by=['from_id', 'to_id'], inplace=True)
    #df.index = range(0, max(df.index))
    df.reset_index(inplace=True, drop=True)

    return df
#endf stream_tree_order_end_nodes


def pnt2line(pnt, start, end):
    """
    http://www.fundza.com/vectors/point2line/index.html
    calulate the distance from a point to a segment(start,end)

    Parameters
    ----------
    pnt: 1d array
    start: 1d array
    end: 1d array

    Returns
    -------
    distance: float
        euclidean distance from pnt to the segment
    nearest: 1d array
        the nearest point on the segment
    """
    pnt = np.array(pnt)
    start = np.array(start)
    end = np.array(end)

    line_vec = end - start
    pnt_vec = pnt - start
    line_len = np.linalg.norm(line_vec)
    line_unitvec = line_vec/line_len
    pnt_vec_scaled = pnt_vec/line_len
    t = np.dot(line_unitvec, pnt_vec_scaled)
    #print(t)
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0

    nearest = line_vec * t
    dist = np.linalg.norm(nearest -  pnt_vec)
    nearest = nearest + start
    return (dist, nearest)

def tree_milestone_belonging(adata, stream_tree='stream_tree', df_branches=None, iscopy=False, verbose=True):
    """
    calculate the belonging of each node, top two nearest milestone.
    each node calculate all milestone distances.
    for the top 2, which top are in the branches list

    Should be similar as stream, each node need project to the segment of each branch to decide which branch it belongs to.
    otherwise there would be a problem of branch belong assigning, e.g.
    The following x is close to o2 and o3, but x is in the branch o1-o2.

             |-----------o
             |         |-o3
    ---------o1-----x--o2
             |         |-----o
             |------------------------

    Parameters
    ----------
    adata: AnnData
        adata that contains the stream tree
    stream_tree: str
        key of the stream tree in adata.uns
    df_branches: pd.DataFrame
        dataframe to store branches structure
    iscopy: bool
        return a copy of adata if True
    verbose: bool
        print verbose information
    """
    #stream_tree = 'stream_tree'
    #df_branches = df
    cumsum_mean = adata.obsm['cumsum_mean']
    adata = adata.copy() if iscopy else adata

    ## create a dataframe to store cumsum_dist
    df_dist = pd.DataFrame(columns=  [f"{df_branches.loc[j, 'from']}->{df_branches.loc[j, 'to']}" for j in df_branches.index])
    cumsum_branch = []
    df_percent = pd.DataFrame(columns=  ['start_milestone', 'end_milestone', 'start_pct', 'end_pct', 'nearest'])
    for i in range(adata.n_obs): ## each node
        #print(i)
        dist_dic = {}
        shortest_dist = -10 ## intialized as a negative number
        shortest_info = []
        for j in df_branches.index:
            start_name = df_branches.loc[j, 'from']
            end_name = df_branches.loc[j, 'to']
            start = nx.get_node_attributes(adata.uns[stream_tree], 'cumsum')[start_name]
            end = nx.get_node_attributes(adata.uns[stream_tree], 'cumsum')[end_name]
            pnt = cumsum_mean[i, :]
            dist, nearest = pnt2line(pnt, start, end)
            dstart = np.linalg.norm(nearest-start)
            dend = np.linalg.norm(nearest-end)
            #print(f'[{start_name}  ->  {end_name}]   ', round(dist,2), "    starts: ", round( dstart,2), "    end: ",round(dend, 2))
            dist_dic[f'{start_name}->{end_name}'] = [dist]

            #store the shortest dist info
            if (shortest_dist < 0) or (shortest_dist > dist):
                shortest_dist = dist
                shortest_info = (start_name, end_name, 1-(dstart/(dstart+dend)), 1-(dend/(dstart+dend)), nearest)

        #print(shortest_info)
        df_percent = pd.concat([df_percent,
                                pd.DataFrame({
                                    'start_milestone':[shortest_info[0]],
                                    'end_milestone':[shortest_info[1]],
                                    'start_pct':[shortest_info[2]],
                                    'end_pct':[shortest_info[3]],
                                    'nearest':[shortest_info[4]]
                                })])
        cumsum_branch.append(f'{shortest_info[0]}->{shortest_info[1]}')
        df_dist = pd.concat([df_dist, pd.DataFrame(dist_dic)])
        #break

    if verbose:
        print(datetime.now(), "adding cells cumsum branch assignment[cumsum_branch] to adata.obs...")
    adata.obs['cumsum_branch'] = cumsum_branch

    if verbose:
        print(datetime.now(), "adding cells cumsum dist [cumsum_dist] to adata.obsm...")
    df_dist.index = adata.obs_names
    adata.obsm['cumsum_dist'] = df_dist

    if verbose:
        print(datetime.now(), "adding cells percentage to milestones [cumsum_percent] to adata.obsm...")

    df_percent.index = adata.obs_names
    adata.obsm['cumsum_percent'] = df_percent

    return adata if iscopy else None


def get_milestone_percentage(adata, obsm_key='cumsum_percent'):
    """
    get dataframe for dynverse like:
    	cell_id	milestone_id	percentage
           0	root	0.824578
           1	root	0.94362

    Parameters
    ----------
    adata: AnnData
        adata that contains the stream tree
    obsm_key: str
        key of the obsm that contains the percentage information
    """
    df = adata.obsm[obsm_key]
    df1 = df.loc[:, ('start_milestone', 'start_pct')]
    df2 = df.loc[:, ('end_milestone', 'end_pct')]
    df1['cell_id'] = df1.index
    df2['cell_id'] = df2.index
    df1 = df1.rename(columns={"start_milestone": "milestone_id", "start_pct": "percentage"})
    df2 = df2.rename(columns={"end_milestone": "milestone_id", "end_pct": "percentage"})

    return pd.concat([df1, df2])
