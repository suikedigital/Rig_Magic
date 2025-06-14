"use client"

import { useRouter } from "next/navigation"
import Image from "next/image"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { boatData } from "@/lib/boat-data"

export function FeaturedBoats() {
  const router = useRouter()
  const featuredBoats = boatData.slice(0, 3)

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {featuredBoats.map((boat) => (
        <Card key={boat.id} className="overflow-hidden">
          <div className="relative h-48">
            <Image src={boat.imageUrl || "/placeholder.svg"} alt={boat.name} fill className="object-cover" />
          </div>
          <CardContent className="p-4">
            <h3 className="text-lg font-semibold">{boat.name}</h3>
            <p className="text-sm text-muted-foreground">
              {boat.manufacturer} {boat.model}
            </p>
            <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
              <div>
                <span className="font-medium">Length:</span> {boat.hull.length}ft
              </div>
              <div>
                <span className="font-medium">Year:</span> {boat.year}
              </div>
              <div>
                <span className="font-medium">Type:</span> {boat.type}
              </div>
              <div>
                <span className="font-medium">Mast:</span> {boat.rig.mastType}
              </div>
            </div>
          </CardContent>
          <CardFooter className="p-4 pt-0">
            <Button variant="outline" className="w-full" onClick={() => router.push(`/boats/${boat.id}`)}>
              View Details
            </Button>
          </CardFooter>
        </Card>
      ))}
    </div>
  )
}
