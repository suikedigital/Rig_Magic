import GoogleProvider from "next-auth/providers/google"
import AppleProvider from "next-auth/providers/apple"

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      profile(profile) {
        // Map Google's 'sub' to 'id' for NextAuth user object
        return {
          id: profile.sub,
          name: profile.name,
          email: profile.email,
          image: profile.picture,
        }
      },
    }),
    AppleProvider({
      clientId: process.env.APPLE_CLIENT_ID!,
      clientSecret: process.env.APPLE_CLIENT_SECRET!,
    }),
    // Add more providers here
  ],
  callbacks: {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    async jwt({ token, account, user }: any) {
      if (account) {
        token.accessToken = account.id_token || account.access_token
      }
      if (user && user.id) {
        token.id = user.id
      }
      return token
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    async session({ session, token }: any) {
      session.accessToken = token.accessToken
      if (token.id) {
        session.user = session.user || {}
        session.user.id = token.id

        // Ensure user exists in user_profile service
        const userProfileUrl = process.env.NEXT_PUBLIC_USER_PROFILE_API_URL || "http://user_profile:8005";
        const userId = token.id;
        try {
          const res = await fetch(`${userProfileUrl}/users/${userId}`);
          if (res.status === 404) {
            // Create user if not exists (minimal required fields)
            await fetch(`${userProfileUrl}/users/`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                user_id: userId,
                role: "customer",
                yacht_ids: [],
                subscription_status: "free"
              }),
            });
          }
        } catch (err) {
          // Optionally log error
          console.error("User profile check/create failed:", err);
        }
      }
      return session
    },
  },
}
