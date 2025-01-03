package de.tu_darmstadt.rs.synbio.common.library;

import de.tu_darmstadt.rs.synbio.common.LogicType;

import java.util.List;

public class GateRealization {

    private final String identifier;
    private final LogicType logicType;
    private final String group;

    private boolean isCharacterized = false;
    private GateCharacterization characterization;

    /* constructor for un-characterized realizations */

    public GateRealization(String identifier, LogicType type, String group) {
        this.identifier = identifier;
        this.logicType = type;
        this.group = group;
    }

    /* constructor for characterized realizations */

    public GateRealization(String identifier, LogicType type, String group, GateCharacterization characterization) {
        this(identifier, type, group);
        this.characterization = characterization;
        this.isCharacterized = true;
    }

    public String getIdentifier() {
        return identifier;
    }

    public LogicType getLogicType() {
        return logicType;
    }

    public String getGroup() {
        return group;
    }

    public GateCharacterization getCharacterization() {
        return characterization;
    }

    public boolean isCharacterized() {
        return isCharacterized;
    }

    @Override
    public String toString() { return identifier; }

    public static class GateCharacterization {

        /* library values */
        private final double ymax;
        private final double ymin;
        private final double k;
        private final double n;

        private final double iLower;
        private final double iUpper;

        private final double jLower;
        private final double jUpper;

        private final Particles particles;

        /* derived values */
        private final double xm;
        private final double ym;
        private final double grad;

        public GateCharacterization(double ymax, double ymin, double iLower, double iUpper, double jLower, double jUpper, double k, double n, Particles particles) {

            this.ymax = ymax;
            this.ymin = ymin;

            this.iLower = iLower;
            this.iUpper = iUpper;

            this.jLower = jLower;
            this.jUpper = jUpper;

            this.k = k;
            this.n = n;

            this.particles = particles;

            this.ym = ((ymax - ymin) / 2 ) + ymin;
            this.xm = Math.pow(((ymax-ymin)/(ym-ymin) - 1), 1/n) * k;
            this.grad = ((ymin - ymax) * n * Math.pow(xm / k, n)) / (xm * Math.pow(1 + Math.pow(xm / k, n), 2));
        }

        /* getters for library values */

        public double getYmax() {
            return ymax;
        }

        public double getYmin() {
            return ymin;
        }

        public double getILower() { return iLower; }

        public double getIUpper() { return iUpper; }

        public double getJLower() { return jLower; }

        public double getJUpper() { return jUpper; }

        public double getK() {
            return k;
        }

        public double getN() {
            return n;
        }

        public Particles getParticles() {
            return particles;
        }

        /* getters for derived values */

        public double getXm() {
            return xm;
        }

        public double getYm() {
            return ym;
        }

        public double getGrad() {
            return grad;
        }

        public double getEuclidean(GateRealization.GateCharacterization cmp, Double[] normalization, Double[] proxWeights) {
            return Math.sqrt(proxWeights[0] * Math.pow((this.xm - cmp.getXm()) / normalization[0], 2) + proxWeights[1] * Math.pow((this.ym - cmp.getYm()) / normalization[1], 2) + proxWeights[2] * Math.pow((this.grad - cmp.getGrad()) / normalization[2], 2));
        }

        public double getMaxCelloScore()    {
            return ymax / ymin;
        }
    }

    public static class Particles {

        final List<Double> ymax;
        final List<Double> ymin;
        final int num;

        public Particles(List<Double> ymax, List<Double> ymin) {
            this.ymax = ymax;
            this.ymin = ymin;
            this.num = ymax.size();
        }

        public int getNum() {
            return num;
        }

        public Double getYmax(int n) {
            return ymax.get(n);
        }

        public Double getYmin(int n) {
            return ymin.get(n);
        }
    }

}
