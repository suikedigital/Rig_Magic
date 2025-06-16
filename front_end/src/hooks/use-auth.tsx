"use client"
import { useSession, signIn, signOut } from "next-auth/react"

export function useAuth() {
  const { data: session, status } = useSession()
  // Wrap signOut to always use current page as callbackUrl
  const signOutWithCallback = (options = {}) => {
    return signOut({ callbackUrl: window.location.href, ...options })
  }
  return {
    user: session?.user ?? null,
    status,
    signIn,
    signOut: signOutWithCallback,
  }
}
