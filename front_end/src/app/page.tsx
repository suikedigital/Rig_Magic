import { SearchBoats } from "@/components/search-boats"
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselPrevious,
  CarouselNext,
} from "@/components/ui/carousel"

export default function Home() {
  return (
    <main className="w-full pt-20 py-8 flex flex-col items-center">
      <div className="flex flex-col md:flex-row items-center justify-center py-14 gap-8 w-full">
        {/* Centered, Larger Carousel */}
        <div className="w-full max-w-4xl flex justify-center mx-auto scale-125">
          <Carousel>
            <CarouselContent>
              <CarouselItem>
                <div className="p-10 bg-card rounded-2xl shadow-xl flex flex-col items-center text-center">
                  <img src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80" alt="Shop Rigging" className="mb-6 rounded-lg w-full h-60 object-cover" />
                  <h3 className="text-2xl font-bold mb-3 text-primary">All your boat, data in one place</h3>
                  <p className="text-muted-foreground text-lg">Copy one of our yacht assest, and keep all infomation about your boat in one place</p>
                </div>
              </CarouselItem>
              <CarouselItem>
                <div className="p-10 bg-card rounded-2xl shadow-xl flex flex-col items-center text-center">
                  <img src="https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=600&q=80" alt="Manage Boats" className="mb-6 rounded-lg w-full h-60 object-cover" />
                  <h3 className="text-2xl font-bold mb-3 text-primary">Build, Customise and Create</h3>
                  <p className="text-muted-foreground text-lg">Add, customize, and create all your yacht equipment, all in one place.</p>
                </div>
              </CarouselItem>
              <CarouselItem>
                <div className="p-10 bg-card rounded-2xl shadow-xl flex flex-col items-center text-center">
                  <img src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80" alt="Service & Support" className="mb-6 rounded-lg w-full h-60 object-cover" />
                  <h3 className="text-2xl font-bold mb-3 text-primary">Yacht Services</h3>
                  <p className="text-muted-foreground text-lg">Book maintenance, get reminders, and access expert support anytime.</p>
                </div>
              </CarouselItem>
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </div>
      </div>

      {/* Prominent Search */}
      <div className="my-8 w-full flex justify-center">
        <SearchBoats />
      </div>
    </main>
  )
}