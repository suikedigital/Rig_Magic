import { notFound } from "next/navigation"
import { CloneBoatForm } from "@/components/clone-boat-form"
import { boatData } from "@/lib/boat-data"

export default function CloneBoatPage({ params }: { params: { id: string } }) {
  const boat = boatData.find((b) => b.id === params.id)

  if (!boat) {
    notFound()
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Clone: {boat.name}</h1>
      <CloneBoatForm originalBoat={boat} />
    </main>
  )
}
