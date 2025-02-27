#define MAX_N_NODES 1300 // maximum size of tree that we will be dealing with. For larger trees, use mallocs on corresponding arrays

typedef double realnumber;
typedef unsigned long int longint;
typedef short int shortint;

typedef struct {
    shortint first;
    shortint second;
} edge;

realnumber tree_cost_projection(shortint inner_flag, shortint compute_M_flag, realnumber *M, shortint num_nodes, shortint T, realnumber *data, realnumber gamma_init[], shortint root_node, edge *tree, shortint *adjacency_mat, shortint *final_degrees, shortint *adj_list);
