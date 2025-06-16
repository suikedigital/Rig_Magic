"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import type { Boat } from "@/lib/types"
import { useToast } from "@/hooks/use-toast"
import { useAuth } from "@/hooks/use-auth"
import { Info, Ship, Sailboat, Wind, Waves, Anchor } from "lucide-react"

interface MyBoatEditFormProps {
  boatId: string
}

export function MyBoatEditForm({ boatId }: MyBoatEditFormProps) {
  const [boat, setBoat] = useState<Boat | null>(null)
  const [activeTab, setActiveTab] = useState("profile")
  const router = useRouter()
  const { toast } = useToast()
  const { user } = useAuth()

  useEffect(() => {
    if (!user) {
      router.push("/")
      return
    }

    // Mock boat data - in real app, fetch user's boat
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

  const handleProfileChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    if (!boat) return
    const { name, value } = e.target
    setBoat((prev) =>
      prev
        ? {
            ...prev,
            [name]: value,
          }
        : null,
    )
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // In a real app, this would save to a database
    toast({
      title: "Yacht updated successfully!",
      description: "Your changes have been saved.",
    })

    router.push(`/my-boats/${boatId}`)
  }

  if (!boat) {
    return <div>Loading...</div>
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Edit: {boat.name}</h1>
        <p className="text-muted-foreground">
          {boat.manufacturer} {boat.model} • {boat.year}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid grid-cols-3 md:grid-cols-6 w-full">
            <TabsTrigger value="profile" className="flex items-center gap-2">
              <Info className="h-4 w-4" />
              <span className="hidden sm:inline">Profile</span>
            </TabsTrigger>
            <TabsTrigger value="hull" className="flex items-center gap-2">
              <Ship className="h-4 w-4" />
              <span className="hidden sm:inline">Hull</span>
            </TabsTrigger>
            <TabsTrigger value="rig" className="flex items-center gap-2">
              <Sailboat className="h-4 w-4" />
              <span className="hidden sm:inline">Rig Specs</span>
            </TabsTrigger>
            <TabsTrigger value="saildata" className="flex items-center gap-2">
              <Wind className="h-4 w-4" />
              <span className="hidden sm:inline">Sail Data</span>
            </TabsTrigger>
            <TabsTrigger value="sails" className="flex items-center gap-2">
              <Waves className="h-4 w-4" />
              <span className="hidden sm:inline">Sails</span>
            </TabsTrigger>
            <TabsTrigger value="ropes" className="flex items-center gap-2">
              <Anchor className="h-4 w-4" />
              <span className="hidden sm:inline">Ropes</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="profile" className="space-y-4 pt-4">
            <Card className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="name">Yacht Name</Label>
                  <Input id="name" name="name" value={boat.name} onChange={handleProfileChange} />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="manufacturer">Manufacturer</Label>
                  <Input
                    id="manufacturer"
                    name="manufacturer"
                    value={boat.manufacturer}
                    onChange={handleProfileChange}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="model">Model</Label>
                  <Input id="model" name="model" value={boat.model} onChange={handleProfileChange} />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="year">Year</Label>
                  <Input id="year" name="year" type="number" value={boat.year} onChange={handleProfileChange} />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="type">Type</Label>
                  <Input id="type" name="type" value={boat.type} onChange={handleProfileChange} />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="designer">Designer</Label>
                  <Input id="designer" name="designer" value={boat.designer} onChange={handleProfileChange} />
                </div>

                <div className="space-y-2 md:col-span-2">
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    name="description"
                    value={boat.description}
                    onChange={handleProfileChange}
                    rows={5}
                  />
                </div>
              </div>
            </Card>
          </TabsContent>

          {/* Add other tabs as needed */}
        </Tabs>

        <div className="flex justify-end gap-4">
          <Button type="button" variant="outline" onClick={() => router.push(`/my-boats/${boat.id}`)}>
            Cancel
          </Button>
          <Button type="submit">Save Changes</Button>
        </div>
      </form>
    </div>
  )
}
