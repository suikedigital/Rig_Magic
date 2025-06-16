"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Slider } from "@/components/ui/slider"
import { ShoppingCart, AlertTriangle, Info } from "lucide-react"
import type { Boat } from "@/lib/types"
import { useToast } from "@/hooks/use-toast"
import { useCart } from "@/hooks/use-cart"

interface StandingRiggingProps {
  boat: Boat
}

const riggingSpecs = [
  {
    id: "standard",
    name: "Standard",
    description: "1x19 Stainless Steel wire rigging",
    priceMultiplier: 1.0,
  },
  {
    id: "premium",
    name: "Premium",
    description: "High-grade stainless steel with swaged terminals",
    priceMultiplier: 1.5,
  },
  {
    id: "rod",
    name: "Rod Rigging",
    description: "Solid rod rigging for reduced stretch",
    priceMultiplier: 2.2,
  },
  {
    id: "composite",
    name: "Composite",
    description: "Lightweight PBO or carbon fiber rigging",
    priceMultiplier: 3.5,
  },
]

const terminalTypes = [
  { id: "swaged", name: "Swaged", description: "Standard factory swaged terminals" },
  { id: "mechanical", name: "Mechanical", description: "Field-serviceable mechanical terminals" },
  { id: "stemball", name: "Stemball", description: "Articulating stemball terminals" },
  { id: "toggle", name: "Toggle", description: "Toggle terminals for improved articulation" },
]

export function StandingRiggingSelector({ boat }: StandingRiggingProps) {
  const [selectedSpec, setSelectedSpec] = useState("")
  const [customRigging, setCustomRigging] = useState<Record<string, any>>({})
  const [mastTension, setMastTension] = useState(15) // Default tension percentage
  const { toast } = useToast()
  const { addToCart } = useCart()

  // Calculate rigging lengths based on boat specs
  const calculateRiggingLengths = () => {
    // These are simplified calculations - in a real app, these would be more complex
    const mastHeight = boat.rig.mastHeight
    const forestayLength = Math.sqrt(Math.pow(mastHeight * 0.95, 2) + Math.pow(boat.sailData.J, 2))
    const backstayLength = Math.sqrt(Math.pow(mastHeight, 2) + Math.pow(boat.sailData.J * 0.5, 2))
    const upperShroudLength = mastHeight * 0.9
    const lowerShroudLength = mastHeight * 0.6
    const intermediateLength = mastHeight * 0.75

    return {
      forestay: Math.round(forestayLength * 10) / 10,
      backstay: Math.round(backstayLength * 10) / 10,
      upperShrouds: Math.round(upperShroudLength * 10) / 10,
      lowerShrouds: Math.round(lowerShroudLength * 10) / 10,
      intermediates: Math.round(intermediateLength * 10) / 10,
    }
  }

  const riggingLengths = calculateRiggingLengths()

  // Calculate base prices based on length and diameter
  const calculateBasePrice = (length: number, diameter: number) => {
    const baseRate = diameter * 10 // $10 per mm of diameter
    return Math.round(length * baseRate)
  }

  // Calculate total price
  const calculateTotal = () => {
    if (!selectedSpec) return 0

    const specMultiplier = riggingSpecs.find((s) => s.id === selectedSpec)?.priceMultiplier || 1.0

    // Base prices for each component
    const forestayPrice = calculateBasePrice(riggingLengths.forestay, boat.rig.standingRigging.forestay.diameter)
    const backstayPrice = calculateBasePrice(riggingLengths.backstay, boat.rig.standingRigging.backstay.diameter)
    const shroudsPrice = calculateBasePrice(
      riggingLengths.upperShrouds + riggingLengths.lowerShrouds + riggingLengths.intermediates,
      boat.rig.standingRigging.shrouds.diameter,
    )

    // Apply spec multiplier
    const totalPrice = (forestayPrice + backstayPrice + shroudsPrice) * specMultiplier

    // Add terminal costs
    const terminalCost = 200 // Base cost for standard terminals
    const terminalUpcharge =
      customRigging.upperTerminals === "stemball" || customRigging.upperTerminals === "toggle" ? 300 : 0

    return Math.round(totalPrice + terminalCost + terminalUpcharge)
  }

  const handleAddToCart = () => {
    if (!selectedSpec) {
      toast({
        title: "Please select a rigging specification",
        description: "Choose a rigging package that matches your sailing needs.",
        variant: "destructive",
      })
      return
    }

    const specName = riggingSpecs.find((s) => s.id === selectedSpec)?.name || "Standard"

    addToCart({
      id: `standing-rigging-${Date.now()}`,
      name: `${specName} Standing Rigging Package`,
      description: `Complete standing rigging package for ${boat.name}`,
      price: calculateTotal(),
      type: "standing-rigging",
      details: {
        spec: selectedSpec,
        forestayLength: riggingLengths.forestay,
        backstayLength: riggingLengths.backstay,
        upperShroudsLength: riggingLengths.upperShrouds,
        lowerShroudsLength: riggingLengths.lowerShrouds,
        upperTerminals: customRigging.upperTerminals || "swaged",
        lowerTerminals: customRigging.lowerTerminals || "swaged",
        mastTension: mastTension,
      },
    })

    toast({
      title: "Added to cart",
      description: `${specName} standing rigging package has been added to your cart.`,
    })
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Standing Rigging Package</CardTitle>
          <CardDescription>
            Configure a complete standing rigging package for your yacht based on its specifications.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-4">
            <Label>Rigging Specification</Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {riggingSpecs.map((spec) => (
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
                        <Badge variant="secondary">{spec.priceMultiplier}x</Badge>
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
                <div className="flex justify-between items-center">
                  <Label>Calculated Rigging Lengths</Label>
                  <Button variant="outline" size="sm" className="flex items-center gap-1">
                    <Info className="h-4 w-4" />
                    How we calculate
                  </Button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Card>
                    <CardContent className="p-4">
                      <div className="space-y-1">
                        <p className="text-sm text-muted-foreground">Forestay</p>
                        <div className="flex justify-between">
                          <span className="font-medium">{riggingLengths.forestay} ft</span>
                          <span className="text-sm text-muted-foreground">
                            {boat.rig.standingRigging.forestay.diameter}mm
                          </span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4">
                      <div className="space-y-1">
                        <p className="text-sm text-muted-foreground">Backstay</p>
                        <div className="flex justify-between">
                          <span className="font-medium">{riggingLengths.backstay} ft</span>
                          <span className="text-sm text-muted-foreground">
                            {boat.rig.standingRigging.backstay.diameter}mm
                          </span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4">
                      <div className="space-y-1">
                        <p className="text-sm text-muted-foreground">Upper Shrouds</p>
                        <div className="flex justify-between">
                          <span className="font-medium">{riggingLengths.upperShrouds} ft</span>
                          <span className="text-sm text-muted-foreground">
                            {boat.rig.standingRigging.shrouds.diameter}mm
                          </span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4">
                      <div className="space-y-1">
                        <p className="text-sm text-muted-foreground">Lower Shrouds</p>
                        <div className="flex justify-between">
                          <span className="font-medium">{riggingLengths.lowerShrouds} ft</span>
                          <span className="text-sm text-muted-foreground">
                            {boat.rig.standingRigging.shrouds.diameter}mm
                          </span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4">
                      <div className="space-y-1">
                        <p className="text-sm text-muted-foreground">Intermediates</p>
                        <div className="flex justify-between">
                          <span className="font-medium">{riggingLengths.intermediates} ft</span>
                          <span className="text-sm text-muted-foreground">
                            {boat.rig.standingRigging.shrouds.diameter}mm
                          </span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4">
                      <div className="space-y-1">
                        <p className="text-sm text-muted-foreground">Total Length</p>
                        <div className="flex justify-between">
                          <span className="font-medium">
                            {riggingLengths.forestay +
                              riggingLengths.backstay +
                              riggingLengths.upperShrouds +
                              riggingLengths.lowerShrouds +
                              riggingLengths.intermediates}{" "}
                            ft
                          </span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label>Terminal Types</Label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>Upper Terminals</Label>
                    <Select
                      value={customRigging.upperTerminals || ""}
                      onValueChange={(value) =>
                        setCustomRigging((prev) => ({
                          ...prev,
                          upperTerminals: value,
                        }))
                      }
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select terminal type" />
                      </SelectTrigger>
                      <SelectContent>
                        {terminalTypes.map((type) => (
                          <SelectItem key={type.id} value={type.id}>
                            <div>
                              <div className="font-medium">{type.name}</div>
                              <div className="text-sm text-muted-foreground">{type.description}</div>
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label>Lower Terminals</Label>
                    <Select
                      value={customRigging.lowerTerminals || ""}
                      onValueChange={(value) =>
                        setCustomRigging((prev) => ({
                          ...prev,
                          lowerTerminals: value,
                        }))
                      }
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select terminal type" />
                      </SelectTrigger>
                      <SelectContent>
                        {terminalTypes.map((type) => (
                          <SelectItem key={type.id} value={type.id}>
                            <div>
                              <div className="font-medium">{type.name}</div>
                              <div className="text-sm text-muted-foreground">{type.description}</div>
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label>Mast Tension Setting</Label>
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <span>Looser (Cruising)</span>
                    <span>Tighter (Racing)</span>
                  </div>
                  <Slider
                    value={[mastTension]}
                    min={10}
                    max={25}
                    step={1}
                    onValueChange={(value) => setMastTension(value[0])}
                  />
                  <div className="flex justify-center">
                    <Badge variant="outline">{mastTension}% of breaking strength</Badge>
                  </div>
                </div>
              </div>

              <Separator />

              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-semibold">Total Package Price</h3>
                  <p className="text-sm text-muted-foreground">Includes all rigging, terminals, and installation kit</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold">${calculateTotal()}</div>
                  <Button onClick={handleAddToCart} className="mt-2">
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
            <p className="text-sm">• All standing rigging is custom manufactured to your boat's specifications</p>
            <p className="text-sm">• Professional installation is strongly recommended</p>
            <p className="text-sm">• Rigging comes with a 5-year warranty against manufacturing defects</p>
            <p className="text-sm">• Delivery time is typically 2-3 weeks from order confirmation</p>
            <p className="text-sm">
              • A rigging specialist will contact you to confirm all measurements before production
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
