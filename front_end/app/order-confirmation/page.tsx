"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { CheckCircle, ArrowRight } from "lucide-react"

export default function OrderConfirmationPage() {
  const router = useRouter()

  // Generate a random order number
  const orderNumber = `RM-${Math.floor(100000 + Math.random() * 900000)}`

  useEffect(() => {
    // If user refreshes this page, redirect to home
    const handleBeforeUnload = () => {
      sessionStorage.setItem("orderConfirmed", "true")
    }

    window.addEventListener("beforeunload", handleBeforeUnload)

    const confirmed = sessionStorage.getItem("orderConfirmed")
    if (confirmed) {
      router.push("/")
    }

    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload)
    }
  }, [router])

  return (
    <main className="container mx-auto px-4 py-12">
      <Card className="max-w-2xl mx-auto">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <CheckCircle className="h-16 w-16 text-green-500" />
          </div>
          <CardTitle className="text-2xl">Order Confirmed!</CardTitle>
          <CardDescription>Thank you for your purchase</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="text-center">
            <p className="text-lg">Your order number is:</p>
            <p className="text-2xl font-bold">{orderNumber}</p>
          </div>

          <div className="bg-muted p-4 rounded-md">
            <p className="font-medium mb-2">What happens next?</p>
            <ol className="list-decimal list-inside space-y-2 text-sm">
              <li>You will receive an order confirmation email with details of your purchase.</li>
              <li>Our rigging specialists will review your order and may contact you to confirm measurements.</li>
              <li>Your custom rigging will be manufactured to your specifications.</li>
              <li>We'll notify you when your order ships with tracking information.</li>
            </ol>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button onClick={() => router.push("/my-boats")}>View My Boats</Button>
            <Button variant="outline" onClick={() => router.push("/")}>
              Continue Shopping
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </main>
  )
}
