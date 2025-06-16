"use client"

import React, { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { getApiBase } from "@/lib/getApiBase"

export function YachtAdminList() {
  const [yachts, setYachts] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string|null>(null)
  const [deleteId, setDeleteId] = useState("")
  const [deleting, setDeleting] = useState<string|null>(null)

  useEffect(() => {
    const fetchYachts = async () => {
      setLoading(true)
      setError(null)
      try {
        const apiBase = getApiBase()
        const res = await fetch(`${apiBase}/yachts/search?query=&boat_type=all`)
        const data = await res.json()
        // Sort by yacht_id descending, take last 10
        const sorted = Array.isArray(data) ? [...data].sort((a, b) => Number(b.yacht_id) - Number(a.yacht_id)).slice(0, 10) : []
        setYachts(sorted)
      } catch (e) {
        setError("Failed to fetch yachts")
      } finally {
        setLoading(false)
      }
    }
    fetchYachts()
  }, [deleting])

  const handleDelete = async (id: string) => {
    setDeleting(id)
    setError(null)
    try {
      const apiBase = getApiBase()
      const res = await fetch(`${apiBase}/yacht/${id}`, { method: "DELETE" })
      if (!res.ok) throw new Error("Delete failed")
      setYachts(yachts => yachts.filter(y => String(y.yacht_id) !== String(id)))
    } catch (e) {
      setError("Failed to delete yacht")
    } finally {
      setDeleting(null)
    }
  }

  const handleDeleteById = async () => {
    if (!deleteId) return
    await handleDelete(deleteId)
    setDeleteId("")
  }

  return (
    <div className="my-8">
      <Card className="mb-8">
        <CardContent className="p-6">
          <h3 className="text-xl font-bold mb-4">Last 10 Yachts Created</h3>
          {loading ? <div>Loading...</div> : null}
          {error ? <div className="text-red-500 mb-2">{error}</div> : null}
          <ul className="divide-y">
            {yachts.map(yacht => (
              <li key={yacht.yacht_id} className="flex items-center justify-between py-2">
                <span>
                  <span className="font-mono text-sm">{yacht.yacht_id}</span> &mdash; {yacht.model || yacht.yacht_class || "(no name)"}
                </span>
                <Button variant="destructive" size="sm" disabled={deleting === String(yacht.yacht_id)} onClick={() => handleDelete(yacht.yacht_id)}>
                  {deleting === String(yacht.yacht_id) ? "Deleting..." : "Delete"}
                </Button>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
      <Card>
        <CardContent className="p-6">
          <h3 className="text-xl font-bold mb-4">Delete Yacht by ID</h3>
          <div className="flex gap-2">
            <input
              className="border rounded px-2 py-1 font-mono"
              type="text"
              placeholder="Enter Yacht ID"
              value={deleteId}
              onChange={e => setDeleteId(e.target.value)}
            />
            <Button variant="destructive" onClick={handleDeleteById} disabled={!deleteId || deleting === deleteId}>
              {deleting === deleteId ? "Deleting..." : "Delete by ID"}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
