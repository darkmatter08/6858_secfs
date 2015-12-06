import copy, base64, pickle
import secfs.fs
import secfs.crypto

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
    def __init__(self, root):
        # list of version structures
        self.l = {}
        self.root = root

    def increment(self, u, p, u_ihandle, g_ihandle=None):
        """
        u = mod_as
        p = prinipal
        u_ihandle = hash of the user's itable, where user is mod_as
        g_ihandle = hash of the group's itable

        To update the VSL by getting the most recent VV, 
        copying it into a new VS, incrementing the principal's version 
        by one on this copy, and setting the user_ihandle and group_ihandles
        in this new VS.
        """
        if p.is_group():
            assert g_ihandle is not None

        # u not in VSL; add an VS() for them
        if u not in self.l:
            self.l[u] = VS()

        # finding the most recent VV across all VSs
        bestsum = -1
        bestkey = None
        for k in self.l.keys(): # k is prinipal of that VS
            v = self.l[k] # vs of principal k
            s = sum(v.version_vector.values())
            if s > bestsum:
                bestsum = s
                bestkey = k

        old_VS = self.l[bestkey]

        # copy version vector
        old_vv = old_VS.version_vector
        new_vv = copy.deepcopy(old_vv)
        if p not in new_vv:
            new_vv[p] = 0
        new_vv[p] += 1

        # setup new VS
        new_VS = VS()
        new_VS.ihandle = u_ihandle
        new_VS.group_ihandles = copy.deepcopy(self.l[u].group_ihandles)
        if p.is_group():
            new_VS.group_ihandles[p] = g_ihandle

        # copy new VV into new VS
        new_VS.version_vector = new_vv

        # update the VSL with the new VS for this user
        self.l[u] = new_VS

    def updateSignedVSL(self, user, vs):
        print("signing user: {}".format(user))
        key = secfs.crypto.keys[user]
        pickled_vs = pickle.dumps(vs)
        signature = secfs.crypto.sign(key, pickled_vs)
        self.l[user] = (signature, pickled_vs)

    def generateUnsignedVSL(self):
        vsl = VSL(self.root)
        for user in self.l.keys():
            (signature, pickled_vs) = self.l[user]
            if user in secfs.fs.usermap:
                pubkey = secfs.fs.usermap[user]
                if not secfs.crypto.verify(pubkey, signature, pickled_vs):
                    print("signed user:{}".format(user))
                    raise RuntimeError("bad signature on VS of: {}".format(user))
            vs = pickle.loads(pickled_vs)
            vsl.l[user] = vs
        return vsl


