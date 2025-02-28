#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>
#include <omp.h>

#define INIT_TEMP 1000.0   // Initial temperature
#define COOLING_RATE 0.995 // Cooling rate per iteration
#define ITERATIONS 1000  // Max iterations per thread
#define NUM_THREADS 4      // Number of parallel SA runs

// Function to check if a vertex can be added to the independent set
bool is_valid(int **adj, bool *independent_set, int n, int new_vertex) {
    for (int i = 0; i < n; i++) {
        if (independent_set[i] && adj[new_vertex][i] == 1) {
            return false;
        }
    }
    return true;
}

// Function to compute the size of an independent set
int independent_set_size(bool *independent_set, int n) {
    int size = 0;
    for (int i = 0; i < n; i++) {
        if (independent_set[i]) {
            size++;
        }
    }
    return size;
}

// Simulated Annealing for Maximum Independent Set (parallel version)
void simulated_annealing_mis(int **adj, int n, bool *global_best_set) {
    int global_best_size = 0;
    bool **best_sets = (bool **)malloc(NUM_THREADS * sizeof(bool *));

    #pragma omp parallel num_threads(NUM_THREADS)
    {
        int thread_id = omp_get_thread_num();
        bool *independent_set = (bool *)calloc(n, sizeof(bool));
        bool *best_set = (bool *)calloc(n, sizeof(bool));
        int best_size = 0;
        double T = INIT_TEMP;

        for (int i = 0; i < n; i++) {
            if (rand() % 2 == 0 && is_valid(adj, independent_set, n, i)) {
                independent_set[i] = true;
            }
        }
        best_size = independent_set_size(independent_set, n);
        for (int i = 0; i < n; i++) best_set[i] = independent_set[i];

        // Simulated Annealing loop
        for (int iter = 0; iter < ITERATIONS; iter++) {
            int v = rand() % n; // Pick a random vertex

            // Flip the vertex state (add/remove it from the set)
            bool prev_state = independent_set[v];
            independent_set[v] = !prev_state;

            // Ensure the new set remains independent
            if (!is_valid(adj, independent_set, n, v)) {
                independent_set[v] = prev_state; // Revert if invalid
            } else {
                // EXTRA VALIDATION: Ensure entire set is still independent
                for (int i = 0; i < n; i++) {
                    if (independent_set[i]) {
                        for (int j = 0; j < n; j++) {
                            if (i != j && independent_set[j] && adj[i][j] == 1) {
                                independent_set[v] = prev_state; // Revert if found conflict
                                break;
                            }
                        }
                    }
                }
                int new_size = independent_set_size(independent_set, n);
                int size_diff = new_size - best_size;

                // Accept better solutions or probabilistically accept worse ones
                if (size_diff > 0 || (exp(size_diff / T) > ((double)rand() / RAND_MAX) && is_valid(adj, independent_set, n, v))) {
                    if (new_size > best_size) {
                        best_size = new_size;
                        for (int i = 0; i < n; i++) best_set[i] = independent_set[i];
                    }
                } else {
                    independent_set[v] = prev_state; // Revert change
                }
            }

            // Cool down temperature
            T *= COOLING_RATE;
        }
        // Store thread's best result
        best_sets[thread_id] = best_set;

        // Synchronization to update global best solution
        #pragma omp critical
        {
            if (best_size > global_best_size) {
                global_best_size = best_size;
                for (int i = 0; i < n; i++) {
                    global_best_set[i] = best_set[i];
                }
            }
        }

        free(independent_set);
    }

    // Free thread-specific allocations
    for (int t = 0; t < NUM_THREADS; t++) {
        free(best_sets[t]);
    }
    free(best_sets);
}
