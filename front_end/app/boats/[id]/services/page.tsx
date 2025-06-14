import { notFound } from "next/navigation"
import { ServiceBooking } from "@/components/service-booking"
import { boatData } from "@/lib/boat-data"

export default function ServiceBookingPage({ params }: { params: { id: string } }) {
  const boat = boatData.find((b) => b.id === params.id)

  if (!boat) {
    notFound()
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Book Services for {boat.name}</h1>
      <ServiceBooking boat={boat} />
    </main>
  )
}
