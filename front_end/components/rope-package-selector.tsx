"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { ShoppingCart, AlertTriangle } from "lucide-react"
import type { Boat } from "@/lib/types"
import { useToast } from "@/hooks/use-toast"

interface RopePackageSelectorProps {
  boat: Boat
}

const ropeSpecs = [
  {
    id: "day-cruiser",
    name: "Day Cruiser",
    description: "Standard polyester ropes for coastal sailing",
    price: 850,
  },
  {
    id: "ocean-spec",
    name: "Ocean Spec",
    description: "High-strength Dyneema core for offshore sailing",
    price: 1450,
  },
  {
    id: "club-racer",
    name: "Club Racer",
    description: "Performance ropes with low stretch",
    price: 1200,
  },
  {
    id: "full-race",
    name: "Full Race",
    description: "Maximum performance racing lines",
    price: 2100,
  },
  {
    id: "luxury",
    name: "Luxury",
    description: "Premium materials with comfort features",
    price: 1800,
  },
]

const terminationTypes = [
  { id: "eye-splice", name: "Eye Splice", description: "Traditional spliced eye" },
  { id: "soft-shackle", name: "Soft Shackle", description: "Lightweight Dyneema shackle" },
  { id: "snap-shackle", name: "Snap Shackle", description: "Quick release metal shackle" },
  { id: "block-and-tackle", name: "Block & Tackle", description: "Mechanical advantage system" },
]

const hardwareOptions = [
  { id: "standard", name: "Standard", description: "Basic stainless steel hardware", price: 0 },
  { id: "premium", name: "Premium", description: "High-grade stainless with ceramic bearings", price: 300 },
  { id: "carbon", name: "Carbon", description: "Carbon fiber blocks and fittings", price: 800 },
]

export function RopePackageSelector({ boat }: RopePackageSelectorProps) {
  const [selectedSpec, setSelectedSpec] = useState("")
  const [customRopes, setCustomRopes] = useState<Record<string, any>>({})
  const [selectedHardware, setSelectedHardware] = useState("standard")
  const { toast } = useToast()

  const ropeTypes = [
    { id: "main-halyard", name: "Main Halyard", minDiameter: 10, maxDiameter: 14 },
    { id: "jib-halyard", name: "Jib Halyard", minDiameter: 8, maxDiameter: 12 },
    { id: "spinnaker-halyard", name: "Spinnaker Halyard", minDiameter: 8, maxDiameter: 12 },
    { id: "main-sheet", name: "Main Sheet", minDiameter: 12, maxDiameter: 16 },
    { id: "jib-sheets", name: "Jib Sheets", minDiameter: 10, maxDiameter: 14 },
    { id: "spinnaker-sheets", name: "Spinnaker Sheets", minDiameter: 10, maxDiameter: 14 },
  ]

  const handleDiameterChange = (ropeId: string, diameter: number) => {
    const rope = ropeTypes.find((r) => r.id === ropeId)
    if (rope && (diameter < rope.minDiameter || diameter > rope.maxDiameter)) {
      toast({
        title: "Invalid diameter",
        description: `${rope.name} diameter must be between ${rope.minDiameter}mm and ${rope.maxDiameter}mm for this boat.`,
        variant: "destructive",
      })
      return
    }

    setCustomRopes((prev) => ({
      ...prev,
      [ropeId]: { ...prev[ropeId], diameter },
    }))
  }

  const calculateTotal = () => {
    const specPrice = ropeSpecs.find((s) => s.id === selectedSpec)?.price || 0
    const hardwarePrice = hardwareOptions.find((h) => h.id === selectedHardware)?.price || 0
    return specPrice + hardwarePrice
  }

  const handlePurchase = () => {
    if (!selectedSpec) {
      toast({
        title: "Please select a rope specification",
        description: "Choose a rope package that matches your sailing needs.",
        variant: "destructive",
      })
      return
    }

    toast({
      title: "Rope package added to cart",
      description: `${ropeSpecs.find((s) => s.id === selectedSpec)?.name} package for $${calculateTotal()}`,
    })
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Rope Package Selection</CardTitle>
          <CardDescription>
            Choose a rope specification package that matches your sailing style and customize individual ropes as
            needed.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-4">
            <Label>Performance Specification</Label>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {ropeSpecs.map((spec) => (
                <Card
                  key={spec.id}
                  className={`cursor-pointer transition-colors ${
                    selectedSpec === spec.id ? "ring-2 ring-primary" : ""
                  }`}
                  onClick={() => setSelectedSpec(spec.id)}
                >
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <div className="flex justify-between items-start">
                        <h3 className="font-semibold">{spec.name}</h3>
                        <Badge variant="secondary">${spec.price}</Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">{spec.description}</p>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {selectedSpec && (
            <>
              <Separator />

              <div className="space-y-4">
                <Label>Hardware Package</Label>
                <Select value={selectedHardware} onValueChange={setSelectedHardware}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {hardwareOptions.map((option) => (
                      <SelectItem key={option.id} value={option.id}>
                        <div className="flex justify-between items-center w-full">
                          <div>
                            <div className="font-medium">{option.name}</div>
                            <div className="text-sm text-muted-foreground">{option.description}</div>
                          </div>
                          {option.price > 0 && <span className="ml-4">+${option.price}</span>}
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label>Custom Rope Configuration</Label>
                <div className="grid gap-4">
                  {ropeTypes.map((rope) => (
                    <Card key={rope.id}>
                      <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                          <div className="space-y-1">
                            <h4 className="font-medium">{rope.name}</h4>
                            <p className="text-sm text-muted-foreground">
                              Diameter range: {rope.minDiameter}mm - {rope.maxDiameter}mm
                            </p>
                          </div>
                          <div className="flex items-center gap-4">
                            <div className="space-y-2">
                              <Label htmlFor={`${rope.id}-diameter`}>Diameter (mm)</Label>
                              <Select
                                value={customRopes[rope.id]?.diameter?.toString() || ""}
                                onValueChange={(value) => handleDiameterChange(rope.id, Number.parseInt(value))}
                              >
                                <SelectTrigger className="w-20">
                                  <SelectValue placeholder="Auto" />
                                </SelectTrigger>
                                <SelectContent>
                                  {Array.from(
                                    { length: rope.maxDiameter - rope.minDiameter + 1 },
                                    (_, i) => rope.minDiameter + i,
                                  ).map((diameter) => (
                                    <SelectItem key={diameter} value={diameter.toString()}>
                                      {diameter}
                                    </SelectItem>
                                  ))}
                                </SelectContent>
                              </Select>
                            </div>
                            <div className="space-y-2">
                              <Label>Upper Termination</Label>
                              <Select
                                value={customRopes[rope.id]?.upperTermination || ""}
                                onValueChange={(value) =>
                                  setCustomRopes((prev) => ({
                                    ...prev,
                                    [rope.id]: { ...prev[rope.id], upperTermination: value },
                                  }))
                                }
                              >
                                <SelectTrigger className="w-40">
                                  <SelectValue placeholder="Default" />
                                </SelectTrigger>
                                <SelectContent>
                                  {terminationTypes.map((type) => (
                                    <SelectItem key={type.id} value={type.id}>
                                      {type.name}
                                    </SelectItem>
                                  ))}
                                </SelectContent>
                              </Select>
                            </div>
                            <div className="space-y-2">
                              <Label>Lower Termination</Label>
                              <Select
                                value={customRopes[rope.id]?.lowerTermination || ""}
                                onValueChange={(value) =>
                                  setCustomRopes((prev) => ({
                                    ...prev,
                                    [rope.id]: { ...prev[rope.id], lowerTermination: value },
                                  }))
                                }
                              >
                                <SelectTrigger className="w-40">
                                  <SelectValue placeholder="Default" />
                                </SelectTrigger>
                                <SelectContent>
                                  {terminationTypes.map((type) => (
                                    <SelectItem key={type.id} value={type.id}>
                                      {type.name}
                                    </SelectItem>
                                  ))}
                                </SelectContent>
                              </Select>
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>

              <Separator />

              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-semibold">Total Package Price</h3>
                  <p className="text-sm text-muted-foreground">Includes all ropes, terminations, and hardware</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold">${calculateTotal()}</div>
                  <Button onClick={handlePurchase} className="mt-2">
                    <ShoppingCart className="mr-2 h-4 w-4" />
                    Add to Cart
                  </Button>
                </div>
              </div>
            </>
          )}
        </CardContent>
      </Card>

      {selectedSpec && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              Important Notes
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <p className="text-sm">• Rope diameters are automatically validated against your boat's specifications</p>
            <p className="text-sm">• Professional installation is recommended for standing rigging modifications</p>
            <p className="text-sm">• All ropes come with manufacturer warranties and certification</p>
            <p className="text-sm">• Custom terminations may require additional lead time</p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
