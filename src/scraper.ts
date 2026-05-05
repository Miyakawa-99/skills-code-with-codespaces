import { PARKS, type Park } from './parks'
import type { Env, Slot } from './types'

const BASE_URL = 'https://kouen.sports.metro.tokyo.lg.jp/web/'

export async function scanAll(env: Env): Promise<Slot[]> {
  const delay = Number(env.REQUEST_DELAY_MS) || 2500
  const futureDays = Number(env.SCAN_FUTURE_DAYS) || 60
  const dates = futureDateStrings(futureDays)

  const headers = {
    'User-Agent': env.USER_AGENT,
    'Accept-Language': 'ja,en;q=0.5',
    Accept: 'text/html,application/xhtml+xml',
  }

  const session = await openSession(headers)
  const slots: Slot[] = []

  for (const park of PARKS) {
    if (park.id.startsWith('TODO_')) continue
    for (const date of dates) {
      try {
        const parkSlots = await fetchParkDay(session, park, date, headers)
        slots.push(...parkSlots)
      } catch (e) {
        console.error('fetchParkDay failed', park.name, date, e)
      }
      await sleep(delay)
    }
  }

  return slots
}

type Session = {
  cookie: string
}

async function openSession(headers: Record<string, string>): Promise<Session> {
  const res = await fetch(BASE_URL + 'index.jsp', { headers })
  const cookie = res.headers.get('set-cookie') ?? ''
  // jsessionid だけ抽出
  const m = cookie.match(/JSESSIONID=[^;]+/i)
  return { cookie: m ? m[0] : '' }
}

// 1公園×1日ぶんの空き状況を取得して Slot[] を返す。
//
// 実装メモ（README の「スクレイパー実装ガイド」参照）:
//   都立公園スポレクシステムは JSP のフォーム遷移型で、以下の流れで照会する想定です:
//     1) GET  /web/index.jsp                              → JSESSIONID 取得
//     2) POST /web/...select-park.jsp     park=ARIAKE     → 公園選択
//     3) POST /web/...select-sport.jsp    sport=tennis    → 競技選択
//     4) POST /web/...availability.jsp    date=YYYYMMDD   → 空き状況一覧
//   レスポンス HTML から「コート×時間帯×状態」を抽出します。
//
//   実際のパス・パラメータ名はサイトを開いて DevTools の Network タブで観察してください。
//   観察結果に応じて以下を埋めると動作します。
async function fetchParkDay(
  session: Session,
  park: Park,
  date: string,
  headers: Record<string, string>,
): Promise<Slot[]> {
  const reqHeaders = { ...headers, Cookie: session.cookie }

  // TODO: 実際のリクエストに置き換え
  // const res = await fetch(BASE_URL + '...availability.jsp', {
  //   method: 'POST',
  //   headers: { ...reqHeaders, 'Content-Type': 'application/x-www-form-urlencoded' },
  //   body: new URLSearchParams({ park: park.id, date }).toString(),
  // })
  // const html = await res.text()
  // return parseAvailability(html, park, date)
  void reqHeaders
  return []
}

// HTML から「コート×時間帯×空き/不可」を抽出する。
// サイトの table 構造に合わせて実装してください。
// 例: <td class="vacant">○</td> / <td class="occupied">×</td>
export function parseAvailability(html: string, park: Park, date: string): Slot[] {
  // TODO: HTMLRewriter or 正規表現でパース
  void html
  void park
  void date
  return []
}

function futureDateStrings(days: number): string[] {
  const out: string[] = []
  const now = new Date()
  // JST に合わせる（UTC+9）
  const jstNow = new Date(now.getTime() + 9 * 3600_000)
  for (let i = 0; i < days; i++) {
    const d = new Date(jstNow.getTime() + i * 86400_000)
    const y = d.getUTCFullYear()
    const m = String(d.getUTCMonth() + 1).padStart(2, '0')
    const day = String(d.getUTCDate()).padStart(2, '0')
    out.push(`${y}-${m}-${day}`)
  }
  return out
}

function sleep(ms: number): Promise<void> {
  return new Promise((r) => setTimeout(r, ms))
}
