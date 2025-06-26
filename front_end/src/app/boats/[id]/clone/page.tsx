import { getApiBase } from "@/lib/getApiBase"
import { notFound } from "next/navigation"
import { CloneBoatForm } from "@/components/clone-boat-form"

export default async function CloneBoatPage({ params }: { params: { id: string } }) {
  const { id } = params

  // Use the robust yacht API URL for SSR
  const apiBase = getApiBase('yacht')
  const res = await fetch(`${apiBase}/yacht/${id}`, { cache: "no-store" })

  if (!res.ok) {
    notFound()
  }

  const boat = await res.json()

  return (
    <main className="container mx-auto px-4 py-8">
      <CloneBoatForm originalBoat={boat} />
    </main>
  )
}
