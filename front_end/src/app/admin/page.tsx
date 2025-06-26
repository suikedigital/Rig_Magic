import { AdminAddYachtForm } from "@/components/admin-add-yacht-form"
import { YachtAdminList } from "@/components/yacht-admin-list"

// Simple admin check (replace with real auth in production)
const ADMIN_EMAIL = process.env.NEXT_PUBLIC_ADMIN_EMAIL || "admin@example.com"

export default function AdminPage() {
  // TODO: Replace with real authentication check
  // For now, just render the form
  return (
    <main className="container mx-auto px-4 py-8">
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <AdminAddYachtForm />
        </div>
        <div>
          <YachtAdminList />
        </div>
      </div>
    </main>
  )
}
