import re

#All structures that can contain code but should be ignored (typically, strings and comments)
IGNORE = "ignore"
to_ignore = ["'", r"\*"]

#Condition structures, in the form of list of dicts {start, n_branch|single_branch, end}
CONDITION = "condition"
conditions = [{"start":r"\sIF(\s)+", "single_branch":"ELSE", "end":"END-IF"}, {"start":r"\sEVALUATE(\s)+", "multiple_branch":"WHEN", "end":"END-EVALUATE"}]

#Loops structures
LOOP = "loop"
loops = [{}]

PARSABLE = "parsable"
parsable = [{"start":r"EXEC\sSQL", "end":"END-EXEC"}]

#Language special case
SPECIAL = "special"
special = [{"regex":r"\.(\s)+", "effect":"close_all"}]

#_____INTERNAL CONFIG, DO NOT CHANGE______
NODE_CONTROL = "CONTROL"
NODE_FUSED = "FUSED"
NODE_COND_END_ANY = "END_"
NODE_COND_START = "COND_START"
NODE_COND_BRANCH = "COND_BRANCH"
NODE_COND_END = "COND_END"
NODE_SQL = "EXEC"