from matrix_library.matrix import Matrix
from src.graph import WebGraph
from pca_implementation.src.power_iteration import PowerIteration

class PageRank:
    def __init__(self, damping: float = 0.85):
        self.damping = damping

    def fit(self, graph: WebGraph) -> list[float]:
        transition = graph.transition_matrix()
        g_matrix = self.google_matrix(transition)
        n = g_matrix.rows

        r = Matrix([[1/n] for _ in range(n)])

        for _ in range(1000):
            r_new = g_matrix @ r
            diff = sum(abs(r_new.data[i][0]-r.data[i][0]) for i in range(n))
            r = r_new
            if diff < 1e-9:
                break
        self.scores_ = [r.data[i][0] for i in range(n)]
        return self.scores_
    
    def google_matrix(self, M: Matrix) -> Matrix:
        n = M.rows
        d = self.damping
        
        dangling = []
        for j in range(n):
            col_sum = sum(M.data[i][j] for i in range(n))
            dangling.append(1 if col_sum < 1e-10 else 0)
        
        teleport = (1 - d) / n
        g_data = []
        for row in range(n):
            g_row = []
            for col in range(n):
                dangling_fix = d * dangling[col] / n
                g_row.append(d * M.data[row][col] + dangling_fix + teleport)
            g_data.append(g_row)
        
        return Matrix(g_data)

    def rank(self) -> list[tuple[int, float]]:
        return sorted(enumerate(self.scores_), key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    graph = WebGraph(4)
    graph.add_link(0, 1)
    graph.add_link(0, 2)
    graph.add_link(1, 2)
    graph.add_link(2, 0)
    graph.add_link(3, 2)
    page_rank = PageRank(0.85)
    page_rank.fit(graph)
    page_rank.rank()