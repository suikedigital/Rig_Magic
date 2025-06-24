// Utility to get the correct API base URL for both server and client
export function getApiBase(service: string) {
  // Map service names to environment variables (for browser/client)
  const envMap: Record<string, string | undefined> = {
    yacht: process.env.NEXT_PUBLIC_YACHT_API_URL,
    profile: process.env.NEXT_PUBLIC_PROFILE_API_URL,
    user_profile: process.env.NEXT_PUBLIC_USER_PROFILE_API_URL,
    ropes: process.env.NEXT_PUBLIC_ROPES_API_URL,
    sails: process.env.NEXT_PUBLIC_SAILS_API_URL,
    hull_structure: process.env.NEXT_PUBLIC_HULL_STRUCTURE_API_URL,
    saildata: process.env.NEXT_PUBLIC_SAILDATA_API_URL,
    furler: process.env.NEXT_PUBLIC_FURLER_API_URL,
    auth: process.env.NEXT_PUBLIC_AUTH_API_URL,
  };

  // If running in the browser, use the public env variable (localhost)
  if (typeof window !== "undefined") {
    return envMap[service] || "";
  }

  // If running on the server (SSR), use Docker internal hostname
  const dockerMap: Record<string, string> = {
    yacht: "http://yacht:8050",
    profile: "http://profile:8003",
    user_profile: "http://user_profile:8005",
    ropes: "http://ropes:8010",
    sails: "http://sails:8020",
    hull_structure: "http://hull_structure:8004",
    saildata: "http://saildata:8001",
    furler: "http://furler:8002",
    auth: "http://auth_service:3000",
  };
  return dockerMap[service] || envMap[service] || "";
}
