# Preference Generalisation 

Instructions for how to set up and run Preference Generalisation experiments using the Envelope Q-Learning and D3PO algorithms. This setup is designed for a Linux OS. If you are a Windows user then complete the following steps in WSL with anaconda installed in WSL and keep the project in the linux file systme not under /mnt/c.

**SEE OTHER NOTES AT THE BOTTOM OF THE PAGE BEFORE RUNNING ANY CODE!**

## Setting Up

1. Run the command `git clone https://github.com/Cil-liers/preference-generalisation.git` to receive necessary files and then run `cd preference-generalisation`.
2. Next download and install [anaconda](https://www.anaconda.com/docs/getting-started/installation) if not already installed. 
3. Once anaconda is installed create two environments the first called _my_env_ and the second called _my_env_d3po_. These environments represent the conda environments for Envelope Q-Learning and D3PO, respectively.
4. Setting up the environments and their dependencies.  
    
    1. In order to setup _my_env_, run the following commands in order. 
        - `conda create --name my_env`
        - `conda activate my_env` 
        - `conda install python=3.12`
        - `git clone https://github.com/Cil-liers/morl-baselines-ben.git` NOTE: This must be cloned into the preference-generalisation directory.
        - `cd morl-baselines-ben`
        - `pip install -e .` NOTE: In the morl-baselines-ben/pyproject.toml file the pycddlib is commented out as it gave problems (It is not needed to run this code).
        - `conda install mo-gymnasium`
    2. In order to setup _my_env_d3po_, run the following commands in order.
        - `cd ..` NOTE: Ensures one leaves the morl-baselines-ben directory.
        - `git clone https://github.com/Cil-liers/reward-decomposition.git`
        - `cd reward-decomposition`
        - `sudo apt update` and `sudo apt install -y build-essential swig` NOTE: The reason for this is to prevent an error that might occur when running the next command.
        - `conda env create -f environment.yml -n my_env_d3po` NOTE: This may fail as the environment.yml lists box2d-py before swig, when box2d-py needs swig installed. If you have received this error run the above command and then run this command `conda env update -n my_env_d3po -f environment.yml`.
        - `conda activate my_env_d3po`

## Running the Algorithms

To run the each algorithm there exists specific bash files. _run_envelope.sh_ is used to run the Envelope Q-Learning algorithm and _run_d3po.sh_ is used to run the D3PO algorithm. 

1. Running the _run_envelope.sh_ file.

    - When running the _run_envelope.sh_ file one needs to specify which file they desire to run. By default _run_envelope.sh_ runs the default Envelope Q-Learning experiment. To run a different experiment, the interpolation experiment for example, one would must include `ENVELOPE_FILE=envelope_minecart_inter.py` when running the bash command. The experiment files can be found in the envelope directory. 

    - To edit the hyperparameters one needs to go into the envelope directory and change the hyperparameters in the Envelope constructor of the files found in envelope directory. The only hyperparameters that may need to change are `experiment_name` which sets the name of the experiment, `log` which allows one to log the results to [wandb](https://wandb.ai/site/) and `seed` which sets the seed.

    - Once the hyperparameters are edited, run `bash run_envelope.sh` to run the algorithm. If you want to specify an experiment such as the interpolation one, run `ENVELOPE_FILE=envelope_minecart_inter.py bash run_envelope.sh`.

2. Running the _run_d3po.sh_ file.
    
    - When running the _run_d3po.sh_ file one needs to specify which experiment they want to run and whether they want to log their results to [wandb](https://wandb.ai/site/). To log the results and specify which experiment they want to run one needs to include `USE_WANDB=True` and `MAIN_VERSION=main_ppo_extr.py` (if they wanted to run the extrapolation experiment, for example) in their bash command. By default _run_d3po.sh_ does not log the results and uses the default experiment of D3PO. The other experiment files can be found in the D3PO directory. One can edit the hyperparameters on the last line of _run_d3po.sh_. To change the experiment name however one must specify the name they desire at the end of the bash command, for example `bash run_d3po.sh desired_experiment_name`. If one does not specify a name d3po_minecart is used as default.

    - To perform a run that includes logging the results, uses the interpolation experiment and uses a specific experiment name one would run the command `USE_WANDB=True MAIN_VERSION=main_ppo_inter.py bash run_d3po.sh interpolation_experiment`

    - To perform a run without logging the results, uses the default experiment and does not specific an experiment name one would run `bash run_d3po.sh`

## Other Notes 

**DO NOT EDIT THE FOLLOWING FILES!**

1. Any file in the data folder.
2. D3PO/ppo.py as it contains the changes required by D3PO to test generalisation.
3. envelope/envelope.py as it contains changes required by Envelope Q-Learning to test generalisation.

The bash scripts edit the cloned repositories with changes to incorporate generalisation into the algorithms. For Envelope Q-Learning the envelope.py file in the morl-baselines-ben/morl_baselines/multi_policy/envelope/ directory is changed. For D3PO the main_ppo.py and the ppo.py files are changed in the reward-decomposition and reward-decomposition/ppo/ directories, respectively.

To log ones results one must have a [wandb](https://wandb.ai/site/) account. 

