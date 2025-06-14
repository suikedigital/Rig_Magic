"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import Image from "next/image"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface BoatSearchResultsProps {
  query: string
  boat_type: string
}

export function BoatSearchResults({ query, boat_type }: BoatSearchResultsProps) {
  const router = useRouter()
  const [boats, setBoats] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL
    fetch(`${apiBase}/yachts/search?query=${encodeURIComponent(query)}&boat_type=${encodeURIComponent(boat_type)}`)
      .then(res => res.json())
      .then(async data => {
        if (Array.isArray(data)) {
          // For each base yacht, fetch full yacht details from orchestrator
          const boatsWithDetails = await Promise.all(data.map(async (boat) => {
            const yachtId = boat.yacht_id || boat.id;
            const details = await fetch(`${apiBase}/yachts/${yachtId}`).then(r => r.ok ? r.json() : null).catch(() => null);
            // Merge the search result (profile) with orchestrator details for fallback fields
            return { ...boat, ...details };
          }))
          setBoats(boatsWithDetails)
        } else {
          setBoats([])
          console.error("API did not return an array:", data)
        }
        setLoading(false)
      })
      .catch((err) => {
        setBoats([])
        setLoading(false)
        console.error("API fetch error:", err)
      })
  }, [query, boat_type])

  if (loading) {
    return <div>Loading...</div>
  }

  if (boats.length === 0) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-semibold mb-2">No results found</h2>
        <p className="text-muted-foreground">Try adjusting your search criteria or browse our featured boats.</p>
      </div>
    )
  }

  return (
    <div>
      <p className="mb-4 text-muted-foreground">Found {boats.length} boats</p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {boats.map((boat) => (
          <Card key={boat.id} className="overflow-hidden">
            <div className="relative h-48">
              <Image src={boat.imageUrl || "/placeholder.svg"} alt={boat.name || "Yacht image"} fill className="object-cover" />
            </div>
            <CardContent className="p-4">
              <h3 className="text-lg font-semibold"> {boat.yacht_class} {boat.model} {boat.version}</h3>
              <p className="text-sm text-muted-foreground">
                {boat.manufacturer || boat.designer}
              </p>
              <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
                <div>
                  <span className="font-medium">Length:</span> {boat.hull?.loa ? `${(boat.hull.loa / 1000).toFixed(2)} m` : <span className="italic text-gray-400">Loading...</span>}
                </div>
                <div>
                  <span className="font-medium">Year:</span> {boat.production_start}
                </div>
                <div>
                  <span className="font-medium">Type:</span> {boat.hull?.hull_type ? boat.hull.hull_type : "Monohull"}
                </div>
                <div>
                  <span className="font-medium">Displacement:</span> {boat.hull?.displacement ? `${boat.hull.displacement}kg` : <span className="italic text-gray-400">Loading...</span>}
                </div>
                <div>
                  <span className="font-medium">Rig Type:</span> {boat.rig?.rig_type || <span className="italic text-gray-400">Loading...</span>}
                </div>
              </div>
            </CardContent>
            <CardFooter className="p-4 pt-0">
              <Button variant="outline" className="w-full" onClick={() => router.push(`/boats/${boat.id}`)}>
                View Details
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  )
}
