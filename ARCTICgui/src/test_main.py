import unittest

from pipcontrol import boolean_function
from gui.design_goal import LogicCircuitSynth
from gui.design_view import CombinedDesignView

class Test(unittest.TestCase):

    def test_generate_truth_table_From_expr(self) -> None:
        
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

        #Gewuenschtes verhalten fuer XOR operator einfuegen
        
        #Test broken Inputs
        self.assertRaises(Exception, boolean_function.generate_truth_table_from_expr, "a b")
        self.assertRaises(Exception, boolean_function.generate_truth_table_from_expr, "a,b")

    def test_not_connection(self) -> None:
        pass

    def test_nor_connections(self) -> None:
        pass

    def test_in_connections(self) -> None:
        pass

    def test_out_connections(self) -> None:
        pass

    def test_connections(self) -> None:
        pass
    
    def test_not_box(self) -> None:
        pass

    def _nor_box(self) -> None:
        pass

    def test_in_box(self) -> None:
        pass

    def test_out_box(self) -> None:
        pass

    def test_box(self) -> None:
        pass

    def test_nor(self) -> None:
        pass

    def test_LogicCircuitSynth_can_start(self) -> None:
        test_obj = LogicCircuitSynth()
    
    def test_CombinedDesignView(self) -> None:
        test_obj = CombinedDesignView()

         
if __name__ == "__main__":
    unittest.main()
    