import { useState } from 'react'

function Search() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    setSearched(true)
    try {
      const res = await fetch('/api/entries/?limit=100')
      const data = await res.json()
      const q = query.toLowerCase()
      const filtered = data.filter(
        (entry) =>
          entry.content.toLowerCase().includes(q) ||
          entry.category.toLowerCase().includes(q) ||
          (entry.project?.name || '').toLowerCase().includes(q) ||
          entry.tags?.some((t) => t.name.toLowerCase().includes(q))
      )
      setResults(filtered)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-[calc(100vh-40px)]" style={{ background: 'var(--bg-deep)' }}>
      <div className="max-w-3xl mx-auto px-5 py-16">
        <div className="mb-10">
          <h1 className="serif text-4xl italic mb-2" style={{ color: 'var(--text-primary)' }}>
            query
          </h1>
          <p className="text-xs tracking-wider uppercase" style={{ color: 'var(--text-muted)', fontFamily: '"DM Mono", monospace' }}>
            search through your accumulated knowledge
          </p>
        </div>

        <form onSubmit={handleSearch} className="flex gap-0 mb-12">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="what did you work on?"
            className="input-search flex-1"
          />
          <button type="submit" className="btn-primary">
            {loading ? '...' : 'find'}
          </button>
        </form>

        {searched && !loading && results.length === 0 && (
          <div className="py-20 text-center">
            <p className="text-sm" style={{ color: 'var(--text-muted)', fontFamily: '"DM Mono", monospace' }}>
              no matches for "{query}"
            </p>
          </div>
        )}

        {results.length > 0 && (
          <div>
            <div className="flex items-baseline gap-3 mb-6">
              <span className="stat-value">{results.length}</span>
              <span className="stat-label">results</span>
            </div>

            <div className="space-y-px" style={{ background: 'var(--border-muted)' }}>
              {results.map((entry) => (
                <article key={entry.id} className="result-card">
                  <p className="text-sm leading-relaxed mb-3" style={{ color: 'var(--text-primary)' }}>
                    {entry.content}
                  </p>
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="tag">{entry.category}</span>
                    <span className="tag">{entry.difficulty}</span>
                    {entry.project && (
                      <span className="tag tag-accent">{entry.project.name}</span>
                    )}
                    {entry.tags?.map((tag) => (
                      <span key={tag.id} className="tag">{tag.name}</span>
                    ))}
                    <span className="ml-auto text-xs" style={{ color: 'var(--text-muted)', fontFamily: '"DM Mono", monospace' }}>
                      {new Date(entry.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                    </span>
                  </div>
                </article>
              ))}
            </div>
          </div>
        )}

        {!searched && (
          <div className="py-20">
            <div className="grid grid-cols-3 gap-px" style={{ background: 'var(--border-muted)' }}>
              {['entries', 'projects', 'tags'].map((label) => (
                <div key={label} className="p-6 text-center" style={{ background: 'var(--bg-deep)' }}>
                  <span className="stat-label">{label}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Search
