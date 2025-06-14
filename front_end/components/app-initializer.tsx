"use client";

import { useState, ReactNode } from 'react';
import ThemeAwareSplashScreen from './splash-screen'; // Adjust path if needed

interface AppInitializerProps {
  children: ReactNode;
  // You can pass any initial API call for the splash screen here if needed globally
  // For example: globalApiCall?: () => Promise<any>;
}

// Example: Simulate an API call for the splash screen
const simulateInitialLoadApiCall = (): Promise<{ appName: string }> => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (Math.random() > 0.1) { // 90% chance of success
        console.log("Global initial load API call successful");
        resolve({ appName: "RigMagic Suite" });
      } else {
        console.error("Global initial load API call failed");
        reject(new Error("Failed to fetch initial global configuration."));
      }
    }, 1500); // Simulate 1.5 seconds delay
  });
};

export default function AppInitializer({ children }: AppInitializerProps) {
  const [isInitialized, setIsInitialized] = useState(false);
  const [initializationError, setInitializationError] = useState<Error | null>(null);
  const [loadedData, setLoadedData] = useState<any>(null);

  const handleSplashComplete = (data?: any, error?: Error) => {
    console.log("Splash screen sequence finished.");
    if (error) {
      console.error("Initialization error:", error.message);
      setInitializationError(error);
      // Potentially set some default data or handle critical failure
    } else {
      console.log("Initialization successful, data:", data);
      setLoadedData(data);
    }
    setIsInitialized(true); // Mark initialization as complete
  };

  if (!isInitialized) {
    return (
      <ThemeAwareSplashScreen
        // Pass your actual global API call here if you have one
        // If not, the splash screen will just run on its timers
        apiCall={simulateInitialLoadApiCall} // Example API call
        initialMessage="Warming up the engines..."
        minDisplayTime={2000}    // Show for at least 2 seconds
        maxDisplayTime={10000}   // Timeout after 10 seconds
        onComplete={handleSplashComplete}
        showDebugInfo={process.env.NODE_ENV === 'development'} // Show debug info only in development
      />
    );
  }

  // Optional: Render an error state if initialization failed critically
  if (initializationError && !loadedData) { // Example condition for critical failure
     return (
       <div style={{ padding: '20px', textAlign: 'center', color: 'red' }}>
         <h1>Application Initialization Failed</h1>
         <p>{initializationError.message}</p>
         <p>Please try refreshing the page or contact support.</p>
       </div>
     );
  }

  // Render the actual application content once initialized
  return <>{children}</>;
}