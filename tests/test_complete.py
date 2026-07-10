import unittest
import math
from matrix_library.matrix import Matrix
from src.graph import WebGraph
from src.page_rank import PageRank


class TestPageRank(unittest.TestCase):

    # ---------- Helpers ----------

    def col_sums(self, M: Matrix):
        cols = list(zip(*M.data))
        return [sum(col) for col in cols]

    def approx(self, a, b, tol=1e-3):
        return abs(a - b) < tol

    # ---------- Transition Matrix ----------

    def test_transition_matrix_columns_sum_to_one(self):
        g = WebGraph(3)
        g.add_link(0, 1)
        g.add_link(1, 2)
        g.add_link(2, 0)

        T = g.transition_matrix()
        col_sums = self.col_sums(T)

        for s in col_sums:
            self.assertTrue(self.approx(s, 1.0))

    # ---------- PageRank Properties ----------

    def test_pagerank_sums_to_one(self):
        g = WebGraph(4)
        g.add_link(0, 1)
        g.add_link(1, 2)
        g.add_link(2, 3)
        g.add_link(3, 0)

        pr = PageRank()
        scores = pr.fit(g)

        self.assertTrue(self.approx(sum(scores), 1.0))

    def test_pagerank_vector_non_negative(self):
        g = WebGraph(3)
        g.add_link(0, 1)
        g.add_link(1, 2)

        pr = PageRank()
        scores = pr.fit(g)

        for s in scores:
            self.assertTrue(s >= 0)

    # ---------- Dangling Node ----------

    def test_dangling_node_handled(self):
        g = WebGraph(3)
        g.add_link(0, 1)
        # node 2 is dangling (no outgoing links)

        pr = PageRank()
        scores = pr.fit(g)

        # still valid probability distribution
        self.assertTrue(self.approx(sum(scores), 1.0))
        for s in scores:
            self.assertTrue(s >= 0)

    # ---------- Damping Effect ----------

    def test_damping_factor_effect(self):
        g = WebGraph(3)
        g.add_link(0, 1)
        g.add_link(1, 2)
        g.add_link(2, 0)

        pr_low = PageRank(damping=0.5)
        pr_high = PageRank(damping=0.95)

        scores_low = pr_low.fit(g)
        scores_high = pr_high.fit(g)

        # with higher damping, distribution should deviate more from uniform
        uniform = 1 / 3

        deviation_low = sum(abs(s - uniform) for s in scores_low)
        deviation_high = sum(abs(s - uniform) for s in scores_high)

        self.assertTrue(deviation_high >= deviation_low)

    # ---------- Convergence ----------

    def test_convergence(self):
        g = WebGraph(4)
        g.add_link(0, 1)
        g.add_link(1, 2)
        g.add_link(2, 3)
        g.add_link(3, 0)

        pr = PageRank()

        scores1 = pr.fit(g)
        scores2 = pr.fit(g)

        for a, b in zip(scores1, scores2):
            self.assertTrue(self.approx(a, b))

    # ---------- Known Graph Ranking ----------

    def test_known_graph_ranking(self):
        g = WebGraph(3)

        # node 2 gets most links → should rank highest
        g.add_link(0, 2)
        g.add_link(1, 2)
        g.add_link(2, 0)

        pr = PageRank()
        scores = pr.fit(g)

        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

        # node 2 should be top
        self.assertEqual(ranked[0][0], 2)

    # ---------- NetworkX Comparison ----------

    def test_matches_networkx(self):
        try:
            import networkx as nx
        except ImportError:
            self.skipTest("networkx not installed")

        g = WebGraph(4)
        g.add_link(0, 1)
        g.add_link(1, 2)
        g.add_link(2, 0)
        g.add_link(3, 2)

        pr = PageRank()
        my_scores = pr.fit(g)

        # build same graph in networkx
        G = nx.DiGraph()
        G.add_nodes_from(range(4))
        G.add_edge(0, 1)
        G.add_edge(1, 2)
        G.add_edge(2, 0)
        G.add_edge(3, 2)

        nx_scores_dict = nx.pagerank(G, alpha=0.85)
        nx_scores = [nx_scores_dict[i] for i in range(4)]
        nx_scores_dict = nx.pagerank(G, alpha=0.85)
        nx_scores = [nx_scores_dict[i] for i in range(4)]

        print("My scores:  ", my_scores)
        print("NX scores:  ", nx_scores)

        # compare distributions (allow tolerance)
        for a, b in zip(my_scores, nx_scores):
            self.assertTrue(abs(a - b) < 0.05)


if __name__ == "__main__":
    unittest.main()