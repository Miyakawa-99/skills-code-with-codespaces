import type { Snapshot } from './types'

const USER_PREFIX = 'user:'
const SNAPSHOT_KEY = 'snapshot:current'
const LAST_SCAN_KEY = 'meta:lastScanAt'

export async function listUsers(kv: KVNamespace): Promise<string[]> {
  const out: string[] = []
  let cursor: string | undefined
  while (true) {
    const res = await kv.list({ prefix: USER_PREFIX, cursor })
    for (const k of res.keys) out.push(k.name.slice(USER_PREFIX.length))
    if (res.list_complete) break
    cursor = res.cursor
  }
  return out
}

export async function isRegistered(kv: KVNamespace, userId: string): Promise<boolean> {
  return (await kv.get(USER_PREFIX + userId)) !== null
}

export async function addUser(kv: KVNamespace, userId: string): Promise<void> {
  await kv.put(USER_PREFIX + userId, JSON.stringify({ addedAt: Date.now() }))
}

export async function removeUser(kv: KVNamespace, userId: string): Promise<void> {
  await kv.delete(USER_PREFIX + userId)
}

export async function loadSnapshot(kv: KVNamespace): Promise<Snapshot> {
  const raw = await kv.get(SNAPSHOT_KEY)
  return raw ? (JSON.parse(raw) as Snapshot) : {}
}

export async function saveSnapshot(kv: KVNamespace, snap: Snapshot): Promise<void> {
  await kv.put(SNAPSHOT_KEY, JSON.stringify(snap))
}

export async function recordScanTime(kv: KVNamespace): Promise<void> {
  await kv.put(LAST_SCAN_KEY, String(Date.now()))
}
