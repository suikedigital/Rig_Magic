"use client"

import React, { useEffect, useState } from 'react';
import { useRouter } from "next/navigation"
import Image from "next/image"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface HullData {
  hull_type?: string;
  loa?: number;
  lwl?: number;
  beam?: number;
  displacement?: number;
  ballast?: number;
}

interface KeelData {
  keel_type?: string;
  draft?: number;
}

interface BoatSearchResultsProps {
  query: string
  boat_type: string
}

export function BoatSearchResults({ query, boat_type }: BoatSearchResultsProps) {
  const router = useRouter()
  const [boats, setBoats] = useState<any[]>([])
  const [hullData, setHullData] = useState<Record<string, HullData>>({})
  const [keelData, setKeelData] = useState<Record<string, KeelData>>({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL
    console.log("[BoatSearchResults] API Base URL:", apiBase)
    const searchUrl = `${apiBase}/yachts/search?query=${encodeURIComponent(query)}&boat_type=${encodeURIComponent(boat_type)}`
    console.log("[BoatSearchResults] Fetching:", searchUrl)
    fetch(searchUrl)
      .then(res => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setBoats(data)
          // Fetch hull and keel data for each base yacht
          data.forEach(async (boat) => {
            const yachtId = boat.yacht_id || boat.id;
            // Fetch for all base yachts (base_yacht is falsy/null/undefined/0/'0')
            if (!boat.base_yacht) {
              try {
                // Fetch hull data
                const hullRes = await fetch(`${apiBase}/yachts/${yachtId}/hull`)
                if (hullRes.ok) {
                  const hull = await hullRes.json()
                  console.log("Hull response for", yachtId, hull)
                  setHullData(prev => ({
                    ...prev,
                    [yachtId]: hull
                  }))
                } else if (hullRes.status === 404) {
                  setHullData(prev => ({
                    ...prev,
                    [yachtId]: null
                  }))
                  console.warn("No hull data for", yachtId)
                } else {
                  console.error("Hull API not ok for", yachtId, hullRes.status)
                }
              } catch (err) {
                console.error("Hull API error for", yachtId, err)
              }
              try {
                // Fetch keel data
                const keelRes = await fetch(`${apiBase}/yachts/${yachtId}/keel`)
                if (keelRes.ok) {
                  const keel = await keelRes.json()
                  console.log("Keel response for", yachtId, keel)
                  setKeelData(prev => ({
                    ...prev,
                    [yachtId]: keel
                  }))
                } else if (keelRes.status === 404) {
                  setKeelData(prev => ({
                    ...prev,
                    [yachtId]: null
                  }))
                  console.warn("No keel data for", yachtId)
                } else {
                  console.error("Keel API not ok for", yachtId, keelRes.status)
                }
              } catch (err) {
                console.error("Keel API error for", yachtId, err)
              }
            }
          })
        } else if (data && typeof data === 'object' && Object.keys(data).length === 0) {
          // If backend returns empty object, treat as empty array
          setBoats([])
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
    // No splash screen needed, just return null or a minimal loader if desired
    return null
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
        {boats.map((boat) => {
          const yachtId = boat.yacht_id || boat.id;
          const hull = hullData[yachtId];
          const keel = keelData[yachtId];
          return (
            <Card key={boat.id} className="overflow-hidden">
              <div className="relative h-48">
                <Image src={boat.imageUrl || "/placeholder.svg"} alt={boat.name || "Yacht image"} fill className="object-cover" />
              </div>
              <CardContent className="p-4">
                <h3 className="text-lg font-semibold"> {boat.yacht_class} {boat.model} {boat.version}</h3>
                <p className="text-sm text-muted-foreground">
                  {boat.builder || boat.designer}
                </p>
                <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <span className="font-medium">Length:</span> {(() => {
                      if (hull === null) return <span className="italic text-gray-400">No hull data</span>;
                      if (hull?.loa) return `${(hull.loa / 1000).toFixed(2)} m`;
                      return <span className="italic text-gray-400">Loading...</span>;
                    })()}
                  </div>
                  <div>
                    <span className="font-medium">Year:</span> {boat.production_start}
                  </div>
                  <div>
                    <span className="font-medium">Type:</span> {(() => {
                      if (hull?.hull_type) return hull.hull_type;
                      return "Monohull";
                    })()}
                  </div>
                  <div>
                    <span className="font-medium">Disp':</span> {(() => {
                      if (hull === null) return <span className="italic text-gray-400">No hull data</span>;
                      if (hull?.displacement) return `${hull.displacement}kg`;
                      return <span className="italic text-gray-400">Loading...</span>;
                    })()}
                  </div>
                  <div>
                    <span className="font-medium">Keel:</span> {(() => {
                      if (keel === null) return <span className="italic text-gray-400">No keel data</span>;
                      if (keel?.keel_type) return keel.keel_type;
                      return <span className="italic text-gray-400">Loading...</span>;
                    })()}
                  </div>
                  <div>
                    <span className="font-medium">Rig Type:</span> {boat.rig?.rig_type || <span className="italic text-gray-400">Loading...</span>}
                  </div>
                </div>
              </CardContent>
              <CardFooter className="p-4 pt-0">
                <Button variant="outline" className="w-full" onClick={() => router.push(`/boats/${boat.yacht_id}`)}>
                  View Details
                </Button>
              </CardFooter>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
