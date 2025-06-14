"use client"

import { useState, useEffect } from "react"
import Image from "next/image"
// useTheme is no longer needed if all styling relies on CSS variables via Tailwind classes
// import { useTheme } from "next-themes"; 

interface ThemeAwareSplashScreenProps {
  apiCall?: () => Promise<any>
  initialMessage?: string
  minDisplayTime?: number
  maxDisplayTime?: number
  onComplete?: (data?: any, error?: Error) => void
  showDebugInfo?: boolean
}

export default function ThemeAwareSplashScreen({
  apiCall,
  initialMessage = "Loading...",
  minDisplayTime = 1500,
  maxDisplayTime = 10000,
  onComplete,
  showDebugInfo = false,
}: ThemeAwareSplashScreenProps) {
  const [visible, setVisible] = useState(true)
  const [message, setMessage] = useState(initialMessage)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [debugInfo, setDebugInfo] = useState<string | null>(null)
  const [progress, setProgress] = useState(0)

  // const { resolvedTheme } = useTheme(); // No longer needed
  // const [isDark, setIsDark] = useState(false); // No longer needed

  // This useEffect is no longer needed as isDark state is removed
  // useEffect(() => {
  //   setIsDark(resolvedTheme === 'dark');
  // }, [resolvedTheme]);

  useEffect(() => {
    const startTime = Date.now()
    let apiData: any = null
    let apiError: Error | null = null
    let progressInterval: ReturnType<typeof setInterval>; // Changed type
    let maxTimeoutId: ReturnType<typeof setTimeout>;   // Changed type

    const completeLoading = () => {
      const currentTime = Date.now()
      const elapsedTime = currentTime - startTime

      if (elapsedTime < minDisplayTime) {
        setTimeout(() => {
          setVisible(false)
          if (onComplete) onComplete(apiData, apiError || undefined)
        }, minDisplayTime - elapsedTime)
      } else {
        setVisible(false)
        if (onComplete) onComplete(apiData, apiError || undefined)
      }

      clearInterval(progressInterval)
      clearTimeout(maxTimeoutId)
    }

    progressInterval = setInterval(() => {
      setProgress((prev) => {
        const increment = !isLoading ? 5 : 1 // isLoading is used here
        const newProgress = Math.min(prev + increment, 100)
        return newProgress
      })
    }, 100)

    maxTimeoutId = setTimeout(() => {
      if (isLoading) { // isLoading is used here
        setError("Request timed out")
        setIsLoading(false)
        setMessage("Request timed out. Please try again.")
        setTimeout(completeLoading, 2000)
      }
    }, maxDisplayTime)

    if (apiCall) {
      (async () => {
        try {
          setDebugInfo("Sending request...")
          apiData = await apiCall()
          setDebugInfo("Request successful!")
          setMessage("Success! Loading complete.")
          setIsLoading(false)
          setTimeout(completeLoading, 1000)
        } catch (err) {
          apiError = err as Error
          setError(apiError.message)
          setDebugInfo(`Error: ${apiError.message}`)
          setMessage("An error occurred. Please try again.")
          setIsLoading(false)
          setTimeout(completeLoading, 2000)
        }
      })()
    } else {
      setTimeout(() => {
        setIsLoading(false)
        setMessage("Ready!")
        setTimeout(completeLoading, 500)
      }, Math.max(0, minDisplayTime - 500));
    }

    return () => {
      clearInterval(progressInterval)
      clearTimeout(maxTimeoutId)
    }
  }, [apiCall, minDisplayTime, maxDisplayTime, onComplete, isLoading, initialMessage])

  const containerClasses = `fixed inset-0 flex items-center justify-center z-50 ${
    visible ? "animate-fade-in" : "animate-fade-out"
  } bg-background` 
  const textColorClass = error ? "text-destructive" : "text-primary-foreground"; 

  const ringColor = error ? "hsl(var(--destructive))" : "hsl(var(--primary))";
  const debugTextColorClass = "text-muted-foreground";

  return (
    <div className={containerClasses}>
      <div className="flex flex-col items-center justify-center">
        <div className="relative">
          <div className="absolute inset-0 flex items-center justify-center z-10">
            <svg className="absolute inset-0" width="288" height="288" viewBox="0 0 288 288">
              <circle
                cx="144"
                cy="144"
                r="140"
                fill="none"
                strokeWidth="4"
                stroke={ringColor} 
                strokeLinecap="round"
                strokeDasharray="879.2"
                strokeDashoffset={879.2 - (879.2 * progress) / 100}
                transform="rotate(-90 144 144)"
                className="transition-all duration-300 ease-in-out"
              />
            </svg>
          </div>

          <div className="w-64 h-64 relative z-0">
            <Image src="/Logo.png" alt="Rig Magic" fill className="object-contain" priority />
          </div>
        </div>

        <div className="mt-8 text-center">
          <p className={`text-xl font-medium ${textColorClass}`}>{message}</p> 

            {showDebugInfo && debugInfo && (
              <p className={`text-sm mt-2 ${debugTextColorClass}`}>{debugInfo}</p> 
              )}
        </div>
      </div>
    </div>
  )
}