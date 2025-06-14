import { MyBoatOverview } from "@/components/my-boat-overview"

export default function MyBoatPage({ params }: { params: { id: string } }) {
  // In a real app, fetch the user's boat from API
  // For now, we'll use mock data or redirect to create the boat view

  return (
    <main className="container mx-auto px-4 py-8">
      <MyBoatOverview boatId={params.id} />
    </main>
  )
}
