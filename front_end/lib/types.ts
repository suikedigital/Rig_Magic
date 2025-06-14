export interface Boat {
  id: string
  name: string
  manufacturer: string
  model: string
  year: number
  type: string
  designer: string
  description: string
  imageUrl?: string
  hull: Hull
  rig: Rig
  sailData: SailData
  sails: Sail[]
  ropes: Rope[]
}

export interface Hull {
  length: number
  waterlineLength: number
  beam: number
  draft: number
  displacement: number
  ballast: number
  material: string
  keelType: string
  hullType: string
  rudderType: string
  ballastRatio: number
  displacementLengthRatio: number
  sailAreaDisplacementRatio: number
  capsizeScreeningValue: number
}

export interface Rig {
  type: string
  mastType: string
  mastHeight: number
  mastMaterial: string
  boomLength: number
  boomMaterial: string
  standingRigging: {
    forestay: RiggingComponent
    backstay: RiggingComponent
    shrouds: RiggingComponent
  }
  runningRigging: {
    halyards: RunningRiggingComponent
    sheets: RunningRiggingComponent
  }
}

export interface RiggingComponent {
  material: string
  diameter: number
  length?: number
  condition?: number
}

export interface RunningRiggingComponent {
  count: number
  material: string
  diameter?: number
  condition?: number
}

export interface SailData {
  I: number // Foretriangle height
  J: number // Foretriangle base
  P: number // Mainsail luff
  E: number // Mainsail foot
  mainsailArea: number
  foretriangle: number
  totalSailArea100: number
  totalSailArea150: number
  spinnakerArea: number
  downwindSailArea: number
  sailAreaDisplacementRatio: number
  displacementLengthRatio: number
  ballastDisplacementRatio: number
  capsizeScreeningValue: number
}

export interface Sail {
  type: string
  material: string
  area: number
  condition: number
  year: number
  manufacturer: string
  notes: string
  windRange: string
}

export interface Rope {
  name: string
  category: string
  material: string
  diameter: number
  length: number
  condition: number
  purpose?: string
}
