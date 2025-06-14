"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import type { Sail } from "@/lib/types"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

interface SailsTabProps {
  sails: Sail[]
}

export function SailsTab({ sails }: SailsTabProps) {
  const [selectedSail, setSelectedSail] = useState<Sail | null>(null)

  return (
    <div className="space-y-6 p-4">
      <Card>
        <CardHeader>
          <CardTitle>Sail Inventory</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Type</TableHead>
                <TableHead>Material</TableHead>
                <TableHead>Area (sq ft)</TableHead>
                <TableHead>Condition</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sails.map((sail, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{sail.type}</TableCell>
                  <TableCell>{sail.material}</TableCell>
                  <TableCell>{sail.area}</TableCell>
                  <TableCell>{sail.condition}/10</TableCell>
                  <TableCell>
                    <Dialog>
                      <DialogTrigger asChild>
                        <Button variant="outline" size="sm" onClick={() => setSelectedSail(sail)}>
                          Details
                        </Button>
                      </DialogTrigger>
                      <DialogContent className="sm:max-w-[500px]">
                        <DialogHeader>
                          <DialogTitle>{sail.type} Details</DialogTitle>
                        </DialogHeader>
                        <div className="grid gap-4 py-4">
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <h3 className="font-medium text-sm text-muted-foreground">Type</h3>
                              <p className="text-lg">{sail.type}</p>
                            </div>
                            <div>
                              <h3 className="font-medium text-sm text-muted-foreground">Material</h3>
                              <p className="text-lg">{sail.material}</p>
                            </div>
                            <div>
                              <h3 className="font-medium text-sm text-muted-foreground">Area</h3>
                              <p className="text-lg">{sail.area} sq ft</p>
                            </div>
                            <div>
                              <h3 className="font-medium text-sm text-muted-foreground">Condition</h3>
                              <p className="text-lg">{sail.condition}/10</p>
                            </div>
                            <div>
                              <h3 className="font-medium text-sm text-muted-foreground">Year</h3>
                              <p className="text-lg">{sail.year}</p>
                            </div>
                            <div>
                              <h3 className="font-medium text-sm text-muted-foreground">Manufacturer</h3>
                              <p className="text-lg">{sail.manufacturer}</p>
                            </div>
                          </div>
                          <div>
                            <h3 className="font-medium text-sm text-muted-foreground">Notes</h3>
                            <p>{sail.notes}</p>
                          </div>
                          <div>
                            <h3 className="font-medium text-sm text-muted-foreground">Recommended Wind Range</h3>
                            <p>{sail.windRange} knots</p>
                          </div>
                        </div>
                      </DialogContent>
                    </Dialog>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Sail Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="mb-4">Based on your yacht's specifications, here are the recommended sail types and sizes:</p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardContent className="p-4">
                <h3 className="font-semibold mb-2">Mainsail</h3>
                <p className="text-sm text-muted-foreground mb-2">
                  Recommended size: {Math.round(sails.find((s) => s.type === "Mainsail")?.area || 0) + 5} sq ft
                </p>
                <p className="text-sm">
                  Full-battened dacron mainsail with 2 reefs for cruising or laminate for racing.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <h3 className="font-semibold mb-2">Genoa</h3>
                <p className="text-sm text-muted-foreground mb-2">
                  Recommended size: {Math.round(sails.find((s) => s.type === "Genoa")?.area || 0) + 10} sq ft
                </p>
                <p className="text-sm">135% overlap genoa for all-around performance.</p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <h3 className="font-semibold mb-2">Spinnaker</h3>
                <p className="text-sm text-muted-foreground mb-2">
                  Recommended size: {Math.round(sails.find((s) => s.type === "Spinnaker")?.area || 0) + 20} sq ft
                </p>
                <p className="text-sm">Asymmetric spinnaker for easier handling and downwind performance.</p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <h3 className="font-semibold mb-2">Storm Jib</h3>
                <p className="text-sm text-muted-foreground mb-2">
                  Recommended size: {Math.round((sails.find((s) => s.type === "Jib")?.area || 0) * 0.4)} sq ft
                </p>
                <p className="text-sm">Heavy-duty storm jib for severe weather conditions.</p>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
