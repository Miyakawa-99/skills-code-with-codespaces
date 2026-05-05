import { slotKey, type Slot, type Snapshot } from './types'

export function buildSnapshot(slots: Slot[]): Snapshot {
  const snap: Snapshot = {}
  for (const s of slots) snap[slotKey(s)] = s.available
  return snap
}

// 「前回 不可（false / 未知） → 今回 可」になった枠だけを返す。
// 「可 → 不可」は通知しない（埋まっただけなので不要）。
export function detectNewlyAvailable(prev: Snapshot, curr: Slot[]): Slot[] {
  const out: Slot[] = []
  for (const s of curr) {
    if (!s.available) continue
    const k = slotKey(s)
    const prevAvailable = prev[k]
    if (prevAvailable !== true) out.push(s)
  }
  return out
}

export function formatNotification(slots: Slot[]): string {
  // 公園 → 日付 の順でグループ化
  const byPark = new Map<string, Map<string, Slot[]>>()
  for (const s of slots) {
    let dates = byPark.get(s.parkName)
    if (!dates) {
      dates = new Map()
      byPark.set(s.parkName, dates)
    }
    let arr = dates.get(s.date)
    if (!arr) {
      arr = []
      dates.set(s.date, arr)
    }
    arr.push(s)
  }

  const lines: string[] = ['🎾 テニスコートに空きが出ました']
  for (const [park, dates] of byPark) {
    lines.push('')
    lines.push(`【${park}】`)
    const sortedDates = [...dates.keys()].sort()
    for (const date of sortedDates) {
      const items = dates.get(date)!
      items.sort((a, b) => a.time.localeCompare(b.time) || a.court.localeCompare(b.court))
      lines.push(`・${date}`)
      for (const it of items) lines.push(`    ${it.time} ${it.court}`)
    }
  }
  lines.push('')
  lines.push('https://kouen.sports.metro.tokyo.lg.jp/web/')
  return lines.join('\n')
}
