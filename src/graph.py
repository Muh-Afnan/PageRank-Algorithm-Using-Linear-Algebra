from matrix_library.matrix import Matrix

class WebGraph:
    def __init__(self, n_pages: int):
        self.n_pages = n_pages
        self.matrix = self.adjacency_matrix()

    def add_link(self, from_page: int, to_page: int):
        self.matrix.data[from_page][to_page] = 1

    def remove_link(self, from_page: int, to_page: int):
        if self.matrix is not None:
            self.matrix.data[from_page][to_page] = 0

    def adjacency_matrix(self) -> "Matrix":
        self.matrix = Matrix(
            [[0 for _ in range(self.n_pages)] for _ in range(self.n_pages)]
        )
        return self.matrix

    def transition_matrix(self) -> "Matrix":
        matrix_t = self.matrix.transpose()
        for i in range(matrix_t.rows):
            row_sum = sum(matrix_t.data[i])
            for j in range(matrix_t.cols):
                if row_sum > 0:
                    matrix_t.data[i][j] /= row_sum
        return matrix_t.transpose()

    def sumcheck(self) -> bool:
        matrix_tansition = self.transition_matrix()
        matrix_transition_t = matrix_tansition.transpose()
        for i in range(matrix_transition_t.rows):
            row_sum = sum(matrix_transition_t.data[i])
            print(f"Row {i} sum: {row_sum}")
            if abs(row_sum - 1) > 1e-6:
                print(f"Row {i} sums to {row_sum}, which is not 1.")
                return False
        return True


if __name__ == "__main__":
    graph = WebGraph(4)
    graph.add_link(0, 1)
    graph.add_link(0, 2)
    graph.add_link(1, 2)
    graph.add_link(2, 0)
    graph.add_link(3, 2)
    print("Web Graph created with 4 pages and links between them.")
    print(graph.matrix)

    print("Adjacency Matrix:")
    for row in graph.matrix.data:
        print(row)

    print("\nTransition Matrix:")
    for row in graph.transition_matrix().data:
        print(row)

    print("\nSum Check:")
    print(graph.sumcheck())
