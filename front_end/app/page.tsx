import { SearchBoats } from "@/components/search-boats"
import { FeaturedBoats } from "@/components/featured-boats"

export default function Home() {
  return (
    <main className="container mx-auto px-4 py-8">
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold tracking-tight mb-2">Rig Magic</h1>
        <p className="text-lg text-muted-foreground">Find, customize, and service your perfect yacht rigging</p>
      </div>

      <SearchBoats />

      <div className="mt-12">
        <h2 className="text-2xl font-semibold mb-6">Featured Yachts</h2>
        <FeaturedBoats />
      </div>
    </main>
  )
}
