# Installation & Execution

1. ### Clone the repository

```sh
git clone https://github.com/justheretostealcode/ARCTIC-GUI.git
```

2. ### Install Python and Java

Java version 11 is tested, higher versions may not work.

Either get an Java installer from [orecal](https://www.oracle.com/java/technologies/javase/jdk11-archive-downloads.html) or manually install Java from [openjkd](https://jdk.java.net/archive).

#### Manually Java install 

1. download jdk11.0.2 from [here](https://jdk.java.net/archive).

2. unzip the downloded file

3. move the folder to a permanent location

4. add the path to the bin folder in that folder to the PATH environment variable.

   - on Windows: `setx PATH "%PATH%;<path to bin filder>"`
   - on Linux: `echo -e "\\nexport PATH='$PATH:<path to bin filder>'" >> ~/.bashrc`
   - on MacOS: `echo "<path to bin filder>" | sudo tee /etc/paths.d/JDK`

5. ## Install the necessary Python modules.

- numpy==1.26.4
- flet==0.25.1
- scipy
- sympy
- Autograd
- matplotlib
- Cython
- Deprecated
- GvGen
- POT
- seaborn
- pillow

```sh
python -m pip install numpy==1.26.4 flet==0.26.4 scipy sympy Autograd matplotlib Cython Deprecated GvGen POT seaborn pillow
```

4. ### Set the path to the Python binary in `ARCTICsyn/sim.config`

If you use the GUI and want to use the same Python installation for the GUI as for the simulation you don't have to do this step.

This has to be an absolute path to an Python executable.

```toml
PYTHON_BINARY=<<Path to your Python binary>>
```

5. ### Run the GUI for Arctic

```shell
python ARCTICgui/src/main.py
```

oder

```shell
flet run ARCTICgui/src/main.py
```

# ARCTICgui

The Arctic GUI has it's own config files for map, sim and syn. Additionally there is a gui conficg file.

- **LANGUAGE_PATH** path to the language file
- **START_WIDTH** window width at startup in pixel
- **START_HEIGHT** window height at startup pixel



## Language files

the default language file is in `./ARCTICgui/src/lang/en_lang.txt` and for translating the text of the GUI you have to make a new file that copies the keys and translate the values of that file.

```
# Comments
[key]=[value]
```


# Run the Synthesis with Standard Settings

The following example command calls ARCTIC via Gradle and synthesizes the three input Boolean function "**a&(b|c)**".

````shell
cd ./ARCTICsyn
./gradlew run --args="-f a&(b|c)"
````

This command synthesizes the circuit structures and performs technology mapping on them with the preset genetic gate library. When the process is finished, the best found circuit structure and assignment of logic gates as well as the corresponding score is printed out. In the directory `./ARCTICsyn/benchmarks` a new directory corresponding to the run has been created containing all found circuit structures as DOT and JSON files as well as structure and assignment of gates for the resulting circuit.

# Run Synthesis

``` sh
cd ./ARCTICsyn
./gradlew run --args="<argument list>"
```


| argument name              | description                                                  |
| -------------------------- | ------------------------------------------------------------ |
| -f,--function              | is a boolean function with ~ (not), & (and),                 |
| -mc,--mappingConfig        | path to the mapping configuration                            |
| -sc,--simulationConfig     | path to the simulation configuration                         |
| -synconf,--synthesisConfig | path to the synthesis configuration                          |
| -t,--truthtable            | is a string of 1's and 0's that define the output for the boolean function<br />a = 11110000<br />b = 11001100<br />c = 10101010<br />t = XXXXXXXX |

# Run Technology Mapping

``` sh
cd ./ARCTICsyn
./gradlew simulationTestbench --args="<argument list>"
```

|-|--|

| argument name          | description                            |
| ---------------------- | -------------------------------------- |
| -i,--inputPath         | path to the input directory or file    |
| -l,--library           | override library from mapping config   |
| -mc,--mappingConfig    | path to the mapping configuration      |
| -n,--numRepetitions    | iteration number for the test bench    |
| -sc,--simulationConfig | path to the simulation configuration   |
| -w,--proxWeights       | weights for the gate proximity measure |

# Settings for Synthesis, Simulation and Technology Mapping

## Synthesis

The synthesis settings are located in the configuration file `./ARCTICsyn/syn.config`.

**OUTPUT_DIR** Output directory for synthesis results relative to `./ARCTICsyn/`.

**SYN_LIMIT_THREAD_NUM** Limit for the number of threads used by the synthesis. When set to 0, the number of processor cores - 1 is used.

**SYNTHESIS_MODE** gets more options in the future: **EXHAUSTIVE**

**SYNTHESIS_DEPTH** Maximum depth of the synthesized circuits.

**SYNTHESIS_WEIGHT** Maximum weight (number of gates) of the synthesized circuits.

**SYNTHESIS_WEIGHT_RELAXATION** Limit for the circuit weight w.r.t. the minimum circuit size. E.g. a weight relaxation of 2 allows circuits to be at most two gates bigger than the smallest circuit found.

**SYNTHESIS_LIMIT_STRUCTURES_NUM** Absolute limit for the generated number of circuits.

**SYNTHESIS_PROCEED_WITH_TM** continues with Technology Mapping and Simulation after Synthesis if set to **TRUE**

## Simulation

The simulation settings are located in the configuration file `./ARCTICsyn/sim.config`.

**PYTHON_BINARY** Path to the Python binary to be used.

**SIM_LIMIT_THREADS_NUM** Limit for the number of threads used by the synthesis. When set to 0, the number of processor cores - 1 is used.

**SIM_PATH** path to the folder of the Simulation (project folder)

**SIM_SCRIPT** path of the entry point for the Simulation (main file)

**SIM_INIT_ARGS** Initialization arguments for the simulator.

**SIM_ARGS** Simulation specific arguments for the simulator.

## Technology Mapping

The technology mapping settings are located in the configuration file `./ARCTICsyn/map.config`.

**LIBRARY** Library of genetic gates to be used.

**COMPAT_LIBRARY** Compatibility library to be used.

**SEARCH_ALGORITHM** Search algorithm to be used. Currently supported: **EXHAUSTIVE, ANNEALING, BRANCH_AND_BOUND**

**OPTIMIZATION_TYPE**: **MAXIMIZE**, **MINIMIZE**

**STATISTICS** If true, statistics are generated and output in JSON format.

**BAB-SEARCH_STRATEGY** *(Branch-and-Bound specific)* Search strategy of B&B. Currently supported: **DEPTH_FIRST_SEARCH, BREADTH_FIRST_SEARCH, CYCLIC_BEST_FIRST_SEARCH, BEST_FIRST_SEARCH**

**BAB-TYPE** *(Branch-and-Bound specific)* Type of B&B.  Currently supported: **EAGER, LAZY**

**BAB-VISUALIZE** *(Branch-and-Bound specific)* If true, the search tree is visualized as DOT file.

**BAB-STATISTICS** *(Branch-and-Bound specific)* If true, B&B specific statistics are generated.

**BAB-FAST** *(Branch-and-Bound specific)* If true, heuristic mode is activated.

# Further Information / Features

In the following, details about the shipped libraries and debugging and test capabilities is briefly explained.

## Genetic Gate Libraries

Possible choices for the argument **LIBRARY** in `./ARCTICsyn/map.config` are located in the folder `./ARCTICsim/thermo_libs`. The gate libraries contain thermodynamic parameters for promoters, transcription factors (TFs) and the host context. With these parameters, circuit simulations can be performed. The core of the set of libraries is the 'ideal' or base library. It contains numerically fitted thermodynamic parameters for the 40 different gates available in Cello's library (https://github.com/CIDARLAB/cello) and its path is `./ARCTICsim/thermo_libs/thermo_lib_id_ideal.json`.

### Library Generation

The different gate libraries are generated from the base library using different hyperparameters governing the distribution of crosstalk. The naming convention is the following. `thermo_lib_id_xtalk_all_dirichlet_<DIRICHLET>tot<TOTAL>.json`

where

- `<DIRICHLET>` is a label of the concentration parameter of the Dirichlet distribution that governs the crosstalk distribution across non-cognate transcription factors in a gate. It is a value in `{0, 1, ..., 6}`. See below for the actual concentration values.
- `<TOTAL>` is a value specifying how strong crosstalking TF's modify the gate's output in relation to the cognate TF. It is a value in `[0, 1]`, where a `1` specifies that if all crosstalking TF's are present in a unit concentration, the gate's output would be modified as if there was instead the cognate TF present in a unit concentration.

The distribution of crosstalk is governed by a Dirichlet distribution. Thus, the distribution has support on all unit-length vectors with as many entries as there are non-cognate TFs. Usually, every entry has an individual concentration parameter assigned. In our case, these are all equal to a global concentration parameter. This specific instance of Dirichlet distribution is also often called a 'symmetric Dirichlet distribution'. The labels `{0, 1, ..., 6}` of this global concentration are mapped to real concentration values by the following table

| label | real concentration (rounded) |
| ----- | ---------------------------- |
| `0`   | 0.004717                     |
| `1`   | 0.114532                     |
| `2`   | 0.378811                     |
| `3`   | 1.                           |
| `4`   | 2.63984                      |
| `5`   | 8.731212                     |
| `6`   | 212.005864                   |

The lowest label `0` assigns most crosstalk to only one non-cognate TF while the highest label `6` gives a mostly uniform distribution of crosstalk across non-cognate TFs.

## Standalone Simulation

The circuit simulation alone can be tested for a given fixed assignment and structure, i.e. outside of a circuit synthesis loop. This is especially useful to verify results and/or obtain more information about a specific simulation, like output histograms etc.

This is demonstrated on the None Equilibrium Simulator in `./ARCTICsim/simulator_nonequilibrium/`

```sh
$ cd ./ARCTICsim/simulator_nonequilibrium/
$ py main.py <argument list>
...
:> start
<score json data>
:> plasmid
<plasmid json data>
:> quit
```

Arguments can be set by arguments or the config file `./ARCTICsim/simulator_nonequilibrium/settings_config.cfg`

| argument name                                            | description                                                  |
| -------------------------------------------------------- | ------------------------------------------------------------ |
| -h, --help                                               | show this help message and exit                              |
| -s STRUCTURE, --structure STRUCTURE                      | the circuit structure. Must be given as a json or path       |
| -a ASSIGNMENT, --assignment ASSIGNMENT                   | the circuit assignment. Must be given as a json or path      |
| -v VERBOSITY, --verbosity VERBOSITY                      | the verbosity level. Default is 0, but higher levels allow easier debugging. Level 1 prints out circuit vals, Level 2 visualizes <br/> output distributions, and Level 3 visualizes gate output of the circuit |
| -l LIBRARY, --library LIBRARY                            | path to thermodynamic lib                                    |
| -f FUNCTIONAL_SCORE, --functional_score FUNCTIONAL_SCORE | identifier of the functional score to use (either use "ws-log-exp" for the e-score or "cello" for the cello score) |
| -e ENERGY_SCORE, --energy_score ENERGY_SCORE             | identifier of the energy score to use (either of "max", "avg", "sum") |
| -w WASSERSTEIN_P, --wasserstein_p WASSERSTEIN_P          | p value of the wasserstein distance                          |
| -m MODE, --mode MODE                                     | The mode of simulation. "det": Deterministic, "samp": sampling based |
| -n N_SAMPLES, --n_samples N_SAMPLES                      | The number of samples to use                                 |
| -q QUICK, --quick QUICK                                  | Whether to use a quick mode for SensorPromoter which is only successful if all input values to the sensor promoter are equal |