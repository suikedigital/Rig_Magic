"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Settings, Ship, Anchor, Wind, Waves, ShoppingCart } from "lucide-react"
import { useAuth } from "@/hooks/use-auth"
import { RopePackageSelector } from "@/components/rope-package-selector"
import { StandingRiggingSelector } from "@/components/standing-rigging-selector"
import type { Boat } from "@/lib/types"

interface MyBoatOverviewProps {
  boatId: string
}

export function MyBoatOverview({ boatId }: MyBoatOverviewProps) {
  const { user } = useAuth()
  const router = useRouter()
  const [boat, setBoat] = useState<Boat | null>(null)
  const [activeTab, setActiveTab] = useState("overview")

  useEffect(() => {
    if (!user) {
      router.push("/")
      return
    }

    // Mock boat data - in real app, fetch user's boat
    // For demo, we'll create a mock boat
    const mockBoat: Boat = {
      id: boatId,
      name: "My Sea Breeze",
      manufacturer: "Catalina",
      model: "34",
      year: 2018,
      type: "Cruiser",
      designer: "Gerry Douglas",
      description: "My customized cruising sailboat",
      hull: {
        length: 34.0,
        waterlineLength: 29.5,
        beam: 11.3,
        draft: 5.5,
        displacement: 5400,
        ballast: 2200,
        material: "Fiberglass",
        keelType: "Fin Keel",
        hullType: "Monohull",
        rudderType: "Spade Rudder",
        ballastRatio: 40.7,
        displacementLengthRatio: 280,
        sailAreaDisplacementRatio: 16.8,
        capsizeScreeningValue: 2.1,
      },
      rig: {
        type: "Sloop",
        mastType: "Deck Stepped",
        mastHeight: 48.5,
        mastMaterial: "Aluminum",
        boomLength: 12.8,
        boomMaterial: "Aluminum",
        standingRigging: {
          forestay: { material: "1x19 Stainless Steel", diameter: 8 },
          backstay: { material: "1x19 Stainless Steel", diameter: 8 },
          shrouds: { material: "1x19 Stainless Steel", diameter: 6 },
        },
        runningRigging: {
          halyards: { count: 3, material: "Polyester/Dyneema" },
          sheets: { count: 4, material: "Polyester Double Braid" },
        },
      },
      sailData: {
        I: 42.0,
        J: 13.5,
        P: 38.0,
        E: 12.8,
        mainsailArea: 243,
        foretriangle: 284,
        totalSailArea100: 527,
        totalSailArea150: 669,
        spinnakerArea: 850,
        downwindSailArea: 1093,
        sailAreaDisplacementRatio: 16.8,
        displacementLengthRatio: 280,
        ballastDisplacementRatio: 40.7,
        capsizeScreeningValue: 2.1,
      },
      sails: [],
      ropes: [],
    }

    setBoat(mockBoat)
  }, [user, router, boatId])

  if (!boat) {
    return <div>Loading...</div>
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold">{boat.name}</h1>
          <p className="text-muted-foreground">
            {boat.manufacturer} {boat.model} • {boat.year}
          </p>
          <Badge className="mt-2">Your Boat</Badge>
        </div>
        <Button onClick={() => router.push(`/my-boats/${boat.id}/edit`)}>
          <Settings className="mr-2 h-4 w-4" />
          Edit Details
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid grid-cols-5 w-full">
          <TabsTrigger value="overview" className="flex items-center gap-2">
            <Ship className="h-4 w-4" />
            Overview
          </TabsTrigger>
          <TabsTrigger value="running-rigging" className="flex items-center gap-2">
            <Anchor className="h-4 w-4" />
            Running Rigging
          </TabsTrigger>
          <TabsTrigger value="standing-rigging" className="flex items-center gap-2">
            <Anchor className="h-4 w-4" />
            Standing Rigging
          </TabsTrigger>
          <TabsTrigger value="sails" className="flex items-center gap-2">
            <Wind className="h-4 w-4" />
            Sails
          </TabsTrigger>
          <TabsTrigger value="services" className="flex items-center gap-2">
            <Waves className="h-4 w-4" />
            Services
          </TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Hull Specifications</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between">
                  <span>Length:</span>
                  <span>{boat.hull.length}ft</span>
                </div>
                <div className="flex justify-between">
                  <span>Beam:</span>
                  <span>{boat.hull.beam}ft</span>
                </div>
                <div className="flex justify-between">
                  <span>Draft:</span>
                  <span>{boat.hull.draft}ft</span>
                </div>
                <div className="flex justify-between">
                  <span>Displacement:</span>
                  <span>{boat.hull.displacement}kg</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Rig Configuration</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between">
                  <span>Type:</span>
                  <span>{boat.rig.type}</span>
                </div>
                <div className="flex justify-between">
                  <span>Mast:</span>
                  <span>{boat.rig.mastType}</span>
                </div>
                <div className="flex justify-between">
                  <span>Height:</span>
                  <span>{boat.rig.mastHeight}ft</span>
                </div>
                <div className="flex justify-between">
                  <span>Material:</span>
                  <span>{boat.rig.mastMaterial}</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Sail Areas</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between">
                  <span>Mainsail:</span>
                  <span>{boat.sailData.mainsailArea} sq ft</span>
                </div>
                <div className="flex justify-between">
                  <span>Foretriangle:</span>
                  <span>{boat.sailData.foretriangle} sq ft</span>
                </div>
                <div className="flex justify-between">
                  <span>Total (100%):</span>
                  <span>{boat.sailData.totalSailArea100} sq ft</span>
                </div>
                <div className="flex justify-between">
                  <span>Spinnaker:</span>
                  <span>{boat.sailData.spinnakerArea} sq ft</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="running-rigging" className="space-y-6">
          <RopePackageSelector boat={boat} />
        </TabsContent>

        <TabsContent value="standing-rigging" className="space-y-6">
          <StandingRiggingSelector boat={boat} />
        </TabsContent>

        <TabsContent value="sails" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Sail Configuration</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground mb-4">Customize your sail inventory based on your sailing needs.</p>
              <Button>
                <ShoppingCart className="mr-2 h-4 w-4" />
                Configure Sails
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="services" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Book Services</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground mb-4">
                Book professional services for your customized boat configuration.
              </p>
              <Button onClick={() => router.push(`/my-boats/${boat.id}/services`)}>Book Services</Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
