import { MyBoatServiceBooking } from "@/components/my-boat-service-booking"

export default function MyBoatServicePage({ params }: { params: { id: string } }) {
  return (
    <main className="container mx-auto px-4 py-8">
      <MyBoatServiceBooking boatId={params.id} />
    </main>
  )
}
