import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { Boat } from "@/lib/types"

interface ProfileTabProps {
  boat: Boat
}

export function ProfileTab({ boat }: ProfileTabProps) {
  return (
    <div className="space-y-6 p-4">
      <Card>
        <CardHeader>
          <CardTitle>Yacht Profile</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Name</h3>
              <p className="text-lg">{boat.name}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Manufacturer</h3>
              <p className="text-lg">{boat.manufacturer}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Model</h3>
              <p className="text-lg">{boat.model}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Year</h3>
              <p className="text-lg">{boat.year}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Type</h3>
              <p className="text-lg">{boat.type}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Designer</h3>
              <p className="text-lg">{boat.designer}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Description</CardTitle>
        </CardHeader>
        <CardContent>
          <p>{boat.description}</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Specifications</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">LOA</h3>
              <p className="text-lg">{boat.hull.length}ft</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Beam</h3>
              <p className="text-lg">{boat.hull.beam}ft</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Draft</h3>
              <p className="text-lg">{boat.hull.draft}ft</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Displacement</h3>
              <p className="text-lg">{boat.hull.displacement} kg</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Ballast</h3>
              <p className="text-lg">{boat.hull.ballast} kg</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Rig Type</h3>
              <p className="text-lg">{boat.rig.type}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
