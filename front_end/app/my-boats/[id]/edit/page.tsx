import { MyBoatEditForm } from "@/components/my-boat-edit-form"

export default function MyBoatEditPage({ params }: { params: { id: string } }) {
  return (
    <main className="container mx-auto px-4 py-8">
      <MyBoatEditForm boatId={params.id} />
    </main>
  )
}
