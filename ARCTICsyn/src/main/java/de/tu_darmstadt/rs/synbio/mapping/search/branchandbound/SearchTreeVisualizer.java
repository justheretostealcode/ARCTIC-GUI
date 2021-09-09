package de.tu_darmstadt.rs.synbio.mapping.search.branchandbound;

import de.tu_darmstadt.rs.synbio.common.circuit.LogicGate;
import de.tu_darmstadt.rs.synbio.common.library.GateRealization;
import de.tu_darmstadt.rs.synbio.mapping.Assignment;
import de.tu_darmstadt.rs.synbio.mapping.MappingConfiguration;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class SearchTreeVisualizer {
    private final String initialNodeID = "EMPTY_INITIALISATION_NODE";
    private BufferedWriter writer;
    private int expansionIndex;
    private LogicGate[] reversedLogicGates;
    private boolean bVisualize;

    public SearchTreeVisualizer(String structureName, MappingConfiguration mappingConfiguration, LogicGate[] reversedLogicGates, boolean bVisualize) {

        this.reversedLogicGates = reversedLogicGates;
        this.bVisualize = bVisualize;

        if (bVisualize) {
            try {
                File file = new File("visualisation/");
                file.mkdirs();
                file = new File(file.getAbsolutePath(), structureName + "_" + System.currentTimeMillis() + ".dot");
                file.createNewFile();
                writer = new BufferedWriter(new FileWriter(file));


                writer.write("digraph \"" + structureName + "_" + System.currentTimeMillis() + "\" {\n");


                writer.write("ranksep=\"1.2 equally\";\n");
                writer.write(String.format("%s [label=\"root\"];\n", initialNodeID));
            } catch (IOException e) {
                this.bVisualize = false;
                e.printStackTrace();
            }
        }
        expansionIndex = 0;
    }

    public boolean getbVisualize()  {
        return this.bVisualize;
    }

    public void addLeafNode(Assignment assignment, double val, double currentBound) {
        if (!bVisualize)
            return;

        QueueItem item = QueueItem.getQueueItem(assignment, val);
        add(item, currentBound);
    }

    public void addIntermediateNode(QueueItem item, double currentBound) {
        if (!bVisualize)
            return;

        add(item, currentBound);
    }

    public void add(QueueItem item, double currentBound) {
        if (!bVisualize)
            return;

        Assignment assignment = item.assignment;
        double value = item.val;
        int size = assignment.size();
        if (size == 0)
            return;

//        LogicGate gate = reversedLogicGates[size - 1];
//        GateRealization realization = assignment.get(gate);
//        String targetIdentifier = getNodeIdentifier(gate, realization);
//
//        String sourceIdentifier;
//        if (size > 2) {
//            LogicGate sourceGate = reversedLogicGates[size - 2];
//            GateRealization sourceRealization = assignment.get(sourceGate);
//            sourceIdentifier = getNodeIdentifier(sourceGate, sourceRealization);
//            targetIdentifier = sourceIdentifier + "-" + targetIdentifier;
//            LogicGate prevGate = reversedLogicGates[size - 3];
//            sourceIdentifier = getNodeIdentifier(prevGate, assignment.get(prevGate)) + sourceIdentifier;
//
//        }
//        else if (size == 2) {
//
//        }
//        else {
//            targetIdentifier = initialNodeID + "-" + targetIdentifier;
//            sourceIdentifier = initialNodeID;
//        }
        LogicGate gate = reversedLogicGates[size - 1];
        GateRealization realization = assignment.get(gate);
        String sourceIdentifier = "";
        String targetIdentifier = initialNodeID;
        for (int iX = 0; iX < assignment.size(); iX++) {
            LogicGate g = reversedLogicGates[iX];
            sourceIdentifier = targetIdentifier;
            targetIdentifier += "__" + getNodeIdentifier(g, assignment.get(g));
        }

        String targetLabel = String.format("%s (%d)\n[%f | %f]", realization.getIdentifier(), expansionIndex, value, currentBound);
        try {
            writer.write(String.format("%s [label=\"%s\", shape=rect];\n", targetIdentifier, targetLabel));
        } catch (IOException e) {
            e.printStackTrace();
        }
        try {
            writer.write(String.format("%s -> %s;\n", sourceIdentifier, targetIdentifier));
        } catch (IOException e) {
            e.printStackTrace();
        }

        expansionIndex++;
    }

    private String getNodeIdentifier(LogicGate gate, GateRealization realization) {
        String identifier = gate.getIdentifier() + "_" + gate.getLogicType().toString() + "_" + realization.getIdentifier() + "_" + realization.getGroup();
        return identifier;
    }

    public void finish() {
        if (!bVisualize)
            return;

        try {
            writer.write("}");
            writer.flush();
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
