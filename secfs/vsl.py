import copy

# version structure
class VS:
    def __init__(self):
        # user's i-handle
        self.ihandle = None
        # list of some group i-handles
        self.group_ihandles = {}
        # user's version vector
        self.version_vector = {}

    def add_group_ihandle(self, group, ihandle):
        self.group_ihandles[group] = ihandle

# version structure list
class VSL:
    def __init__(self):
        # list of version structures
        self.l = {}
    def increment(self, u, p, u_ihandle, g_ihandle=None):
        if p.is_group():
            assert g_ihandle is not None
        if u not in self.l:
            self.l[u] = VS()
        bestsum = -1
        bestkey = None
        for k,v in self.l:
            s = sum(v.version_vector.values())
            if s > bestsum:
                bestsum = s
                bestkey = k
	old_VS = self.l[bestkey]
        old_vv = old_VS.version_vector
        new_vv = copy.deepcopy(old_vv)
	if p not in new_vv:
	    new_vv[p] = 0
	new_vv[p] += 1
	#setup new VS
	new_VS = VS()
	new_VS.ihandle = u_ihandle
	new_VS.group_ihandles = copy.deepcopy(self.l[u].group_ihandles)
        if p.is_group():
            new_VS.group_ihandles[p] = g_ihandle
	new_VS.version_vector = new_vv
	
	self.l[u] = new_VS
