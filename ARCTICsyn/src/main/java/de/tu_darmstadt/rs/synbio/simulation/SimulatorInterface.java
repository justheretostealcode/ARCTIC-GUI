package de.tu_darmstadt.rs.synbio.simulation;

import com.fasterxml.jackson.databind.ObjectMapper;
import de.tu_darmstadt.rs.synbio.common.LogicType;
import de.tu_darmstadt.rs.synbio.common.circuit.Gate;
import de.tu_darmstadt.rs.synbio.common.library.GateLibrary;
import de.tu_darmstadt.rs.synbio.mapping.Assignment;
import de.tu_darmstadt.rs.synbio.common.circuit.Circuit;
import de.tu_darmstadt.rs.synbio.mapping.util.BranchAndBoundUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.util.*;
import java.util.stream.Collectors;

public class SimulatorInterface {

    private static final Logger logger = LoggerFactory.getLogger(SimulatorInterface.class);

    private static final String scorePrefix = "score: ";

    private final String pythonBinary;
    private final File simulatorPath;
    private final String simScript;
    private final String simInitArgs;
    private final String simArgs;
    private final GateLibrary library;

    private Process simProcess;
    private File structureFile;
    private BufferedReader reader;
    private BufferedWriter writer;
    private BufferedReader errorReader;
    private final ObjectMapper mapper = new ObjectMapper();
    private AssignmentCompiler compiler;

    public enum PropagationMode {
        EXACT,
        BOUNDING,
        HEURISTIC
    }

    public SimulatorInterface(SimulationConfiguration config, GateLibrary gateLibrary) {
        pythonBinary = config.getPythonBinary();
        simulatorPath = config.getSimPath();
        simScript = config.getSimScript();
        simInitArgs = config.getSimInitArgs();
        simArgs = config.getSimArgs();
        library = gateLibrary;
    }

    public boolean initSimulation(Circuit circuit) { //TODO: handle return value

        if (simProcess!= null && simProcess.isAlive())
            simProcess.destroy();

        this.compiler = new AssignmentCompiler(circuit, library);

        try {
            String structureFileName = "structure_" + circuit.getIdentifier() + "_tid" + Thread.currentThread().getId() + "_" + System.nanoTime() + ".json";
            structureFile = new File(simulatorPath, structureFileName);
            circuit.save(structureFile);
            //circuit.print(new File("test.dot"));

            List<String> arguments = new ArrayList<>();
            arguments.addAll(Arrays.asList(pythonBinary, simScript, "-s=" + structureFileName, "-l=" + library.getSourceFile().getAbsolutePath()));
            arguments.addAll(Arrays.asList(simInitArgs.split(" ")));

            ProcessBuilder pb = new ProcessBuilder(arguments.toArray(new String[0]));
            pb.directory(simulatorPath);

            simProcess = pb.start();

            reader = new BufferedReader(new InputStreamReader(simProcess.getInputStream()));
            writer = new BufferedWriter(new OutputStreamWriter(simProcess.getOutputStream()));
            errorReader = new BufferedReader(new InputStreamReader(simProcess.getErrorStream()));

            String output;
            do {
                output = reader.readLine();

                if (!simProcess.isAlive()) {
                    logger.error("Simulator exited on initialization:\n" + getError());
                    shutdown();
                    return false;
                }

            } while (output == null || !output.startsWith("ready"));

            return true;

        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public Double simulate(Assignment assignment, PropagationMode mode) { //TODO: handle null return value

        String additionalArgs = "--propagation_mode=" + mode.ordinal();

        Map<String, Map<?, ?>> assignmentMap = compiler.compile(assignment);

        /*try {
            mapper.writerWithDefaultPrettyPrinter().writeValue(new File("assignment_00000110.json"), assignmentMap);
        } catch (Exception e) {
        }*/

        double score = 0.0;

        try {

            if (!simProcess.isAlive()) {
                logger.error("Simulator exited before simulation start:\n" + getError());
                shutdown();
                return null;
            }

            String assignmentStr = mapper.writeValueAsString(assignmentMap);

            writer.write("update_settings " + simArgs + additionalArgs + " --assignment=" + assignmentStr);
            writer.newLine();
            writer.flush();
            writer.write("start");
            writer.newLine();
            writer.flush();

            String output;
            do {
                output = reader.readLine();

                if (!simProcess.isAlive()) {
                    logger.error("Simulator exited during simulation: " + getError());
                    shutdown();
                    return null;
                }

            } while (output == null || !output.startsWith(scorePrefix));

            output = output.substring(scorePrefix.length());

            // relevant to correctly parse infinity as returned score
            try {
                score = output.equals("inf") ? Double.POSITIVE_INFINITY : Double.parseDouble(output);
            } catch (Exception e) {
                logger.error(e.getMessage());
            }

        } catch (Exception e) {
            e.printStackTrace();
            shutdown();
        }

        return score;
    }

    Double growth;

    public Double getLastGrowth() {
        return growth;
    }

    public void shutdown() {
        structureFile.delete();
        simProcess.destroy();
    }

    private String getError() throws IOException {
        String line;
        StringBuilder error = new StringBuilder();
        while (errorReader.ready() && (line = errorReader.readLine()) != null) {
            error.append(line).append("\n");
        }
        return error.toString();
    }
}
