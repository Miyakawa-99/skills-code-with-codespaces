import type { Context } from 'hono'
import { reply, verifySignature } from './line'
import { addUser, isRegistered, removeUser } from './storage'
import type { Env } from './types'

type LineEvent = {
  type: string
  replyToken?: string
  source?: { userId?: string }
  message?: { type: string; text?: string }
}

const HELP_TEXT = [
  '使えるコマンド:',
  '・「開始」→ 通知を受け取る',
  '・「停止」→ 通知を解除',
  '・「状態」→ 登録状況を確認',
].join('\n')

export async function handleWebhook(c: Context<{ Bindings: Env }>) {
  const sig = c.req.header('x-line-signature') ?? ''
  const body = await c.req.text()
  const ok = await verifySignature(c.env.LINE_CHANNEL_SECRET, body, sig)
  if (!ok) return c.text('unauthorized', 401)

  const { events } = JSON.parse(body) as { events: LineEvent[] }
  for (const ev of events) {
    try {
      await handleEvent(c.env, ev)
    } catch (e) {
      console.error('handleEvent failed', e)
    }
  }
  return c.text('ok')
}

async function handleEvent(env: Env, ev: LineEvent): Promise<void> {
  const userId = ev.source?.userId
  if (!userId) return

  if (ev.type === 'follow') {
    await addUser(env.STATE, userId)
    if (ev.replyToken) {
      await reply(
        env.LINE_CHANNEL_ACCESS_TOKEN,
        ev.replyToken,
        '友だち追加ありがとうございます！\n都立公園テニスコートのキャンセル枠を見つけたらお知らせします。\n\n' +
          HELP_TEXT,
      )
    }
    return
  }

  if (ev.type === 'unfollow') {
    await removeUser(env.STATE, userId)
    return
  }

  if (ev.type === 'message' && ev.message?.type === 'text' && ev.replyToken) {
    const text = (ev.message.text ?? '').trim()
    if (/^(停止|解除|stop)$/i.test(text)) {
      await removeUser(env.STATE, userId)
      await reply(
        env.LINE_CHANNEL_ACCESS_TOKEN,
        ev.replyToken,
        '通知を停止しました。再開するには「開始」と送ってください。',
      )
      return
    }
    if (/^(状態|確認|status)$/i.test(text)) {
      const on = await isRegistered(env.STATE, userId)
      await reply(
        env.LINE_CHANNEL_ACCESS_TOKEN,
        ev.replyToken,
        on ? '通知ON です。' : '通知OFF です。「開始」で登録できます。',
      )
      return
    }
    await addUser(env.STATE, userId)
    await reply(
      env.LINE_CHANNEL_ACCESS_TOKEN,
      ev.replyToken,
      '通知を開始しました。テニスコートに空きが出たらお知らせします。\n\n' + HELP_TEXT,
    )
  }
}
