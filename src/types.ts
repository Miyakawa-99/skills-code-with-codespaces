export type Env = {
  STATE: KVNamespace
  LINE_CHANNEL_ACCESS_TOKEN: string
  LINE_CHANNEL_SECRET: string
  USER_AGENT: string
  REQUEST_DELAY_MS: string
  SCAN_FUTURE_DAYS: string
}

export type Slot = {
  parkId: string
  parkName: string
  date: string
  time: string
  court: string
  available: boolean
}

export type Snapshot = Record<string, boolean>

export const slotKey = (s: Pick<Slot, 'parkId' | 'date' | 'time' | 'court'>) =>
  `${s.parkId}|${s.date}|${s.time}|${s.court}`
