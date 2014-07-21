"""\
Meshgrid goal explorer
"""
from __future__ import absolute_import, division, print_function
import random
import numbers
import collections

from .. import conduits
from .. import tools
from .. import meshgrid
from .s_rand import RandomGoalExplorer


defcfg = RandomGoalExplorer.defcfg._copy(deep=True)
defcfg._describe('res', instanceof=(numbers.Integral, collections.Iterable),
                 docstring='resolution of the meshgrid')
defcfg.classname = 'explorers.MeshgridGoalExplorer'


class MeshgridGoalExplorer(RandomGoalExplorer):
    """\
    Necessitate a sensory bounded environement.
    """
    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(MeshgridGoalExplorer, self).__init__(cfg)
        self._meshgrid = meshgrid.MeshGrid(self.cfg, [c.bounds for c in self.s_channels], cfg.res)

    def explore(self):
        # pick a random bin
        if len(self._meshgrid._nonempty_bins) == 0:
            s_goal = tools.random_signal(self.s_channels)
        else:
            s_bin = random.choice(self._meshgrid._nonempty_bins)
            s_goal = tools.random_signal(self.s_channels, s_bin.bounds)

        m_goal = self._inv_request(s_goal)
        return {'m_goal': m_goal, 's_goal': s_goal, 'from': 'goal.babbling.mesh'}

    def receive(self, feedback):
        super(MeshgridGoalExplorer, self).receive(feedback)
        self._meshgrid.add(tools.to_vector(feedback['s_signal'], self.s_channels), feedback['m_signal'])
