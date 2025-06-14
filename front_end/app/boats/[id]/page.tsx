import { notFound } from "next/navigation"
import { BoatOverview } from "@/components/boat-overview"
import { boatData } from "@/lib/boat-data"

export default function BoatPage({ params }: { params: { id: string } }) {
  const boat = boatData.find((b) => b.id === params.id)

  if (!boat) {
    notFound()
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <BoatOverview boat={boat} />
    </main>
  )
}
