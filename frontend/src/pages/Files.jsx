import { useEffect, useState } from 'react'
import { api } from '../services/api.js'

export default function Files() {
  const [files, setFiles] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.listFiles().then(setFiles).finally(() => setLoading(false))
  }, [])

  async function handleDelete(fileId) {
    await api.deleteFile(fileId)
    setFiles(files.filter((f) => f.file_id !== fileId))
  }

  return (
    <div className="card p-6">
      <h2 className="text-lg font-semibold mb-2">Cloud files</h2>
      <p className="text-xs text-muted mb-4">
        Files exported from the Generate plan page are saved here — this is the object storage side of the
        architecture, separate from the structured plan data in the cloud database.
      </p>

      {loading ? (
        <p className="text-sm text-muted">Loading…</p>
      ) : files.length === 0 ? (
        <p className="text-sm text-muted">No files exported yet. Export a plan from the Generate plan page.</p>
      ) : (
        <div className="space-y-1">
          {files.map((f) => (
            <div key={f.file_id} className="flex justify-between items-center py-2 border-b border-border text-sm">
              <span>📄 {f.filename}</span>
              <span className="flex items-center gap-3 text-muted">
                {f.size_kb} · {new Date(f.uploaded_at).toLocaleDateString()}
                <button onClick={() => handleDelete(f.file_id)} className="btn-ghost">Delete</button>
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
