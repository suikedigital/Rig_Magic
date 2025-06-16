import { useSession, signIn, signOut } from "next-auth/react"

export function useAuth() {
  const { data: session, status } = useSession()
  return {
    user: session?.user ?? null,
    status,
    signIn,
    signOut,
  }
}
