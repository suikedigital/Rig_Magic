import { notFound } from "next/navigation"
import { BoatOverview } from "@/components/boat-overview"
import type { Boat } from "@/lib/types"

// Fetch yacht data from orchestrator API
async function getBoat(id: string) {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"
  const apiUrl = `${apiBase}/yachts/${id}`
  console.log("[BoatPage] Fetching yacht from:", apiUrl)
  try {
    const res = await fetch(apiUrl)
    if (!res.ok) {
      if (res.status === 404) return null
      throw new Error("Failed to fetch yacht data")
    }
    return await res.json()
  } catch (e) {
    console.error("[BoatPage] Error fetching yacht:", e)
    return null
  }
}

export default async function BoatPage({ params }: { params: { id: string } }) {
  const { id } = await params
  const boatData = await getBoat(id)

  if (!boatData) {
    notFound()
  }

  // Construct the Boat prop from the orchestrator API response
  const boat: Boat = {
    id: String(boatData.yacht_id),
    name: boatData.profile?.name || "Base Yacht",
    yacht_class: boatData.profile?.yacht_class || "",
    model: boatData.profile?.model || "",
    version: boatData.profile?.version || "",
    designer: boatData.profile?.designer || "",
    builder: boatData.profile?.builder || "",
    year_introduced: Number(boatData.profile?.year_introduced || boatData.profile?.production_start || 0),
    production_start: Number(boatData.profile?.production_start || 0),
    production_end: Number(boatData.profile?.production_end || 0),
    type: boatData.hull?.hull_type || "",
    
    notes: boatData.profile?.description || boatData.profile?.notes || "",
    imageUrl: boatData.profile?.imageUrl || boatData.profile?.image_url || undefined,
    hull: {
      loa: (boatData.hull?.loa || 0) / 1000,
      lwl: (boatData.hull?.lwl || 0) / 1000,
      beam: (boatData.hull?.beam || 0) / 1000,
      draft: (boatData.keel?.draft || 0) / 1000,
      displacement: boatData.hull?.displacement || 0,
      ballast: boatData.hull?.ballast || 0,
      material: boatData.hull?.construction || "",
      keelType: boatData.keel?.keel_type || boatData.hull?.keel_type || "",
      hullType: boatData.hull?.hull_type || "",
      rudderType: boatData.rudder?.rudder_type || "",
      construction: boatData.hull?.construction || "",
      ballastRatio: boatData.hull?.ballast_ratio || 0,
      displacementLengthRatio: boatData.hull?.displacement_length_ratio || 0,
      sailAreaDisplacementRatio: boatData.hull?.sail_area_displacement_ratio || 0,
      capsizeScreeningValue: boatData.hull?.capsize_screening_value || 0,
    },
    rig: boatData.rig || ({} as any),
    sailData: {
      I: (boatData.saildata?.i || 0) / 1000,
      J: (boatData.saildata?.j || 0) / 1000,
      P: (boatData.saildata?.p || 0) / 1000,
      E: (boatData.saildata?.e || 0) / 1000,
      mainsailArea: boatData.saildata?.mainsail_area || 0,
      foretriangle: boatData.saildata?.foretriangle || 0,
      totalSailArea100: boatData.saildata?.total_sail_area_100 || 0,
      totalSailArea150: boatData.saildata?.total_sail_area_150 || 0,
      spinnakerArea: boatData.saildata?.spinnaker_area || 0,
      downwindSailArea: boatData.saildata?.downwind_sail_area || 0,
      sailAreaDisplacementRatio: boatData.saildata?.sail_area_displacement_ratio || 0,
      displacementLengthRatio: boatData.saildata?.displacement_length_ratio || 0,
      ballastDisplacementRatio: boatData.saildata?.ballast_displacement_ratio || 0,
      capsizeScreeningValue: boatData.saildata?.capsize_screening_value || 0,
    },
    sails: boatData.sails || [],
    ropes: boatData.ropes || [],
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <BoatOverview boat={boat} />
    </main>
  )
}
