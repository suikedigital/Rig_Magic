"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { MapPin, Clock, DollarSign, User, Phone, Mail, CheckCircle, XCircle } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface ServiceJob {
  id: string
  customerName: string
  customerEmail: string
  customerPhone: string
  boatName: string
  boatType: string
  services: string[]
  location: {
    what3words: string
    address: string
    distance: number
  }
  preferredDate: string
  totalEstimate: number
  status: "pending" | "accepted" | "declined" | "completed"
  priority: number
  notes: string
}

export default function ServiceProviderPage() {
  const [jobs, setJobs] = useState<ServiceJob[]>([])
  const [activeTab, setActiveTab] = useState("available")
  const { toast } = useToast()

  useEffect(() => {
    // Mock service jobs - in real app, fetch from API based on provider location
    const mockJobs: ServiceJob[] = [
      {
        id: "1",
        customerName: "John Smith",
        customerEmail: "john@example.com",
        customerPhone: "+1 555-0123",
        boatName: "Sea Breeze",
        boatType: "Catalina 34",
        services: ["Standing Rigging Inspection", "Mast Tuning"],
        location: {
          what3words: "filled.count.soap",
          address: "Marina Bay, San Francisco, CA",
          distance: 2.3,
        },
        preferredDate: "2024-01-15",
        totalEstimate: 550,
        status: "pending",
        priority: 1,
        notes: "Customer mentioned some corrosion on the forestay fitting.",
      },
      {
        id: "2",
        customerName: "Sarah Johnson",
        customerEmail: "sarah@example.com",
        customerPhone: "+1 555-0456",
        boatName: "Wind Dancer",
        boatType: "Beneteau Oceanis 40.1",
        services: ["Running Rigging Replacement", "Sail Repair"],
        location: {
          what3words: "index.home.raft",
          address: "Sausalito Marina, CA",
          distance: 8.7,
        },
        preferredDate: "2024-01-18",
        totalEstimate: 850,
        status: "pending",
        priority: 2,
        notes: "Needs complete jib sheet replacement and minor sail patching.",
      },
      {
        id: "3",
        customerName: "Mike Wilson",
        customerEmail: "mike@example.com",
        customerPhone: "+1 555-0789",
        boatName: "Racing Edge",
        boatType: "J/105",
        services: ["Hull Cleaning", "Antifouling Application"],
        location: {
          what3words: "laptop.purple.desk",
          address: "Berkeley Marina, CA",
          distance: 12.1,
        },
        preferredDate: "2024-01-20",
        totalEstimate: 1100,
        status: "pending",
        priority: 3,
        notes: "Boat needs to be hauled out for bottom work.",
      },
    ]

    setJobs(mockJobs)
  }, [])

  const handleJobAction = (jobId: string, action: "accept" | "decline") => {
    setJobs((prev) =>
      prev.map((job) => (job.id === jobId ? { ...job, status: action === "accept" ? "accepted" : "declined" } : job)),
    )

    toast({
      title: action === "accept" ? "Job accepted!" : "Job declined",
      description: `You have ${action}ed the service request.`,
    })
  }

  const availableJobs = jobs.filter((job) => job.status === "pending")
  const acceptedJobs = jobs.filter((job) => job.status === "accepted")
  const completedJobs = jobs.filter((job) => job.status === "completed")

  return (
    <main className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Service Provider Dashboard</h1>
        <p className="text-muted-foreground">Manage your service requests and jobs</p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="available">Available Jobs ({availableJobs.length})</TabsTrigger>
          <TabsTrigger value="accepted">Accepted Jobs ({acceptedJobs.length})</TabsTrigger>
          <TabsTrigger value="completed">Completed Jobs ({completedJobs.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="available" className="space-y-4">
          {availableJobs.length === 0 ? (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <CheckCircle className="h-16 w-16 text-muted-foreground mb-4" />
                <h2 className="text-xl font-semibold mb-2">No available jobs</h2>
                <p className="text-muted-foreground text-center">
                  Check back later for new service requests in your area.
                </p>
              </CardContent>
            </Card>
          ) : (
            availableJobs
              .sort((a, b) => a.priority - b.priority)
              .map((job) => (
                <Card key={job.id}>
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="flex items-center gap-2">
                          {job.boatName}
                          <Badge variant="outline">Priority {job.priority}</Badge>
                        </CardTitle>
                        <CardDescription>{job.boatType}</CardDescription>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold">${job.totalEstimate}</div>
                        <div className="text-sm text-muted-foreground">Estimated</div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <div className="flex items-center gap-2">
                          <User className="h-4 w-4" />
                          <span>{job.customerName}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Mail className="h-4 w-4" />
                          <span>{job.customerEmail}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Phone className="h-4 w-4" />
                          <span>{job.customerPhone}</span>
                        </div>
                      </div>
                      <div className="space-y-2">
                        <div className="flex items-center gap-2">
                          <MapPin className="h-4 w-4" />
                          <span>{job.location.address}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <MapPin className="h-4 w-4" />
                          <span className="font-mono text-sm">{job.location.what3words}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Clock className="h-4 w-4" />
                          <span>{job.location.distance} miles away</span>
                        </div>
                      </div>
                    </div>

                    <div>
                      <h4 className="font-medium mb-2">Services Requested:</h4>
                      <div className="flex flex-wrap gap-2">
                        {job.services.map((service, index) => (
                          <Badge key={index} variant="secondary">
                            {service}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <div>
                      <h4 className="font-medium mb-2">Preferred Date:</h4>
                      <p>{new Date(job.preferredDate).toLocaleDateString()}</p>
                    </div>

                    {job.notes && (
                      <div>
                        <h4 className="font-medium mb-2">Customer Notes:</h4>
                        <p className="text-sm text-muted-foreground">{job.notes}</p>
                      </div>
                    )}

                    <div className="flex gap-4 pt-4">
                      <Button onClick={() => handleJobAction(job.id, "accept")} className="flex-1">
                        <CheckCircle className="mr-2 h-4 w-4" />
                        Accept Job
                      </Button>
                      <Button variant="outline" onClick={() => handleJobAction(job.id, "decline")} className="flex-1">
                        <XCircle className="mr-2 h-4 w-4" />
                        Decline
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))
          )}
        </TabsContent>

        <TabsContent value="accepted" className="space-y-4">
          {acceptedJobs.length === 0 ? (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Clock className="h-16 w-16 text-muted-foreground mb-4" />
                <h2 className="text-xl font-semibold mb-2">No accepted jobs</h2>
                <p className="text-muted-foreground text-center">
                  Accept jobs from the available tab to see them here.
                </p>
              </CardContent>
            </Card>
          ) : (
            acceptedJobs.map((job) => (
              <Card key={job.id}>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle>{job.boatName}</CardTitle>
                      <CardDescription>{job.boatType}</CardDescription>
                    </div>
                    <Badge>Accepted</Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <User className="h-4 w-4" />
                        <span>{job.customerName}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Phone className="h-4 w-4" />
                        <span>{job.customerPhone}</span>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <MapPin className="h-4 w-4" />
                        <span className="font-mono text-sm">{job.location.what3words}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <DollarSign className="h-4 w-4" />
                        <span>${job.totalEstimate}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-2">
                    {job.services.map((service, index) => (
                      <Badge key={index} variant="secondary">
                        {service}
                      </Badge>
                    ))}
                  </div>

                  <Button className="w-full">Mark as Completed</Button>
                </CardContent>
              </Card>
            ))
          )}
        </TabsContent>

        <TabsContent value="completed" className="space-y-4">
          {completedJobs.length === 0 ? (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <CheckCircle className="h-16 w-16 text-muted-foreground mb-4" />
                <h2 className="text-xl font-semibold mb-2">No completed jobs</h2>
                <p className="text-muted-foreground text-center">Completed jobs will appear here for your records.</p>
              </CardContent>
            </Card>
          ) : (
            completedJobs.map((job) => (
              <Card key={job.id}>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle>{job.boatName}</CardTitle>
                      <CardDescription>{job.boatType}</CardDescription>
                    </div>
                    <Badge variant="secondary">Completed</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex justify-between items-center">
                    <span>{job.customerName}</span>
                    <span className="font-semibold">${job.totalEstimate}</span>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </TabsContent>
      </Tabs>
    </main>
  )
}
