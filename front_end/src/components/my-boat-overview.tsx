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

    // Fetch the real boat data for this user and boatId
    const fetchBoat = async () => {
      try {
        // Fetch user profile to get yacht_ids
        const userRes = await fetch(`${process.env.NEXT_PUBLIC_PROFILE_API_URL}/users/${user.id}`)
        if (!userRes.ok) throw new Error("Failed to fetch user profile")
        const userProfile = await userRes.json()
        const yachtIds = userProfile.yacht_ids || []
        if (!yachtIds.includes(boatId)) {
          setBoat(null)
          return
        }
        // Fetch the yacht details
        const boatRes = await fetch(`${process.env.NEXT_PUBLIC_YACHT_API_URL}/yacht/${boatId}`)
        if (!boatRes.ok) throw new Error("Failed to fetch boat data")
        const boatData = await boatRes.json()
        setBoat({ ...boatData, id: boatId })
      } catch (err) {
        setBoat(null)
      }
    }
    fetchBoat()
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
