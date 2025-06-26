"use client"

import React from "react"
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
import { User, Settings, LogOut, Ship, LogIn } from "lucide-react"
import { useAuth } from "@/hooks/use-auth"
import { CartButton } from "@/components/cart-button"
import { FcGoogle } from "react-icons/fc"
import { FaApple } from "react-icons/fa"

type NavigationProps = {
  centerContent?: React.ReactNode
}

export function Navigation({ centerContent }: NavigationProps) {
  const { user, signIn, signOut } = useAuth()
  const router = useRouter()
  const pathname = usePathname()

  return (
    <nav className="fixed top-0 left-0 w-full z-50 pointer-events-none">
      <div className="flex items-start justify-between w-full px-6 py-4 pointer-events-auto">
        {/* Left: Logo Bar */}
        <div className="glass bg-card border rounded-full px-6 py-2 shadow-lg flex items-center">
          <Link href="/" className="font-bold italic text-2xl tracking-tight text-primary">
            Rig Magic
          </Link>
        </div>
        {/* Center: Custom Content */}
        <div className="flex-1 flex justify-center items-center">
          {centerContent}
        </div>
        {/* Right: Actions Bar */}
        <div className="glass bg-card border rounded-full px-4 py-2 shadow-lg flex items-center space-x-4">
          {user && (
            <Link href="/my-boats">
              <Button variant="ghost" className="flex items-center gap-2">
                <Ship className="h-4 w-4" />
              </Button>
            </Link>
          )}
          <CartButton />
          {user ? (
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
              <DropdownMenuContent className="w-[320px] mt-2 glass bg-card border rounded-xl shadow-lg" align="end" forceMount>
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
          ) : (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="h-8 w-8 p-0 flex items-center justify-center">
                  <LogIn className="h-6 w-6" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent
                className="glass bg-card border rounded-xl shadow-lg mt-2 w-full min-w-[48px] max-w-[160px] px-2 py-2 flex flex-col items-stretch"
                align="end"
                sideOffset={8}
              >
                <DropdownMenuItem
                  onClick={() => signIn("google", { callbackUrl: window.location.origin })}
                  className="p-0 m-0 bg-transparent hover:bg-muted rounded-full flex items-center justify-center"
                  asChild
                >
                  <Button variant="ghost" className="h-8 w-full p-0 flex items-center justify-center">
                    <FcGoogle className="h-6 w-6" />
                  </Button>
                </DropdownMenuItem>
                <DropdownMenuItem
                  onClick={() => signIn("apple", { callbackUrl: window.location.origin })}
                  className="p-0 m-0 bg-transparent hover:bg-muted rounded-full flex items-center justify-center"
                  asChild
                >
                  <Button variant="ghost" className="h-8 w-full p-0 flex items-center justify-center">
                    <FaApple className="h-6 w-6 text-black" />
                  </Button>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          )}
        </div>
      </div>
    </nav>
  )
}