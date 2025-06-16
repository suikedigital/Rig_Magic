"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Ship, Plus, Settings, Trash2 } from "lucide-react"
import { useAuth } from "@/hooks/use-auth"
import type { Boat } from "@/lib/types"

export default function MyBoatsPage() {
  const { user } = useAuth()
  const router = useRouter()
  const [userBoats, setUserBoats] = useState<Boat[]>([])

  useEffect(() => {
    if (!user) {
      router.push("/")
      return
    }

    // Mock user boats - in real app, fetch from API
    const mockUserBoats: Boat[] = [
      // This would be populated with user's cloned boats
    ]
    setUserBoats(mockUserBoats)
  }, [user, router])

  if (!user) {
    return null
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">My Boats</h1>
          <p className="text-muted-foreground">Manage your cloned boats and configurations</p>
        </div>
        <div className="flex items-center gap-4">
          <Badge variant={user.subscription === "premium" ? "default" : "secondary"}>
            {user.subscription === "premium" ? "Premium" : "Free Plan"}
          </Badge>
          <Button onClick={() => router.push("/")}>
            <Plus className="mr-2 h-4 w-4" />
            Clone New Boat
          </Button>
        </div>
      </div>

      {userBoats.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Ship className="h-16 w-16 text-muted-foreground mb-4" />
            <h2 className="text-xl font-semibold mb-2">No boats yet</h2>
            <p className="text-muted-foreground text-center mb-6">
              Clone your first boat to start customizing your rigging and sail configuration.
            </p>
            <Button onClick={() => router.push("/")}>
              <Plus className="mr-2 h-4 w-4" />
              Browse Boats
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {userBoats.map((boat) => (
            <Card key={boat.id} className="overflow-hidden">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  {boat.name}
                  <div className="flex gap-2">
                    <Button size="sm" variant="outline" onClick={() => router.push(`/my-boats/${boat.id}/edit`)}>
                      <Settings className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="outline">
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </CardTitle>
                <CardDescription>
                  {boat.manufacturer} {boat.model} • {boat.year}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Length:</span>
                    <span>{boat.hull.length}ft</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Type:</span>
                    <span>{boat.type}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Rig:</span>
                    <span>{boat.rig.type}</span>
                  </div>
                </div>
                <Button className="w-full mt-4" onClick={() => router.push(`/my-boats/${boat.id}`)}>
                  View Details
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Subscription Status</CardTitle>
          <CardDescription>
            {user.subscription === "free"
              ? `You have cloned ${user.boatsCloned} of ${user.maxFreeBoats} free boats.`
              : "You have unlimited boat cloning with your premium subscription."}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {user.subscription === "free" && (
            <div className="space-y-4">
              <p className="text-sm text-muted-foreground">
                Upgrade to premium to clone unlimited boats and access advanced features.
              </p>
              <Button onClick={() => router.push("/pricing")}>Upgrade to Premium</Button>
            </div>
          )}
        </CardContent>
      </Card>
    </main>
  )
}
