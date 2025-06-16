import { useRouter } from "next/navigation"
import { useAuth } from "@/hooks/use-auth"
import { Button } from "@/components/ui/button"

export function CloneButton({ yachtId }: { yachtId: string }) {
  const { user, signIn } = useAuth()
  const router = useRouter()

  const handleClone = () => {
    const cloneUrl = `/clone-yacht/${yachtId}`
    if (user) {
      router.push(cloneUrl)
    } else {
      signIn(undefined, { callbackUrl: window.location.origin + cloneUrl })
    }
  }

  return (
    <Button onClick={handleClone}>
      Clone This Yacht
    </Button>
  )
}
