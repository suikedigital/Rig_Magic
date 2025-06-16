import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { Hull } from "@/lib/types"

interface HullTabProps {
  hull: Hull
}

export function HullTab({ hull }: HullTabProps) {
  return (
    <div className="space-y-6 p-4">
      <Card>
        <CardHeader>
          <CardTitle>Hull Specifications</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Length Overall (LOA)</h3>
              <p className="text-lg">{hull.loa} mts</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Length Waterline (LWL)</h3>
              <p className="text-lg">{hull.lwl} mts</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Beam</h3>
              <p className="text-lg">{hull.beam} mts</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Draft</h3>
              <p className="text-lg">{hull.draft} mts</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Displacement</h3>
              <p className="text-lg">{hull.displacement} kg</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Ballast</h3>
              <p className="text-lg">{hull.ballast} kg</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Hull Type</h3>
              <p className="text-lg">{hull.hullType}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Hull Material</h3>
              <p className="text-lg">{hull.construction}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Keel Specifications</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Type</h3>
              <p className="text-lg">{hull.keelType}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Rudder Specifications</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Rudder Type</h3>
              <p className="text-lg">{hull.rudderType}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Performance Characteristics</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Ballast Ratio</h3>
              <p className="text-lg">{hull.ballastRatio}%</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Displacement/Length Ratio</h3>
              <p className="text-lg">{hull.displacementLengthRatio}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Sail Area/Displacement Ratio</h3>
              <p className="text-lg">{hull.sailAreaDisplacementRatio}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Capsize Screening Value</h3>
              <p className="text-lg">{hull.capsizeScreeningValue}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
