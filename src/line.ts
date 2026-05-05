const REPLY_URL = 'https://api.line.me/v2/bot/message/reply'
const MULTICAST_URL = 'https://api.line.me/v2/bot/message/multicast'

export async function verifySignature(
  secret: string,
  body: string,
  signature: string,
): Promise<boolean> {
  const key = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign'],
  )
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(body))
  const expected = bufferToBase64(sig)
  return timingSafeEqual(expected, signature)
}

function bufferToBase64(buf: ArrayBuffer): string {
  const bytes = new Uint8Array(buf)
  let s = ''
  for (let i = 0; i < bytes.length; i++) s += String.fromCharCode(bytes[i]!)
  return btoa(s)
}

function timingSafeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false
  let diff = 0
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i)
  return diff === 0
}

export async function reply(token: string, replyToken: string, text: string): Promise<void> {
  const res = await fetch(REPLY_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ replyToken, messages: [{ type: 'text', text }] }),
  })
  if (!res.ok) {
    console.error('LINE reply failed', res.status, await res.text())
  }
}

export async function multicast(
  token: string,
  userIds: string[],
  text: string,
): Promise<void> {
  if (userIds.length === 0) return
  for (let i = 0; i < userIds.length; i += 500) {
    const chunk = userIds.slice(i, i + 500)
    const res = await fetch(MULTICAST_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ to: chunk, messages: [{ type: 'text', text }] }),
    })
    if (!res.ok) {
      console.error('LINE multicast failed', res.status, await res.text())
    }
  }
}
