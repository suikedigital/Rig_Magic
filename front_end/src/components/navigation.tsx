"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter, usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { User, Settings, LogOut, Ship } from "lucide-react"
import { useAuth } from "@/hooks/use-auth"
import { CartButton } from "@/components/cart-button"

export function Navigation() {
  const { user, signIn, signOut } = useAuth()
  const router = useRouter()
  const pathname = usePathname()

  return (
    <>
      <div className="pt-5 px-25">
        <nav
          className="
              max-w-6xl mx-auto
              rounded-full
              border
              bg-card
              backdrop-blur 
              shadow-lg
              overflow-hidden
            "
        >
          <div className="container mx-auto px-4">
            <div className="flex h-16 items-center justify-between relative">
              {/* Left side navigation */}
              <div className="flex items-center space-x-4">
                {user && (
                  <Link href="/my-boats">
                    <Button variant="ghost" className="flex items-center gap-2">
                      <Ship className="h-4 w-4" />
                      My Boats
                    </Button>
                  </Link>
                )}
              </div>

              {/* Centered Logo */}
              <Link href="/" className="absolute left-1/2 transform -translate-x-1/2 flex items-center">
                <img src="/Logo.png" alt="Rig Magic Logo" className="h-12 w-auto" />
              </Link>

              {/* Right side navigation */}
              <div className="flex items-center space-x-4">
                {user ? (
                  <>
                    <CartButton />

                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                          <Avatar className="h-8 w-8">
                            <AvatarImage src={user.image ?? "/placeholder.svg"} alt={user.name ?? "User"} />
                            <AvatarFallback>
                              {(user.name ?? "U")
                                .split(" ")
                                .map((n) => n[0])
                                .join("")}
                            </AvatarFallback>
                          </Avatar>
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent className="w-56" align="end" forceMount>
                        <DropdownMenuLabel className="font-normal">
                          <div className="flex flex-col space-y-1">
                            <p className="text-sm font-medium leading-none">{user.name}</p>
                            <p className="text-xs leading-none text-muted-foreground">{user.email}</p>
                          </div>
                        </DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem onClick={() => router.push("/profile")}>
                          <User className="mr-2 h-4 w-4" />
                          <span>Profile</span>
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => router.push("/settings")}>
                          <Settings className="mr-2 h-4 w-4" />
                          <span>Settings</span>
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem onClick={() => signOut()}>
                          <LogOut className="mr-2 h-4 w-4" />
                          <span>Log out</span>
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </>
                ) : (
                  <>
                    <CartButton />
                    <Button onClick={() => signIn(undefined, { callbackUrl: window.location.origin })}>Sign In</Button>
                  </>
                )}
              </div>
            </div>
          </div>
        </nav>
      </div>
    </>
  )
}
