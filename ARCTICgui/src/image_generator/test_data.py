
structure = '''
{
  "truthtable": "01110101",
  "gate_truthtables": {
    "NOR2_3": "00110000",
    "NOT_4": "00001111",
    "b": "11001100",
    "NOR2_1": "10001010",
    "NOT_2": "01010101",
    "c": "10101010",
    "a": "11110000",
    "O": "01110101",
    "NOT_0": "01110101"
  },
  "graph": {
    "creator": "JGraphT JSON Exporter",
    "version": "1",
    "nodes": [
      {
        "id": "O",
        "type": "OUTPUT_BUFFER"
      },
      {
        "id": "NOT_0",
        "type": "NOT"
      },
      {
        "id": "NOR2_1",
        "type": "NOR2"
      },
      {
        "id": "NOT_2",
        "type": "NOT"
      },
      {
        "id": "c",
        "type": "INPUT"
      },
      {
        "id": "NOR2_3",
        "type": "NOR2"
      },
      {
        "id": "NOT_4",
        "type": "NOT"
      },
      {
        "id": "a",
        "type": "INPUT"
      },
      {
        "id": "b",
        "type": "INPUT"
      }
    ],
    "edges": [
      {
        "id": "1",
        "source": "c",
        "target": "NOT_2",
        "variable": "x"
      },
      {
        "id": "2",
        "source": "NOT_2",
        "target": "NOR2_1",
        "variable": "x"
      },
      {
        "id": "3",
        "source": "a",
        "target": "NOT_4",
        "variable": "x"
      },
      {
        "id": "4",
        "source": "NOT_4",
        "target": "NOR2_3",
        "variable": "y"
      },
      {
        "id": "5",
        "source": "b",
        "target": "NOR2_3",
        "variable": "x"
      },
      {
        "id": "6",
        "source": "NOR2_3",
        "target": "NOR2_1",
        "variable": "y"
      },
      {
        "id": "7",
        "source": "NOR2_1",
        "target": "NOT_0",
        "variable": "x"
      },
      {
        "id": "8",
        "source": "NOT_0",
        "target": "O",
        "variable": "x"
      }
    ]
  }
}
'''
assignment = '''
{
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
'''
plasmid = '''
[
    [
        "Gene 0 (P b -> CDS NOR2_6): P=sensor_promoter_Pxyl UTR=utr_Kozak34 CDS=protein_HKCI T=None",
        "Gene 2 (P a -> CDS OUTPUT_OR2_9): P=sensor_promoter_Ptet UTR=utr_Kozak6 CDS=protein_YFP T=None",
        "Gene 4 (P c -> CDS NOR2_7): P=sensor_promoter_Plac UTR=utr_Kozak7 CDS=protein_QacR T=None",
        "Gene 6 (P NOR2_6 -> CDS NOR2_7): P=promoter_pHKCI1 UTR=utr_Kozak7 CDS=protein_QacR T=None",
        "Gene 8 (P NOR2_7 -> CDS NOR2_8): P=promoter_pQacR1 UTR=utr_Kozak24 CDS=protein_LexA T=None",
        null,
        null,
        null
    ],
    [
        "Gene 1 (P NOT_1 -> CDS NOR2_8): P=promoter_pBm3RI1 UTR=utr_Kozak24 CDS=protein_LexA T=None",
        "Gene 3 (P NOT_1 -> CDS NOR2_6): P=promoter_pBm3RI1 UTR=utr_Kozak34 CDS=protein_HKCI T=None",
        "Gene 5 (P b -> CDS NOT_1): P=sensor_promoter_Pxyl UTR=utr_Kozak4 CDS=protein_BM3RI T=None",
        "Gene 7 (P NOR2_8 -> CDS OUTPUT_OR2_9): P=promoter_pLexA1 UTR=utr_Kozak6 CDS=protein_YFP T=None",
        null,
        null,
        null,
        null
    ]
]
'''
score = '''
{
    "functional_score": {
        "OUTPUT_OR2_9": 374.3338269136759
    },
    "energy_score": 60534.90038044803,
    "detailed_energy_score": {
        "e_p": 0.010326680727633805, 
        "e_tx": 725.6222845537709, 
        "e_tl": 59809.267769213526
    }
}
'''