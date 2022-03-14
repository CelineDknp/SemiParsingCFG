import re
from Utils.constants import *

#All structures that can contain code but should be ignored (typically, strings and comments)
IGNORE = "ignore"
to_ignore = ["'", r"\*"]

#Condition structures, in the form of list of dicts {start, n_branch|single_branch, end}
CONDITION = "condition"
conditions = [{"start":r"\sIF(\s)+", "single_branch":"ELSE", "end":"END-IF"}, {"start":r"\sEVALUATE(\s)+", "multiple_branch":"WHEN", "end":"END-EVALUATE"}]

#Loops structures
LOOP = "loop"
loops = [{"start":r"\sGO(\s)?TO(\s)+", "type":"label", "label-regex":r"^\s{7}([^\s*])+(\s)*\."}, {"start":r"\sNEXT\sSENTENCE(\s)*", "type":"control-flow", "control-type":NODE_COND_END_ANY}]

PARSABLE = "parsable"
parsable = [{"start":r"EXEC\sSQL", "end":"END-EXEC"}]

#Language special case
SPECIAL = "special"
special = [{"regex":r"(\s)*PROCEDURE\sDIVISION", "effect":"start_parse"}, {"regex":r"\.(\s)+", "effect":"close_all"}]

