export interface Boat {
  id: string
  yacht_id?: number // Added for orchestrator compatibility
  name: string
  yacht_class?: string // Added for compatibility with BoatOverview
  model: string
  version?: string
  designer?: string
  builder?: string
  year_introduced?: number
  production_start?: number
  production_end?: number
  type: string
  notes?: string
  imageUrl?: string
  hull: Hull
  rig: Rig
  sailData: SailData
  sails: Sail[]
  ropes: Rope[]
}

export interface Hull {
  loa: number;
  lwl: number;
  beam: number;
  draft: number;
  displacement: number;
  ballast: number;
  material: string;
  keelType: string;
  hullType: string;
  rudderType: string;
  construction: string;
  ballastRatio: number;
  displacementLengthRatio: number;
  sailAreaDisplacementRatio: number;
  capsizeScreeningValue: number;
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

export interface UserProfileApi {
  user_id: string;
  role: string;
  yacht_ids: string[];
  telephone?: string;
  address?: {
    street: string;
    city: string;
    postcode: string;
    country: string;
  };
  subscription_status?: string;
  payment_info?: {
    card_last4?: string;
    stripe_customer_id?: string;
    billing_email?: string;
  };
  company_name?: string;
}
