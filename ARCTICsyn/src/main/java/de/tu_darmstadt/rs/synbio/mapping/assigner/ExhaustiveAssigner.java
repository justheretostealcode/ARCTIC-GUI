package de.tu_darmstadt.rs.synbio.mapping.assigner;

import de.tu_darmstadt.rs.synbio.common.*;
import de.tu_darmstadt.rs.synbio.common.circuit.Circuit;
import de.tu_darmstadt.rs.synbio.common.circuit.Gate;
import de.tu_darmstadt.rs.synbio.common.library.GateLibrary;
import de.tu_darmstadt.rs.synbio.common.library.GateRealization;
import de.tu_darmstadt.rs.synbio.mapping.Assignment;
import de.tu_darmstadt.rs.synbio.mapping.util.PermutationIterator;
import org.apache.commons.math3.util.CombinatoricsUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.stream.Collectors;

public class ExhaustiveAssigner implements Assigner {

    private static final Logger logger = LoggerFactory.getLogger(ExhaustiveAssigner.class);

    // gates
    private final Map<LogicType, List<GateRealization>> availableGates;
    private final LinkedHashMap<LogicType, List<Gate>> circuitGates; // linked for iteration order
    private final Gate outputGate;
    private final GateRealization outputRealization;

    // permutation variables
    private final HashMap<LogicType, PermutationIterator<GateRealization>> permutationIterators;
    private final HashMap<LogicType, Long> numPermutations;
    private final long numTotalPermutations;
    private long currentPermutation = 0;

    // assignment buffer
    private final HashMap<LogicType, List<GateRealization>> assignedRealizations;

    public ExhaustiveAssigner(GateLibrary gateLib, Circuit circuit) {

        Thread.currentThread().setPriority(Thread.NORM_PRIORITY + 1);

        // initialize gate library
        this.availableGates = new HashMap<>(gateLib.getRealizations());
        availableGates.remove(LogicType.OUTPUT);

        // initialize circuit gate map
        this.circuitGates = new LinkedHashMap<>();
        this.numPermutations = new HashMap<>();
        for (LogicType type : availableGates.keySet()) {
            ArrayList<Gate> gates = circuit.vertexSet().stream().filter(g -> g.getLogicType() == type).collect(Collectors.toCollection(ArrayList::new));
            circuitGates.put(type, gates);
            numPermutations.put(type, getNumAssignments(type));
        }

        outputGate = circuit.getOutputBuffer();
        outputRealization = gateLib.getOutputDevice();

        // initialize permutation iterators
        this.permutationIterators = new HashMap<>();
        for (LogicType type : availableGates.keySet()) {
            permutationIterators.put(type, new PermutationIterator<>(availableGates.get(type), circuitGates.get(type).size()));
        }

        this.numTotalPermutations = getNumAssignments();

        this.assignedRealizations = new HashMap<>();
    }

    public long getNumTotalPermutations() {
        return numTotalPermutations;
    }

    private long getNumAssignments() {

        long totalVariations = 1;

        for (LogicType type : availableGates.keySet()) {
            totalVariations *= getNumAssignments(type);
        }

        return totalVariations;
    }

    private long getNumAssignments(LogicType type) {

        int n = availableGates.get(type).size();
        int k = circuitGates.get(type).size();
        return CombinatoricsUtils.factorial(n) / CombinatoricsUtils.factorial(n - k);
    }

    private boolean nextAssignment() {

        // generate assignments until there are more and a valid one is found

        do {
            long divider = 1;

            // for every gate type, calculate if the iterator needs to be updated
            for (LogicType type : circuitGates.keySet()) {

                if (!circuitGates.get(type).isEmpty() && currentPermutation % divider == 0) {
                    assignedRealizations.put(type, permutationIterators.get(type).next());
                }

                divider *= numPermutations.get(type);
            }

            currentPermutation++;

        } while (!groupConstraintsFulfilled() && (currentPermutation != numTotalPermutations));

        return (currentPermutation < numTotalPermutations);
    }

    private boolean groupConstraintsFulfilled() {

        List<String> usedGroups = new ArrayList<>();

        for (List<GateRealization> realizationsOfType : assignedRealizations.values()) {
            for (GateRealization realization : realizationsOfType) {
                if (usedGroups.contains(realization.getGroup())) {
                    return false;
                } else {
                    usedGroups.add(realization.getGroup());
                }
            }
        }

        return true;
    }

    /*
     * Generates the next assignment map. Returns null if there is no new assignment.
     */

    public synchronized Assignment getNextAssignment() {

        if (!nextAssignment())
            return null;

        Assignment assignment = new Assignment(outputGate, outputRealization);

        for (LogicType type : circuitGates.keySet()) {

            List<Gate> originalGates = circuitGates.get(type);
            List<GateRealization> replacements = assignedRealizations.get(type);

            for (int i = 0; i < originalGates.size(); i++) {
                assignment.put(originalGates.get(i), replacements.get(i));
            }
        }

        return assignment;
    }
}
