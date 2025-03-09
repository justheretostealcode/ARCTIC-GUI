"""
Data storage module for plasmid visualization.
Contains test data and constants used by the visualization code.
"""

# Colors for each element in the top and bottom rows
ELEMENT_COLORS_BY_ROW = {
    0: [  # top row
        (1.0, 0.7, 0.7),  # pink
        (0.0, 0.0, 1.0),  # blue
        (1.0, 0.5, 0.0),  # orange
        (1.0, 0.5, 0.0),  # orange
        (0.0, 1.0, 0.0)   # green
    ],
    1: [  # bottom row
        (0.0, 1.0, 0.0),  # green
        (1.0, 0.7, 0.7),  # pink
        (1.0, 0.0, 0.0),  # red
        (0.0, 0.0, 1.0)   # blue
    ]
}

# Graph structure
GRAPH_DATA = {
    "nodes": [
        {"id": "O", "type": "OUTPUT_BUFFER"},
        {"id": "NOT_0", "type": "NOT"},
        {"id": "NOR2_1", "type": "NOR2"},
        {"id": "NOT_2", "type": "NOT"},
        {"id": "c", "type": "INPUT"},
        {"id": "NOR2_3", "type": "NOR2"},
        {"id": "NOT_4", "type": "NOT"},
        {"id": "a", "type": "INPUT"},
        {"id": "b", "type": "INPUT"}
    ],
    "edges": [
        {"id": "1", "source": "c", "target": "NOT_2", "variable": "x"},
        {"id": "2", "source": "NOT_2", "target": "NOR2_1", "variable": "x"},
        {"id": "3", "source": "a", "target": "NOT_4", "variable": "x"},
        {"id": "4", "source": "NOT_4", "target": "NOR2_3", "variable": "y"},
        {"id": "5", "source": "b", "target": "NOR2_3", "variable": "x"},
        {"id": "6", "source": "NOR2_3", "target": "NOR2_1", "variable": "y"},
        {"id": "7", "source": "NOR2_1", "target": "NOT_0", "variable": "x"},
        {"id": "8", "source": "NOT_0", "target": "O", "variable": "x"}
    ]
}



assignment = {
  "a": "input_3",
  "b": "input_1",
  "c": "input_2",
  "NOT_0": "P1_PsrA",
  "NOT_2": "P1_IcaR",
  "NOT_4": "P1_PhlF",
  "NOR2_1": "P1_QacR",
  "NOR2_3": "P1_HKCI",
  "O": "output_1"
}

# Test data for plasmid visualization
TEST_PLASMID_DATA = [
    [
        "Gene 0 (P b -> CDS NOR2_6): P=sensor_promoter_Pxyl UTR=utr_Kozak34 CDS=protein_HKCI T=None",
        "Gene 2 (P a -> CDS OUTPUT_OR2_9): P=sensor_promoter_Ptet UTR=utr_Kozak6 CDS=protein_YFP T=None",
        "Gene 4 (P c -> CDS NOR2_7): P=sensor_promoter_Plac UTR=utr_Kozak7 CDS=protein_QacR T=None",
        "Gene 6 (P NOR2_6 -> CDS NOR2_7): P=promoter_pHKCI1 UTR=utr_Kozak7 CDS=protein_QacR T=None",
        "Gene 8 (P NOR2_7 -> CDS NOR2_8): P=promoter_pQacR1 UTR=utr_Kozak24 CDS=protein_LexA T=None"
    ],
    [
        "Gene 1 (P NOT_1 -> CDS NOR2_8): P=promoter_pBm3RI1 UTR=utr_Kozak24 CDS=protein_LexA T=None",
        "Gene 3 (P NOT_1 -> CDS NOR2_6): P=promoter_pBm3RI1 UTR=utr_Kozak34 CDS=protein_HKCI T=None",
        "Gene 5 (P b -> CDS NOT_1): P=sensor_promoter_Pxyl UTR=utr_Kozak4 CDS=protein_BM3RI T=None",
        "Gene 7 (P NOR2_8 -> CDS OUTPUT_OR2_9): P=promoter_pLexA1 UTR=utr_Kozak6 CDS=protein_YFP T=None"
    ]
]
