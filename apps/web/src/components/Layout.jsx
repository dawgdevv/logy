import { Link, useLocation } from 'react-router-dom'

const navItems = [
  { path: '/', label: 'graph' },
  { path: '/search', label: 'search' },
]

function Layout({ children }) {
  const location = useLocation()

  return (
    <div className="min-h-screen">
      <div className="grain" />

      <header className="fixed top-0 left-0 right-0 z-50 h-10 flex items-center px-5 border-b"
        style={{ background: 'var(--bg-deep)', borderColor: 'var(--border-muted)' }}>
        <div className="flex items-center gap-6 w-full">
          <Link to="/" className="flex items-center gap-2 no-underline">
            <span className="w-2 h-2 rounded-full" style={{ background: 'var(--accent)' }} />
            <span className="text-xs font-medium tracking-widest uppercase"
              style={{ color: 'var(--text-primary)', fontFamily: '"DM Mono", monospace' }}>
              logy
            </span>
          </Link>

          <nav className="flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className="px-2.5 py-1 text-xs tracking-wide no-underline transition-colors"
                style={{
                  fontFamily: '"DM Mono", monospace',
                  color: location.pathname === item.path
                    ? 'var(--accent)'
                    : 'var(--text-muted)',
                }}
              >
                {item.label}
              </Link>
            ))}
          </nav>

          <div className="ml-auto flex items-center gap-3">
            <span className="text-xs" style={{ color: 'var(--text-muted)', fontFamily: '"DM Mono", monospace' }}>
              {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
            </span>
          </div>
        </div>
      </header>

      <main className="pt-10">
        {children}
      </main>
    </div>
  )
}

export default Layout
