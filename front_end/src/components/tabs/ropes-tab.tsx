import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { Rope } from "@/lib/types"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import logger from '../../logger';

interface PossibleRope {
  rope_type: string
}

interface RopesTabProps {
  ropes: Rope[] | PossibleRope[]
  isBaseYacht?: boolean
}

export function RopesTab({ ropes, isBaseYacht = false }: RopesTabProps) {
  if (isBaseYacht) {
    logger.info('[RopesTab] isBaseYacht:', { isBaseYacht, ropes });
    return (
      <div className="space-y-6 p-4">
        <Card>
          <CardHeader>
            <CardTitle>Base Ropes Inventory</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Type</TableHead>
                  {/* Optionally add Area or Length if available in the future */}
                </TableRow>
              </TableHeader>
              <TableBody>
                {(ropes as PossibleRope[]).map((rope, index) => {
                  // Insert space before 'Halyard' if present, and between camel case words
                  let displayType = rope.rope_type
                  displayType = displayType.replace(/([a-z])([A-Z])/g, '$1 $2')
                  displayType = displayType.replace(/ Halyard$/, ' Halyard') // ensure space before Halyard
                  return (
                    <TableRow key={index}>
                      <TableCell className="font-medium">{displayType}</TableCell>
                    </TableRow>
                  )
                })}
              </TableBody>
            </Table>
            <div className="mt-4 text-muted-foreground text-sm">
              To see full rope details and add your own, <b>sign in and clone this boat</b>.
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  // Only cast to Rope[] for non-base yachts
  const runningRigging = (ropes as Rope[]).filter((rope) => rope.category === "Running Rigging")
  const controlLines = (ropes as Rope[]).filter((rope) => rope.category === "Control Lines")
  const dockingLines = (ropes as Rope[]).filter((rope) => rope.category === "Docking Lines")

  return (
    <div className="space-y-6 p-4">
      <Card>
        <CardHeader>
          <CardTitle>Running Rigging</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Material</TableHead>
                <TableHead>Diameter</TableHead>
                <TableHead>Length</TableHead>
                <TableHead>Condition</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {runningRigging.map((rope, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{rope.name}</TableCell>
                  <TableCell>{rope.material}</TableCell>
                  <TableCell>{rope.diameter}mm</TableCell>
                  <TableCell>{rope.length}m</TableCell>
                  <TableCell>{rope.condition}/10</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Control Lines</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Material</TableHead>
                <TableHead>Diameter</TableHead>
                <TableHead>Length</TableHead>
                <TableHead>Condition</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {controlLines.map((rope, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{rope.name}</TableCell>
                  <TableCell>{rope.material}</TableCell>
                  <TableCell>{rope.diameter}mm</TableCell>
                  <TableCell>{rope.length}m</TableCell>
                  <TableCell>{rope.condition}/10</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Docking Lines</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Material</TableHead>
                <TableHead>Diameter</TableHead>
                <TableHead>Length</TableHead>
                <TableHead>Condition</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {dockingLines.map((rope, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{rope.name}</TableCell>
                  <TableCell>{rope.material}</TableCell>
                  <TableCell>{rope.diameter}mm</TableCell>
                  <TableCell>{rope.length}m</TableCell>
                  <TableCell>{rope.condition}/10</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Rope Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="mb-4">Based on your yacht's specifications, here are our rope recommendations:</p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardContent className="p-4">
                <h3 className="font-semibold mb-2">Halyards</h3>
                <p className="text-sm">Dyneema core with polyester cover, 10-12mm diameter depending on load.</p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <h3 className="font-semibold mb-2">Sheets</h3>
                <p className="text-sm">Polyester double braid, 10-14mm diameter depending on sail size.</p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <h3 className="font-semibold mb-2">Control Lines</h3>
                <p className="text-sm">Polyester or Dyneema blend, 8-10mm diameter for optimal handling.</p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <h3 className="font-semibold mb-2">Docking Lines</h3>
                <p className="text-sm">Nylon three-strand or double braid, 14-16mm diameter for shock absorption.</p>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
