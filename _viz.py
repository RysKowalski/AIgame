from pathlib import Path
from collections import defaultdict


def cluster_dot(input_path: str, output_path: str) -> None:
    with open(input_path) as f:
        lines = f.readlines()

    nodes: dict[str, str] = {}
    edges: list[str] = []
    files_by_dir: defaultdict[str, list[str]] = defaultdict(list)

    for line in lines:
        line = line.strip()

        if "->" in line:
            edges.append(line)
        elif line and line.endswith(";") and "[" not in line:
            node = line.replace(";", "")
            nodes[node] = line
            path = Path(node)
            files_by_dir[str(path.parent)].append(node)

    out: list[str] = []
    out.append("digraph G {")
    out.append("compound=true;")

    for i, (directory, files) in enumerate(files_by_dir.items()):
        out.append(f"subgraph cluster_{i} {{")
        out.append(f'label="{directory}";')

        for f in files:
            out.append(f)

        out.append("}")

    out.extend(edges)
    out.append("}")

    with open(output_path, "w") as f:
        f.write("\n".join(out))


cluster_dot("graph.dot", "graph_clustered.dot")
