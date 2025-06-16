"use client"

import { useSession, signIn } from "next-auth/react"
import { useEffect } from "react"

export default function CloneYachtPage({ params }: { params: { yachtId: string } }) {
  const { status } = useSession()

  useEffect(() => {
    if (status === "unauthenticated") {
      signIn(undefined, { callbackUrl: window.location.href })
    }
  }, [status])

  if (status === "loading") return <div>Loading...</div>

  // ...existing clone yacht creation UI...
  return <div>Clone Yacht Page for {params.yachtId}</div>
}
