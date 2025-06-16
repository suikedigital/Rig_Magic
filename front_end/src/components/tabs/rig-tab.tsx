"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"
import type { Rig } from "@/lib/types"
import { useAuth } from "@/hooks/use-auth"
import { Lock } from "lucide-react"

interface RigTabProps {
  rig: Rig
}

export function RigTab({ rig }: RigTabProps) {
  const router = useRouter()
  const { user } = useAuth()

  return (
    <div className="space-y-6 p-4">
      <Card>
        <CardHeader>
          <CardTitle>Rig Specifications</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Rig Type</h3>
              <p className="text-lg">{rig.type}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Mast Type</h3>
              <p className="text-lg">{rig.mastType}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Mast Height</h3>
              <p className="text-lg">{rig.mastHeight}ft</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Mast Material</h3>
              <p className="text-lg">{rig.mastMaterial}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Boom Length</h3>
              <p className="text-lg">{rig.boomLength}ft</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Boom Material</h3>
              <p className="text-lg">{rig.boomMaterial}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Standing Rigging</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {user ? (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h3 className="font-medium text-sm text-muted-foreground">Forestay Material</h3>
                  <p className="text-lg">{rig.standingRigging.forestay.material}</p>
                </div>
                <div>
                  <h3 className="font-medium text-sm text-muted-foreground">Forestay Diameter</h3>
                  <p className="text-lg">{rig.standingRigging.forestay.diameter}mm</p>
                </div>
                <div>
                  <h3 className="font-medium text-sm text-muted-foreground">Backstay Material</h3>
                  <p className="text-lg">{rig.standingRigging.backstay.material}</p>
                </div>
                <div>
                  <h3 className="font-medium text-sm text-muted-foreground">Backstay Diameter</h3>
                  <p className="text-lg">{rig.standingRigging.backstay.diameter}mm</p>
                </div>
                <div>
                  <h3 className="font-medium text-sm text-muted-foreground">Shrouds Material</h3>
                  <p className="text-lg">{rig.standingRigging.shrouds.material}</p>
                </div>
                <div>
                  <h3 className="font-medium text-sm text-muted-foreground">Shrouds Diameter</h3>
                  <p className="text-lg">{rig.standingRigging.shrouds.diameter}mm</p>
                </div>
              </div>
              <Button variant="outline" className="mt-4" onClick={() => router.push(`/rigging/standing`)}>
                View Detailed Standing Rigging
              </Button>
            </>
          ) : (
            <div className="text-center py-8 space-y-4">
              <Lock className="h-12 w-12 mx-auto text-muted-foreground" />
              <div>
                <h3 className="text-lg font-semibold">Detailed Rigging Information</h3>
                <p className="text-muted-foreground">Sign in to view complete rigging specifications and details</p>
              </div>
              <div className="grid grid-cols-2 gap-4 opacity-50">
                <div className="bg-muted p-3 rounded">
                  <div className="h-4 bg-muted-foreground/20 rounded mb-2"></div>
                  <div className="h-6 bg-muted-foreground/20 rounded"></div>
                </div>
                <div className="bg-muted p-3 rounded">
                  <div className="h-4 bg-muted-foreground/20 rounded mb-2"></div>
                  <div className="h-6 bg-muted-foreground/20 rounded"></div>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Running Rigging</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {user ? (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h3 className="font-medium text-sm text-muted-foreground">Halyards</h3>
                  <p className="text-lg">{rig.runningRigging.halyards.count} lines</p>
                </div>
                <div>
                  <h3 className="font-medium text-sm text-muted-foreground">Halyard Material</h3>
                  <p className="text-lg">{rig.runningRigging.halyards.material}</p>
                </div>
                <div>
                  <h3 className="font-medium text-sm text-muted-foreground">Sheets</h3>
                  <p className="text-lg">{rig.runningRigging.sheets.count} lines</p>
                </div>
                <div>
                  <h3 className="font-medium text-sm text-muted-foreground">Sheet Material</h3>
                  <p className="text-lg">{rig.runningRigging.sheets.material}</p>
                </div>
              </div>
              <Button variant="outline" className="mt-4" onClick={() => router.push(`/rigging/running`)}>
                View Detailed Running Rigging
              </Button>
            </>
          ) : (
            <div className="text-center py-8 space-y-4">
              <Lock className="h-12 w-12 mx-auto text-muted-foreground" />
              <div>
                <h3 className="text-lg font-semibold">Running Rigging Details</h3>
                <p className="text-muted-foreground">Sign in to access detailed running rigging specifications</p>
              </div>
              <div className="grid grid-cols-2 gap-4 opacity-50">
                <div className="bg-muted p-3 rounded">
                  <div className="h-4 bg-muted-foreground/20 rounded mb-2"></div>
                  <div className="h-6 bg-muted-foreground/20 rounded"></div>
                </div>
                <div className="bg-muted p-3 rounded">
                  <div className="h-4 bg-muted-foreground/20 rounded mb-2"></div>
                  <div className="h-6 bg-muted-foreground/20 rounded"></div>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
