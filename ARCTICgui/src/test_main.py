import unittest

from pipcontrol import boolean_function
from gui.design_goal import LogicCircuitSynth
from gui.design_view import CombinedDesignView
from image_generator import logic_circuit

class Test(unittest.TestCase):

    def test_generate_truth_table_from_expr(self) -> None:
        """Test the correct truth table generation"""
        #Test and operator
        result = boolean_function.generate_truth_table_from_expr("a&b")
        a_and_b = [['a', 'b', 'a&b'], [0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
        self.assertEqual(result, a_and_b)

        #Test or operator
        result = boolean_function.generate_truth_table_from_expr("a|b")
        a_or_b = [['a', 'b', 'a|b'], [0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        self.assertEqual(result, a_or_b)

        #Test not operator
        result = boolean_function.generate_truth_table_from_expr("~c")
        not_a = [['c', "~c"], [0, 1], [1, 0]]
        self.assertEqual(result, not_a)

        #Test XOR
        result = boolean_function.generate_truth_table_from_expr("c^a")
        c_xor_a = [['c', 'a', 'c^a'], [0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
        self.assertEqual(result, c_xor_a)

        #Test broken Inputs
        self.assertRaises(Exception, boolean_function.generate_truth_table_from_expr, "a b")
        self.assertRaises(Exception, boolean_function.generate_truth_table_from_expr, "a,b")

    def test_LogicCircuitSynth_can_start(self) -> None:
        test_obj = LogicCircuitSynth()
    
    def test_CombinedDesignView(self) -> None:
        test_obj = CombinedDesignView()
    
    def test_getNoNodes(self) -> None:
        self.assertEqual(logic_circuit.getNodes({
            'nodes':[],
            'edges':[],
        }),{})
        self.assertEqual(logic_circuit.getNodes({
            'nodes':[{'id':'a', 'type':'INPUT'}, {'id':'nor1', 'type':'NOR2'}, {'id':'out', 'type':'OUTPUT'}],
            'edges':[{'source':'a', 'target':'nor1'}, {'source':'a', 'target':'nor1'}, {'source':'nor1', 'target':'out'}],
        }),{
            'a':{'type':'INPUT', 'sources':[], 'targets':['nor1', 'nor1']},
            'nor1':{'type':'NOR2', 'sources':['a', 'a'], 'targets':['out']},
            'out':{'type':'OUTPUT', 'sources':['nor1'], 'targets':[]},
        })
        self.assertEqual(logic_circuit.getNodes({
            'nodes':[{'id':'a', 'type':'INPUT'}, {'id':'not1', 'type':'NOT'}, {'id':'nor1', 'type':'NOR2'}, {'id':'out', 'type':'OUTPUT'}],
            'edges':[{'source':'a', 'target':'not1'}, {'source':'not1', 'target':'nor1'}, {'source':'a', 'target':'nor1'}, {'source':'nor1', 'target':'out'}],
        }),{
            'a':{'type':'INPUT', 'sources':[], 'targets':['not1', 'nor1']},
            'not1':{'type':'NOT', 'sources':['a'], 'targets':['nor1']},
            'nor1':{'type':'NOR2', 'sources':['not1', 'a'], 'targets':['out']},
            'out':{'type':'OUTPUT', 'sources':['nor1'], 'targets':[]},
        })
        self.assertEqual(logic_circuit.getNodes({
            'nodes':[{'id':'a', 'type':'INPUT'}, {'id':'nor1', 'type':'NOR2'}, {'id':'out', 'type':'OUTPUT_OR2'}],
            'edges':[{'source':'a', 'target':'nor1'}, {'source':'a', 'target':'nor1'}, {'source':'nor1', 'target':'out'}, {'source':'nor1', 'target':'out'}],
        }),{
            'a': {'type': 'INPUT', 'sources': [], 'targets': ['nor1', 'nor1']},
            'nor1': {'type': 'NOR2', 'sources': ['a', 'a'], 'targets': ['OR2', 'OR2']},
            'OR2': {'type': 'OR2', 'sources': ['nor1', 'nor1'], 'targets': ['out']},
            'out': {'type': 'OUTPUT_BUFFER', 'sources': ['OR2'], 'targets': []}
        })
    def test_getRankNodes(self)->None:
        self.assertEqual(logic_circuit.getRankNodes({}), [])
        self.assertEqual(logic_circuit.getRankNodes({
            'a':{'type':'INPUT', 'sources':[], 'targets':['nor1', 'nor1']},
            'nor1':{'type':'NOR2', 'sources':['a', 'a'], 'targets':['out']},
            'out':{'type':'OUTPUT', 'sources':['nor1'], 'targets':[]},
        }), [['a'], ['nor1'], ['out']])
        self.assertEqual(logic_circuit.getRankNodes(nodes:={
            'a':{'type':'INPUT', 'sources':[], 'targets':['not1', 'nor1']},
            'not1':{'type':'NOT', 'sources':['a'], 'targets':['nor1']},
            'nor1':{'type':'NOR2', 'sources':['not1', 'a'], 'targets':['out']},
            'out':{'type':'OUTPUT', 'sources':['nor1'], 'targets':[]},
        }), [['a'], ['not1', 'BYPASS_a'], ['nor1'], ['out']])
        self.assertTrue('BYPASS_a' in nodes)
        self.assertEqual(nodes['a'], {'type':'INPUT', 'sources':[], 'targets':['BYPASS_a', 'not1']})
        self.assertEqual(nodes['BYPASS_a'], {'type':'BYPASS', 'sources':['a'], 'targets':['nor1']})
        self.assertEqual(nodes['nor1'], {'type':'NOR2', 'sources':['not1', 'BYPASS_a'], 'targets':['out']})
        self.assertEqual(logic_circuit.getRankNodes({
            'a':{'type':'INPUT', 'sources':[], 'targets':['nor1']},
            'b':{'type':'INPUT', 'sources':[], 'targets':['nor1']},
            'nor1':{'type':'NOR2', 'sources':['a', 'b'], 'targets':['out']},
            'out':{'type':'OUTPUT', 'sources':['nor1'], 'targets':[]},
        }), [['a', 'b'], ['nor1'], ['out']])

if __name__ == "__main__":""
    unittest.main()
