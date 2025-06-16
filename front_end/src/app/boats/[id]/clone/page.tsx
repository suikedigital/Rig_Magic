import { notFound } from "next/navigation"
import { CloneBoatForm } from "@/components/clone-boat-form"
import { boatData } from "@/lib/boat-data"

export default async function CloneBoatPage({ params }: { params: { id: string } } | { params: Promise<{ id: string }> }) {
  const resolvedParams = await params as { id: string };
  const { id } = resolvedParams;
  const boat = boatData.find((b) => b.id === id);

  if (!boat) {
    notFound();
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Clone: {boat.name}</h1>
      <CloneBoatForm originalBoat={boat} />
    </main>
  );
}
