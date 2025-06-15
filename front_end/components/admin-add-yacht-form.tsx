"use client"

import React, { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"

const initialProfile = {
  name: "",
  yacht_class: "",
  model: "",
  version: "",
  builder: "",
  designer: "",
  year_introduced: "",
  production_start: "",
  production_end: "",
  country_of_origin: "",
  notes: "",
}
const initialHull = {
  hull_type: "",
  loa: "",
  lwl: "",
  beam: "",
  displacement: "",
  ballast: "",
  construction: "",
}
const initialKeel = { keel_type: "", draft: "" }
const initialRudder = { rudder_type: "" }
const initialSaildata = { i: "", j: "", p: "", e: "" }

export function AdminAddYachtForm() {
  const [profile, setProfile] = useState(initialProfile)
  const [hull, setHull] = useState(initialHull)
  const [keel, setKeel] = useState(initialKeel)
  const [rudder, setRudder] = useState(initialRudder)
  const [saildata, setSaildata] = useState(initialSaildata)
  const [possibleSails, setPossibleSails] = useState<string[]>([])
  const [possibleRopes, setPossibleRopes] = useState<string[]>([])
  const [sailInput, setSailInput] = useState("")
  const [ropeInput, setRopeInput] = useState("")
  const [submitting, setSubmitting] = useState(false)
  const [result, setResult] = useState<string|null>(null)

  // Handlers
  const handleProfileChange = (e: React.ChangeEvent<HTMLInputElement>) => setProfile({ ...profile, [e.target.name]: e.target.value })
  const handleHullChange = (e: React.ChangeEvent<HTMLInputElement>) => setHull({ ...hull, [e.target.name]: e.target.value })
  const handleKeelChange = (e: React.ChangeEvent<HTMLInputElement>) => setKeel({ ...keel, [e.target.name]: e.target.value })
  const handleRudderChange = (e: React.ChangeEvent<HTMLInputElement>) => setRudder({ ...rudder, [e.target.name]: e.target.value })
  const handleSaildataChange = (e: React.ChangeEvent<HTMLInputElement>) => setSaildata({ ...saildata, [e.target.name]: e.target.value })

  // Add/remove sails/ropes
  const addSail = () => {
    if (sailInput && !possibleSails.includes(sailInput)) setPossibleSails([...possibleSails, sailInput])
    setSailInput("")
  }
  const removeSail = (s: string) => setPossibleSails(possibleSails.filter(x => x !== s))
  const addRope = () => {
    if (ropeInput && !possibleRopes.includes(ropeInput)) setPossibleRopes([...possibleRopes, ropeInput])
    setRopeInput("")
  }
  const removeRope = (r: string) => setPossibleRopes(possibleRopes.filter(x => x !== r))

  // Submit handler
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    setResult(null)
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"
      // Generate a random yacht_id (timestamp-based)
      const yacht_id = Date.now()
      // Compose payload for orchestrator
      const payload: any = {
        yacht_id,
        profile: {
          ...profile,
          year_introduced: profile.year_introduced ? Number(profile.year_introduced) : undefined,
          production_start: profile.production_start ? Number(profile.production_start) : undefined,
          production_end: profile.production_end ? Number(profile.production_end) : undefined,
        },
        hull: {
          ...hull,
          loa: hull.loa ? Number(hull.loa) * 1000 : undefined,
          lwl: hull.lwl ? Number(hull.lwl) * 1000 : undefined,
          beam: hull.beam ? Number(hull.beam) * 1000 : undefined,
          displacement: hull.displacement ? Number(hull.displacement) : undefined,
          ballast: hull.ballast ? Number(hull.ballast) : undefined,
          construction: hull.construction,
        },
        saildata: {
          i: saildata.i ? Number(saildata.i) * 1000 : undefined,
          j: saildata.j ? Number(saildata.j) * 1000 : undefined,
          p: saildata.p ? Number(saildata.p) * 1000 : undefined,
          e: saildata.e ? Number(saildata.e) * 1000 : undefined,
        },
        possible_sails: possibleSails,
        possible_ropes: possibleRopes,
      };
      // Only include keel if keel_type is non-empty
      if (keel.keel_type) {
        payload.keel = {
          keel_type: keel.keel_type,
          draft: keel.draft ? Number(keel.draft) * 1000 : undefined,
        };
      }
      // Only include rudder if rudder_type is non-empty
      if (rudder.rudder_type) {
        payload.rudder = { rudder_type: rudder.rudder_type };
      }

      const res = await fetch(`${apiBase}/yachts/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
      if (res.ok) {
        setResult("Yacht added successfully!")
        setProfile(initialProfile)
        setHull(initialHull)
        setKeel(initialKeel)
        setRudder(initialRudder)
        setSaildata(initialSaildata)
        setPossibleSails([])
        setPossibleRopes([])
      } else {
        setResult("Failed to add yacht. Check input and try again.")
      }
    } catch (e) {
      setResult("Error: " + (e as Error).message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Card className="max-w-5xl mx-auto mt-8"> {/* Increased max width */}
      <CardContent className="p-8"> {/* More padding for a wider look */}
        <h2 className="text-2xl font-bold mb-4">Add New Base Yacht</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Profile & Hull Section side by side */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8"> {/* 2 columns on md+ screens */}
            <div>
              <h3 className="font-semibold mb-2">Profile</h3>
              <div className="grid grid-cols-1 gap-4">
                {Object.entries(initialProfile).map(([key, _]) => (
                  <Input key={key} name={key} placeholder={key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())} value={profile[key as keyof typeof profile] as string} onChange={handleProfileChange} />
                ))}
              </div>
            </div>
            <div>
              <h3 className="font-semibold mb-2">Hull</h3>
              <div className="grid grid-cols-1 gap-4">
                {Object.entries(initialHull).map(([key, _]) => (
                  <Input key={key} name={key} placeholder={key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())} value={hull[key as keyof typeof hull] as string} onChange={handleHullChange} />
                ))}
              </div>
            </div>
          </div>
          {/* Keel Section */}
          <div>
            <h3 className="font-semibold mb-2 mt-4">Keel</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input name="keel_type" placeholder="Keel Type" value={keel.keel_type} onChange={handleKeelChange} />
              <Input name="draft" placeholder="Draft (m)" value={keel.draft} onChange={handleKeelChange} />
            </div>
          </div>
          {/* Rudder Section */}
          <div>
            <h3 className="font-semibold mb-2 mt-4">Rudder</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input name="rudder_type" placeholder="Rudder Type" value={rudder.rudder_type} onChange={handleRudderChange} />
            </div>
          </div>
          {/* Saildata Section */}
          <div>
            <h3 className="font-semibold mb-2 mt-4">Sail Data (I, J, P, E)</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input name="i" placeholder="I (m)" value={saildata.i} onChange={handleSaildataChange} />
              <Input name="j" placeholder="J (m)" value={saildata.j} onChange={handleSaildataChange} />
              <Input name="p" placeholder="P (m)" value={saildata.p} onChange={handleSaildataChange} />
              <Input name="e" placeholder="E (m)" value={saildata.e} onChange={handleSaildataChange} />
            </div>
          </div>
          {/* Possible Sails Section */}
          <div>
            <h3 className="font-semibold mb-2 mt-4">Possible Sails</h3>
            <div className="flex gap-2 mb-2">
              <Input value={sailInput} onChange={e => setSailInput(e.target.value)} placeholder="Sail type (e.g. Main, Genoa)" />
              <Button type="button" onClick={addSail}>Add</Button>
            </div>
            <div className="flex flex-wrap gap-2">
              {possibleSails.map(s => (
                <span key={s} className="bg-muted px-2 py-1 rounded flex items-center gap-1">{s} <Button type="button" size="sm" variant="ghost" onClick={() => removeSail(s)}>×</Button></span>
              ))}
            </div>
          </div>
          {/* Possible Ropes Section */}
          <div>
            <h3 className="font-semibold mb-2 mt-4">Possible Ropes</h3>
            <div className="flex gap-2 mb-2">
              <Input value={ropeInput} onChange={e => setRopeInput(e.target.value)} placeholder="Rope type (e.g. Main Halyard)" />
              <Button type="button" onClick={addRope}>Add</Button>
            </div>
            <div className="flex flex-wrap gap-2">
              {possibleRopes.map(r => (
                <span key={r} className="bg-muted px-2 py-1 rounded flex items-center gap-1">{r} <Button type="button" size="sm" variant="ghost" onClick={() => removeRope(r)}>×</Button></span>
              ))}
            </div>
          </div>
          <Button type="submit" disabled={submitting} className="w-full mt-4">
            {submitting ? "Adding..." : "Add Yacht"}
          </Button>
          {result && <div className="mt-2 text-center text-sm text-muted-foreground">{result}</div>}
        </form>
      </CardContent>
    </Card>
  )
}
