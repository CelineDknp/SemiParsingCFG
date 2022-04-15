import regex as re
from .constants import *

#All structures that can contain code but should be ignored (typically, strings and comments)
IGNORE = "ignore"
to_ignore = [{"regex": r"(('(.)*$\s{7}-\s*))?('(.)*')", "type":"string"}, {"regex":r"((\s)*\*(.)*$)+", "type":"comment"}]

#Condition structures, in the form of list of dicts {start, n_branch|single_branch, end}
CONDITION = "condition"
conditions = [{"start":r"\sIF(\s)+", "condition_delimiter":r"\sTHEN(\s)+", "mandatory_delimiter":False, "single_branch":"ELSE\s", "end":"\sEND-IF"}, {"start":r"\sEVALUATE(\s)+", "multiple_branch":"\sWHEN", "end":"\sEND-EVALUATE"}]

#Loops structures
# start: regex for the start of the loop structure
# type: label, multiple_label or control-flow
# goback: True if the execution goes back after the paragraph, false if not
# for label-type: inline-label regex and label-regex regex (first one for the label in the loop call, second for the label in the code body)
# for control-type, control-type = regex towards control-flow
LOOP = "loop"
loops = [{"start":r"\sGO(\s)?TO(\s)+", "type":"label", "goback":False, "inline-label":r"([^\s*.])+(\s)*", "label-regex":r"^\s{7}([^\s*])+(\s)*\."},
         {"start":r"\sPERFORM(\s)+", "type":"multiple_label", "goback":True, "separator":r"(\s)+THRU(\s)*", "inline-label":r"([^\s*.])+(\s)*", "label-regex":r"^\s{7}([^\s*])+(\s)*\."},
         {"start":r"\sPERFORM(\s)+", "type":"label", "goback":True, "inline-label":r"([^\s*.])+(\s)*", "label-regex":r"^\s{7}([^\s*])+(\s)*\."},
         {"start":r"\sNEXT\sSENTENCE(\s)*", "type":"control-flow", "goback":False, "control-type": NODE_COND_END_ANY, "control-regex":r"\.(\s)*$"}
         ]

PARSABLE = "parsable"
parsable = [{"start":r"EXEC\sSQL", "end":"END-EXEC"}]

#Language special case
SPECIAL = "special"
special = [{"regex":r"(\s)*PROCEDURE\sDIVISION", "effect":"start_parse"}, {"regex":r"\.(\s)*$", "effect":"close_all"}]

