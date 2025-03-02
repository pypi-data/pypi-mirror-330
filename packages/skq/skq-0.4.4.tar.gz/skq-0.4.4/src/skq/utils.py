import numpy as np
from plotly import graph_objects as go


def _check_quantum_state_array(X):
    """Ensure that input are normalized state vectors of the right size."""
    if len(X.shape) != 2:
        raise ValueError("Input must be a 2D array.")

    # Check if all inputs are complex
    if not np.iscomplexobj(X):
        raise ValueError("Input must be a complex array.")

    # Check if input is normalized.
    normalized = np.allclose(np.linalg.norm(X, axis=-1), 1)
    if not normalized:
        not_normalized = X[np.linalg.norm(X, axis=-1) != 1]
        raise ValueError(f"Input state vectors must be normalized. Got non-normalized vectors: '{not_normalized}'")

    # Check if input is a valid state vector
    _, n_states = X.shape
    num_qubits = int(np.log2(n_states))
    assert n_states == 2**num_qubits, f"Expected state vector length {2**num_qubits}, got {n_states}."
    return True


def to_bitstring(arr: np.array) -> list[str]:
    """
    Convert a 2D binary array to a list of bitstrings.
    :param arr: A 2D binary array
    For example:
    [[0, 1],
     [1, 0]]
    :return: List of bitstrings
    For example:
    ['01', '10']
    """
    return ["".join(map(str, m)) for m in arr]


def matrix_heatmap(matrix: np.array, title: str = "Matrix Heatmap") -> go.Figure:
    """
    Visualize a matrix as a heatmap.
    :param matrix: A 2D array
    :param title: Title of the plot
    :return: A plotly figure
    """
    fig = go.Figure(data=go.Heatmap(z=np.real(matrix), colorscale="RdBu", zmin=-1, zmax=1, text=np.real(matrix).round(3), texttemplate="%{text}", textfont={"size": 10}, hoverongaps=False))
    fig.update_layout(title=title, xaxis_title="Column Index", yaxis_title="Row Index")
    return fig


def bloch(state: np.array) -> go.Figure:
    """
    Plot single qubit state on a Bloch sphere (3D plot).
    :param state: A statevector array for a single qubit
    :return: A plotly figure
    """

    def calculate_coordinates(theta, phi):
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)
        return x, y, z

    fig = go.Figure()
    alpha, beta = state[0], state[1]
    theta = 2 * np.arccos(np.abs(alpha))
    phi = np.angle(beta) - np.angle(alpha)
    x, y, z = calculate_coordinates(theta, phi)
    surface_phi, surface_theta = np.mgrid[0 : 2 * np.pi : 100j, 0 : np.pi : 50j]
    xs, ys, zs = calculate_coordinates(surface_theta, surface_phi)

    fig.add_trace(go.Surface(x=xs, y=ys, z=zs, opacity=0.5, colorscale="Blues", showscale=False))

    fig.add_trace(go.Scatter3d(x=[0, x], y=[0, y], z=[0, z], mode="lines+markers+text", marker=dict(size=10, color="green"), line=dict(color="green", width=8), textposition="top center", showlegend=True, name=f"{alpha:.3f}|0⟩ + {beta:.3f}|1⟩"))

    fig.add_trace(go.Scatter3d(x=[0, 0, 1, -1, 0, 0], y=[0, 0, 0, 0, 1, -1], z=[1, -1, 0, 0, 0, 0], mode="markers", marker=dict(size=5, color="black"), hovertext=["|0⟩", "|1⟩", "|+⟩", "|-⟩", "|i⟩", "|-i⟩"], showlegend=False, name="Basis states"))

    boundary_phi = np.linspace(0, 2 * np.pi, 100)
    coords = [(np.cos(boundary_phi), np.sin(boundary_phi), np.zeros_like(boundary_phi)), (np.zeros_like(boundary_phi), np.cos(boundary_phi), np.sin(boundary_phi)), (np.cos(boundary_phi), np.zeros_like(boundary_phi), np.sin(boundary_phi))]

    for x, y, z in coords:
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color="black", width=2), showlegend=False, name="Axes"))

    fig.update_layout(
        legend=dict(
            font=dict(size=20),
            x=0.05,
            y=0.95,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig


def measure_state(state: np.array) -> int:
    """
    Measure a quantum state and return a classical bit.
    :param state: A statevector array
    :return: A classical bit
    """
    # Absolute value squared gives us the probability distribution from the statevector
    p = np.abs(state) ** 2
    # Sample from probability distribution to get classical bits
    return np.random.choice([0, 1], p=p)
