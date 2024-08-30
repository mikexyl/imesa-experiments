set shell := ["bash", "-c"]

noise := '3'
zeros := '1'
r := '3'
nr := '5'
dataset_dir := '/workspaces/src/imesa-experiments/data/datasets'

generate-2d-noise:
  mkdir -p {{dataset_dir}}/2d_10r_noised && \
  experiments/scripts/make-multi-robot-dataset-2d -o {{dataset_dir}}/2d_10r_noised -n {{noise}} -nr 10 -r {{r}} --xlims -50 50 --ylims -50 50 --noised_zeros {{zeros}} --zeros_sigmas {{noise}} {{noise}} 1

plot-many-results:
  ./experiments/scripts/plot-many-results -d {{dataset_dir}}/2d_10r_noised/raido/aligned -r /workspaces/src/imesa-experiments/results/2d_10r_noised -g 2 5

make-2d-10r-noise-prior:
  mkdir -p {{dataset_dir}}/2d_{{nr}}r_noised_prior && \
  for i in $(seq 5 1 20); do \
    experiments/scripts/make-multi-robot-dataset-2d \
     -o {{dataset_dir}}/2d_{{nr}}r_noised_prior \
     -n $i \
     -nr {{nr}} \
     -r {{r}} \
     --xlims -50 50 \
     --ylims -50 50 \
     --prior_noise_sigmas $i $i 1 \
     --noised_zeros 3 ; \
  done

make-2d-5r-random-prior:
  mkdir -p {{dataset_dir}}/2d_5r_random_prior && \
  experiments/scripts/make-multi-robot-dataset-2d \
    -o {{dataset_dir}}/2d_5r_random_prior \
    -nr 5 \
    -n random \
    -r {{r}} \
    --xlims -50 50 \
    --ylims -50 50 \
    --noised_zeros 2 

make-2d-5r-zero-prior:
  mkdir -p {{dataset_dir}}/2d_5r_zero_prior && \
  experiments/scripts/make-multi-robot-dataset-2d \
    -o {{dataset_dir}}/2d_5r_zero_prior \
    -nr 5 \
    -n zero \
    -r {{r}} \
    --xlims -50 50 \
    --ylims -50 50 \
    --noised_zeros 4

make-2d-nr-noise:
  mkdir -p {{dataset_dir}}/2d_nr && \
  for i in $(seq 2 1 20); do \
    experiments/scripts/make-multi-robot-dataset-2d \
     -o {{dataset_dir}}/2d_nr_noised \
     -n $i \
     -nr $i \
     -r {{r}} \
     --xlims -50 50 \
     --ylims -50 50 \
     --prior_noise_sigmas $i $i 1 \
     --noised_zeros 3 ; \
  done
