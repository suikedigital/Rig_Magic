"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import type { Boat } from "@/lib/types"
import { useToast } from "@/hooks/use-toast"
import { useAuth } from "@/hooks/use-auth"

interface CloneBoatFormProps {
  originalBoat: Boat
}

const boatSpecs = [
  {
    id: "day-cruiser",
    name: "Day Cruiser",
    description: "Optimized for day sailing and coastal cruising",
  },
  {
    id: "ocean-spec",
    name: "Ocean Spec",
    description: "Built for offshore and ocean sailing",
  },
  {
    id: "club-racer",
    name: "Club Racer",
    description: "Performance setup for club racing",
  },
  {
    id: "full-race",
    name: "Full Race",
    description: "Maximum performance racing configuration",
  },
  {
    id: "luxury",
    name: "Luxury",
    description: "Premium materials and comfort-focused setup",
  },
]

export function CloneBoatForm({ originalBoat }: CloneBoatFormProps) {
  const [formData, setFormData] = useState({
    name: `${originalBoat.name} - Copy`,
    spec: "",
    notes: "",
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const router = useRouter()
  const { toast } = useToast()
  const { user } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    // Simulate API call to clone boat
    await new Promise((resolve) => setTimeout(resolve, 2000))

    // Create cloned boat ID
    const clonedBoatId = `${originalBoat.id}-clone-${Date.now()}`

    toast({
      title: "Boat cloned successfully!",
      description: `${formData.name} has been added to your fleet.`,
    })

    setIsSubmitting(false)
    router.push(`/my-boats/${clonedBoatId}`)
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Clone Boat Configuration</CardTitle>
          <CardDescription>
            Set up your cloned boat with basic information and performance specifications.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="name">Boat Name</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="Enter your boat's name"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="spec">Performance Specification</Label>
              <Select value={formData.spec} onValueChange={(value) => setFormData({ ...formData, spec: value })}>
                <SelectTrigger>
                  <SelectValue placeholder="Select a performance specification" />
                </SelectTrigger>
                <SelectContent>
                  {boatSpecs.map((spec) => (
                    <SelectItem key={spec.id} value={spec.id}>
                      <div>
                        <div className="font-medium">{spec.name}</div>
                        <div className="text-sm text-muted-foreground">{spec.description}</div>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="notes">Additional Notes</Label>
              <Textarea
                id="notes"
                value={formData.notes}
                onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                placeholder="Any specific requirements or modifications..."
                rows={4}
              />
            </div>

            <div className="flex justify-end gap-4">
              <Button type="button" variant="outline" onClick={() => router.back()}>
                Cancel
              </Button>
              <Button type="submit" disabled={isSubmitting || !formData.spec}>
                {isSubmitting ? "Cloning..." : "Clone Boat"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>What happens next?</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <h4 className="font-medium">Rigging Configuration</h4>
              <p className="text-sm text-muted-foreground">
                Customize your running and standing rigging with rope packages and hardware options.
              </p>
            </div>
            <div className="space-y-2">
              <h4 className="font-medium">Sail Inventory</h4>
              <p className="text-sm text-muted-foreground">
                Modify your sail configuration based on your chosen performance specification.
              </p>
            </div>
            <div className="space-y-2">
              <h4 className="font-medium">Service Booking</h4>
              <p className="text-sm text-muted-foreground">
                Book professional services for installation and maintenance of your custom setup.
              </p>
            </div>
            <div className="space-y-2">
              <h4 className="font-medium">Ongoing Updates</h4>
              <p className="text-sm text-muted-foreground">
                Continue to modify and update your boat's specifications at any time.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
