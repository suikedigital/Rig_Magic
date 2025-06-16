// Utility to get the correct API base URL for server/client
export function getApiBase() {
  if (typeof window === "undefined") {
    // Server-side (in Docker): use Docker service name
    return process.env.NEXT_PUBLIC_API_BASE_URL || "http://yacht:8050";
  } else {
    // Client-side (browser): use localhost
    return "http://localhost:8050";
  }
}
