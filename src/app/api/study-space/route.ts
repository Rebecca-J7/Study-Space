import { NextRequest, NextResponse } from 'next/server'

const BACKEND = process.env.STUDYSPACE_BACKEND || 'http://localhost:8001'

export async function POST(req: NextRequest) {
  const url = new URL(req.url)
  const path = url.pathname.replace('/api/study-space', '') || '/'
  const backendUrl = `${BACKEND}${path}`

  const body = await req.text()
  const headers: Record<string, string> = {}
  req.headers.forEach((value, key) => {
    headers[key] = value as string
  })

  try {
    const res = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        ...headers,
        'content-type': headers['content-type'] || 'application/json',
      },
      body,
    })

    const text = await res.text()
    return new NextResponse(text, { status: res.status })
  } catch (err) {
    return new NextResponse(JSON.stringify({ error: 'Proxy error', details: String(err) }), { status: 500 })
  }
}
