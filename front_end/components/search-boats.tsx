"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Search } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export function SearchBoats() {
  const router = useRouter()
  const [searchQuery, setSearchQuery] = useState("")
  const [boatType, setBoatType] = useState("all")

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    router.push(`/search?query=${encodeURIComponent(searchQuery)}&boat_type=${boatType}`)
  }

  return (
    <div className="bg-card rounded-xl p-6 shadow-sm border">
      <h2 className="text-xl font-semibold mb-4">Find Your Yacht</h2>
      <form onSubmit={handleSearch} className="space-y-4">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <Input
              placeholder="Search by yacht name, model, or manufacturer..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full"
            />
          </div>
          <div className="w-full md:w-48">
            <Select value={boatType} onValueChange={setBoatType}>
              <SelectTrigger>
                <SelectValue placeholder="Boat Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                <SelectItem value="sailboat">Sailboat</SelectItem>
                <SelectItem value="catamaran">Catamaran</SelectItem>
                <SelectItem value="yacht">Yacht</SelectItem>
                <SelectItem value="cruiser">Cruiser</SelectItem>
                <SelectItem value="racer">Racer</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Button type="submit" className="w-full md:w-auto">
            <Search className="mr-2 h-4 w-4" />
            Search
          </Button>
        </div>
      </form>
    </div>
  )
}
