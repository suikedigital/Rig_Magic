import { SearchBoatsNav } from "@/components/search-boats-nav"
import { BoatSearchResults } from "@/components/boat-search-results"
import { Navigation } from "@/components/navigation"
import { getApiBase } from "@/lib/getApiBase"

// Helper to fetch and normalize minimal boat data for a search result card
async function fetchMinimalBoat(id: string) {
  const apiUrl = `${getApiBase('yacht')}/yacht/${id}` // Use yacht service
  const res = await fetch(apiUrl)
  if (!res.ok) return null
  const boatData = await res.json()
  // Robustly extract hull, keel, and rig fields
  const hull = boatData.hull || {}
  const keel = boatData.keel || {}
  const rig = boatData.rig || {}
  return {
    id: String(boatData.yacht_id),
    name: boatData.profile?.name || "Base Yacht",
    yacht_class: boatData.profile?.yacht_class || "",
    model: boatData.profile?.model || "",
    builder: boatData.profile?.builder || "",
    designer: boatData.profile?.designer || "",
    production_start: boatData.profile?.production_start || null,
    imageUrl: boatData.profile?.imageUrl || boatData.profile?.image_url || undefined,
    hull: {
      loa: (hull.loa || 0) / 1000,
      beam: (hull.beam || 0) / 1000,
      hull_type: hull.hull_type || null,
      construction: hull.construction || null,
      displacement: hull.displacement || null,
      ballast: hull.ballast || null,
    },
    keel: {
      keel_type: keel.keel_type || hull.keel_type || null,
      draft: keel.draft ? (keel.draft / 1000) : null,
    },
    rig: {
      rig_type: rig.rig_type || rig.type || null,
    },
  }
}

export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<{ query?: string; boat_type?: string }>
}) {
  const params = await searchParams
  const query = params?.query || ""
  const boat_type = params?.boat_type || "all"
  const searchUrl = `${getApiBase('yacht')}/yachts/search?query=${encodeURIComponent(query)}&boat_type=${encodeURIComponent(boat_type)}`
  const res = await fetch(searchUrl)
  const data = await res.json()
  let boats: any[] = []
  if (Array.isArray(data)) {
    boats = await Promise.all(
      data.map(async (boat: any) => {
        const yachtId = boat.yacht_id || boat.id
        // Fetch minimal boat data for card
        return await fetchMinimalBoat(yachtId)
      })
    )
    boats = boats.filter(Boolean) // Remove nulls if any fetch failed
  }
  return (
    <>
      <Navigation centerContent={<SearchBoatsNav />} />
      <main className="container mx-auto px-4 py-8 pt-20">
        <BoatSearchResults boats={boats} />
      </main>
    </>
  )
}