import re
from .constants import *

"""Condition structures
start: regex for the start of the condition structure
single_branch | multiple_branch : regex for a conditon branch
end: regex for the end of the condition
*condition_delimiter: regex for a condition delimiter, if any
*mandatory_delimiter: boolean signifying if the condition delimiter is mandatory
"""
conditions = [
    {"start":r"\sIF(\s)+", "condition_delimiter":r"\sTHEN(\s)+", "mandatory_delimiter":False, "single_branch":r"ELSE\s", "end":r"\sEND-IF"}, 
    {"start":r"\sEVALUATE(\s)+", "multiple_branch":r"\sWHEN", "end":r"\sEND-EVALUATE", "special_case":r"\sWHEN\s*.*\n\s+WHEN"}
]

"""Loops structures
start: regex for the start of the loop structure
type: label | multiple_label | control-flow
goback: True if the execution goes back after the paragraph, false if not
for label-type: 
    inline-label: regex for the label after the loop structure
    label-regex: regex for the label in the code body
for control-flow:
    control-type: node type towards wich the loop jumps (see node types in Utils/contants.py)
    control-regex: regex for the element towards which  the loop jumps
"""
loops = [
    {"start":r"\sGO(\s)?TO(\s)+", "type":"label", "goback":False, "inline-label":r"([^\s*.])+(\s)*", "label-regex":r"^\s{7}([^\s*])+(\s)*\."},
    {"start":r"\sPERFORM(\s)+", "type":"multiple_label", "goback":True, "separator":r"(\s)+(THRU|THROUGH)(\s)+", "inline-label":r"([^\s*.])+", "label-regex":r"^\s{7}([^\s*])+(\s)*\."},
    {"start":r"\sPERFORM(\s)+", "type":"label", "goback":True, "inline-label":r"([^\s*.])+(\s)", "label-regex":r"^\s{7}([^\s*])+(\s)*\."},
    {"start":r"\sPERFORM(((.*)(\s)+VARYING(\s)+.*(\s)+FROM(\s)+.*(\s)+BY(\s)+.*)|.*)?(\s)+UNTIL.*", "type":"block","end":r"(\s)*END-PERFORM(\s)*", "branch":"VARYING", "condition":"UNTIL", "goback":True},
    {"start":r"\sNEXT\sSENTENCE(\s)*", "type":"control-flow", "goback":False, "control-type": NODE_COND_END_ANY, "control-regex":r"\.(\s)*$"}
]
"""Structure that we want to parse
start: regex for the start of the structure
end: regex for the end of the structure
[Note] The text found in between the start and end regex will be parsed
"""
parsable = [{"start":r"EXEC\sSQL", "end":r"END-EXEC"}]

#Language special case (first in this list to speedup parsing)
special = [{"regex":r"(\s)*PROCEDURE\sDIVISION", "effect":"start_parse"}, {"regex":r"\.(\s)*$", "effect":"close_all"}]

#All structures that can contain code but should be ignored (typically, strings and comments)
to_ignore = [
    {"regex": r"('.*$\s{7}-\s*)?'[^\n']*'", "type":"string"}, 
    {"regex":r"^\s{6}((\s)*\*(.)*$)+", "type":"comment"}
]

