import { AdminAddYachtForm } from "@/components/admin-add-yacht-form"

// Simple admin check (replace with real auth in production)
const ADMIN_EMAIL = process.env.NEXT_PUBLIC_ADMIN_EMAIL || "admin@example.com"

export default function AdminPage() {
  // TODO: Replace with real authentication check
  // For now, just render the form
  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Admin Panel</h1>
      <p className="mb-4 text-muted-foreground">Add new base yachts to the system.</p>
      <AdminAddYachtForm />
    </main>
  )
}
