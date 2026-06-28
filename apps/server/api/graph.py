from fastapi import APIRouter

from packages.cognee.graph import get_graph

router = APIRouter(prefix="/api/graph", tags=["graph"])


@router.get("/")
def get_knowledge_graph():
    """Get the knowledge graph as nodes and edges for React Flow."""
    graph = get_graph()

    nodes = []
    for node_id, data in graph.nodes(data=True):
        node_type = data.get("type", "unknown")
        nodes.append(
            {
                "id": node_id,
                "position": {"x": 0, "y": 0},
                "data": {"label": data.get("name", data.get("content", node_id)[:50])},
                "type": node_type,
            }
        )

    edges = []
    for source, target, data in graph.edges(data=True):
        edges.append(
            {
                "id": f"{source}-{target}",
                "source": source,
                "target": target,
                "label": data.get("relationship", ""),
            }
        )

    return {"nodes": nodes, "edges": edges}
