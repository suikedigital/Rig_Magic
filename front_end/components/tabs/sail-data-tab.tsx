import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { SailData } from "@/lib/types"

interface SailDataTabProps {
  sailData: SailData
}

export function SailDataTab({ sailData }: SailDataTabProps) {
  return (
    <div className="space-y-6 p-4">
      <Card>
        <CardHeader>
          <CardTitle>Sail Measurements</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">I (Foretriangle Height)</h3>
              <p className="text-lg">{sailData.I}ft</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">J (Foretriangle Base)</h3>
              <p className="text-lg">{sailData.J}ft</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">P (Mainsail Luff)</h3>
              <p className="text-lg">{sailData.P}ft</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">E (Mainsail Foot)</h3>
              <p className="text-lg">{sailData.E}ft</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Sail Areas</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Mainsail Area</h3>
              <p className="text-lg">{sailData.mainsailArea} sq ft</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Foretriangle Area</h3>
              <p className="text-lg">{sailData.foretriangle} sq ft</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Total Sail Area (100% Jib)</h3>
              <p className="text-lg">{sailData.totalSailArea100} sq ft</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Total Sail Area (150% Genoa)</h3>
              <p className="text-lg">{sailData.totalSailArea150} sq ft</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Spinnaker Area</h3>
              <p className="text-lg">{sailData.spinnakerArea} sq ft</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Downwind Sail Area</h3>
              <p className="text-lg">{sailData.downwindSailArea} sq ft</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Performance Ratios</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Sail Area/Displacement Ratio</h3>
              <p className="text-lg">{sailData.sailAreaDisplacementRatio}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Displacement/Length Ratio</h3>
              <p className="text-lg">{sailData.displacementLengthRatio}</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Ballast/Displacement Ratio</h3>
              <p className="text-lg">{sailData.ballastDisplacementRatio}%</p>
            </div>
            <div>
              <h3 className="font-medium text-sm text-muted-foreground">Capsize Screening Value</h3>
              <p className="text-lg">{sailData.capsizeScreeningValue}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
