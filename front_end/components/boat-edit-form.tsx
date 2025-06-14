"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import type { Boat } from "@/lib/types"
import { useToast } from "@/hooks/use-toast"
import { Info, Ship, Sailboat, Wind, Waves, Anchor } from "lucide-react"

interface BoatEditFormProps {
  boat: Boat
}

export function BoatEditForm({ boat: initialBoat }: BoatEditFormProps) {
  const [boat, setBoat] = useState<Boat>({ ...initialBoat })
  const [activeTab, setActiveTab] = useState("profile")
  const router = useRouter()
  const { toast } = useToast()

  const handleProfileChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setBoat((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleHullChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setBoat((prev) => ({
      ...prev,
      hull: {
        ...prev.hull,
        [name]: value,
      },
    }))
  }

  const handleRigChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target

    // Handle nested properties
    if (name.includes(".")) {
      const [category, subcategory, property] = name.split(".")

      setBoat((prev) => ({
        ...prev,
        rig: {
          ...prev.rig,
          [category]: {
            ...prev.rig[category],
            [subcategory]: {
              ...prev.rig[category][subcategory],
              [property]: value,
            },
          },
        },
      }))
    } else {
      setBoat((prev) => ({
        ...prev,
        rig: {
          ...prev.rig,
          [name]: value,
        },
      }))
    }
  }

  const handleSailDataChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setBoat((prev) => ({
      ...prev,
      sailData: {
        ...prev.sailData,
        [name]: value,
      },
    }))
  }

  const handleSailChange = (index: number, field: string, value: string) => {
    setBoat((prev) => ({
      ...prev,
      sails: prev.sails.map((sail, i) => (i === index ? { ...sail, [field]: value } : sail)),
    }))
  }

  const handleRopeChange = (index: number, field: string, value: string) => {
    setBoat((prev) => ({
      ...prev,
      ropes: prev.ropes.map((rope, i) => (i === index ? { ...rope, [field]: value } : rope)),
    }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // In a real app, this would save to a database
    toast({
      title: "Yacht updated successfully!",
      description: "Your changes have been saved.",
    })

    router.push(`/boats/${boat.id}`)
  }

  return (
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
                <Input id="manufacturer" name="manufacturer" value={boat.manufacturer} onChange={handleProfileChange} />
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

        <TabsContent value="hull" className="space-y-4 pt-4">
          <Card className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="length">Length Overall (ft)</Label>
                <Input
                  id="length"
                  name="length"
                  type="number"
                  step="0.1"
                  value={boat.hull.length}
                  onChange={handleHullChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="waterlineLength">Waterline Length (ft)</Label>
                <Input
                  id="waterlineLength"
                  name="waterlineLength"
                  type="number"
                  step="0.1"
                  value={boat.hull.waterlineLength}
                  onChange={handleHullChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="beam">Beam (ft)</Label>
                <Input
                  id="beam"
                  name="beam"
                  type="number"
                  step="0.1"
                  value={boat.hull.beam}
                  onChange={handleHullChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="draft">Draft (ft)</Label>
                <Input
                  id="draft"
                  name="draft"
                  type="number"
                  step="0.1"
                  value={boat.hull.draft}
                  onChange={handleHullChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="displacement">Displacement (kg)</Label>
                <Input
                  id="displacement"
                  name="displacement"
                  type="number"
                  value={boat.hull.displacement}
                  onChange={handleHullChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="ballast">Ballast (kg)</Label>
                <Input
                  id="ballast"
                  name="ballast"
                  type="number"
                  value={boat.hull.ballast}
                  onChange={handleHullChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="material">Hull Material</Label>
                <Input id="material" name="material" value={boat.hull.material} onChange={handleHullChange} />
              </div>

              <div className="space-y-2">
                <Label htmlFor="ke elType">Keel Type</Label>
                <Input id="keelType" name="keelType" value={boat.hull.keelType} onChange={handleHullChange} />
              </div>
            </div>
          </Card>
        </TabsContent>

        <TabsContent value="rig" className="space-y-4 pt-4">
          <Card className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="rigType">Rig Type</Label>
                <Input id="rigType" name="type" value={boat.rig.type} onChange={handleRigChange} />
              </div>

              <div className="space-y-2">
                <Label htmlFor="mastType">Mast Type</Label>
                <Input id="mastType" name="mastType" value={boat.rig.mastType} onChange={handleRigChange} />
              </div>

              <div className="space-y-2">
                <Label htmlFor="mastHeight">Mast Height (ft)</Label>
                <Input
                  id="mastHeight"
                  name="mastHeight"
                  type="number"
                  step="0.1"
                  value={boat.rig.mastHeight}
                  onChange={handleRigChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="mastMaterial">Mast Material</Label>
                <Input id="mastMaterial" name="mastMaterial" value={boat.rig.mastMaterial} onChange={handleRigChange} />
              </div>

              <div className="space-y-2">
                <Label htmlFor="boomLength">Boom Length (ft)</Label>
                <Input
                  id="boomLength"
                  name="boomLength"
                  type="number"
                  step="0.1"
                  value={boat.rig.boomLength}
                  onChange={handleRigChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="boomMaterial">Boom Material</Label>
                <Input id="boomMaterial" name="boomMaterial" value={boat.rig.boomMaterial} onChange={handleRigChange} />
              </div>
            </div>
          </Card>
        </TabsContent>

        <TabsContent value="saildata" className="space-y-4 pt-4">
          <Card className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="I">I (Foretriangle Height) ft</Label>
                <Input
                  id="I"
                  name="I"
                  type="number"
                  step="0.1"
                  value={boat.sailData.I}
                  onChange={handleSailDataChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="J">J (Foretriangle Base) ft</Label>
                <Input
                  id="J"
                  name="J"
                  type="number"
                  step="0.1"
                  value={boat.sailData.J}
                  onChange={handleSailDataChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="P">P (Mainsail Luff) ft</Label>
                <Input
                  id="P"
                  name="P"
                  type="number"
                  step="0.1"
                  value={boat.sailData.P}
                  onChange={handleSailDataChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="E">E (Mainsail Foot) ft</Label>
                <Input
                  id="E"
                  name="E"
                  type="number"
                  step="0.1"
                  value={boat.sailData.E}
                  onChange={handleSailDataChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="mainsailArea">Mainsail Area (sq ft)</Label>
                <Input
                  id="mainsailArea"
                  name="mainsailArea"
                  type="number"
                  value={boat.sailData.mainsailArea}
                  onChange={handleSailDataChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="foretriangle">Foretriangle Area (sq ft)</Label>
                <Input
                  id="foretriangle"
                  name="foretriangle"
                  type="number"
                  value={boat.sailData.foretriangle}
                  onChange={handleSailDataChange}
                />
              </div>
            </div>
          </Card>
        </TabsContent>

        <TabsContent value="sails" className="space-y-4 pt-4">
          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">Sail Inventory</h3>
            <div className="space-y-4">
              {boat.sails.map((sail, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor={`sail-type-${index}`}>Type</Label>
                      <Input
                        id={`sail-type-${index}`}
                        value={sail.type}
                        onChange={(e) => handleSailChange(index, "type", e.target.value)}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor={`sail-material-${index}`}>Material</Label>
                      <Input
                        id={`sail-material-${index}`}
                        value={sail.material}
                        onChange={(e) => handleSailChange(index, "material", e.target.value)}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor={`sail-area-${index}`}>Area (sq ft)</Label>
                      <Input
                        id={`sail-area-${index}`}
                        type="number"
                        value={sail.area}
                        onChange={(e) => handleSailChange(index, "area", e.target.value)}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor={`sail-condition-${index}`}>Condition (1-10)</Label>
                      <Input
                        id={`sail-condition-${index}`}
                        type="number"
                        min="1"
                        max="10"
                        value={sail.condition}
                        onChange={(e) => handleSailChange(index, "condition", e.target.value)}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor={`sail-year-${index}`}>Year</Label>
                      <Input
                        id={`sail-year-${index}`}
                        type="number"
                        value={sail.year}
                        onChange={(e) => handleSailChange(index, "year", e.target.value)}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor={`sail-manufacturer-${index}`}>Manufacturer</Label>
                      <Input
                        id={`sail-manufacturer-${index}`}
                        value={sail.manufacturer}
                        onChange={(e) => handleSailChange(index, "manufacturer", e.target.value)}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </TabsContent>

        <TabsContent value="ropes" className="space-y-4 pt-4">
          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">Rope Inventory</h3>
            <div className="space-y-4">
              {boat.ropes.map((rope, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor={`rope-name-${index}`}>Name</Label>
                      <Input
                        id={`rope-name-${index}`}
                        value={rope.name}
                        onChange={(e) => handleRopeChange(index, "name", e.target.value)}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor={`rope-material-${index}`}>Material</Label>
                      <Input
                        id={`rope-material-${index}`}
                        value={rope.material}
                        onChange={(e) => handleRopeChange(index, "material", e.target.value)}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor={`rope-diameter-${index}`}>Diameter (mm)</Label>
                      <Input
                        id={`rope-diameter-${index}`}
                        type="number"
                        value={rope.diameter}
                        onChange={(e) => handleRopeChange(index, "diameter", e.target.value)}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor={`rope-length-${index}`}>Length (m)</Label>
                      <Input
                        id={`rope-length-${index}`}
                        type="number"
                        value={rope.length}
                        onChange={(e) => handleRopeChange(index, "length", e.target.value)}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor={`rope-condition-${index}`}>Condition (1-10)</Label>
                      <Input
                        id={`rope-condition-${index}`}
                        type="number"
                        min="1"
                        max="10"
                        value={rope.condition}
                        onChange={(e) => handleRopeChange(index, "condition", e.target.value)}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor={`rope-category-${index}`}>Category</Label>
                      <Input
                        id={`rope-category-${index}`}
                        value={rope.category}
                        onChange={(e) => handleRopeChange(index, "category", e.target.value)}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </TabsContent>
      </Tabs>

      <div className="flex justify-end gap-4">
        <Button type="button" variant="outline" onClick={() => router.push(`/boats/${boat.id}`)}>
          Cancel
        </Button>
        <Button type="submit">Save Changes</Button>
      </div>
    </form>
  )
}
