import { detectNewlyAvailable, buildSnapshot, formatNotification } from './diff'
import { multicast } from './line'
import { scanAll } from './scraper'
import {
  listUsers,
  loadSnapshot,
  recordScanTime,
  saveSnapshot,
} from './storage'
import type { Env } from './types'

export async function runScan(env: Env): Promise<void> {
  // ユーザーが0人ならサイトに余計な負荷をかけない
  const users = await listUsers(env.STATE)
  if (users.length === 0) {
    console.log('no users registered, skipping scan')
    return
  }

  // JST 深夜 (0:00–5:59) はスキップ
  const jstHour = new Date(Date.now() + 9 * 3600_000).getUTCHours()
  if (jstHour < 6) {
    console.log('quiet hours, skipping scan')
    return
  }

  const slots = await scanAll(env)
  if (slots.length === 0) {
    console.log('scraper returned no slots (likely TODO not yet implemented)')
    return
  }

  const prev = await loadSnapshot(env.STATE)
  const newlyAvailable = detectNewlyAvailable(prev, slots)
  const next = buildSnapshot(slots)
  await saveSnapshot(env.STATE, next)
  await recordScanTime(env.STATE)

  if (newlyAvailable.length === 0) {
    console.log('no new openings')
    return
  }

  const text = formatNotification(newlyAvailable)
  await multicast(env.LINE_CHANNEL_ACCESS_TOKEN, users, text)
  console.log(`notified ${users.length} users about ${newlyAvailable.length} openings`)
}
