import { SearchBoats } from "@/components/search-boats"
import { Carousel } from "@/components/ui/carousel"

export default function Home() {
  return (
    <main className="w-full py-8">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between py-14 gap-8 w-full">
        {/* Left: Massive, Hard Left-Aligned Title & Subtitle */}
        <div className="flex-1 flex flex-col items-start justify-start pl-0">
          <h1 className="text-[7vw] md:text-[8vw] font-extrabold tracking-tight mb-4 italic text-transparent bg-clip-text bg-gradient-to-br from-rigMagicBlue to-blue-900 leading-none drop-shadow-lg text-left">
            Rig Magic
          </h1>
          <h2 className="text-3xl md:text-5xl font-semibold mb-2 text-primary text-left">
            Because Owning Your Yacht
          </h2>
          <h2 className="text-3xl md:text-5xl font-semibold mb-2 text-primary text-left">
            Shouldn't Be a
          </h2>
          <h2 className="text-4xl md:text-6xl font-extrabold mb-4 text-rigMagicBlue italic drop-shadow text-left">
            Rigamarole
          </h2>
          <p className="text-xl md:text-2xl text-muted-foreground max-w-xl text-left">
            Every System. Every Detail. Under Control.
          </p>
        </div>
        {/* Right: Carousel */}
        <div className="flex-1 flex justify-center w-full max-w-md">
          <Carousel />
        </div>
      </div>

      {/* Prominent Search */}
      <div className="my-8">
        <SearchBoats />
      </div>
    </main>
  )
}