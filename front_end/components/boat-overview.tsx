"use client"

import { useState } from "react"
import Image from "next/image"
import { useRouter } from "next/navigation"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Copy, Anchor, Ship, Sailboat, Ruler, Wind, Waves, Calendar, Info } from "lucide-react"
import type { Boat } from "@/lib/types"
import { ProfileTab } from "@/components/tabs/profile-tab"
import { HullTab } from "@/components/tabs/hull-tab"
import { RigTab } from "@/components/tabs/rig-tab"
import { SailDataTab } from "@/components/tabs/sail-data-tab"
import { SailsTab } from "@/components/tabs/sails-tab"
import { RopesTab } from "@/components/tabs/ropes-tab"
import { useToast } from "@/hooks/use-toast"
import { useAuth } from "@/hooks/use-auth"
import { AuthDialog } from "@/components/auth-dialog"

interface BoatOverviewProps {
  boat: Boat
}

export function BoatOverview({ boat }: BoatOverviewProps) {
  const router = useRouter()
  const { toast } = useToast()
  const [activeTab, setActiveTab] = useState("profile")
  const { user } = useAuth()
  const [showAuthDialog, setShowAuthDialog] = useState(false)

  const handleClone = () => {
    if (!user) {
      setShowAuthDialog(true)
      return
    }

    if (user.subscription === "free" && user.boatsCloned >= user.maxFreeBoats) {
      toast({
        title: "Upgrade required",
        description: "You've reached your free boat limit. Upgrade to clone more boats.",
        variant: "destructive",
      })
      router.push("/pricing")
      return
    }

    router.push(`/boats/${boat.id}/clone`)
  }

  const handleBookService = () => {
    router.push(`/boats/${boat.id}/services`)
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row gap-6 items-start">
        <div className="w-full md:w-1/2 relative rounded-lg overflow-hidden">
          <div className="aspect-[4/3] relative">
            <Image src={boat.imageUrl || "/placeholder.svg"} alt={boat.name} fill className="object-cover" />
          </div>
        </div>

        <div className="w-full md:w-1/2 space-y-4">
          <div>
            <h1 className="text-3xl font-bold">{boat.name}</h1>
            <p className="text-xl text-muted-foreground">
              {boat.manufacturer} {boat.model}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Card>
              <CardContent className="p-4 flex items-center gap-3">
                <Ship className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Type</p>
                  <p className="text-lg">{boat.type}</p>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4 flex items-center gap-3">
                <Ruler className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Length</p>
                  <p className="text-lg">{boat.hull.length}ft</p>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4 flex items-center gap-3">
                <Calendar className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Year</p>
                  <p className="text-lg">{boat.year}</p>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4 flex items-center gap-3">
                <Sailboat className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Rig Type</p>
                  <p className="text-lg">{boat.rig.type}</p>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 pt-4">
            <Button size="lg" className="flex-1 gap-2" onClick={handleClone}>
              <Copy className="h-5 w-5" />
              Clone This Yacht
            </Button>

            <Button variant="outline" size="lg" className="flex-1" onClick={handleBookService}>
              Book Services
            </Button>
          </div>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid grid-cols-3 md:grid-cols-6 w-full">
          <TabsTrigger value="profile" className="flex items-center gap-2">
            <Info className="h-4 w-4" />
            <span className="hidden sm:inline">Profile</span>
          </TabsTrigger>
          <TabsTrigger value="hull" className="flex items-center gap-2">
            <Ship className="h-4 w-4" />
            <span className="hidden sm:inline">Hull</span>
          </TabsTrigger>
          <TabsTrigger value="rig" className="flex items-center gap-2">
            <Sailboat className="h-4 w-4" />
            <span className="hidden sm:inline">Rig Specs</span>
          </TabsTrigger>
          <TabsTrigger value="saildata" className="flex items-center gap-2">
            <Wind className="h-4 w-4" />
            <span className="hidden sm:inline">Sail Data</span>
          </TabsTrigger>
          <TabsTrigger value="sails" className="flex items-center gap-2">
            <Waves className="h-4 w-4" />
            <span className="hidden sm:inline">Sails</span>
          </TabsTrigger>
          <TabsTrigger value="ropes" className="flex items-center gap-2">
            <Anchor className="h-4 w-4" />
            <span className="hidden sm:inline">Ropes</span>
          </TabsTrigger>
        </TabsList>

        <TabsContent value="profile">
          <ProfileTab boat={boat} />
        </TabsContent>

        <TabsContent value="hull">
          <HullTab hull={boat.hull} />
        </TabsContent>

        <TabsContent value="rig">
          <RigTab rig={boat.rig} />
        </TabsContent>

        <TabsContent value="saildata">
          <SailDataTab sailData={boat.sailData} />
        </TabsContent>

        <TabsContent value="sails">
          <SailsTab sails={boat.sails} />
        </TabsContent>

        <TabsContent value="ropes">
          <RopesTab ropes={boat.ropes} />
        </TabsContent>
      </Tabs>
      <AuthDialog
        open={showAuthDialog}
        onOpenChange={setShowAuthDialog}
        onSuccess={() => {
          setShowAuthDialog(false)
          router.push(`/boats/${boat.id}/clone`)
        }}
      />
    </div>
  )
}
