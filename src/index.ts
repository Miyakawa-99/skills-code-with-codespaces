import { Hono } from 'hono'
import { runScan } from './scan'
import { handleWebhook } from './webhook'
import type { Env } from './types'

const app = new Hono<{ Bindings: Env }>()

app.get('/', (c) => c.text('court-watcher: ok'))
app.post('/webhook', handleWebhook)

export default {
  fetch: app.fetch,
  async scheduled(_event: ScheduledEvent, env: Env, ctx: ExecutionContext) {
    ctx.waitUntil(runScan(env))
  },
} satisfies ExportedHandler<Env>
