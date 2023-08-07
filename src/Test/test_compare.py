import pytest
from main import compare_graphs


# Testing the base matching 
def test_base_case():
    teq = compare_graphs("raincodeData/VisualisationExamples/V1/if_normal_full_match.COB", "raincodeData/VisualisationExamples/V2/if_normal_full_match.COB")
    assert teq.equivalent == True #Comparing two of the same graphs should be True
    g1 = teq.g1
    g2 = teq.g2
    for l in g1.all_transitions:
        assert l.match == 1
    for l in g2.all_transitions:
        assert l.match == 1

#Testing special case with if fact
def test_if_fact():
    teq = compare_graphs("raincodeData/VisualisationExamples/V1/if_fact.COB", "raincodeData/VisualisationExamples/V2/if_fact.COB")
    assert teq.equivalent == True #This is a working factorization case
    g1 = teq.g1
    g2 = teq.g2
    for l in g1.all_transitions:
        assert l.match == 1
    for l in g2.all_transitions:
        assert l.match == 1

#Testing special case with if eval
#def test_if_eval():
#    teq = compare_graphs("TestFiles/pytest/if_before_eval_test_file.COB", "TestFiles/pytest/evaluate_simple_test_file.COB")
#    assert teq.equivalent == True #This is a working evaluate case
#    g1 = teq.g1
#    g2 = teq.g2
#    for l in g1.all_transitions:
#        assert l.match == 1
#    for l in g2.all_transitions:
#        assert l.match == 1

# Testing the base matching with a skip
def test_base_skip_case():
    teq = compare_graphs("raincodeData/VisualisationExamples/V1/if_skip.COB", "raincodeData/VisualisationExamples/V2/if_skip.COB")
    assert teq.equivalent == True 
    g1 = teq.g1
    g2 = teq.g2
    for l in g1.all_transitions:
        assert l.match == 1
    for l in g2.all_transitions:
        if "B" in l.label:
            assert l.match == 0 #Both IF branches should be skipped
        else:
            assert l.match == 1 #All other should be matched

# Testing the base matching with a non-equivalent file
def test_base_no_match_case():
    teq = compare_graphs("raincodeData/VisualisationExamples/V1/if_no_match.COB", "raincodeData/VisualisationExamples/V2/if_no_match.COB")
    assert teq.equivalent == False 
    g1 = teq.g1
    g2 = teq.g2
    for l in g1.all_transitions:
        if l.label == "INTERNAL":
            assert l.match == 1
        else:
            assert l.match == -1

    for l in g2.all_transitions:
        if l.label == "INTERNAL":
            assert l.match == 1
        elif "C" in l.label: #No match
            assert l.match == -1
        elif "D" in l.label: #neither
            assert l.match == -1
        else: #Did not explore further
            assert l.match == -2