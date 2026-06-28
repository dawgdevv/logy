import { useCallback, useEffect, useState } from 'react'
import { ReactFlow, Controls, Background } from '@xyflow/react'
import '@xyflow/react/dist/style.css'

const nodeStyles = {
  entry: { background: 'var(--accent-glow)', border: '1px solid var(--accent-dim)', color: 'var(--text-primary)' },
  person: { background: 'var(--bg-elevated)', border: '1px solid var(--border-subtle)', color: 'var(--accent)' },
  technology: { background: 'var(--bg-elevated)', border: '1px solid var(--border-subtle)', color: 'var(--text-secondary)' },
  entity: { background: 'var(--bg-elevated)', border: '1px solid var(--border-subtle)', color: 'var(--text-muted)' },
}

function Graph() {
  const [nodes, setNodes] = useState([])
  const [edges, setEdges] = useState([])
  const [stats, setStats] = useState(null)

  useEffect(() => {
    fetch('/api/graph/')
      .then((res) => res.json())
      .then((data) => {
        if (data.nodes) {
          const styled = data.nodes.map((node) => ({
            ...node,
            style: nodeStyles[node.type] || nodeStyles.entity,
            sourcePosition: 'right',
            targetPosition: 'left',
          }))
          setNodes(styled)
        }
        if (data.edges) {
          const styled = data.edges.map((edge) => ({
            ...edge,
            style: { stroke: 'var(--border-subtle)', strokeWidth: 1 },
            animated: false,
          }))
          setEdges(styled)
        }
      })
      .catch(console.error)
  }, [])

  const onNodesChange = useCallback((changes) => {
    setNodes((nds) => {
      const updated = [...nds]
      changes.forEach((change) => {
        if (change.type === 'position' && change.position) {
          const node = updated.find((n) => n.id === change.id)
          if (node) node.position = change.position
        }
      })
      return updated
    })
  }, [])

  return (
    <div className="relative" style={{ background: 'var(--bg-deep)' }}>
      <div className="absolute top-4 left-5 z-10 flex items-baseline gap-4">
        <h1 className="serif text-2xl italic" style={{ color: 'var(--text-primary)' }}>
          knowledge graph
        </h1>
        {nodes.length > 0 && (
          <span className="text-xs" style={{ color: 'var(--text-muted)', fontFamily: '"DM Mono", monospace' }}>
            {nodes.length} nodes · {edges.length} edges
          </span>
        )}
      </div>

      <div className="graph-container">
        {nodes.length === 0 ? (
          <div className="absolute inset-0 flex items-center justify-center z-10">
            <div className="text-center">
              <p className="serif text-xl italic mb-2" style={{ color: 'var(--text-muted)' }}>
                empty graph
              </p>
              <p className="text-xs" style={{ color: 'var(--text-muted)', fontFamily: '"DM Mono", monospace' }}>
                entries will appear as they are enriched
              </p>
            </div>
          </div>
        ) : (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            fitView
            fitViewOptions={{ padding: 0.2 }}
          >
            <Controls position="bottom-right" />
            <Background
              color="var(--border-muted)"
              gap={40}
              size={1}
            />
          </ReactFlow>
        )}
      </div>
    </div>
  )
}

export default Graph
