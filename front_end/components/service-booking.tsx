"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Checkbox } from "@/components/ui/checkbox"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { CalendarIcon, Wrench, Anchor, Wind, Waves, Settings, CheckCircle } from "lucide-react"
import type { Boat } from "@/lib/types"
import { useToast } from "@/hooks/use-toast"
import { format } from "date-fns"

interface ServiceBookingProps {
  boat: Boat
}

const serviceCategories = [
  {
    id: "rigging",
    name: "Rigging Services",
    icon: Anchor,
    services: [
      { id: "standing-rigging-inspection", name: "Standing Rigging Inspection", price: 250 },
      { id: "running-rigging-replacement", name: "Running Rigging Replacement", price: 500 },
      { id: "mast-tuning", name: "Mast Tuning", price: 300 },
      { id: "rigging-maintenance", name: "General Rigging Maintenance", price: 200 },
    ],
  },
  {
    id: "sails",
    name: "Sail Services",
    icon: Wind,
    services: [
      { id: "sail-repair", name: "Sail Repair", price: 150 },
      { id: "sail-cleaning", name: "Sail Cleaning", price: 100 },
      { id: "sail-inspection", name: "Sail Inspection", price: 75 },
      { id: "new-sail-consultation", name: "New Sail Consultation", price: 200 },
    ],
  },
  {
    id: "hull",
    name: "Hull Services",
    icon: Waves,
    services: [
      { id: "hull-cleaning", name: "Hull Cleaning", price: 300 },
      { id: "antifouling", name: "Antifouling Application", price: 800 },
      { id: "hull-inspection", name: "Hull Inspection", price: 200 },
      { id: "gelcoat-repair", name: "Gelcoat Repair", price: 400 },
    ],
  },
  {
    id: "mechanical",
    name: "Mechanical Services",
    icon: Settings,
    services: [
      { id: "engine-service", name: "Engine Service", price: 400 },
      { id: "winch-service", name: "Winch Service", price: 150 },
      { id: "electrical-check", name: "Electrical System Check", price: 250 },
      { id: "plumbing-service", name: "Plumbing Service", price: 200 },
    ],
  },
]

export function ServiceBooking({ boat }: ServiceBookingProps) {
  const [selectedServices, setSelectedServices] = useState<string[]>([])
  const [selectedDate, setSelectedDate] = useState<Date>()
  const [contactInfo, setContactInfo] = useState({
    name: "",
    email: "",
    phone: "",
    notes: "",
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const router = useRouter()
  const { toast } = useToast()

  const handleServiceToggle = (serviceId: string) => {
    setSelectedServices((prev) =>
      prev.includes(serviceId) ? prev.filter((id) => id !== serviceId) : [...prev, serviceId],
    )
  }

  const calculateTotal = () => {
    return serviceCategories
      .flatMap((category) => category.services)
      .filter((service) => selectedServices.includes(service.id))
      .reduce((total, service) => total + service.price, 0)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2000))

    toast({
      title: "Service booking confirmed!",
      description: "We'll contact you shortly to confirm the details.",
    })

    setIsSubmitting(false)
    router.push(`/boats/${boat.id}`)
  }

  return (
    <div className="space-y-8">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Wrench className="h-5 w-5" />
            Available Services
          </CardTitle>
          <CardDescription>Select the services you need for your {boat.name}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {serviceCategories.map((category) => (
              <Card key={category.id}>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-lg">
                    <category.icon className="h-5 w-5" />
                    {category.name}
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {category.services.map((service) => (
                    <div key={service.id} className="flex items-center space-x-2">
                      <Checkbox
                        id={service.id}
                        checked={selectedServices.includes(service.id)}
                        onCheckedChange={() => handleServiceToggle(service.id)}
                      />
                      <Label htmlFor={service.id} className="flex-1 cursor-pointer">
                        {service.name}
                      </Label>
                      <span className="font-medium">${service.price}</span>
                    </div>
                  ))}
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {selectedServices.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Booking Details</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name</Label>
                  <Input
                    id="name"
                    value={contactInfo.name}
                    onChange={(e) => setContactInfo((prev) => ({ ...prev, name: e.target.value }))}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={contactInfo.email}
                    onChange={(e) => setContactInfo((prev) => ({ ...prev, email: e.target.value }))}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="phone">Phone</Label>
                  <Input
                    id="phone"
                    type="tel"
                    value={contactInfo.phone}
                    onChange={(e) => setContactInfo((prev) => ({ ...prev, phone: e.target.value }))}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label>Preferred Date</Label>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button variant="outline" className="w-full justify-start text-left font-normal">
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {selectedDate ? format(selectedDate, "PPP") : "Select date"}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0">
                      <Calendar mode="single" selected={selectedDate} onSelect={setSelectedDate} initialFocus />
                    </PopoverContent>
                  </Popover>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="notes">Additional Notes</Label>
                <Textarea
                  id="notes"
                  placeholder="Any specific requirements or notes about the services..."
                  value={contactInfo.notes}
                  onChange={(e) => setContactInfo((prev) => ({ ...prev, notes: e.target.value }))}
                  rows={4}
                />
              </div>

              <div className="border-t pt-4">
                <div className="flex justify-between items-center mb-4">
                  <span className="text-lg font-semibold">Total Estimate:</span>
                  <span className="text-2xl font-bold">${calculateTotal()}</span>
                </div>

                <div className="space-y-2 mb-4">
                  <h4 className="font-medium">Selected Services:</h4>
                  <ul className="space-y-1">
                    {serviceCategories
                      .flatMap((category) => category.services)
                      .filter((service) => selectedServices.includes(service.id))
                      .map((service) => (
                        <li key={service.id} className="flex justify-between text-sm">
                          <span>{service.name}</span>
                          <span>${service.price}</span>
                        </li>
                      ))}
                  </ul>
                </div>

                <Button type="submit" className="w-full" size="lg" disabled={isSubmitting || !selectedDate}>
                  {isSubmitting ? (
                    "Booking..."
                  ) : (
                    <>
                      <CheckCircle className="mr-2 h-4 w-4" />
                      Book Services
                    </>
                  )}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
