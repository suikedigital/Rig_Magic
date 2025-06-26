"use client"

import React from 'react';
import { useRouter } from "next/navigation"
import Image from "next/image"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselPrevious,
  CarouselNext,
} from "@/components/ui/carousel"
import logger from '../logger';

interface HullData {
  hull_type?: string;
  loa?: number;
  lwl?: number;
  beam?: number;
  displacement?: number;
  ballast?: number;
}

interface KeelData {
  keel_type?: string;
  draft?: number;
}

interface RigData {
  rig_type?: string;
}

interface MinimalBoatResult {
  id: string;
  name?: string;
  yacht_class?: string;
  model?: string;
  version?: string;
  builder?: string;
  designer?: string;
  production_start?: string | number;
  imageUrl?: string;
  hull?: HullData | null;
  keel?: KeelData | null;
  rig?: RigData | null;
}

interface BoatSearchResultsProps {
  boats: MinimalBoatResult[];
}

export function BoatSearchResults({ boats }: BoatSearchResultsProps) {
  const router = useRouter();

  if (!boats || boats.length === 0) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-semibold mb-2">No results found</h2>
        <p className="text-muted-foreground">Try adjusting your search criteria or browse our featured boats.</p>
      </div>
    );
  }

  return (
    <div>
      
      <p className="mb-4 glass text-muted-foreground">Found {boats.length} boats</p>
      
      <Carousel className="w-full">
        <CarouselContent className="-ml-2 md:-ml-4">
          {boats.map((boat) => {
            const hull = boat.hull;
            const keel = boat.keel;
            // Debug output
            logger.info('Boat card:', { id: boat.id, hull, keel, rig: boat.rig });
            
            return (
              <CarouselItem key={boat.id} className="pl-2 md:pl-4 md:basis-1/2 lg:basis-1/3">
                <Card className="overflow-hidden h-full">
                  <div className="relative h-48">
                    <Image src={boat.imageUrl || "/placeholder.svg"} alt={boat.name || "Yacht image"} fill className="object-cover" />
                  </div>
                  <CardContent className="p-4">
                    <h3 className="text-lg font-semibold">{boat.yacht_class} {boat.model} {boat.version}</h3>
                    <p className="text-sm text-muted-foreground">
                      {boat.builder || boat.designer}
                    </p>
                    <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
                      <div>
                        <span className="font-medium">Length:</span> {(() => {
                          if (!hull) return <span className="italic text-gray-400">No hull data</span>;
                          if (hull.loa) return `${hull.loa >= 10 ? hull.loa.toFixed(2) + ' m' : (hull.loa * 3.28084).toFixed(1) + ' ft'}`;
                          return <span className="italic text-gray-400">N/A</span>;
                        })()}
                      </div>
                      <div>
                        <span className="font-medium">Beam:</span> {(() => {
                          if (!hull) return <span className="italic text-gray-400">No hull data</span>;
                          if (hull.beam) return `${hull.beam >= 2 ? hull.beam.toFixed(2) + ' m' : (hull.beam * 3.28084).toFixed(1) + ' ft'}`;
                          return <span className="italic text-gray-400">N/A</span>;
                        })()}
                      </div>
                      <div>
                        <span className="font-medium">Draft:</span> {(() => {
                          if (keel && keel.draft) return `${keel.draft >= 1 ? keel.draft.toFixed(2) + ' m' : (keel.draft * 3.28084).toFixed(1) + ' ft'}`;
                          return <span className="italic text-gray-400">N/A</span>;
                        })()}
                      </div>
                      <div>
                        <span className="font-medium">Year:</span> {boat.production_start || <span className="italic text-gray-400">N/A</span>}
                      </div>
                      <div>
                        <span className="font-medium">Hull Type:</span> {hull?.hull_type || <span className="italic text-gray-400">N/A</span>}
                      </div>
                      <div>
                        <span className="font-medium">Keel Type:</span> {keel?.keel_type || <span className="italic text-gray-400">N/A</span>}
                      </div>
                      <div>
                        <span className="font-medium">Disp:</span> {hull?.displacement ? `${hull.displacement} kg` : <span className="italic text-gray-400">N/A</span>}
                      </div>
                      <div>
                        <span className="font-medium">Ballast:</span> {hull?.ballast ? `${hull.ballast} kg` : <span className="italic text-gray-400">N/A</span>}
                      </div>
                      <div>
                        <span className="font-medium">Rig Type:</span> {boat.rig?.rig_type || <span className="italic text-gray-400">N/A</span>}
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter className="p-4 pt-0">
                    <Button variant="outline" className="w-full" onClick={() => router.push(`/boats/${boat.id}`)}>
                      View Details
                    </Button>
                  </CardFooter>
                </Card>
              </CarouselItem>
            );
          })}
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
    </div>
  );
}