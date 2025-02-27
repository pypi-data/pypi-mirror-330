#include <stdio.h>
#include <stdlib.h>
#include "project_onto_PPM.h"

int main(int argc, const char * argv[]) {
    
    // we are going to minimize || DF - D U M ||, where D is diagonal, U is a matrix of ancestors, and M is a vector of vectors in the simplex
    
    // read the flag that sets the cols of M to be on the probability simplex, or on the interior+boundary of the probability simplex
    // If inner_flag=1, then cols must sum to 1.
    int inner_flag = 0;
    
    // we read a file with all of the data
    FILE* fptr = stdin;
    // read buff
    int Ibuff;
    float Dbuff;
    // read the size of the data
    shortint num_nodes, T;
    fscanf(fptr, "%d ", &Ibuff); num_nodes = (shortint) Ibuff;
    fscanf(fptr, "%d\n", &Ibuff); T = (shortint) Ibuff;
    // read the F data
    realnumber *data = (realnumber *) malloc(num_nodes*T*sizeof(realnumber));
    for (int i = 0; i < num_nodes*T - 1; i++){
        fscanf(fptr, "%f ", &Dbuff); data[i] = (realnumber) Dbuff;
    }
    fscanf(fptr, "%f\n", &Dbuff); data[num_nodes*T - 1] = (realnumber) Dbuff;
    // read the diagonal data
    realnumber *gamma_init = (realnumber *) malloc(num_nodes*sizeof(realnumber));
    for (int i = 0; i < num_nodes - 1; i++){
        fscanf(fptr, "%f ", &Dbuff); gamma_init[i] = (realnumber) 1/(Dbuff*Dbuff);
    }
    fscanf(fptr, "%f\n", &Dbuff); gamma_init[num_nodes - 1] = (realnumber) 1/(Dbuff*Dbuff);
    // transform the data, F_hat, before computing the cost
    for (int t = 0; t < T; t++) {
        for (int i = 0; i < num_nodes; i++) {
            data[T*i + t] = data[T*i + t] / gamma_init[i];
        }
    }
    // read the root
    shortint root_node;
    fscanf(fptr, "%d\n", &Ibuff); root_node = (shortint) Ibuff;
    // read the list of degrees
    shortint *final_degrees = (shortint *) malloc(num_nodes*sizeof(shortint));
    for (int i = 0; i < num_nodes - 1; i++){
        fscanf(fptr, "%d ", &Ibuff); final_degrees[i] = (shortint) Ibuff;
    }
    fscanf(fptr, "%d\n", &Ibuff); final_degrees[num_nodes - 1] = (shortint) Ibuff;
    // read the tree adjacency matrix. Read as an undirected graph. The tree must be connected. All node degrees >= 1
    shortint *adj_list = (shortint *) malloc(num_nodes*num_nodes*sizeof(shortint));
    for (int i = 0; i < num_nodes; i++){
        for (int j = 0; j < final_degrees[i] - 1; j++){
            fscanf(fptr, "%d ", &Ibuff); adj_list[num_nodes*i + j] = (shortint) Ibuff;
        }
        fscanf(fptr, "%d\n", &Ibuff); adj_list[num_nodes*i + final_degrees[i] - 1] = (shortint) Ibuff;
    }
    
    // read output flag
    fscanf(fptr, "%d\n", &Ibuff);
    shortint compute_M_flag = Ibuff;
    fclose(fptr);

    
    realnumber *M_recon = (realnumber * ) malloc(num_nodes*T*sizeof(realnumber));
    realnumber cost = tree_cost_projection(inner_flag,compute_M_flag, M_recon, num_nodes, T, data, gamma_init, root_node, NULL, NULL, final_degrees, adj_list);
    
    // output result
    fptr = stdout;
    fprintf(fptr, "%f\n", (float) cost);
    
    if (compute_M_flag == 1){
        for (int i = 0; i < T*num_nodes; i++){
            fprintf(fptr, "%f ", (float) M_recon[i]);
        }
    }
    fprintf(fptr, "\n");
    fclose(fptr);
    
    free(M_recon);
    free(gamma_init);
    free(final_degrees);
    free(adj_list);
    free(data);
    
     
    return 0;
}
