package de.tu_darmstadt.rs.synbio.mapping;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.PropertyAccessor;
import com.fasterxml.jackson.databind.ObjectMapper;
import de.tu_darmstadt.rs.synbio.common.circuit.Circuit;
import de.tu_darmstadt.rs.synbio.common.library.GateLibrary;
import de.tu_darmstadt.rs.synbio.mapping.search.*;
import de.tu_darmstadt.rs.synbio.simulation.SimulationConfiguration;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringWriter;
import java.util.Arrays;
import java.util.Properties;

public class MappingConfiguration {

    private static final Logger logger = LoggerFactory.getLogger(MappingConfiguration.class);

    private final MappingConfiguration.SearchAlgorithm searchAlgorithm;
    private final MappingConfiguration.OptimizationType optimizationType;
    private boolean statistics;

    private MappingConfiguration.BAB_SearchStrategy babSearchStrategy;
    private MappingConfiguration.BAB_Type babType;
    private boolean babStatistics;
    private boolean babVisualization;
    private boolean babFast;
    private BAB_Sort_Order babLibraryOrder;
    private BAB_Sort_Order babChildrenOrder;
    private BAB_INPUT_SPECIFICATION_TYPE babInputSpecificationType;

    private int numRepetitions;

    public enum SearchAlgorithm {
        EXHAUSTIVE, ANNEALING, BRANCH_AND_BOUND
    }

    public enum OptimizationType {
        MAXIMIZE {
            @Override
            public boolean compare(double current, double candidate) {
                return candidate > current;
            }
        },

        MINIMIZE {
            @Override
            public boolean compare(double current, double candidate) {
                return candidate < current;
            }
        };

        public abstract boolean compare(double current, double candidate);
    }

    public enum BAB_SearchStrategy {
        DEPTH_FIRST_SEARCH, BREADTH_FIRST_SEARCH, BEST_FIRST_SEARCH, CYCLIC_BEST_FIRST_SEARCH
    }

    public enum BAB_Type {
        EAGER, LAZY
    }

    public enum BAB_Sort_Order {
        UNSORTED, SORTED, SHUFFLED, REVERSED
    }

    /**
     * INFTY: + infinity and - infinity are assigned as input concentrations
     * EQUAL: All input buffers receive the same low and high concentration
     * PRECISE: Each input buffer gets a dedicated input specification
     */
    public enum BAB_INPUT_SPECIFICATION_TYPE {
        INPRECISE, EQUAL, PRECISE
    }

    public MappingConfiguration(String configFile) throws Exception {

        /* config file handling */

        Properties props = new Properties();
        InputStream is = null;
        is = new FileInputStream(configFile);
        props.load(is);

        switch (props.getProperty("SEARCH_ALGORITHM")) {
            case "EXHAUSTIVE":
                searchAlgorithm = SearchAlgorithm.EXHAUSTIVE;
                break;
            case "ANNEALING":
                searchAlgorithm = SearchAlgorithm.ANNEALING;
                break;
            case "BRANCH_AND_BOUND":
                searchAlgorithm = SearchAlgorithm.BRANCH_AND_BOUND;
                break;
            default:
                throw new IOException("Unknown search algorithm! (Available algorithms: " + Arrays.toString(SearchAlgorithm.values()) + ")");
        }

        switch (props.getProperty("OPTIMIZATION_TYPE")) {
            case "MAXIMIZE":
                optimizationType = OptimizationType.MAXIMIZE;
                break;
            case "MINIMIZE":
                optimizationType = OptimizationType.MINIMIZE;
                break;
            default:
                throw new IOException("Unknown optimization type! (Available types: " + Arrays.toString(OptimizationType.values()) + ")");
        }

        statistics = props.getProperty("STATISTICS", "false").equalsIgnoreCase("true");

        numRepetitions = Integer.valueOf(props.getProperty("REPETITIONS", "-1"));



        if (SearchAlgorithm.BRANCH_AND_BOUND == searchAlgorithm) {   // The following fields are only necessary for BranchAndBound
            switch (props.getProperty("BAB-TYPE")) {
                case "EAGER":
                    babType = BAB_Type.EAGER;
                    break;
                case "LAZY":
                    babType = BAB_Type.LAZY;
                    break;
                default:
                    babType = BAB_Type.EAGER;
            }

            switch (props.getProperty("BAB-SEARCH_STRATEGY")) {
                case "DEPTH_FIRST_SEARCH":
                    babSearchStrategy = BAB_SearchStrategy.DEPTH_FIRST_SEARCH;
                    break;
                case "BREADTH_FIRST_SEARCH":
                    babSearchStrategy = BAB_SearchStrategy.BREADTH_FIRST_SEARCH;
                    break;
                case "CYCLIC_BEST_FIRST_SEARCH":
                    babSearchStrategy = BAB_SearchStrategy.CYCLIC_BEST_FIRST_SEARCH;
                    break;
                case "BEST_FIRST_SEARCH":
                    babSearchStrategy = BAB_SearchStrategy.BEST_FIRST_SEARCH;
                    break;
                default:
                    babSearchStrategy = BAB_SearchStrategy.BEST_FIRST_SEARCH;
            }

            babStatistics = props.getProperty("BAB-STATISTICS", "false").equalsIgnoreCase("true");

            babVisualization = props.getProperty("BAB-VISUALIZE", "false").equalsIgnoreCase("true");
            babFast = props.getProperty("BAB-FAST", "true").equalsIgnoreCase("true");

            switch (props.getProperty("BAB-LIBRARY_ORDER", "SORTED")) {
                case "UNSORTED":
                    babLibraryOrder = BAB_Sort_Order.UNSORTED;
                    break;
                case "SORTED":
                    babLibraryOrder = BAB_Sort_Order.SORTED;
                    break;
                case "SHUFFLED":
                    babLibraryOrder = BAB_Sort_Order.SHUFFLED;
                    break;
                case "REVERSED":
                    babLibraryOrder = BAB_Sort_Order.REVERSED;
                    break;
                default:
                    babLibraryOrder = BAB_Sort_Order.SORTED;
                    break;
            }

            switch (props.getProperty("BAB-CHILDREN_ORDER", "SORTED")) {
                case "UNSORTED":
                    babChildrenOrder = BAB_Sort_Order.UNSORTED;
                    break;
                case "SORTED":
                    babChildrenOrder = BAB_Sort_Order.SORTED;
                    break;
                case "SHUFFLED":
                    babChildrenOrder = BAB_Sort_Order.SHUFFLED;
                    break;
                case "REVERSED":
                    babChildrenOrder = BAB_Sort_Order.REVERSED;
                    break;
                default:
                    babChildrenOrder = BAB_Sort_Order.SORTED;
                    break;
            }

            switch (props.getProperty("BAB-INPUT_SPECIFICATION_TYPE", "PRECISE")) {
                case "INPRECISE":
                    babInputSpecificationType = BAB_INPUT_SPECIFICATION_TYPE.INPRECISE;
                    break;
                case "EQUAL":
                    babInputSpecificationType = BAB_INPUT_SPECIFICATION_TYPE.EQUAL;
                    break;
                case "PRECISE":
                    babInputSpecificationType = BAB_INPUT_SPECIFICATION_TYPE.PRECISE;
                    break;
                default:
                    babInputSpecificationType = BAB_INPUT_SPECIFICATION_TYPE.PRECISE;
                    break;
            }


        }
    }

    public void print() {
        logger.info("\tsearch algorithm: " + searchAlgorithm.name());
        logger.info("\toptimization type: " + optimizationType.name());
    }

    public OptimizationType getOptimizationType() {
        return optimizationType;
    }

    public boolean getStatistics() {
        return statistics;
    }

    public BAB_Type getBabType() {
        return babType;
    }

    public BAB_SearchStrategy getBabSearchStrategy() {
        return babSearchStrategy;
    }

    public boolean getBabStatistics() {
        return babStatistics;
    }

    public boolean getBabVisualization() {
        return babVisualization;
    }

    public boolean getBabFast() {
        return babFast;
    }

    public BAB_Sort_Order getBabLibraryOrder() {
        return babLibraryOrder;
    }

    public BAB_Sort_Order getBabChildrenOrder() {
        return babChildrenOrder;
    }

    public BAB_INPUT_SPECIFICATION_TYPE getBabInputSpecificationType() {
        return babInputSpecificationType;
    }

    public int getNumRepetitions()  {
        return numRepetitions;
    }

    /* factories */

    public AssignmentSearchAlgorithm getSearchAlgorithm(Circuit structure, GateLibrary lib, SimulationConfiguration simConfig) {

        switch (searchAlgorithm) {
            case ANNEALING:
                return new SimulatedAnnealingSearch(structure, lib, this, simConfig);
            case BRANCH_AND_BOUND:
                return new BranchAndBoundSearch(structure, lib, this, simConfig);
            default:
                return new ExhaustiveSearch(structure, lib, this, simConfig);
        }
    }

    public String toJSON() {
        ObjectMapper mapper = new ObjectMapper();
        mapper.setVisibility(PropertyAccessor.FIELD, JsonAutoDetect.Visibility.ANY);

        StringWriter writer = new StringWriter();
        try {
            mapper.writerWithDefaultPrettyPrinter().writeValue(writer, this);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return writer.toString();
    }


    @Override
    public String toString() {
        return toJSON();
    }
}