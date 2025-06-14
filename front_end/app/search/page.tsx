import { SearchBoats } from "@/components/search-boats"
import { BoatSearchResults } from "@/components/boat-search-results"

export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<{ query?: string; boat_type?: string }>
}) {
  const params = await searchParams
  const query = params?.query || ""
  const boat_type = params?.boat_type || "all"

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Search Results</h1>

      <div className="mb-8">
        <SearchBoats />
      </div>

      <BoatSearchResults query={query} boat_type={boat_type} />
    </main>
  )
}
