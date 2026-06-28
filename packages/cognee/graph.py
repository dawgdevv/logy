import networkx as nx

from packages.shared.config import settings


def get_graph() -> nx.Graph:
    """Get or create the knowledge graph."""
    graph_path = settings.graph_dir / "knowledge.graphml"
    if graph_path.exists():
        return nx.read_graphml(graph_path)
    return nx.Graph()


def save_graph(graph: nx.Graph) -> None:
    """Save the knowledge graph to disk."""
    settings.graph_dir.mkdir(parents=True, exist_ok=True)
    graph_path = settings.graph_dir / "knowledge.graphml"
    nx.write_graphml(graph, graph_path)


def add_entry_node(
    graph: nx.Graph,
    entry_id: int,
    content: str,
    category: str,
    summary: str | None = None,
    **attrs: object,
) -> None:
    """Add an entry node to the graph."""
    graph.add_node(
        f"entry_{entry_id}",
        type="entry",
        entry_id=entry_id,
        content=content,
        category=category,
        summary=summary or "",
        **attrs,
    )


def add_entity_node(
    graph: nx.Graph,
    name: str,
    entity_type: str,
    **attrs: object,
) -> None:
    """Add an entity node (person, technology, etc.) to the graph."""
    node_id = f"{entity_type}_{name.lower().replace(' ', '_')}"
    if not graph.has_node(node_id):
        graph.add_node(
            node_id,
            type=entity_type,
            name=name,
            **attrs,
        )


def add_relationship(
    graph: nx.Graph,
    source: str,
    target: str,
    relationship_type: str,
    **attrs: object,
) -> None:
    """Add a relationship edge between two nodes."""
    graph.add_edge(
        source,
        target,
        relationship=relationship_type,
        **attrs,
    )


def get_entry_context(graph: nx.Graph, entry_id: int) -> dict[str, list[str]]:
    """Get all entities connected to an entry."""
    node_id = f"entry_{entry_id}"
    if not graph.has_node(node_id):
        return {"people": [], "technologies": [], "entities": []}

    context: dict[str, list[str]] = {"people": [], "technologies": [], "entities": []}
    for neighbor in graph.neighbors(node_id):
        node = graph.nodes[neighbor]
        node_type = node.get("type", "")
        name = node.get("name", "")
        if node_type == "person":
            context["people"].append(name)
        elif node_type == "technology":
            context["technologies"].append(name)
        elif node_type == "entity":
            context["entities"].append(name)

    return context
