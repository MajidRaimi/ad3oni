export function GET() {
  return new Response("pong", {
    headers: { "Content-Type": "text/plain" },
  });
}
