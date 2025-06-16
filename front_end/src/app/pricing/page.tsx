"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Check, Star } from "lucide-react"
import { useAuth } from "@/hooks/use-auth"
import { useToast } from "@/hooks/use-toast"

export default function PricingPage() {
  const { user } = useAuth()
  const router = useRouter()
  const { toast } = useToast()
  const [isUpgrading, setIsUpgrading] = useState(false)

  const handleUpgrade = async () => {
    setIsUpgrading(true)

    // Simulate payment processing
    await new Promise((resolve) => setTimeout(resolve, 2000))

    toast({
      title: "Upgrade successful!",
      description: "Welcome to Rig Magic Premium. You now have unlimited boat cloning.",
    })

    setIsUpgrading(false)
    router.push("/my-boats")
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">Choose Your Plan</h1>
        <p className="text-xl text-muted-foreground">Unlock the full potential of yacht rigging management</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        <Card className="relative">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              Free Plan
              {user?.subscription === "free" && <Badge>Current Plan</Badge>}
            </CardTitle>
            <CardDescription>Perfect for getting started</CardDescription>
            <div className="text-3xl font-bold">
              $0<span className="text-lg font-normal">/month</span>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <ul className="space-y-3">
              <li className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                <span>1 free boat clone</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                <span>Basic boat specifications</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                <span>Service booking</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                <span>Community support</span>
              </li>
            </ul>
            <Button variant="outline" className="w-full" disabled={user?.subscription === "free"}>
              {user?.subscription === "free" ? "Current Plan" : "Get Started"}
            </Button>
          </CardContent>
        </Card>

        <Card className="relative border-primary">
          <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
            <Badge className="bg-primary text-primary-foreground">
              <Star className="h-3 w-3 mr-1" />
              Most Popular
            </Badge>
          </div>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              Premium Plan
              {user?.subscription === "premium" && <Badge>Current Plan</Badge>}
            </CardTitle>
            <CardDescription>For serious yacht enthusiasts</CardDescription>
            <div className="text-3xl font-bold">
              $29<span className="text-lg font-normal">/month</span>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <ul className="space-y-3">
              <li className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                <span>Unlimited boat cloning</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                <span>Advanced rigging details</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                <span>Custom rope packages</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                <span>Priority service booking</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                <span>Performance analytics</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                <span>Expert support</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                <span>API access</span>
              </li>
            </ul>
            <Button
              className="w-full"
              onClick={handleUpgrade}
              disabled={isUpgrading || user?.subscription === "premium"}
            >
              {isUpgrading ? "Processing..." : user?.subscription === "premium" ? "Current Plan" : "Upgrade Now"}
            </Button>
          </CardContent>
        </Card>
      </div>

      <div className="mt-12 text-center">
        <h2 className="text-2xl font-bold mb-4">Frequently Asked Questions</h2>
        <div className="max-w-2xl mx-auto space-y-4">
          <Card>
            <CardContent className="p-6">
              <h3 className="font-semibold mb-2">Can I cancel anytime?</h3>
              <p className="text-muted-foreground">
                Yes, you can cancel your subscription at any time. Your premium features will remain active until the
                end of your billing period.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <h3 className="font-semibold mb-2">What happens to my boats if I downgrade?</h3>
              <p className="text-muted-foreground">
                You'll keep all your cloned boats, but you won't be able to clone new ones until you upgrade again or
                delete existing boats.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <h3 className="font-semibold mb-2">Do you offer refunds?</h3>
              <p className="text-muted-foreground">
                We offer a 30-day money-back guarantee for all premium subscriptions. Contact support for assistance.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  )
}
