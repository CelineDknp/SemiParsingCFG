import pytest
from main import compare_graphs


# Testing the base matching 
def test_base_case():
    teq = compare_graphs("raincodeData/VisualisationExamples/V1/if_normal_full_match.COB", "raincodeData/VisualisationExamples/V2/if_normal_full_match.COB")
    g1 = teq.g1
    g2 = teq.g2
    for n in g1.all_states:
        if n.id == 156: #Start node
            assert len(n.matches) == 1
            assert n.matches[0] == 163
        if n.id == 157: #P1
            assert len(n.matches) == 1
            assert n.matches[0] == 163
        if n.id == 158: #P2
            assert len(n.matches) == 1
            assert n.matches[0] == 163
        if n.id == 159: #IF
            assert len(n.matches) == 1
            assert n.matches[0] == 164
        if n.id == 160: #P3
            assert len(n.matches) == 1
            assert n.matches[0] == 165
        if n.id == 161: #P4
            assert len(n.matches) == 1
            assert n.matches[0] == 165
        if n.id == 162: #End
            assert len(n.matches) == 1
            assert n.matches[0] == 166

    for n in g2.all_states:
        if n.id == 163: #Start node
            assert len(n.matches) == 3
            assert 156 in n.matches
            assert 157 in n.matches
            assert 158 in n.matches
        if n.id == 164: #If
            assert len(n.matches) == 1
            assert n.matches[0] == 159
        if n.id == 165: #P3
            assert len(n.matches) == 2
            assert 160 in n.matches
            assert 161 in n.matches
        if n.id == 166: #End node
            assert len(n.matches) == 1
            assert n.matches[0] == 162

#Testing special case with if fact
def test_if_fact():
    teq = compare_graphs("raincodeData/VisualisationExamples/V1/if_fact.COB", "raincodeData/VisualisationExamples/V2/if_fact.COB")
    g1 = teq.g1
    g2 = teq.g2
    for n in g1.all_states:
        if n.id == 167: #Start node
            assert len(n.matches) == 1
            assert n.matches[0] == 172
        if n.id == 168: #If 1
            assert len(n.matches) == 1
            assert n.matches[0] == 173
        if n.id == 169: #If 2
            assert len(n.matches) == 1
            assert n.matches[0] == 173
        if n.id == 170: #If 3
            assert len(n.matches) == 1
            assert n.matches[0] == 173
        if n.id == 171: #End
            assert len(n.matches) == 1
            assert n.matches[0] == 174

    for n in g2.all_states:
        if n.id == 172: #Start node
            assert len(n.matches) == 1
            assert n.matches[0] == 167
        if n.id == 173: #If
            assert len(n.matches) == 3
            assert 168 in n.matches
            assert 169 in n.matches
            assert 170 in n.matches
        if n.id == 174: #End node
            assert len(n.matches) == 1
            assert n.matches[0] == 171

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
    g1 = teq.g1
    g2 = teq.g2
    for n in g1.all_states:
        if n.id == 175: #Start node
            assert len(n.matches) == 1
            assert n.matches[0] == 178
        if n.id == 176: #If 1
            assert len(n.matches) == 1
            assert n.matches[0] == 179
        if n.id == 177: #End
            assert len(n.matches) == 1
            assert n.matches[0] == 181

    for n in g2.all_states:
        if n.id == 178: #Start node
            assert len(n.matches) == 1
            assert n.matches[0] == 175
        if n.id == 179: #If 1
            assert len(n.matches) == 1
            assert n.matches[0] == 176
        if n.id == 180: #If 2
            assert len(n.matches) == 0
        if n.id == 181: #End node
            assert len(n.matches) == 1
            assert n.matches[0] == 177

# Testing the base matching with a non-equivalent file
def test_base_no_match_case():
    teq = compare_graphs("raincodeData/VisualisationExamples/V1/if_no_match.COB", "raincodeData/VisualisationExamples/V2/if_no_match.COB")
    g1 = teq.g1
    g2 = teq.g2
    for n in g1.all_states:
        if n.id == 182: #Start node
            assert len(n.matches) == 1
            assert n.matches[0] == 185
        if n.id == 183: #If 1
            assert len(n.matches) == 0
        if n.id == 184: #End
            assert len(n.matches) == 1
            assert n.matches[0] == 188

    for n in g2.all_states:
        if n.id == 185: #Start node
            assert len(n.matches) == 1
            assert n.matches[0] == 182
        if n.id == 186: #If 1
            assert len(n.matches) == 0
        if n.id == 187: #If 2
            assert len(n.matches) == 0
        if n.id == 188: #End node
            assert len(n.matches) == 1
            assert n.matches[0] == 184