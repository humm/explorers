from __future__ import absolute_import, division, print_function
import unittest
import random

import forest

import dotdot
import learners
import explorers

import testenvs

class TestMeshgridGoalExplorer(unittest.TestCase):

    def test_s_rand(self):

        mbounds = ((23, 34), (-3, -2))
        sbounds = ((0, 1), (-1, -0), (101, 1001))
        env = testenvs.BoundedRandomEnv(mbounds, sbounds)
        exp_cfg = explorers.MeshgridGoalExplorer.defcfg._deepcopy()
        exp_cfg.m_channels = env.m_channels
        exp_cfg.s_channels = env.s_channels
        exp_cfg.learner = learners.RandomLearner.defcfg._deepcopy()
        exp_cfg.res = 100

        exp = explorers.MeshgridGoalExplorer(exp_cfg)

        for t in range(100):
            order = exp.explore()
            self.assertTrue(all(c.bounds[0] <= order['m_goal'][c.name] <= c.bounds[1] for c in env.m_channels))
            feedback = env.execute(order)
            exp.receive(feedback)

if __name__ == '__main__':
    unittest.main()
