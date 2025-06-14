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
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Name</h3>
              <p className="text-lg">{boat.name}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Make</h3>
              <p className="text-lg">{boat.yacht_class}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Model</h3>
              <p className="text-lg">{boat.model}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Version</h3>
              <p className="text-lg">{boat.version}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Type</h3>
              <p className="text-lg">{boat.type}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
         <CardHeader>
          <CardTitle>Design</CardTitle>
        </CardHeader>
      <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Designer</h3>
              <p className="text-lg">{boat.designer}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Builder</h3>
              <p className="text-lg">{boat.builder}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Year Introduced</h3>
              <p className="text-lg">{boat.year_introduced}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Production started</h3>
              <p className="text-lg">{boat.year_introduced}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Production ended</h3>
              <p className="text-lg">{boat.year_introduced}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Type</h3>
              <p className="text-lg">{boat.type}</p>
            </div>
          </div>
        </CardContent>
      </Card>
      

      <Card>
        <CardHeader>
          <CardTitle>Notes</CardTitle>
        </CardHeader>
        <CardContent>
          <p>{boat.notes}</p>
        </CardContent>
      </Card>
    </div>
  )
}
