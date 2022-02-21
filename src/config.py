import re

#All structures that can contain code but should be ignored (typically, strings and comments)
to_ignore = ["'", r"\*"]

#Condition structures, in the form of list of dicts {open, n_branch|single_branch, close}
conditions = [{"open":r"\sIF(\s)+", "single_branch":"ELSE", "close":"END-IF"}]

#Loops structures
loops = [{}]

parsable = [{"start":r"EXEC\sSQL", "end":"END-EXEC"}]

#Language special case
special = [{"regex":r"\.(\s)+", "effect":"close_all"}]